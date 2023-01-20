import ckan.plugins as plugins

from ckan.model import Session

from flask import Blueprint

from ckanext.datapackage_creator.controllers import datapackage_creator
from ckanext.datapackage_creator.logic import (
    save_datapackage, inference_data, save_datapackage_resource, datapackage_show,
    datapackage_resource_show, generate_datapackage_json
)
from ckanext.datapackage_creator.cli import get_commands
from ckanext.datapackage_creator.model import DatapackageResource
from ckanext.datapackage_creator.converter import ckan_to_frictionless


class DatapackageCreatorPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IPackageController)

    def read(self, entity) -> None:
        pass

    def create(self, entity) -> None:
        pass

    def edit(self, entity):
        pass

    def delete(self, entity) -> None:
        pass

    def after_dataset_create(self, context, pkg_dict) -> None:
        pass

    def after_dataset_update(self, context, pkg_dict):
        pass

    def after_dataset_delete(self, context, pkg_dict):
        pass

    def after_dataset_show(self, context, pkg_dict):
        pass

    def before_dataset_search(self, search_params):
        return search_params

    def after_dataset_search(self, search_results, search_params):
        return search_results

    def before_dataset_index(self, pkg_dict):
        return pkg_dict

    def before_dataset_view(self, pkg_dict):
        pkg_dict['datapackage_json'] = ckan_to_frictionless(pkg_dict)
        return pkg_dict

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
        blueprint.add_url_rule(
            "/show-datapackage/<package_id>", view_func=datapackage_creator.datapackage_show,
            endpoint='datapackage_show', methods=['GET']
        )
        blueprint.add_url_rule(
            "/show-datapackage-resource/<resource_id>", view_func=datapackage_creator.datapackage_resource_show,
            endpoint='datapackage_resource_show', methods=['GET']
        )
        blueprint.add_url_rule(
            "/show-datapackage-json/<package_id>", view_func=datapackage_creator.datapackage_json_show,
            endpoint='datapackage_json_show', methods=['GET']
        )
        blueprint.add_url_rule(
            "/show-settings", view_func=datapackage_creator.settings_show,
            endpoint='settings_show', methods=['GET']
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
            'datapackage_show': datapackage_show,
            'datapackage_resource_show': datapackage_resource_show,
            'generate_datapackage_json': generate_datapackage_json,
        }

    def get_commands(self):
        return get_commands()
