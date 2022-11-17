import json

from ckan.common import config

from ckanext.datapackage_creator.decorators import singleton


@singleton
class Settings(object):

    def __init__(self):
        self.config = {}
        datapackage_creator_config = config.get('datapackage_creator', None)
        if datapackage_creator_config is not None:
            with open(datapackage_creator_config, 'r') as datapackage_creator_json:
                self.config = json.loads(datapackage_creator_json.read())

    def get(self, name, default=None):
        return self.config.get(name, default)


settings = Settings()
