import pandas as pd
import pickle

from apps.kstorage.models import User, Project
from research.project_recommender.field_sim_calculator import FieldSimCalculator

class UserProjectRelationManager:
    '''
    Relation Manager
    '''
    def __init__(self):
        self.users = User.objects.all()
        self.projects = Project.objects.all()
        self.sim_calc = FieldSimCalculator()
        self.user_project_df = self.create_sim_table()

    @staticmethod
    def create_sim_table():
        # Create empty similarity table
        user_ids = User.objects.values_list('id', flat=True)
        project_ids = Project.objects.values_list('id', flat=True)
        user_project_df = pd.DataFrame(index=user_ids, columns=project_ids)
        return user_project_df

    def fill_sim_table(self):
        for user in self.users:
            for project in self.projects:
                u_fields = user.expertises
                p_fields = project.categories
                sim = self.sim_calc.calc_sim_by_fields(u_fields, p_fields)
                self.user_project_df.loc[user.id, project.id] = sim
        return self.user_project_df

    def get_sim_table(self):
        return self.user_project_df

    def get_picked_sim_table(self):
        return pickle.dumps(self.user_project_df)

    def get_users_count(self):
        return len(self.user_project_df)

    def get_projects_count(self):
        return len(self.user_project_df.columns)

