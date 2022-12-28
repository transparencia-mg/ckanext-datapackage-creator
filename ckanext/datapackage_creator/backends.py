import frictionless


class BaseBackend(object):

    def describe_resource(self, resource, *args, **kwargs):
        raise NotImplementedError()

    def extract_resource(self, resource, *args, **kwargs):
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


default = FritionlesseBackend()
