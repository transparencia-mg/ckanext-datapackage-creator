import mimetypes

from frictionless import describe


def inference_data(filepath):
    try:
        result = describe(filepath)
    except Exception as ex:
        result = {}
    data = {
        'metadata': result,
        'content_type': mimetypes.guess_type(filepath),
    }
    return data
