from django.db import models


class UserProjectRelation(models.Model):
    '''
    The UserProjectRelation represent how a user is related to a project.

    Attributes:
        projects_count: The number of projects.
        users_count: The number of users.
        data_frame: Binary data of pickled dataframe where row are user_id and column are project_id
        created_at: The date when MLAlgorithm was added.
    '''

    users_count = models.IntegerField()
    projects_count = models.IntegerField()
    data_frame = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
