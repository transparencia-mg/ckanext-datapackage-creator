import os
import json
import tempfile
import threading
import requests
import frictionless

from flask import make_response, request

from slugify import slugify

import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.common import config
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
    response.data = json.dumps(result, default=str)
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


def delete_resource(resource_id):
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
    data = {
        'id': resource_id,
        'state': 'deleted'
    }
    data_response = {
        'has_error': False,
        'package': None
    }
    try:
        resource = get_action('resource_patch')(context, data)
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
    metadata = data['metadata']
    try:
        package_data = get_action('package_patch')(context, package_data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        def _validate():
            token = settings.get('token')
            session = requests.Session()
            if token:
                session.headers['Authorization'] = token
            site_url = config.get('ckan.site_url')
            if site_url.endswith('/'):
                url = f"{site_url}datapackage-creator/show-datapackage-json/{data['id']}"
            else:
                url = f"{site_url}/datapackage-creator/show-datapackage-json/{data['id']}"
            with frictionless.system.use_http_session(session) as ctx:
                datapackage_json = requests.get(url).json()
                package = frictionless.Package(datapackage_json)
                validation = package.validate(skip_errors=["byte-count-error"])
            datapackage = model.Session.query(Datapackage).filter(
                Datapackage.package_id==package_data['id']
            ).order_by(Datapackage.created.desc()).first()
            new_datapackage = Datapackage()
            new_datapackage.package_id = package_data['id']
            new_datapackage.errors = validation.to_dict()
            if datapackage:
                new_datapackage.data = datapackage.data
            else:
                new_datapackage.data = json.loads(metadata)
            model.Session.add(new_datapackage)
            model.Session.commit()
        threading.Thread(target=_validate).start()
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
        'id': package_id,
    }
    data = {
        'id': package_id
    }
    try:
        toolkit.check_access('package_show', context, data)
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('Unauthorized to create a dataset'))
    response = make_response()
    response.content_type = 'application/json'
    data = {
        'id': package_id
    }
    try:
        package = get_action('package_show')(context, data)
        data = {
            'package_id': package['id']
        }
        datapackage = get_action('datapackage_show')(context, data)
    except Exception as ex:
        datapackage = Datapackage()
    datapackage_json = row_to_dict(datapackage)
    datapackage_json['errors_json'] = datapackage.errors_json()
    datapackage_json['data_json'] = datapackage.data_json()
    data_response = {
        'datapackage': datapackage_json,
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
    admin = model.Session.query(model.User).filter(model.User.sysadmin==True, model.User.name!='default').first()
    context = {
        'model': model,
        'session': model.Session,
        'user': admin.name,
        'auth_user_obj': admin,
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


def datapackage_validation_show(package_id):
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
    package = get_action('package_show')(context, data)
    datapackage_list = model.Session.query(Datapackage).filter(
        Datapackage.package_id==package['id']
    ).order_by(Datapackage.created.desc())
    return toolkit.render(
        'datapackage_creator/validation_read.html',
        extra_vars={
            'datapackage_list': datapackage_list,
            'pkg_dict': package
        }
    )
