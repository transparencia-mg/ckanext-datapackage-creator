import os
import json
import tempfile

from flask import make_response, request

import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.logic import get_action, ValidationError

from ckanext.datapackage_creator.inference import inference_data


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
    del data['metadata']
    data_response = {
        'has_error': False,
        'resource': None
    }
    try:
        resource = get_action('resource_create')(context, data)
    except ValidationError as e:
        data_response['errors'] = e.error_dict
        data_response['error_summary'] = e.error_summary
        data_response['has_error'] = True
    else:
        data_response['resource'] = resource
    response = make_response()
    response.content_type = 'application/json'
    response.data = json.dumps(data_response)
    return response
