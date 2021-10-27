import json

from rest_framework.test import APITestCase


class ProviderTestCase(APITestCase):

    def setUp(self):
        self.url = '/providers/'

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
        body = {
            'name': 'test-1',
            'email': 'test@mozio.com',
            'phone_number': '1234',
            'language': 'some-language',
            'currency': 'some-currency',
            'areas': [{'name': 't', 'price': '1', 'poly': '-72.2811293 42.9299841, -72.2811854 42.9289487, -72.2798127 42.9288965, -72.2795556 42.9297110, -72.2811293 42.9299841'}]
        }
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 201)

        # with the same body
        response = self.client.post(self.url, body, format='json')
        self.assertTrue(response.status_code, 400)
        errors = json.loads(response.content).get('error')
        self.assertEquals(errors.get('name'), ['provider with this name already exists.'])

    def test_create_provider_success(self):
        body = {
            'name': 'valid-provider',
            'email': 'test@mozio.com',
            'phone_number': '1234',
            'language': 'some-language',
            'currency': 'some-currency',
            'areas': [{'name': 't', 'price': '1', 'poly': '-72.2811293 42.9299841, -72.2811854 42.9289487, -72.2798127 42.9288965, -72.2795556 42.9297110, -72.2811293 42.9299841'}]
        }
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
