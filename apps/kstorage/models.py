from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(default="default@kollab.default")
    role = models.CharField(max_length=50, null=True)
    faculty = models.IntegerField(null=True)
    expertises = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)))
    skills = ArrayField(models.CharField(max_length=50))
    year = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.email


class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    project_status = models.SmallIntegerField(default=1, null=True)
    expertises = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)))
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title
