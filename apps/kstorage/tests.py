from django.test import TestCase
from django.utils import timezone
from apps.kstorage.models import User, Project


class UserTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        u = User.objects.create(id=1, email="eit@gmail.com", role="student", faculty=1, year="1",
                                expertises=[[1, 2, 3], [5, 6]])

    def test_user_has_correct_attributes(self):
        """Users should have correct attributes"""
        u1 = User.objects.get(id=1)
        self.assertEqual("student", u1.role)
        self.assertEqual(1, u1.faculty)
        self.assertEqual("1", u1.year)
        self.assertEqual([[1, 2, 3], [5, 6]], u1.expertises)


class ProjectTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        p = Project.objects.create(id=1, title="Title 1", project_status=1, created_at=t, updated_at=t,
                                   categories=[[1, 2, 3], [5, 6]])

    def test_project_has_many_expertises(self):
        """Projects should have correct attributes"""
        p1 = Project.objects.get(id=1)
        self.assertEqual("Title 1", p1.title)
        self.assertEqual(1, p1.project_status)
        self.assertEqual([[1, 2, 3], [5, 6]], p1.expertises)
