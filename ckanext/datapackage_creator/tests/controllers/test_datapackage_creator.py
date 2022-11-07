import json
import pytest
import responses

import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as toolkit


@pytest.mark.ckan_config('ckan.plugins', 'datapackage_creator')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestDataackageCreatorController():

    @responses.activate
    def test_inference_resource(self, app):
        user = factories.User()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        data = {
            'file': (open('test_data.csv', 'rb'), 'test_data.csv')
        }
        url = toolkit.url_for('datapackage_creator.inference')
        response = app.post(
            url, extra_environ=env, data=data
        )
        assert 200 == response.status_code
        result = json.loads(response.body)
        fields = ['id_fonte', 'cd_fonte', 'nome']
        result_fields = [f['name'] for f in result['metadata']['schema']['fields']]
        for field in fields:
            assert field in result_fields
