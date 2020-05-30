import pickle
import traceback

from apps.kstorage.models import User, Project
from apps.ml.models import Relation

from apps.ml.recommender import Recommender
from research.project_recommender.relation_calculator import RelationCalcByFields
from research.project_recommender.relationship import ProjectRelationship


class ProjectFieldsBased(Recommender):
    endpoint_name = "related_project"
    algorithm_name = "Related Projects by Fields"
    owner = "Nattaphol"
    description = "Recommend a related projects of a given project using its fields"
    version = "0.0.1"
    status = "production"

    @classmethod
    def pre_calculate(cls):
        print(f'{ProjectFieldsBased.__name__}: Create project and project relation by fields.')
        # Relation table for project/project
        project_by_fields = ProjectRelationship()
        project_by_fields.fill_relations()
        Relation.objects.get_or_create(row_count=project_by_fields.row_count(),
                                       col_count=project_by_fields.col_count(),
                                       row_type=project_by_fields.row_type(),
                                       col_type=project_by_fields.col_type(),
                                       data_frame=project_by_fields.get_pickled_relations(),
                                       alg_type=project_by_fields.alg_type())

    def preprocessing(self, input_data):
        project_id = input_data['project_id']
        if Project.objects.filter(id=project_id).exists():
            return project_id
        return -1

    def predict(self, input_data):
        latest_relation = Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__,
                                                  alg_type=RelationCalcByFields.__name__).last()
        relation_df = pickle.loads(latest_relation.data_frame)

        if input_data == -1:
            return relation_df.sample(n=1)
        else:
            return relation_df.loc[[input_data]]

    def postprocessing(self, prediction):
        prediction = prediction.melt().sort_values('value', ascending=False)
        top_100_projects = prediction.head(100)['variable'].to_list()
        return {"projects": top_100_projects, "label": "related_projects", "status": "OK",
                "alg_name": ProjectFieldsBased.algorithm_name}

    def compute_prediction(self, input_data):
        try:
            processed_input_data = self.preprocessing(input_data)
            prediction = self.predict(processed_input_data)
            processed_prediction = self.postprocessing(prediction)

        except Exception as e:
            traceback.print_exc()
            return {"status": "Error", "message": str(e)}

        return processed_prediction
