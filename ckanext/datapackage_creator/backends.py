import pydoc
import frictionless

from ckanext.datapackage_creator.settings import settings


class BaseBackend(object):

    def describe_resource(self, resource, *args, **kwargs):
        raise NotImplementedError()

    def validate_resource(self, resource, *args, **kwargs):
        raise NotImplementedError()


class FritionlesseBackend(BaseBackend):

    def describe_resource(self, resource, *args, **kwargs):
        return frictionless.describe_resource(resource, *args, **kwargs)

    def extract_resource(self, resource, *args, **kwargs):
        return frictionless.extract_resource(resource, *args, **kwargs)

    def validate_resource(self, resource, *args, **kwargs):
        raise NotImplementedError()


BackendClass = pydoc.locate(
    settings.get('backend', 'ckanext.datapackage_creator.backends.FritionlesseBackend')
)
default = BackendClass()
