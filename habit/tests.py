
from rest_framework.test import APITestCase
from rest_framework import status

from habit.models import Habit
from users.models import User, UserRoles


class HabitsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            id=1,
            email='test@test.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
            chat_id=123456
        )
        self.user.set_password('1234567')
        self.user.save()
        response = self.client.post('/api/token/', {"email": "test@test.com", "password": "1234567"})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'test'

    def test_habit_create(self):
        habit_test = Habit.objects.create(name="test", place="test", time="13:00",
                                          action="test",
                                          is_pleasurable=True, periodic=1, reward=None, execution_time="00:01",
                                          public=True, owner=self.user, associated_habit=None)
        response = self.client.post('/api/habits/', {'name': "test2", "place": "test", "time": "13:00",
                                                     "action": "test", "is_pleasurable": True,
                                                     "periodic": 1, "reward": 'None', "execution_time": "00:01",
                                                     "public": True, "owner": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(habit_test.name, 'test')

    def test_get_habit(self):
        self.test_habit_create()
        response = self.client.get(f'/api/habits/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'test', 'place': 'test', 'time': '13:00:00',
                                           'action': 'test', 'is_pleasurable': True, 'periodic': 1,
                                           'reward': None, 'execution_time': '00:01:00', 'public': True, 'owner': 1,
                                           'associated_habit': None})

    def test_list_habits(self):
        self.test_habit_create()
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_list_habits_public(self):
        self.test_habit_create()
        response = self.client.get('/api/public_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 2)
