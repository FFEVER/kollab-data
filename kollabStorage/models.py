from django.db import models


class Expertise(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    parent_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    expertises = models.ManyToManyField(Expertise)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.first_name + " " + self.last_name


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
