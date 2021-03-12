from django.test import TransactionTestCase
from ..models import User, Team, User_Team
from django.db import IntegrityError


class UserTeamModelTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json']

    # Testing unique constraint user team
    def test_unique_constraint(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        userteam1 = User_Team(user=user1, team=team1)
        userteam1.save()
        userteam2 = User_Team(user=user1, team=team1)
        self.assertRaises(IntegrityError, lambda: userteam2.save())

    # Testing a User can belong to many teams
    def test_user_can_belong_to_many_teams(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        team2 = Team.objects.get(name='Tech Event Volunteers')
        team3 = Team.objects.get(name='Partnership Management')
        team4 = Team.objects.get(name='Social Media')
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=team1),
            User_Team(user=user1, team=team2),
            User_Team(user=user1, team=team3),
            User_Team(user=user1, team=team4),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 4)

    # Testing a Team can have multiple Users
    def test_team_can_have_many_users(self):
        user1 = User.objects.get(email="director@example.com")
        user2 = User.objects.get(email="leader@example.com")
        user3 = User.objects.get(email="volunteer@example.com")
        team1 = Team.objects.get(name='Hackathon Volunteers')
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=team1),
            User_Team(user=user2, team=team1),
            User_Team(user=user3, team=team1),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 3)
