import os
import json
import tempfile

from flask import make_response, request

from slugify import slugify

import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.logic import get_action, ValidationError
from ckan.views.dataset import _tag_string_to_list

from ckanext.datapackage_creator.utils import row_to_dict
from ckanext.datapackage_creator.model import Datapackage, DatapackageResource
from ckanext.datapackage_creator.validation import validate_resource, validate_package
from ckanext.datapackage_creator.settings import settings
from ckanext.datapackage_creator.backends import default as default_backend


def inference():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    response = make_response()
    response.content_type = 'application/json'
    file = request.files['file']
    _, extension = os.path.splitext(file.filename)
    tmp = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    file.save(tmp)
    tmp.close()
    action = get_action('inference_data')
    data = {
        'filepath': tmp.name,
    }
    try:
        result = action(context, data)
        result['has_error'] = False
        result['error_summary'] = ''
    except:
        result = {
            'has_error': True,
            'error_summary': 'Error in data inference'
        }
    else:
        result['has_error'] = False
        result['error_summary'] = ''
        name, ext = os.path.splitext(file.filename)
        result['metadata']['name'] = slugify(name)
    response.data = json.dumps(result)
    return response


def settings_show():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
        'for_edit': True,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    response = make_response()
    response.content_type = 'application/json'
    options = {
        'resource': settings.get('resource', {'required': [], 'editable': []}),
        'package': settings.get('package', {'required': [], 'editable': []}),
    }
    response.data = json.dumps(options)
    return response


def save_resource():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
        'for_edit': True,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    data = request.form.copy()
    data['state'] = 'active'
    data['url_type'] = 'upload'
    resource_id = data.get('id')
    if not resource_id:
        data['upload'] = request.files['upload']
    metadata = data['metadata']
    del data['metadata']
    data_response = {
        'has_error': False,
        'resource': None
    }
    data_validate = data.copy()
    data_validate['fields'] = json.loads(metadata).get('fields')
    try:
        validate_resource(data_validate)
        if resource_id:
            action = get_action('resource_patch')
        else:
            action = get_action('resource_create')
        resource = action(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        data_response['resource'] = resource
        save_datapackage_resource = get_action('save_datapackage_resource')
        data_package_resource = {
            'metadata': metadata,
            'resource_id': resource['id'],
            'errors': {}
        }
        save_datapackage_resource(context, data_package_resource)
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response


def delete_resource():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
        'for_edit': True,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    data = request.form.copy()
    data_response = {
        'has_error': False,
        'package': None
    }
    try:
        resource = get_action('resource_delete')(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response


def save_package():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
        'for_edit': True,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    data = request.form.copy()
    tag_string = data.pop('tag_string')
    data['tags'] = _tag_string_to_list(tag_string)
    package_id = data.get('id')
    if not package_id:
        data['state'] = 'draft'
        data['_ckan_phase'] = 'dataset_new_1'
        package_action = get_action('package_create')
    else:
        package_action = get_action('package_patch')
    metadata = data.pop('metadata')
    metadata_json = json.loads(metadata)
    data['extras'] = metadata_json['extras']
    data_response = {
        'has_error': False,
        'package': None,
    }
    try:
        validate_package(data)
        package = package_action(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        data_response['package'] = package
        save_datapackage = get_action('save_datapackage')
        data_datapackage = {
            'package_id': package['id'],
            'metadata': metadata
        }
        save_datapackage(context, data_datapackage)
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response


def publish_package():
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
        'for_edit': True,
    }
    try:
        toolkit.check_access('package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    data_response = {
        'has_error': False,
    }
    data = request.form.copy()
    data['state'] = 'active'
    package_data = {
        'id': data['id'],
        'state': 'active'
    }
    try:
        get_action('package_patch')(context, package_data)
        frictionless_package = get_action('generate_datapackage_json')(context, package_data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        validation = default_backend.validate_package(frictionless_package)
        datapackage = model.Session.query(Datapackage).filter(
            Datapackage.package_id==package_data['id']
        ).order_by(Datapackage.created.desc()).first()
        if datapackage:
            datapackage.errors = validation.to_dict()
            model.Session.commit()
    default_backend.validate_package(package_data)
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response


def datapackage_show(package_id):
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
    }
    try:
        toolkit.check_access('package_show', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    response = make_response()
    response.content_type = 'application/json'
    data = {
        'package_id': package_id
    }
    try:
        datapackage = get_action('datapackage_show')(context, data)
    except Exception as ex:
        datapackage = Datapackage()
    data = {
        'id': package_id
    }
    package = get_action('package_show')(context, data)
    data_response = {
        'datapackage': row_to_dict(datapackage),
        'package': package,
    }
    response.data = json.dumps(data_response)
    return response


def datapackage_resource_show(resource_id):
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
    }
    try:
        toolkit.check_access('package_show', context)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    response = make_response()
    response.content_type = 'application/json'
    data = {
        'resource_id': resource_id
    }
    try:
        datapackage_resource = get_action('datapackage_resource_show')(context, data)
    except:
        datapackage_resource = DatapackageResource()
    data = {
        'id': resource_id
    }
    resource = get_action('resource_show')(context, data)
    data_response = {
        'datapackage_resource': row_to_dict(datapackage_resource),
        'resource': resource,
    }
    response.data = json.dumps(data_response)
    return response


def datapackage_json_show(package_id):
    context = {
        'model': model,
        'session': model.Session,
        'user': toolkit.c.user,
        'auth_user_obj': toolkit.c.userobj,
        'api_version': 3,
    }
    data = {
        'id': package_id
    }
    frictionless_package = get_action('generate_datapackage_json')(context, data)
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(frictionless_package)
    return response
