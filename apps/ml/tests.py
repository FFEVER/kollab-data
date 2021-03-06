from django.test import TestCase
import inspect

from apps.ml.project_recommender.fields_or_interacted_based import FieldsOrInteractedBased
from apps.ml.project_recommender.project_to_user_fields_based import ProjectToUserFieldsBased
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased
from apps.ml.registry import RecRegistry
from apps.kstorage.models import User, Project
from apps.ml.related_project.project_fields_based import ProjectFieldsBased
from apps.ml.services import ProjectRecommenderService
from apps.ml.user_recommender.user_to_project_fields_based import UserToProjectFieldsBased


class RecommenderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(RecommenderTest, cls).setUpTestData()
        User.objects.create(id=13, email="eit@gmail.com", role="student", faculty_id=1, year="1",
                            fields=[[1, 2, 3], [5, 6, -1]], skills=["a", "b", "c"],
                            joined_projects=[1, 2, 3], starred_projects=[4, 5, 6], viewed_projects=[7, 8, 9],
                            followed_projects=[10, 11, 12])
        Project.objects.create(id=1, title="test", project_status=1, fields=[[1, 2, -1], [5, 6, -1]],
                               tags=["tag1", "tag2"], created_at="2020-03-22T10:19:12.782Z",
                               updated_at="2020-03-22T10:19:12.782Z")

        ProjectRecommenderService.perform_precalculations()

    def test_project_to_user_fields_based(self):
        input_data = {"user_id": 13}
        my_alg = ProjectToUserFieldsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        self.assertEqual(ProjectToUserFieldsBased.algorithm_name, response['alg_name'])

    def test_interacted_projects_based(self):
        input_data = {"user_id": 13}
        my_alg = InteractedProjectsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        self.assertEqual(InteractedProjectsBased.algorithm_name, response['alg_name'])

    def test_fields_or_interacted_based_with_old_user(self):
        input_data = {"user_id": 13}
        my_alg = FieldsOrInteractedBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        # Old user should use InteractedProjectBased algorithm
        self.assertEqual(InteractedProjectsBased.algorithm_name, response['alg_name'])

    def test_fields_or_interacted_based_with_new_user(self):
        input_data = {"user_id": 1}
        my_alg = FieldsOrInteractedBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        # New user should use UserProjectFieldsBased algorithm
        self.assertEqual(ProjectToUserFieldsBased.algorithm_name, response['alg_name'])

    def test_project_fields_based(self):
        input_data = {"project_id": 1}
        my_alg = ProjectFieldsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)
        self.assertEqual(ProjectFieldsBased.algorithm_name, response['alg_name'])

    def test_user_to_project_fields_based(self):
        input_data = {"project_id": 1}
        my_alg = UserToProjectFieldsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('users' in response)
        self.assertEqual(UserToProjectFieldsBased.algorithm_name, response['alg_name'])

    def test_registry(self):
        registry = RecRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = ProjectToUserFieldsBased.endpoint_name
        algorithm_object = ProjectToUserFieldsBased()
        algorithm_name = ProjectToUserFieldsBased.algorithm_name
        algorithm_status = ProjectToUserFieldsBased.status
        algorithm_version = ProjectToUserFieldsBased.version
        algorithm_owner = ProjectToUserFieldsBased.owner
        algorithm_description = ProjectToUserFieldsBased.description
        algorithm_code = inspect.getsource(ProjectToUserFieldsBased)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                               algorithm_status, algorithm_version, algorithm_owner,
                               algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
