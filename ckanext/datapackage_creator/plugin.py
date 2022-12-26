import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint

from ckanext.datapackage_creator.controllers import datapackage_creator
from ckanext.datapackage_creator.logic import (
    save_datapackage, inference_data, save_datapackage_resource
)


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
        blueprint.add_url_rule(
            "/delete-resource", view_func=datapackage_creator.delete_resource,
            endpoint='delete_resource', methods=['DELETE']
        )
        blueprint.add_url_rule(
            "/save-package", view_func=datapackage_creator.save_package,
            endpoint='save_package', methods=['POST']
        )
        blueprint.add_url_rule(
            "/publish-package", view_func=datapackage_creator.publish_package,
            endpoint='publish_package', methods=['POST']
        )
        return blueprint

    def update_config(self, config):
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_template_directory(config, 'templates')

    def get_actions(self):
        return {
            'save_datapackage': save_datapackage,
            'save_datapackage_resource': save_datapackage_resource,
            'inference_data': inference_data,
        }
