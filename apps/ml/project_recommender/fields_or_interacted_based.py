import traceback

from apps.kstorage.models import User

from apps.ml.project_recommender.interacted_projects_based import InteractedProjectsBased
from apps.ml.project_recommender.user_project_fields_based import ProjectToUserFieldsBased
from apps.ml.recommender import Recommender


class FieldsOrInteractedBased(Recommender):
    endpoint_name = "project_recommender"
    algorithm_name = "Fields or Interacted Projects Based"
    owner = "Nattaphol"
    description = "Recommend projects based on projects that a user interacts with in the past " \
                  "or based on their fields depending on the user's interactions in the past."
    version = "0.0.2"
    status = "production"

    @classmethod
    def pre_calculate(cls):
        print(f'{FieldsOrInteractedBased.__name__}: Create user and project relation by fields.')
        ProjectToUserFieldsBased.pre_calculate()
        InteractedProjectsBased.pre_calculate()

    def preprocessing(self, input_data):
        user_id = input_data['user_id']
        if User.objects.filter(id=user_id).exists():
            return input_data

        input_data['user_id'] = -1
        return input_data

    def predict(self, input_data):
        if input_data['user_id'] == -1:
            return ProjectToUserFieldsBased().compute_prediction(input_data)

        user = User.objects.filter(id=input_data['user_id']).last()
        if self.have_enough_history(user):
            return InteractedProjectsBased().compute_prediction(input_data)
        else:
            return ProjectToUserFieldsBased().compute_prediction(input_data)

    def postprocessing(self, prediction):
        return prediction

    def compute_prediction(self, input_data):
        try:
            processed_input_data = self.preprocessing(input_data)
            prediction = self.predict(processed_input_data)
            processed_prediction = self.postprocessing(prediction)

        except Exception as e:
            traceback.print_exc()
            return {"status": "Error", "message": str(e)}

        return processed_prediction

    def have_enough_history(self, user):
        if len(user.viewed_projects) > 3:
            return True
        elif len(user.joined_projects) >= 1:
            return True
        elif len(user.starred_projects) >= 1:
            return True
        elif len(user.followed_projects) >= 1:
            return True
        return False
