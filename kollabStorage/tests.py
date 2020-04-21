from django.test import TestCase
from django.utils import timezone
from kollabStorage.models import User, Expertise, Project


class UserTestCase(TestCase):
    def setUp(self):
        t = timezone.now().isoformat()
        u = User.objects.create(id=1, first_name="f1",
                                last_name="l1", created_at=t, updated_at=t)
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
