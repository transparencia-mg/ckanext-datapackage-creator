import mimetypes
import frictionless

from ckanext.datapackage_creator.backends import default as inference_backend


def inference_data(filepath):
    result = inference_backend.describe_resource(filepath)
    try:
        rows = inference_backend.extract_resource(filepath)
        for field in result['schema']['fields']:
            field['rows'] = [row[field['name']] for row in rows]
            field['required'] = False
            field['description'] = ''
            field['format'] = 'default'
            field['unique'] = False
    except TypeError:
        pass
    data = {
        'metadata': result,
        'content_type': mimetypes.guess_type(filepath),
    }
    return data
