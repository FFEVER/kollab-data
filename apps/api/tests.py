from django.test import TestCase
from rest_framework.test import APIClient

from apps.kstorage.models import User, Project
from apps.ml.services import ProjectRecommenderService


class EndpointTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(EndpointTests, cls).setUpTestData()
        User.objects.create(id=13, expertises=[[1, 2, 3], [4, 5, -1]], email="test@test.com", role="student",
                            faculty_id=1, skills=["skill1", "skill2"], year="1")
        Project.objects.create(id=1, title="test", project_status=1, categories=[[1, 2, -1], [5, 6, -1]],
                               tags=["tag1", "tag2"], created_at="2020-03-22T10:19:12.782Z",
                               updated_at="2020-03-22T10:19:12.782Z")

        ProjectRecommenderService.perform_precalculations()

    def test_project_rec(self):
        client = APIClient()
        input_data = {"user_id": 13}
        classifier_url = "/api/v1/project_recommender/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("projects" in response.data)
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)

    def test_project_rec_with_unknown_user(self):
        client = APIClient()
        input_data = {"user_id": 1}
        classifier_url = "/api/v1/project_recommender/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("projects" in response.data)
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
