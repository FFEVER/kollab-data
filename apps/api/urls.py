from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.api.views import EndpointViewSet
from apps.api.views import RecAlgorithmViewSet
from apps.api.views import RecAlgorithmStatusViewSet
from apps.api.views import RecRequestViewSet
from apps.api.views import PredictView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"recalgorithms", RecAlgorithmViewSet, basename="recalgorithms")
router.register(r"recalgorithmstatuses", RecAlgorithmStatusViewSet, basename="recalgorithmstatuses")
router.register(r"recrequests", RecRequestViewSet, basename="recrequests")

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    url(
        r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
]
