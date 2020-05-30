from apps.ml.project_recommender.fields_or_interacted_based import FieldsOrInteractedBased


class ProjectRecommenderService:

    @staticmethod
    def perform_precalculations():
        FieldsOrInteractedBased.pre_calculate()
