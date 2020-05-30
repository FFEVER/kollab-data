from apps.kstorage.models import User, Project
from apps.ml.models import Relation
import pickle

from apps.ml.recommender import Recommender
from research.project_recommender.relation_calculator import RelationCalcByInteractions
from research.project_recommender.relationship import UserProjectRelationship, ProjectRelationship


class InteractedProjectsBased(Recommender):
    endpoint_name = "project_recommender"
    algorithm_name = "Interacted Projects Based"
    owner = "Nattaphol"
    description = "Recommend projects based on projects that a user interacts with in the past"
    version = "0.0.2"
    status = "production"

    @classmethod
    def pre_calculate(cls):
        print(f'{InteractedProjectsBased.__name__}: Create project relation by fields.')
        cls.create_project_relation_by_fields()
        print(f'{InteractedProjectsBased.__name__}: Create user and project relation by interactions.')
        cls.create_user_project_relation_by_interactions()

    @staticmethod
    def create_project_relation_by_fields():
        # Relation table for project/project
        project_by_fields = ProjectRelationship()
        project_by_fields.fill_relations()
        Relation.objects.create(row_count=project_by_fields.row_count(),
                                col_count=project_by_fields.col_count(),
                                row_type=project_by_fields.row_type(),
                                col_type=project_by_fields.col_type(),
                                data_frame=project_by_fields.get_picked_relations(),
                                alg_type=project_by_fields.alg_type())

    @staticmethod
    def create_user_project_relation_by_interactions():
        # Relation table for past interactions based
        user_project_interactions = UserProjectRelationship(calculator_class=RelationCalcByInteractions)
        user_project_interactions.fill_relations()
        Relation.objects.create(row_count=user_project_interactions.row_count(),
                                col_count=user_project_interactions.col_count(),
                                row_type=user_project_interactions.row_type(),
                                col_type=user_project_interactions.col_type(),
                                data_frame=user_project_interactions.get_picked_relations(),
                                alg_type=user_project_interactions.alg_type())

    def preprocessing(self, input_data):
        user_id = input_data['user_id']
        if User.objects.filter(id=user_id).exists():
            return user_id
        return -1

    def predict(self, input_data):
        latest_relation = Relation.objects.filter(row_type=User.__name__, col_type=Project.__name__,
                                                  alg_type=RelationCalcByInteractions.__name__).last()
        relation_df = pickle.loads(latest_relation.data_frame)

        if input_data == -1:
            return relation_df.sample(n=1)
        else:
            return relation_df.loc[[input_data]]

    def postprocessing(self, prediction):
        prediction = prediction.melt().sort_values('value', ascending=False)
        top_100_projects = prediction.head(100)['variable'].to_list()
        return {"projects": top_100_projects, "label": "top_related_projects", "status": "OK",
                "alg_name": InteractedProjectsBased.algorithm_name}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
