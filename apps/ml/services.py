from research.project_recommender.project_recommender import UserProjectRelationship
from apps.ml.models import UserProjectRelation
from apps.ml.project_recommender.user_project_fields_based import UserProjectFieldsBased


class ProjectRecommenderService:

    @staticmethod
    def create_sim_tables():
        # Relation table for fields based
        user_project_by_fields = UserProjectRelationship()
        user_project_by_fields.fill_relations()
        UserProjectRelation.objects.create(users_count=user_project_by_fields.row_count(),
                                           projects_count=user_project_by_fields.col_count(),
                                           data_frame=user_project_by_fields.get_picked_relations(),
                                           alg_type=UserProjectFieldsBased.__name__)
        # Relation table for past interactions based

    @classmethod
    def perform_precalculations(cls):
        cls.create_sim_tables()
