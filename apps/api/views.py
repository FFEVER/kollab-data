from django.db import transaction
import json
from numpy.random import rand

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.exceptions import APIException

from apps.api.models import Endpoint
from apps.api.serializers import EndpointSerializer
from apps.api.models import RecAlgorithm
from apps.api.serializers import RecAlgorithmSerializer
from apps.api.models import RecAlgorithmStatus
from apps.api.serializers import RecAlgorithmStatusSerializer
from apps.api.models import RecRequest
from apps.api.serializers import RecRequestSerializer

from apps.ml.registry import MLRegistry
from recommender.wsgi import registry


class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = RecAlgorithmSerializer
    queryset = RecAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = RecAlgorithmStatus.objects.filter(parent_mlalgorithm=instance.parent_mlalgorithm,
                                                     created_at__lt=instance.created_at,
                                                     active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    RecAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])


class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = RecAlgorithmStatusSerializer
    queryset = RecAlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)
        except Exception as e:
            raise APIException(str(e))


class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = RecRequestSerializer
    queryset = RecRequest.objects.all()


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = RecAlgorithm.objects.filter(parent_endpoint__name=endpoint_name, status__status=algorithm_status,
                                           status__active=True)

        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1
            target_algorithm = algs[alg_index]
        else:
            target_algorithm = algs.last()

        algorithm_object = registry.endpoints[target_algorithm.id]
        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = RecRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlalgorithm=target_algorithm,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)
