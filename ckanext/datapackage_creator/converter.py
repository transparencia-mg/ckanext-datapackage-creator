import json

from ckan.model import Session

from frictionless_ckan_mapper import ckan_to_frictionless as converter

from ckanext.datapackage_creator.model import Datapackage, DatapackageResource


def ckan_resource_to_frictionless(resource):
    frictionless_resource = converter.resource(resource)
    frictionless_resource['path'] = resource['url']
    datapackage_resource = Session.query(DatapackageResource).filter(
        DatapackageResource.resource_id==resource['id']
    ).order_by(DatapackageResource.created.desc()).first()
    if datapackage_resource:
        extras = json.loads(datapackage_resource.data)
        frictionless_resource['schema'] = {
            'fields': [],
        }
        foreign_keys = []
        try:
            fields = extras['fields']
        except:
            pass
        uniques = []
        for field in fields:
            field_dict = {
                'name': field.get('name', ''),
                'description': field.get('description', ''),
                'title': field.get('title', ''),
                'format': field.get('format'),
                'description': field.get('description', ''),
                'type': field.get('type', ''),
            }
            unique = field.get('unique')
            if unique:
                uniques.append(field.get('name', ''))
            primary_key = field.get('primary_key')
            if primary_key:
                uniques.append(field['name'])
                frictionless_resource['schema']['primaryKey'] = field['name']
            foreign_key = field.get('foreign_key')
            if foreign_key:
                try:
                    resource, resource_field = foreign_key.split()
                except:
                    pass
                else:
                    foreign_keys.append(
                        {
                            'fields': field['name'],
                            'reference': {
                                "resource": resource,
                                "fields": resource_field
                            }
                        }
                    )
            if uniques:
                frictionless_resource['schema']['uniqueKeys'] = uniques
            frictionless_resource['schema']['fields'].append(field_dict)
        if foreign_keys:
            frictionless_resource['foreignKeys'] = []
    return frictionless_resource


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
        resources = []
        for resource in package['resources']:
            frictionless_resource = ckan_resource_to_frictionless(resource)
            resources.append(frictionless_resource)
        frictionless_package['resources'] = resources
    except:
        pass
    return frictionless_package
