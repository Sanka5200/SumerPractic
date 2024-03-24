from django.db import models

class Baza(models.Model):
    group = models.CharField('Группа', max_length=30, default='')
    comments = models.CharField('Комментарий', max_length=50, default='')
    text = models.TextField('Текст')
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.group
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"