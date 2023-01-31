import json

from ckan.model import Session

from frictionless_ckan_mapper import ckan_to_frictionless as converter

from ckanext.datapackage_creator.model import Datapackage, DatapackageResource


def ckan_to_frictionless(package):
    package_id = package['id']
    datapackage = Session.query(Datapackage).filter(
        Datapackage.package_id==package_id
    ).order_by(Datapackage.created.desc()).first()
    frictionless_package = converter.dataset(package)
    try:
        if datapackage:
            extras = json.loads(datapackage.data)
            frictionless_package['contributors'] = []
            for contributor in extras['contributors']:
                contributor_item = {
                    'title': contributor['name'],
                    'role': contributor['type'].lower(),
                    'email': contributor['email'],
                }
                if contributor['url'].strip():
                    contributor_item['path'] = contributor['url']
                frictionless_package['contributors'].append(contributor_item)
            frictionless_package['frequency'] = extras['frequency']
            for extra in package['extras']:
                frictionless_package[extra['key']] = extra['value']
        resources = []
        for resource in package['resources']:
            frictionless_resource = converter.resource(resource)
            datapackage_resource = Session.query(DatapackageResource).filter(
                DatapackageResource.resource_id==resource['id']
            ).order_by(DatapackageResource.created.desc()).first()
            if datapackage_resource:
                extras = json.loads(datapackage_resource.data)
                frictionless_resource['schema'] = {
                    'fields': [],
                    'foreignKeys': []
                }
                try:
                    fields = extras['inference']['metadata']['schema']['fields']
                except:
                    continue
                for field in fields:
                    field_dict = {
                        'name': field['name'],
                        'description': field['description'],
                        'title': field['title'],
                        'format': field['format'],
                        'description': field['description'],
                        'type': field['type'],
                    }
                    primary_key = field.get('primary_key')
                    if primary_key:
                        frictionless_resource['schema']['primary_key'] = field['name']
                    foreign_key = field.get('foreign_key')
                    if foreign_key:
                        try:
                            resource, resource_field = foreign_key.split()
                        except:
                            pass
                        else:
                            frictionless_resource['schema']['foreignKeys'].append(
                                {
                                    'fields': field['name'],
                                    'reference': {
                                        "resource": resource,
                                        "fields": resource_field
                                    }
                                }
                            )
                    frictionless_resource['schema']['fields'].append(field_dict)
            resources.append(frictionless_resource)
        frictionless_package['resources'] = resources
    except:
        pass
    return frictionless_package
