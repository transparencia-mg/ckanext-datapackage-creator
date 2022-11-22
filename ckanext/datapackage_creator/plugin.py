import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint

from ckanext.datapackage_creator.controllers import datapackage_creator


class DatapackageCreatorPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)

    def get_blueprint(self):
        blueprint = Blueprint('datapackage_creator', __name__, url_prefix='/datapackage-creator')
        blueprint.add_url_rule(
            "/inference", view_func=datapackage_creator.inference,
            endpoint='inference', methods=['POST']
        )
        blueprint.add_url_rule(
            "/save-resource", view_func=datapackage_creator.save_resource,
            endpoint='save_resource', methods=['POST']
        )
        return blueprint

    def update_config(self, config):
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_template_directory(config, 'templates')

    def get_actions(self):
        return {}
