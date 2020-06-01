import itertools
import traceback

from scipy.spatial.distance import cosine
from abc import ABC, abstractmethod
import pickle
import numpy as np

from apps.ml.models import Relation
from apps.kstorage.models import User, Project


class RelationCalculator(ABC):
    @abstractmethod
    def calc_relation(self, obj_a, obj_b):
        pass


class RelationCalcByFields(RelationCalculator):
    def calc_relation(self, obj_a, obj_b):
        return self.calc_sim_by_fields(obj_a.fields, obj_b.fields)

    @staticmethod
    def field_similarity(f1, f2):
        if f1[0] == f2[0]:
            if f1[1] == f2[1]:
                if f1[2] == f2[2]:
                    return 1
                return 0.7
            return 0.3
        return 0

    @staticmethod
    def unique_fields(field_list_1, field_list_2):
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


class RelationCalcByInteractions(RelationCalculator):
    MEMBER_WEIGHT = 4
    STAR_WEIGHT = 3
    FOLLOW_WEIGHT = 3
    VIEW_WEIGHT = 2

    MAX_MEMBERS = 3
    MAX_STARS = 8
    MAX_FOLLOWS = 8
    MAX_VIEWS = 16

    def __init__(self):
        self.project_df = pickle.loads(
            Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__,
                                    alg_type=RelationCalcByFields.__name__).last().data_frame)

    def calc_relation(self, user: User, project: Project):
        try:
            if not self.__check_conditions(user, project):
                return 0

            m_weights, m_sims = self.calc_by_weighted_values(project, user.joined_projects, self.MEMBER_WEIGHT,
                                                             1, self.MAX_MEMBERS)
            s_weights, s_sims = self.calc_by_weighted_values(project, user.starred_projects, self.STAR_WEIGHT,
                                                             1, self.MAX_STARS)
            f_weights, f_sims = self.calc_by_weighted_values(project, user.followed_projects, self.FOLLOW_WEIGHT,
                                                             1, self.MAX_FOLLOWS)
            v_weights, v_sims = self.calc_by_weighted_values(project, user.viewed_projects, self.VIEW_WEIGHT,
                                                             1, self.MAX_VIEWS)

            sim_list = m_sims + s_sims + f_sims + v_sims
            weight_list = m_weights + s_weights + f_weights + v_weights

            if sum(weight_list) == 0:
                return 0

            weighted_avg = np.average(sim_list, weights=weight_list)
            return weighted_avg

        except Exception as e:
            traceback.print_exc()
            print("Exception while calculating relation,", e)
            return 0

    def __check_conditions(self, user, project):
        if project.id in user.joined_projects:
            return False
        return True

    def calc_by_weighted_values(self, target_project, comparing_project_ids, max_weight, min_weight, max_n_projects):
        count = 0
        sim_list = []
        weight_list = []
        current_weight = max_weight

        for comparing_id in comparing_project_ids:
            if comparing_id not in self.project_df:
                continue

            if count == max_n_projects:
                break

            row_id = target_project.id
            similarity = self.project_df.loc[row_id, comparing_id]

            sim_list.append(similarity)
            weight_list.append(current_weight)

            count += 1
            current_weight = self.__normalize_weight(max_weight, min_weight, max_n_projects, count)

        return weight_list, sim_list

    def __normalize_weight(self, max_weight, min_weight, max_n_projects, count):
        return max_weight - (count * ((max_weight - min_weight) / (max_n_projects - 1)))


class UserToUserCalcByInteractions(RelationCalculator):
    def __init__(self):
        self.project_df = pickle.loads(
            Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__,
                                    alg_type=RelationCalcByFields.__name__).last().data_frame)

    def calc_relation(self, user1, user2):
        try:
            u1_projects = user1.interacted_projects()
            u2_projects = user2.interacted_projects()
            return self.calc_sim_by_interacted_projects(u1_projects, u2_projects)
        except Exception as e:
            traceback.print_exc()
            print("Exception while calculating relation,", e)
            return 0

    def calc_sim_by_interacted_projects(self, project_list_1, project_list_2):
        if len(project_list_1) == 0 or len(project_list_2) == 0:
            return 0

        unique = list(set(project_list_1).union(project_list_2))
        sim_list_1 = list()
        sim_list_2 = list()
        for p_id in unique:
            if p_id not in self.project_df:
                continue

            # Similarity vector of user 1
            sim_temp_1 = []
            for p1_id in project_list_1:
                if p1_id not in self.project_df:
                    continue
                sim_temp_1.append(self.project_df.loc[p1_id, p_id])

            # Similarity vector of user 2
            sim_temp_2 = []
            for p2_id in project_list_2:
                if p2_id not in self.project_df:
                    continue
                sim_temp_2.append(self.project_df.loc[p2_id, p_id])

            sim_list_1.append(max(sim_temp_1))
            sim_list_2.append(max(sim_temp_2))

        val_out = 1 - cosine(sim_list_1, sim_list_2)
        return val_out


class UserProjectCalcBySimilarUsers(RelationCalculator):
    def __init__(self):
        self.project_df = pickle.loads(
            Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__,
                                    alg_type=RelationCalcByFields.__name__).last().data_frame)
        self.user_df = pickle.loads(
            Relation.objects.filter(row_type=User.__name__, col_type=User.__name__,
                                    alg_type=UserToUserCalcByInteractions.__name__).last().data_frame)

    def calc_relation(self, target_user_id, similar_users):
        try:
            all_projects = set()
            all_users = dict()
            all_weights = dict()
            for u in similar_users:
                user = User.objects.get(pk=u)
                projects = user.interacted_projects()
                all_users[user.id] = projects
                all_weights[user.id] = self.user_df.loc[target_user_id, u]
                all_projects = all_projects.union(projects)

            all_projects = list(all_projects)

            # print("all projects", all_projects)
            # print("users:", all_users)
            # print("weights:", all_weights)
            weighted_sims = self.calc_weighted_sims(all_projects, all_users, all_weights)

            # print("weighted sims:", weighted_sims)

            return all_projects, weighted_sims

        except Exception as e:
            traceback.print_exc()
            print("Exception while calculating relation,", e)
            return [], []

    def max_sim(self, p_target, p_list):
        sim = 0
        if p_target not in self.project_df:
            return sim
        for p in p_list:
            if p not in self.project_df:
                continue
            new_sim = self.project_df.loc[p_target, p]
            if new_sim > sim:
                sim = new_sim
        return sim

    def calc_weighted_sims(self, all_projects, all_users, all_weights):
        weighted_sims = []
        for project_id in all_projects:
            sim_temp = []
            for key in all_users:
                sim = self.max_sim(project_id, all_users[key])
                sim_temp.append(sim)

            weighted_sims.append(np.average(sim_temp, weights=list(all_weights.values())))

        return weighted_sims


class ProjectUserCalcBySimilarProjects(RelationCalculator):

    def __init__(self):
        self.project_df = pickle.loads(
            Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__,
                                    alg_type=RelationCalcByFields.__name__).last().data_frame)

        self.user_df = pickle.loads(
            Relation.objects.filter(row_type=User.__name__, col_type=User.__name__,
                                    alg_type=RelationCalcByFields.__name__).last().data_frame)

    def calc_relation(self, target_project_id, similar_projects):
        try:
            all_users = set()
            all_projects = dict()
            all_weights = dict()
            for p in similar_projects:
                project = Project.objects.get(pk=p)
                users = project.interacted_users()
                all_projects[project.id] = users
                all_weights[project.id] = self.project_df.loc[target_project_id, p]
                all_users = all_users.union(users)

            all_users = list(all_users)

            print("all users", all_users)
            print("projects:", all_projects)
            print("weights:", all_weights)
            weighted_sims = self.calc_weighted_sims(all_users, all_projects, all_weights)

            print("weighted sims:", weighted_sims)

            return all_users, weighted_sims

        except Exception as e:
            traceback.print_exc()
            print("Exception while calculating relation,", e)
            return [], []

    def max_sim(self, u_target, u_list):
        sim = 0
        if u_target not in self.user_df:
            return sim
        for u in u_list:
            if u not in self.user_df:
                continue
            new_sim = self.user_df.loc[u_target, u]
            if new_sim > sim:
                sim = new_sim
        return sim

    def calc_weighted_sims(self, all_users, all_projects, all_weights):
        weighted_sims = []
        for user_id in all_users:
            sim_temp = []
            for key in all_projects:
                sim = self.max_sim(user_id, all_projects[key])
                sim_temp.append(sim)

            weighted_sims.append(np.average(sim_temp, weights=list(all_weights.values())))

        return weighted_sims
