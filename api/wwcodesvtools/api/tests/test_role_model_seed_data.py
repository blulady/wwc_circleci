from django.test import TestCase
from ..models import Role


class RoleModelSeedDataTestCase(TestCase):

    def test_role_seed_data(self):
        roles = Role.objects.values_list('name', flat=True)
        roles = list(roles)
        self.assertEqual(len(roles), 3)
        self.assertEqual(roles[0], Role.VOLUNTEER)
        self.assertEqual(roles[1], Role.LEADER)
        self.assertEqual(roles[2], Role.DIRECTOR)
