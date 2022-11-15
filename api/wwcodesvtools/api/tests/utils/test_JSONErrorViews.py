import json
from django.test import TestCase


class TestJSONErrorViews(TestCase):

    def test_404_JSONview(self):
        response = self.client.get('/endpoint/not/found')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Endpoint not found (404)')
