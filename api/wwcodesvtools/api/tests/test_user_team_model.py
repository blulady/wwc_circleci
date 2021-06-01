from django.test import TransactionTestCase
from ..models import User, Team, User_Team, Role
from django.db import IntegrityError


class UserTeamModelTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    # Testing unique constraint user team
    def test_unique_constraint(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        role1 = Role.objects.get(name=Role.DIRECTOR)
        userteam1 = User_Team(user=user1, team=team1, role=role1)
        userteam1.save()
        userteam2 = User_Team(user=user1, team=team1, role=role1)
        self.assertRaises(IntegrityError, lambda: userteam2.save())

    # Testing not-null constraint user role
    def test_not_null_constraint(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        userteam1 = User_Team(user=user1, team=team1, role=None)
        self.assertRaises(IntegrityError, lambda: userteam1.save())

    # Testing a User can belong to many teams with the same role
    def test_user_can_belong_to_many_teams_same_role(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        team2 = Team.objects.get(name='Tech Event Volunteers')
        team3 = Team.objects.get(name='Partnership Management')
        role1 = Role.objects.get(name=Role.DIRECTOR)
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=team1, role=role1),
            User_Team(user=user1, team=team2, role=role1),
            User_Team(user=user1, team=team3, role=role1)
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 17)

    # Testing a User can belong to many teams with different role
    def test_user_can_belong_to_many_teams_diff_roles(self):
        user1 = User.objects.get(email="director@example.com")
        team1 = Team.objects.get(name='Host Management')
        team2 = Team.objects.get(name='Tech Event Volunteers')
        team3 = Team.objects.get(name='Partnership Management')
        team4 = Team.objects.get(name='Social Media')
        role1 = Role.objects.get(name=Role.VOLUNTEER)
        role2 = Role.objects.get(name=Role.LEADER)
        role3 = Role.objects.get(name=Role.DIRECTOR)
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=team1, role=role1),
            User_Team(user=user1, team=team2, role=role2),
            User_Team(user=user1, team=team3, role=role3),
            User_Team(user=user1, team=team4, role=role1),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 18)

    # Testing a Team and Role can have multiple Users
    def test_team_can_have_many_users(self):
        user1 = User.objects.get(email="director@example.com")
        user2 = User.objects.get(email="leader@example.com")
        user3 = User.objects.get(email="volunteer@example.com")
        team1 = Team.objects.get(name='Hackathon Volunteers')
        role1 = Role.objects.get(name=Role.DIRECTOR)
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=team1, role=role1),
            User_Team(user=user2, team=team1, role=role1),
            User_Team(user=user3, team=team1, role=role1),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 17)

    # Testing Users with Role and without a Team
    def test_team_role_without_team(self):
        user2 = User.objects.get(email="leader@example.com")
        user3 = User.objects.get(email="volunteer@example.com")
        role2 = Role.objects.get(name=Role.LEADER)
        role3 = Role.objects.get(name=Role.VOLUNTEER)
        User_Team.objects.bulk_create([
            User_Team(user=user2, team=None, role=role2),
            User_Team(user=user3, team=None, role=role3),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 16)

    # Testing a user with different roles and without a team
    def test_user_with_roles_without_team(self):
        user1 = User.objects.get(email="director@example.com")
        role1 = Role.objects.get(name=Role.DIRECTOR)
        role2 = Role.objects.get(name=Role.LEADER)
        role3 = Role.objects.get(name=Role.VOLUNTEER)
        User_Team.objects.bulk_create([
            User_Team(user=user1, team=None, role=role1),
            User_Team(user=user1, team=None, role=role2),
            User_Team(user=user1, team=None, role=role3),
        ])
        user_teams = User_Team.objects.all()
        self.assertEqual(user_teams.count(), 17)
