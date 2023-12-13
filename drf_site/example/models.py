from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    title = models.CharField(_('title'), max_length=255)

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_('student'))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('subject'))
    date = models.DateField()
    result = models.PositiveSmallIntegerField(_('result'))


class Question(models.Model):
    text = models.TextField(_('text'))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('subject'))

    def __str__(self):
        return self.text[:30] + '...'


class Answer(models.Model):
    text = models.TextField(_('text'))
    is_correct = models.BooleanField(_('is correct'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('question'))

    def __str__(self):
        return self.text[:30] + '...'


class Testing(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, verbose_name=_('attempt'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('question'))
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=_('answer'))
