from django.test import TestCase
from django.urls import reverse


class APIDocsViewTests(TestCase):

    def test_get(self):
        url = reverse('api_doc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
