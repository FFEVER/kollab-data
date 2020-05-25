from research.project_recommender.project_recommender import UserProjectRelationManager
from apps.ml.models import UserProjectRelation


class ProjectRecommenderService:

    @staticmethod
    def create_sim_tables():
        user_project_sim = UserProjectRelationManager()
        user_project_sim.create_sim_table()
        user_project_sim.fill_sim_table()
        UserProjectRelation.objects.create(users_count=user_project_sim.get_users_count(),
                                           projects_count=user_project_sim.get_projects_count(),
                                           data_frame=user_project_sim.get_picked_sim_table(),
                                           alg_type=)

    @classmethod
    def perform_precalculations(cls):
        cls.create_sim_tables()
