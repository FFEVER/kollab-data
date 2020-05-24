from django.test import TestCase
import inspect

from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased
from apps.ml.registry import MLRegistry

from django.core.management import call_command

class MLTests(TestCase):

    def test_user_project_fields_based(self):
        call_command("fetch_data")
        input_data = { "user_id": 13 }
        my_alg = UserProjectFieldsBased()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertTrue('projects' in response)

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
