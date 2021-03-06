from rest_framework import serializers
from apps.api.models import Endpoint
from apps.api.models import RecAlgorithm
from apps.api.models import RecAlgorithmStatus
from apps.api.models import RecRequest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields


class RecAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlalgorithm):
        return RecAlgorithmStatus.objects.filter(parent_algorithm=mlalgorithm).latest('created_at').status

    class Meta:
        model = RecAlgorithm
        read_only_fields = ("id", "name", "description", "code",
                            "version", "owner", "created_at",
                            "parent_endpoint", "current_status")
        fields = read_only_fields


class RecAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at",
                  "parent_algorithm")


class RecRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecRequest
        read_only_fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "created_at",
            "parent_algorithm",
        )
        fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "feedback",
            "created_at",
            "parent_algorithm",
        )
