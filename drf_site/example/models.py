from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    """
    Модель представляющая вопросы
    """
    title = models.CharField(_('Тема'), max_length=255)

    class Meta:
        verbose_name = "Задания"  # описание модели в админке
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):  - метод для автоматического добавления слага в модель
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


class Student(models.Model):
    """
    Модель студентов
    """
    name = models.CharField(_('Фамилия и имя'), max_length=255)

    class Meta:
        verbose_name = "Студенты"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.name


class Attempt(models.Model):
    """
    Модель попыток
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_('Студент'))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Предмет'))
    date = models.DateField(verbose_name="Дата")
    result = models.PositiveSmallIntegerField(_('Результат'))

    class Meta:
        verbose_name = "Попытки"
        verbose_name_plural = "Попытки"


class Question(models.Model):
    """
    Модель вопросов
    """
    text = models.TextField(_('Текст вопроса'))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Предмет'))

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text[:30] + '...'


class Answer(models.Model):
    """
    Модель ответов
    """
    text = models.TextField(_('Ответ'))
    is_correct = models.BooleanField(_('Результат'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'))

    class Meta:
        verbose_name = "Ответы"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text[:30] + '...'


class Testing(models.Model):
    """
    Модель тестирования
    """
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, verbose_name=_('Попытка'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'))
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=_('Ответ'))

    class Meta:
        verbose_name = "Тестирование"
        verbose_name_plural = "Тестирование"
