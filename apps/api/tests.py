from django.test import TestCase
from rest_framework.test import APIClient


class EndpointTests(TestCase):

    def test_predict_view(self):
        client = APIClient()
        input_data = {"user_id": 13}
        classifier_url = "/api/v1/project_recommender/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("projects" in response.data)
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
