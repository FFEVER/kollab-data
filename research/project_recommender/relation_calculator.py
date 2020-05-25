import itertools
from scipy.spatial.distance import cosine
from abc import ABC, abstractmethod


class RelationCalculator(ABC):
    @classmethod
    @abstractmethod
    def calc_relation(cls, obj_a, obj_b):
        pass


class RelationCalcByFields(RelationCalculator):
    @classmethod
    def calc_relation(cls, obj_a, obj_b):
        cls.calc_sim_by_fields(obj_a.fields, obj_b.fields)

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

    @classmethod
    def calc_sim_by_fields(cls, field_list_1, field_list_2):
        unique = cls.unique_fields(field_list_1, field_list_2)
        sim_list_1 = list()
        sim_list_2 = list()
        for field in unique:
            # Similarity vector of list of fields 1
            sim_temp = []
            for f1 in field_list_1:
                sim_temp.append(cls.field_similarity(field, f1))
            sim_list_1.append(max(sim_temp))

            # Similarity vector of list of fields 2
            sim_temp = []
            for f2 in field_list_2:
                sim_temp.append(cls.field_similarity(field, f2))
            sim_list_2.append(max(sim_temp))

        val_out = 1 - cosine(sim_list_1, sim_list_2)
        return val_out


class RelationCalcByInteractions(RelationCalculator):

    @classmethod
    def calc_relation(cls, obj_a, obj_b):
        return 0
