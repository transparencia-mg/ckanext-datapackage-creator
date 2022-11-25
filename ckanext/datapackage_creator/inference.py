import mimetypes

from frictionless import describe_resource, extract_resource


def inference_data(filepath):
    result = describe_resource(filepath)
    try:
        rows = extract_resource(filepath)
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
