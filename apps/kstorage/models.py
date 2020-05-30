from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(default="default@kollab.default")
    role = models.CharField(max_length=50, null=True)
    faculty_id = models.IntegerField(null=True)
    fields = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)), default=list)
    skills = ArrayField(models.CharField(max_length=50, blank=True, null=True), default=list)
    joined_projects = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    starred_projects = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    viewed_projects = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    followed_projects = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    year = models.CharField(max_length=20, null=True)

    def interacted_projects(self):
        return self.joined_projects + self.starred_projects + self.viewed_projects + self.followed_projects

    def __str__(self):
        return self.email


class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    project_status = models.SmallIntegerField(default=1, null=True)
    fields = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)), default=list)
    tags = ArrayField(models.CharField(max_length=50, blank=True, null=True), default=list)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title
