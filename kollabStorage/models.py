from django.db import models


class Expertise(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    parent_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(default="default@kollab.default")
    role = models.CharField(max_length=50, null=True)
    faculty = models.CharField(max_length=150, null=True)
    expertises = models.ManyToManyField(Expertise)
    year = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.email


class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    short_desc = models.TextField()
    long_desc = models.TextField()
    expertises = models.ManyToManyField(Expertise)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Skill(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
