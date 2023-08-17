from rest_framework import viewsets, generics
from habit.models import Habit
from habit.pagination import HabitPagination
from habit.serializers import HabitSerializers
from habit.services import create_habit_plan
from users.models import UserRoles


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)
        habit = serializer.save()
        create_habit_plan(habit)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)


class HabitsListView(generics.ListAPIView):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(public=True)
