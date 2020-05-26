from django.db import models

class Relation(models.Model):
    '''
    The UserProjectRelation represent how a user is related to a project.

    Attributes:
        row_count: The number of row.
        col_count: The number of column.
        row_type: The type of row (User or Project).
        col_type: The type of col (User or Project).
        data_frame: Binary data of pickled dataframe.
        alg_type: The calculation type.
        created_at: The date when MLAlgorithm was added.
    '''

    row_count = models.IntegerField()
    col_count = models.IntegerField()
    row_type = models.CharField(max_length=50, default="User")
    col_type = models.CharField(max_length=50, default="Project")
    data_frame = models.BinaryField()
    alg_type = models.CharField(max_length=50, default="RelationCalcByFields")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.alg_type
