from django.conf import settings
from django.test import TestCase
from rest_framework import status


class SettingsTestCase(TestCase):
    fixtures = ['foos']

    def test_bulk_delete_response_no_content(self):
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', False)
        response = self.client.delete('/foos/')
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_bulk_restore_response_no_content(self):
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', False)
        response = self.client.patch('/foos/restore/')
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_permission_denied_bulk_hard_delete(self):
        setattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', False)
        response = self.client.delete('/foos/?permanent=1')
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_can_bulk_hard_delete(self):
        setattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', True)
        setattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', True)

        response = self.client.delete('/foos/?permanent=1')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response_data = response.json()
        self.assertEquals(4, response_data.get('count'))

        self.assertIn('count_per_model', response_data)
        self.assertIn('tests.Foo', response_data.get('count_per_model'))
        self.assertEquals(4, response_data['count_per_model']['tests.Foo'])
