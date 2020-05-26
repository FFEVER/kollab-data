from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased
from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased


class ProjectRecommenderService:

    @staticmethod
    def perform_precalculations():
        UserProjectFieldsBased.pre_calculate()
        InteractedProjectsBased.pre_calculate()
