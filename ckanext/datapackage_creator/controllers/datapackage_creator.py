import os
import json
import tempfile

from flask import make_response, request

import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.logic import get_action, ValidationError

from ckanext.datapackage_creator.logic import inference_data


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
    result = inference_data(tmp.name)
    _, name = os.path.split(file.filename)
    result['metadata']['name'] = name
    response.data = json.dumps(result)
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
    metadata = data['metadata']
    package_id = data['package_id']
    del data['metadata']
    resource_id = data.get('id')
    data_response = {
        'has_error': False,
        'resource': None
    }
    try:
        if resource_id:
            action = get_action('resource_update')
        else:
            get_action('resource_create')
        resource = action(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        data_response['resource'] = resource
        extras_data = {
            'extras': [
                {
                    'key': 'datapackage_creator',
                    'value': json.dumps({
                        resource['id']: metadata
                    })
                }
            ],
            'id': package_id
        }
        try:
            action = get_action('package_update')
            action(context, extras_data)
        except ValidationError as e:
            print(e.error_dict)
            print(e.error_summary)
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
    data['_ckan_phase'] = 'dataset_new_1'
    data['state'] = 'draft'
    package_creator_action = get_action('package_create')
    data_response = {
        'has_error': False,
        'package': None
    }
    try:
        package = package_creator_action(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        data_response['package'] = package
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
    try:
        action = get_action('package_update')
        action(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response

