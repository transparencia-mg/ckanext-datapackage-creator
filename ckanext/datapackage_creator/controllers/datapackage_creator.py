import os
import json
import tempfile

from flask import make_response, request

from ckanext.datapackage_creator.inference import inference_data


def inference():
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
