from django.test import TestCase
from django.utils import timezone
from kollabStorage.models import User, Expertise, Project


class UserTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        u = User.objects.create(id=1, email="eit@gmail.com", role="student", faculty="SE", year="1")
        e1 = Expertise.objects.create(id=1, name="Mathematics")
        e2 = Expertise.objects.create(id=2, name="Sciences")
        u.expertises.add(e1)
        u.expertises.add(e2)

    def test_user_has_many_expertises(self):
        """Users should has many Expertise"""
        u1 = User.objects.get(id=1)
        e1 = Expertise.objects.get(id=1)
        e2 = Expertise.objects.get(id=1)
        self.assertIn(e1, u1.expertises.all())
        self.assertIn(e2, u1.expertises.all())


class ProjectTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        p = Project.objects.create(id=1, title="Title 1", short_desc="short desc",
                                   long_desc="long desc", project_status=1, created_at=t, updated_at=t)
        e1 = Expertise.objects.create(id=1, name="Mathematics")
        e2 = Expertise.objects.create(id=2, name="Sciences")
        p.expertises.add(e1)
        p.expertises.add(e2)

    def test_project_has_many_expertises(self):
        """Projects should has many Expertise"""
        p1 = Project.objects.get(id=1)
        e1 = Expertise.objects.get(id=1)
        e2 = Expertise.objects.get(id=1)
        self.assertIn(e1, p1.expertises.all())
        self.assertIn(e2, p1.expertises.all())
