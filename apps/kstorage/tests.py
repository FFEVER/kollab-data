from django.test import TestCase
from django.utils import timezone
from apps.kstorage.models import User, Project


class UserTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        u = User.objects.create(id=1, email="eit@gmail.com", role="student", faculty_id=1, year="1",
                                fields=[[1, 2, 3], [5, 6, -1]], skills=["a", "b", "c"],
                                joined_projects=[1, 2, 3], starred_projects=[4, 5, 6], viewed_projects=[7, 8, 9],
                                followed_projects=[10, 11, 12])

    def test_user_has_correct_attributes(self):
        """Users should have correct attributes"""
        u1 = User.objects.get(id=1)
        self.assertEqual("student", u1.role)
        self.assertEqual(1, u1.faculty_id)
        self.assertEqual("1", u1.year)
        self.assertEqual([[1, 2, 3], [5, 6, -1]], u1.fields)
        self.assertEqual(["a", "b", "c"], u1.skills)
        self.assertEqual([1, 2, 3], u1.joined_projects)
        self.assertEqual([4, 5, 6], u1.starred_projects)
        self.assertEqual([7, 8, 9], u1.viewed_projects)
        self.assertEqual([10, 11, 12], u1.followed_projects)


class ProjectTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        p = Project.objects.create(id=1, title="Title 1", project_status=1, created_at=t, updated_at=t,
                                   fields=[[1, 2, 3], [5, 6, -1]], tags=["a", "b", "c"])

    def test_project_has_many_expertises(self):
        """Projects should have correct attributes"""
        p1 = Project.objects.get(id=1)
        self.assertEqual("Title 1", p1.title)
        self.assertEqual(1, p1.project_status)
        self.assertEqual([[1, 2, 3], [5, 6, -1]], p1.fields)
        self.assertEqual(["a", "b", "c"], p1.tags)
