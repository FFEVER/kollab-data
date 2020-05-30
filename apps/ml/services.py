from apps.ml.project_recommender.fields_or_interacted_based import FieldsOrInteractedBased
from apps.ml.related_project.project_fields_based import ProjectFieldsBased
from apps.ml.user_recommender.user_to_project_fields_based import UserToProjectFieldsBased


class ProjectRecommenderService:

    @staticmethod
    def perform_precalculations():
        FieldsOrInteractedBased.pre_calculate()
        ProjectFieldsBased.pre_calculate()
        UserToProjectFieldsBased.pre_calculate()
