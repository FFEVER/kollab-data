import pandas as pd
import pickle
from abc import ABC, abstractmethod

from apps.kstorage.models import User, Project
from research.project_recommender.relation_calculator import RelationCalcByFields, RelationCalcByInteractions


class Relationship(ABC):
    '''
        Based class for relationships
    '''

    def __init__(self, index, columns, calculator):
        self.relations_df = pd.DataFrame(index=index, columns=columns)
        self.calculator = calculator

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

    @abstractmethod
    def row_type(self):
        pass

    @abstractmethod
    def col_type(self):
        pass

    def alg_type(self):
        return self.calculator.__name__

class UserProjectRelationship(Relationship):
    '''
        Handle relations for users and projects
    '''

    def __init__(self, index=User.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True),
                 calculator=RelationCalcByFields):
        super().__init__(index, columns, calculator)
        self.users = User.objects.all()
        self.projects = Project.objects.all()

    def fill_relations(self):
        for user in self.users:
            for project in self.projects:
                sim = self.calculator.calc_relation(user, project)
                self.relations_df.loc[user.id, project.id] = sim
        return self.relations_df

    def row_type(self):
        return User.__name__

    def col_type(self):
        return Project.__name__


class ProjectRelationship(Relationship):
    '''
        Handle relations for users and projects
    '''

    def __init__(self, index=Project.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True),
                 calculator=RelationCalcByFields):
        super().__init__(index, columns, calculator)
        self.projects = Project.objects.all()
        self.sim_calc = RelationCalcByFields()

    def fill_relations(self):
        for project_row in self.projects:
            for project_col in self.projects:
                sim = self.calculator.calc_relation(project_row, project_col)
                self.relations_df.loc[project_row.id, project_col.id] = sim
        return self.relations_df

    def row_type(self):
        return Project.__name__

    def col_type(self):
        return Project.__name__
