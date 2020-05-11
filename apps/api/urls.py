from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.api.views import EndpointViewSet
from apps.api.views import MLAlgorithmViewSet
from apps.api.views import MLAlgorithmStatusViewSet
from apps.api.views import MLRequestViewSet
from apps.api.views import PredictView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"mlalgorithms", MLAlgorithmViewSet, basename="mlalgorithms")
router.register(r"mlalgorithmstatuses", MLAlgorithmStatusViewSet, basename="mlalgorithmstatuses")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    url(
        r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
]
