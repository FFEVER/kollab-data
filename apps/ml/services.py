from research.project_recommender.project_recommender import UserProjectSimilarity


class ProjectRecommenderService:

    @staticmethod
    def create_sim_tables():
        user_project_sim = UserProjectSimilarity()
        user_project_sim.create_sim_table()
        user_project_sim.dump_sim_table()

    @classmethod
    def perform_precalculations(cls):
        cls.create_sim_tables()
