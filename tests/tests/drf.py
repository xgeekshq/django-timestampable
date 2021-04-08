from django.conf import settings
from django.test import TestCase
from rest_framework import status
from tests.models import Foo


class SoftDeleteModelViewSetTestCase(TestCase):
    fixtures = ['foos']

    def setUp(self):
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', True)
        setattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', False)

    def test_get_objects(self):
        response = self.client.get('/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = response.json()
        self.assertEquals(3, len(results))

    def test_get_objects_deleted(self):
        response = self.client.get('/deleted/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = response.json()
        self.assertEquals(1, len(results))

    def test_get_objects_with_deleted(self):
        response = self.client.get('/with-deleted/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = response.json()
        self.assertEquals(4, len(results))

    def test_get_object_deleted(self):
        pk_active = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'
        pk_deleted = '381b0e65-bc13-43de-b216-8673c18aa645'

        response = self.client.get('/deleted/{}/'.format(pk_active))
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

        response = self.client.get('/deleted/{}/'.format(pk_deleted))
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response_data = response.json()
        self.assertEquals(pk_deleted, response_data.get('id'))

    def test_get_object_with_deleted(self):
        pk_active = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'
        pk_deleted = '381b0e65-bc13-43de-b216-8673c18aa645'

        for pk in [pk_active, pk_deleted]:
            response = self.client.get('/with-deleted/{}/'.format(pk))
            self.assertEquals(status.HTTP_200_OK, response.status_code)

            response_data = response.json()
            self.assertEquals(pk, response_data.get('id'))

    def test_delete_one_object(self):
        pk = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'

        response = self.client.delete('/{}/'.format(pk))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_soft_delete_one_object(self):
        pk = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'

        response = self.client.delete('/{}/?permanent=0'.format(pk))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_hard_delete_one_object(self):
        pk = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'

        response = self.client.delete('/{}/?permanent=1'.format(pk))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_one_object_with_permanent_invalid(self):
        pk = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'

        for invalid_option in ['123', 'abc', 'a0s8', ' ']:
            response = self.client.delete('/{}/?permanent={}'.format(pk, invalid_option))
            self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_with_truthful_permanent_options(self):
        setattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', True)
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', False)

        truthful_options = [
            't', 'T',
            'y', 'Y', 'yes', 'Yes', 'YES',
            'true', 'True', 'TRUE',
            'on', 'On', 'ON',
            '1', 1,
            True
        ]

        for option in truthful_options:
            foo = Foo(name='test')
            foo.save()

            response = self.client.delete('/{}/?permanent={}'.format(foo.pk, option))
            self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code, 'invalid option: {}'.format(option))

    def test_delete_with_falsy_permanent_options(self):
        pk = '32a6fab2-9e0f-4d23-9a3b-c642470e629d'

        falsely_options = [
            'f', 'F',
            'n', 'N', 'no', 'No', 'NO',
            'false', 'False', 'FALSE',
            'off', 'Off', 'OFF',
            '0', 0,
            'null',
            False
        ]

        for option in falsely_options:
            response = self.client.delete('/{}/?permanent={}'.format(pk, option))
            self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code, 'invalid option: {}'.format(option))

            response = self.client.patch('/{}/restore/'.format(pk))
            self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_restore_one_object(self):
        pk = '381b0e65-bc13-43de-b216-8673c18aa645'

        response = self.client.patch('/{}/restore/'.format(pk))
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response_data = response.json()
        self.assertEquals(pk, response_data.get('id'))

    def test_delete_objects(self):
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', True)

        response = self.client.delete('/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response_data = response.json()
        self.assertEquals(3, response_data.get('count'))

    def test_restore_objects(self):
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', True)

        self.client.delete('/')

        response = self.client.patch('/restore/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response_data = response.json()
        self.assertEquals(4, response_data.get('count'))
