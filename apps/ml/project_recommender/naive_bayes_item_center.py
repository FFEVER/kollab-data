import joblib
import pandas as pd
from recommender.settings import BASE_DIR

from apps.kstorage.models import Project


class NaiveBayesItemCenter:
    def __init__(self):
        path_to_artifacts = BASE_DIR + "/research/project_recommender/"
        # self.values_fill_missing = joblib.load(path_to_artifacts + "train_mode.joblib")
        # self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        # self.model = joblib.load(path_to_artifacts + "random_forest.joblib")

    def preprocessing(self, input_data):
        return input_data

    def predict(self, input_data):
        return [1, 2, 3, 4]
        # return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        # stub to be changed
        project_ids = Project.objects.all().values_list('id', flat=True)
        return {"projects": project_ids}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
