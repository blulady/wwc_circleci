from django.test import TestCase
from ..models import Team


class TeamModelSeedDataTestCase(TestCase):

    def test_team_seed_data(self):
        teams = Team.objects.values_list('name', flat=True)
        teams = list(teams)
        self.assertEqual(len(teams), 7)
        self.assertEqual(teams[0], 'Event Volunteers')
        self.assertEqual(teams[1], 'Hackathon Volunteers')
        self.assertEqual(teams[2], 'Host Management')
        self.assertEqual(teams[3], 'Partnership Management')
        self.assertEqual(teams[4], 'Social Media')
        self.assertEqual(teams[5], 'Tech Event Volunteers')
        self.assertEqual(teams[6], 'Volunteer Management')
