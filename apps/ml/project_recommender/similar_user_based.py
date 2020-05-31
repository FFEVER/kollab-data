from apps.kstorage.models import User, Project
from apps.ml.models import Relation
import pickle

from apps.ml.recommender import Recommender
from research.project_recommender.relation_calculator import UserProjectCalcBySimilarUsers
from research.project_recommender.relationship import UserRelationship, UserProjectRelationFromSimilarUsers


class SimilarUserBased(Recommender):
    endpoint_name = "project_recommender"
    algorithm_name = "Similar User Based (Collaborative)"
    owner = "Nattaphol"
    description = "Recommend to Student A the projects that the students similar to A interacts with in the past (Collaborative)"
    version = "0.0.1"
    status = "production"

    @classmethod
    def pre_calculate(cls):
        print(f'{SimilarUserBased.__name__}: Create user and user relation by interactions.')
        cls.create_user_relation_by_interactions()
        print(f'{SimilarUserBased.__name__}: Create user and project relation by similar users.')
        cls.create_user_project_relation_by_similar_users()

    @staticmethod
    def create_user_relation_by_interactions():
        # Relation table for user/user
        sim_users_relation = UserRelationship()
        sim_users_relation.fill_relations()
        Relation.objects.get_or_create(row_count=sim_users_relation.row_count(),
                                col_count=sim_users_relation.col_count(),
                                row_type=sim_users_relation.row_type(),
                                col_type=sim_users_relation.col_type(),
                                data_frame=sim_users_relation.get_pickled_relations(),
                                alg_type=sim_users_relation.alg_type())

    @staticmethod
    def create_user_project_relation_by_similar_users():
        # Relation of users and projects from similar users
        u_p_rela_from_sim_users = UserProjectRelationFromSimilarUsers(k=4)
        u_p_rela_from_sim_users.fill_relations()
        Relation.objects.get_or_create(row_count=u_p_rela_from_sim_users.row_count(),
                                col_count=u_p_rela_from_sim_users.col_count(),
                                row_type=u_p_rela_from_sim_users.row_type(),
                                col_type=u_p_rela_from_sim_users.col_type(),
                                data_frame=u_p_rela_from_sim_users.get_pickled_relations(),
                                alg_type=u_p_rela_from_sim_users.alg_type())

    def preprocessing(self, input_data):
        user_id = input_data['user_id']
        if User.objects.filter(id=user_id).exists():
            return user_id
        return -1

    def predict(self, input_data):
        latest_relation = Relation.objects.filter(row_type=User.__name__, col_type=Project.__name__,
                                                  alg_type=UserProjectCalcBySimilarUsers.__name__).last()
        relation_df = pickle.loads(latest_relation.data_frame)

        if input_data == -1:
            return relation_df.sample(n=1)
        else:
            return relation_df.loc[[input_data]]

    def postprocessing(self, prediction):
        prediction = prediction.melt().sort_values('value', ascending=False)
        top_100_projects = prediction.head(100)['variable'].to_list()
        return {"projects": top_100_projects, "label": "Recommended projects from similar users", "status": "OK",
                "alg_name": SimilarUserBased.algorithm_name}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
