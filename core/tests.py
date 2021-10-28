import json

from rest_framework.test import APITestCase


class ProviderTestCase(APITestCase):

    def setUp(self):
        self.url = '/providers/'

    def _build_provider_payload(self, name='provider'):
        payload = {
            'name': name,
            'email': 'test@mozio.com',
            'phone_number': '1234',
            'language': 'some-language',
            'currency': 'some-currency',
            'areas': [{'name': 't', 'price': '1', 'poly': '-72.2811293 42.9299841, -72.2811854 42.9289487, -72.2798127 42.9288965, -72.2795556 42.9297110, -72.2811293 42.9299841'}]
        }
        return payload

    def fetch_providers(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)
        return response

    def test_create_provider_invalid_attributes(self):
        # empty attributes
        body = {
            'name': 'test-1',
        }
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 400)

        errors = json.loads(response.content).get('error')
        field_required_msg = ['This field is required.']
        self.assertEquals(errors.get('areas'), field_required_msg)
        self.assertEquals(errors.get('email'), field_required_msg)
        self.assertEquals(errors.get('phone_number'), field_required_msg)
        self.assertEquals(errors.get('language'), field_required_msg)
        self.assertEquals(errors.get('currency'), field_required_msg)

        # invalid polygon
        body = {
            'name': 'test-1',
            'email': 'test@mozio.com',
            'phone_number': '1234',
            'language': 'some-language',
            'currency': 'some-currency',
            'areas': [{'name': 't', 'price': '1', 'poly': '-98.503358 29.335668, -98.503086 29.335668'}]
        }
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 400)
        errors = json.loads(response.content).get('error')
        self.assertEquals(errors.get('areas')[0].get('poly'), ['Invalid Polygon Area'])

    def test_duplicated_provider(self):
        body = self._build_provider_payload(name='provider-test')
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 201)

        # with the same body
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 400)
        errors = json.loads(response.content).get('error')
        self.assertEquals(errors.get('name'), ['provider with this name already exists.'])

    def test_create_provider_success(self):
        body = self._build_provider_payload(name='valid-provider')
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 201)

        provider = json.loads(response.content)
        self.assertIsNotNone(provider.get('id'))
        self.assertEquals(provider.get('name'), body['name'])
        self.assertEquals(provider.get('email'), body['email'])
        self.assertEquals(provider.get('phone_number'), body['phone_number'])
        self.assertEquals(provider.get('language'), body['language'])
        self.assertEquals(provider.get('currency'), body['currency'])

        areas = provider.get('areas')[0]
        body_areas = body['areas'][0]
        self.assertEquals(areas.get('name'), body_areas['name'])
        self.assertEquals(areas.get('price'), body_areas['price'])
        # NOTE: GEOSGeometry precision .0000001 rounds to lower 0.0000009999999 (10cm length difference)
        # self.assertEquals(areas.get('poly'), body_areas['poly'])

    def test_list_provider(self):
        # seek how many we have
        response = self.fetch_providers()
        actual_providers_count = len(json.loads(response.content))

        body = self._build_provider_payload(name='valid-provider1')
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 201)

        response = self.fetch_providers()

        providers = json.loads(response.content)
        self.assertEqual(len(providers), actual_providers_count + 1)

    def test_delete_provider_invalid_attribute(self):
        invalid_id = 'some-invalid-id-1234'
        response = self.client.delete(f'{self.url}{invalid_id}/')
        self.assertEquals(response.status_code, 404)
        content = json.loads(response.content)

        self.assertEquals(content.get('error'), 'Invalid provider id')

    def test_delete_provider(self):
        # actual count
        response = self.fetch_providers()
        providers_count = len(json.loads(response.content))

        body = self._build_provider_payload(name='valid-provider-to-delete')
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 201)
        valid_id = json.loads(response.content).get('id')

        # and now delete it
        response = self.client.delete(f'{self.url}{valid_id}/')
        self.assertEquals(response.status_code, 200)

        # check with same count
        response = self.fetch_providers()
        self.assertEquals(len(json.loads(response.content)), providers_count)
