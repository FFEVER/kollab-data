import pandas as pd
import pickle
from abc import ABC, abstractmethod

from apps.kstorage.models import User, Project
from research.project_recommender.relation_calculator import RelationCalcByFields, RelationCalcByInteractions, \
    UserToUserCalcByInteractions


class Relationship(ABC):
    '''
        Based class for relationships
    '''

    def __init__(self, index, columns, calculator_class):
        self.relations_df = pd.DataFrame(index=index, columns=columns)
        self.calculator = calculator_class()

    @abstractmethod
    def fill_relations(self):
        pass

    def get_relations(self):
        return self.relations_df

    def get_pickled_relations(self):
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
        return type(self.calculator).__name__


class UserProjectRelationship(Relationship):
    '''
        Handle relations for users and projects
    '''

    def __init__(self, index=User.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True),
                 calculator_class=RelationCalcByFields):
        super().__init__(index, columns, calculator_class)
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


class ProjectUserRelationship(Relationship):
    '''
        Handle relations for projects and users
    '''

    def __init__(self, index=Project.objects.values_list('id', flat=True),
                 columns=User.objects.values_list('id', flat=True),
                 calculator_class=RelationCalcByFields):
        super().__init__(index, columns, calculator_class)
        self.users = User.objects.all()
        self.projects = Project.objects.all()

    def fill_relations(self):
        for project in self.projects:
            for user in self.users:
                sim = self.calculator.calc_relation(project, user)
                self.relations_df.loc[project.id, user.id] = sim
        return self.relations_df

    def row_type(self):
        return Project.__name__

    def col_type(self):
        return User.__name__


class ProjectRelationship(Relationship):
    '''
        Handle relations for projects and projects
    '''

    def __init__(self, index=Project.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True),
                 calculator_class=RelationCalcByFields):
        super().__init__(index, columns, calculator_class)
        self.projects = Project.objects.all()

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

class UserRelationship(Relationship):
    '''
        Handle relations for users and users
    '''

    def __init__(self, index=User.objects.values_list('id', flat=True),
                 columns=User.objects.values_list('id', flat=True),
                 calculator_class=UserToUserCalcByInteractions):
        super().__init__(index, columns, calculator_class)
        self.users = User.objects.all()

    def fill_relations(self):
        for user_row in self.users:
            for user_col in self.users:
                sim = self.calculator.calc_relation(user_row, user_col)
                self.relations_df.loc[user_row.id, user_col.id] = sim
        return self.relations_df

    def row_type(self):
        return User.__name__

    def col_type(self):
        return User.__name__
