from django.db import models

from users.models import NULLABLE


class Habit(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE,
                              verbose_name='юзер', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, verbose_name='действие')
    is_pleasurable = models.BooleanField(default=True,
                                         verbose_name='полезная привычка')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                         **NULLABLE,
                                         verbose_name='связанная привычка')
    periodic = models.IntegerField(default=1, verbose_name='периодичность')
    reward = models.CharField(max_length=150, verbose_name='похвала',
                              **NULLABLE)
    execution_time = models.TimeField(verbose_name='время выполнения',
                                      **NULLABLE)
    public = models.BooleanField(default=True, verbose_name='публичность')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
