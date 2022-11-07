import os
import json
import tempfile

from flask import make_response, request

import ckan.model as model
import ckan.plugins.toolkit as toolkit

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
    response.data = json.dumps(result)
    return response
