from apps.api.models import Endpoint
from apps.api.models import RecAlgorithm
from apps.api.models import RecAlgorithmStatus


class RecRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        # get algorithm
        database_object, algorithm_created = RecAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint)
        if algorithm_created:
            status = RecAlgorithmStatus(status=algorithm_status,
                                        created_by=owner,
                                        parent_algorithm=database_object,
                                        active=True)
            status.save()

        # add to registry
        self.endpoints[database_object.id] = algorithm_object
