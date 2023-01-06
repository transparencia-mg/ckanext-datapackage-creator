import mimetypes
import datetime as dt

from ckan.logic import get_action

from ckanext.datapackage_creator.backends import default as inference_backend
from ckanext.datapackage_creator.model import Datapackage, DatapackageResource
from ckanext.datapackage_creator.converter import ckan_to_frictionless


def inference_data(context, data):
    filepath = data['filepath']
    result = inference_backend.describe_resource(filepath)
    try:
        rows = inference_backend.extract_resource(filepath)
        for field in result['schema']['fields']:
            field['rows'] = [row[field['name']] for row in rows]
            field['required'] = False
            field['description'] = ''
            field['format'] = 'default'
            field['unique'] = False
            field['extras'] = []
            field['primary_key'] = False
            field['foreign_key'] = ''
    except TypeError:
        pass
    data = {
        'metadata': result,
        'content_type': mimetypes.guess_type(filepath),
    }
    return data


def save_datapackage(context, data):
    metadata = data['metadata']
    package_id = data['package_id']
    Session = context['model'].Session
    datapackage = Datapackage()
    datapackage.package_id = package_id
    datapackage.data = metadata
    datapackage.created = dt.datetime.utcnow()
    datapackage.errors = data.get('errors')
    Session.add(datapackage)
    Session.commit()
    return datapackage


def save_datapackage_resource(context, data):
    metadata = data['metadata']
    resource_id = data['resource_id']
    Session = context['model'].Session
    datapackage_resource = DatapackageResource()
    datapackage_resource.resource_id = resource_id
    datapackage_resource.data = metadata
    datapackage_resource.created = dt.datetime.utcnow()
    datapackage_resource.errors = data.get('errors')
    Session.add(datapackage_resource)
    Session.commit()
    return datapackage_resource


def datapackage_show(context, data):
    package_id = data['package_id']
    Session = context['model'].Session
    datapackage = Session.query(Datapackage).filter(
        Datapackage.package_id==package_id
    ).order_by(Datapackage.created.desc()).first()
    return datapackage


def datapackage_resource_show(context, data):
    resource_id = data['resource_id']
    Session = context['model'].Session
    datapackage_resource = Session.query(DatapackageResource).filter(
        DatapackageResource.resource_id==resource_id
    ).order_by(DatapackageResource.created.desc()).first()
    return datapackage_resource


def generate_datapackage_json(context, data):
    package = get_action('package_show')(context, data)
    return ckan_to_frictionless(package)
