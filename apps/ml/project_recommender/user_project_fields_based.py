import pandas as pd
from recommender.settings import BASE_DIR
from apps.kstorage.models import User
from apps.ml.models import UserProjectRelation
import pickle


class UserProjectFieldsBased:
    endpoint_name = "project_recommender"
    algorithm_name = "User's and project's fields based"
    owner = "Nattaphol"
    description = "Predict projects based on user and project fields"
    version = "0.0.1"
    status = "production"

    def __init__(self):
        self.path_to_artifacts = BASE_DIR + "/research/project_recommender/"

    def preprocessing(self, input_data):

        user_id = input_data['user_id']
        if User.objects.filter(id=user_id).exists():
            return user_id
        return -1

    def predict(self, input_data):
        latest_relation = UserProjectRelation.objects.last()
        relation_df = pickle.loads(latest_relation.data_frame)

        if input_data == -1:
            return relation_df.sample(n=1)
        else:
            return relation_df.loc[[input_data]]

    def postprocessing(self, prediction):
        prediction = prediction.melt().sort_values('value', ascending=False)
        top_100_projects = prediction.head(100)['variable'].to_list()
        return {"projects": top_100_projects, "label": "top_related_projects", "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
