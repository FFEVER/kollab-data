import pickle

from apps.kstorage.models import User, Project
from apps.ml.models import Relation
from apps.ml.recommender import Recommender
from research.project_recommender.relation_calculator import RelationCalcByFields
from research.project_recommender.relationship import UserProjectRelationship


class UserProjectFieldsBased(Recommender):
    endpoint_name = "project_recommender"
    algorithm_name = "User's and project's fields based"
    owner = "Nattaphol"
    description = "Predict projects based on user and project fields"
    version = "0.0.3"
    status = "production"

    @classmethod
    def pre_calculate(cls):
        print(f'{UserProjectFieldsBased.__name__}: Create user and project relation by fields.')
        user_project_by_fields = UserProjectRelationship()
        user_project_by_fields.fill_relations()
        Relation.objects.create(row_count=user_project_by_fields.row_count(),
                                col_count=user_project_by_fields.col_count(),
                                row_type=user_project_by_fields.row_type(),
                                col_type=user_project_by_fields.col_type(),
                                data_frame=user_project_by_fields.get_pickled_relations(),
                                alg_type=user_project_by_fields.alg_type())

    def preprocessing(self, input_data):
        user_id = input_data['user_id']
        if User.objects.filter(id=user_id).exists():
            return user_id
        return -1

    def predict(self, input_data):
        latest_relation = Relation.objects.filter(row_type=User.__name__, col_type=Project.__name__,
                                                  alg_type=RelationCalcByFields.__name__).last()
        relation_df = pickle.loads(latest_relation.data_frame)

        if input_data == -1:
            return relation_df.sample(n=1)
        else:
            return relation_df.loc[[input_data]]

    def postprocessing(self, prediction):
        prediction = prediction.melt().sort_values('value', ascending=False)
        top_100_projects = prediction.head(100)['variable'].to_list()
        return {"projects": top_100_projects, "label": "top_related_projects", "status": "OK",
                "alg_name": UserProjectFieldsBased.algorithm_name}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
