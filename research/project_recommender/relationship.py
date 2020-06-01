import pandas as pd
import pickle
from abc import ABC, abstractmethod

from apps.kstorage.models import User, Project
from research.project_recommender.relation_calculator import RelationCalcByFields, RelationCalcByInteractions, \
    UserToUserCalcByInteractions, UserProjectCalcBySimilarUsers, ProjectUserCalcBySimilarProjects


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


class UserProjectRelationFromSimilarUsers(Relationship):
    '''
        Handle relations for users and projects calculated using similar users (collaborative)
    '''

    def __init__(self, index=User.objects.values_list('id', flat=True),
                 columns=Project.objects.values_list('id', flat=True),
                 calculator_class=UserProjectCalcBySimilarUsers, k=10):
        super().__init__(index, columns, calculator_class)
        self.users = User.objects.all()
        self.projects = Project.objects.all()
        self.user_df = self.calculator.user_df
        self.k = k

    def get_k_similar_users(self, target_user):
        similar_users_df = self.user_df.loc[[target_user]].melt().sort_values('value', ascending=False)
        filtered_similar_users_df = similar_users_df.loc[similar_users_df['value'] != 0]
        similar_users = filtered_similar_users_df.head(self.k)['variable'].to_list()
        return similar_users

    def fill_relations(self):
        self.relations_df.fillna(0, inplace=True)
        for user in self.users:
            similar_users = self.get_k_similar_users(user.id)
            projects, sims = self.calculator.calc_relation(user.id, similar_users)
            # print("projects", projects)
            # print("sims", sims)
            for i in range(len(projects)):
                if not self.projects.filter(id=projects[i]).exists():
                    continue
                self.relations_df.loc[user.id, projects[i]] = sims[i]
        return self.relations_df

    def row_type(self):
        return User.__name__

    def col_type(self):
        return Project.__name__


class ProjectUserRelationFromSimilarProjects(Relationship):
    '''
        Handle relations for projects and users calculated using similar projects (collaborative)
    '''

    def __init__(self, index=Project.objects.values_list('id', flat=True),
                 columns=User.objects.values_list('id', flat=True),
                 calculator_class=ProjectUserCalcBySimilarProjects, k=10):
        super().__init__(index, columns, calculator_class)
        self.users = User.objects.all()
        self.projects = Project.objects.all()
        self.project_df = self.calculator.project_df
        self.k = k

    def get_k_similar_projects(self, target_project):
        similar_projects_df = self.project_df.loc[[target_project]].melt().sort_values('value', ascending=False)
        filtered_similar_projects_df = similar_projects_df.loc[similar_projects_df['value'] != 0]
        similar_projects = filtered_similar_projects_df.head(self.k)['variable'].to_list()
        return similar_projects

    def fill_relations(self):
        self.relations_df.fillna(0, inplace=True)
        for project in self.projects:
            similar_projects = self.get_k_similar_projects(project.id)
            users, sims = self.calculator.calc_relation(project.id, similar_projects)
            # print("users", users)
            # print("sims", sims)
            for i in range(len(users)):
                if not self.users.filter(id=users[i]).exists():
                    continue
                if users[i] in project.members:
                    # Do not recommend the user that already in the target project
                    continue
                self.relations_df.loc[project.id, users[i]] = sims[i]
        return self.relations_df

    def row_type(self):
        return Project.__name__

    def col_type(self):
        return User.__name__
