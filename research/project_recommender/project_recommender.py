import pandas as pd
import pickle
from abc import ABC, abstractmethod

from apps.kstorage.models import User, Project
from research.project_recommender.field_sim_calculator import FieldSimCalculator


class Relationship(ABC):
    '''
        Based class for relationships
    '''

    def __init__(self, index, columns):
        self.relations_df = pd.DataFrame(index=index, columns=columns)

    @abstractmethod
    def fill_relations(self):
        pass

    def get_relations(self):
        return self.relations_df

    def get_picked_relations(self):
        return pickle.dumps(self.relations_df)

    def row_count(self):
        return len(self.relations_df)

    def col_count(self):
        return len(self.relations_df.columns)


class UserProjectRelationship(Relationship):
    '''
        Handle relations for users and projects
    '''

    def __init__(self, index=User.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True)):
        super().__init__(index, columns)
        self.users = User.objects.all()
        self.projects = Project.objects.all()
        self.sim_calc = FieldSimCalculator()

    def fill_relations(self):
        for user in self.users:
            for project in self.projects:
                u_fields = user.expertises
                p_fields = project.categories
                sim = self.sim_calc.calc_sim_by_fields(u_fields, p_fields)
                self.relations_df.loc[user.id, project.id] = sim
        return self.relations_df


class ProjectRelationship(Relationship):
    '''
        Handle relations for users and projects
    '''

    def __init__(self, index=Project.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True)):
        super().__init__(index, columns)
        self.projects = Project.objects.all()
        self.sim_calc = FieldSimCalculator()

    def fill_relations(self):
        for project_row in self.projects:
            for project_col in self.projects:
                row_fields = project_row.categories
                col_fields = project_col.categories
                sim = self.sim_calc.calc_sim_by_fields(row_fields, col_fields)
                self.relations_df.loc[project_row.id, project_col.id] = sim
        return self.relations_df
