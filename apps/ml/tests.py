from django.test import TestCase
import inspect

from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased
from apps.ml.registry import MLRegistry
from apps.kstorage.models import User, Project
from apps.ml.services import ProjectRecommenderService


class MLTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(MLTests, cls).setUpTestData()
        User.objects.create(id=13, fields=[[1, 2, 3], [4, 5, -1]], email="test@test.com", role="student",
                            faculty_id=1, skills=["skill1", "skill2"], year="1")
        Project.objects.create(id=1, title="test", project_status=1, fields=[[1, 2, -1], [5, 6, -1]],
                               tags=["tag1", "tag2"], created_at="2020-03-22T10:19:12.782Z",
                               updated_at="2020-03-22T10:19:12.782Z")

        ProjectRecommenderService.perform_precalculations()

    def test_user_project_fields_based(self):
        input_data = {"user_id": 13}
        my_alg = UserProjectFieldsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        self.assertEqual(UserProjectFieldsBased.algorithm_name, response['alg_name'])

    def test_interacted_projects_based(self):
        input_data = {"user_id": 13}
        my_alg = InteractedProjectsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        self.assertEqual(InteractedProjectsBased.algorithm_name, response['alg_name'])

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = UserProjectFieldsBased.endpoint_name
        algorithm_object = UserProjectFieldsBased()
        algorithm_name = UserProjectFieldsBased.algorithm_name
        algorithm_status = UserProjectFieldsBased.status
        algorithm_version = UserProjectFieldsBased.version
        algorithm_owner = UserProjectFieldsBased.owner
        algorithm_description = UserProjectFieldsBased.description
        algorithm_code = inspect.getsource(UserProjectFieldsBased)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                               algorithm_status, algorithm_version, algorithm_owner,
                               algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
