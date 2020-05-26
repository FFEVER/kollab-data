import itertools
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
            Relation.objects.filter(row_type=Project.__name__, col_type=Project.__name__).last().data_frame)

    def calc_relation(self, user: User, project: Project):
        try:
            if self.__check_conditions(user, project) == False:
                return 0

            sim_list = []
            print("member")
            m_sim = self.calc_by_weighted_values(project, user.joined_projects, self.MEMBER_WEIGHT, self.MAX_MEMBERS)
            sim_list.append(m_sim)
            print("\nstar")
            s_sim = self.calc_by_weighted_values(project, user.starred_projects, self.STAR_WEIGHT, self.MAX_STARS)
            sim_list.append(s_sim)
            print("\nfollow")
            f_sim = self.calc_by_weighted_values(project, user.followed_projects, self.FOLLOW_WEIGHT, self.MAX_FOLLOWS)
            sim_list.append(f_sim)
            print("\nview")
            v_sim = self.calc_by_weighted_values(project, user.viewed_projects, self.VIEW_WEIGHT, self.MAX_VIEWS)
            sim_list.append(v_sim)

            return np.average(sim_list)

        except Exception as e:
            print("Exception while calculating relation,", str(e))
            return 0

    def __check_conditions(self, user, project):
        if project.id in user.joined_projects:
            return False
        return True

    def calc_by_weighted_values(self, target_project, comparing_project_ids, max_weight, max_n_projects):
        if len(comparing_project_ids) <= 0:
            return 0
        count = 0
        sim_list = []
        weight_list = []
        current_weight = max_weight

        for comparing_id in comparing_project_ids:
            if not comparing_id in self.project_df:
                continue

            row_id = target_project.id
            similarity = self.project_df.loc[row_id, comparing_id]

            sim_list.append(similarity)
            weight_list.append(current_weight)

            count += 1
            current_weight = self.__normalize_weight(max_weight, max_n_projects, count)

        weighted_avg = np.average(sim_list, weights=weight_list)

        print("sim_list", sim_list)
        print("weight_list", weight_list)
        print("weighted_avg", weighted_avg)

        return weighted_avg

    def __normalize_weight(self, max_weight, max_n_projects, count):
        return max_weight - (count * (max_weight / max_n_projects))
