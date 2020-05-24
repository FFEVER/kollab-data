import itertools

from scipy.spatial.distance import cosine
import pandas as pd
import pickle

from apps.kstorage.models import User, Project


class FieldSimCalculator:
    def field_similarity(self, f1, f2):
        if f1[0] == f2[0]:
            if f1[1] == f2[1]:
                if f1[2] == f2[2]:
                    return 1
                return 0.7
            return 0.3
        return 0

    def unique_fields(self, field_list_1, field_list_2):
        '''
            Return a list of unique fields
            e.g. [[1,2],[8,9]] + [[8,9],[10,11]] = [[1,2],[8,9],[10,11]]
        '''
        f = field_list_1 + field_list_2
        f.sort()
        return list(f for f, _ in itertools.groupby(f))

    def calc_sim_by_fields(self, field_list_1, field_list_2):
        unique = self.unique_fields(field_list_1, field_list_2)
        sim_list_1 = list()
        sim_list_2 = list()
        for field in unique:
            # Similarity vector of list of fields 1
            sim_temp = []
            for f1 in field_list_1:
                sim_temp.append(self.field_similarity(field, f1))
            sim_list_1.append(max(sim_temp))

            # Similarity vector of list of fields 2
            sim_temp = []
            for f2 in field_list_2:
                sim_temp.append(self.field_similarity(field, f2))
            sim_list_2.append(max(sim_temp))

        val_out = 1 - cosine(sim_list_1, sim_list_2)
        return val_out


class UserProjectSimilarity:
    def __init__(self):
        self.users = User.objects.all()
        self.projects = Project.objects.all()
        self.sim_calc = FieldSimCalculator()
        self.user_project_df = self.create_sim_table()

    def create_sim_table(self):
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
