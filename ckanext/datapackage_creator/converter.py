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
                frictionless_package['contributors'].append({
                    'title': contributor['name'],
                    'role': contributor['type'].lower(),
                    'path': contributor['url'],
                    'email': contributor['email'],
                })
            frictionless_package['frequency'] = extras['frequency']
            for extra in package['extras']:
                frictionless_package[extra['key']] = extra['value']
        resources = []
        for resource in package['resources']:
            frictionless_resource = converter.resource(resource)
            resources.append(frictionless_resource)
        frictionless_package['resources'] = resources
    except:
        pass
    return frictionless_package
