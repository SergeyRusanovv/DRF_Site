from django.contrib import admin, messages
from django.http import HttpRequest

from example.models import (
    Subject,
    Student,
    Attempt,
    Question,
    Answer,
    Testing
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = "id", "title",
    list_display_links = "title",
    ordering = "id",
    list_per_page = 10  # пагинация
    search_fields = ["title"]  # поля по которым будет происходить поиск
    list_filter = ["title"]  # отображение фильтров справа
    # filter_horizontal = ["example"] - для изменения позиции и отрисовки виджета типа связей MTM
    # filter_vertical = ["example"] - для изменения позиции и отрисовки виджета типа связей MTM


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = "id", "name",
    list_display_links = "name",
    ordering = "id",
    list_per_page = 10
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    fields = ["student", "subject", "result"]  # только эти поля будут доступны для редактирования
    list_display = "id", "student", "subject", "date", "result"
    list_display_links = "student", "subject", "date", "result"
    ordering = "id",
    list_per_page = 10
    search_fields = ["result", "subject__title"]
    list_filter = ["result", "subject__title"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = "id", "text", "subject", "short_info"
    list_display_links = "text", "subject"
    ordering = "id",
    list_per_page = 10
    search_fields = ["text", "subject__title"]
    list_filter = ["text", "subject__title"]

    @admin.display(description="Краткое описание", ordering="text")  # для изменения заголовка колонки в админке
    def short_info(self, question: Question):  # для отображения доп информации в колонках модели в админке
        return f"Описание: {len(question.text)} символов"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ["text"]    # только для чтения, редактировать нельзя
    list_display = "id", "text", "is_correct", "question"
    list_display_links = "text", "question"
    ordering = "id",
    list_editable = "is_correct",  # редактирование
    list_per_page = 10
    actions = ("set_correct_answer", "set_incorrect_answer")
    search_fields = ["text", "question__text"]
    list_filter = ["text", "question__text", "is_correct"]
    # prepopulated_fields = {"slug": ("title", )}  - автоматическое создание слага (обязательно редактируемый)

    @admin.action(description="Установить ответы правильными")
    def set_correct_answer(self, request: HttpRequest, queryset):  # добавления пользовательского действия в админке
        count = queryset.update(is_correct=True)
        self.message_user(request, f"Изменено {count} ответов")

    @admin.action(description="Установить ответы неправильными")
    def set_incorrect_answer(self, request: HttpRequest, queryset):  # добавления пользовательского действия в админке
        count = queryset.update(is_correct=False)
        self.message_user(request, f"Изменено {count} ответов", level=messages.WARNING)
        # сообщение при применении действия с иконкой внимание /\


@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    # exclude = ["attempt"]  - это поле исключается из редактируемых
    list_display = "id", "attempt", "question", "answer"
    list_display_links = "attempt",
    ordering = "id",  # сортировка
    list_editable = "question", "answer"
    list_per_page = 10
    search_fields = ["question__text", "answer__text"]
    list_filter = ["question__text", "answer__text"]
