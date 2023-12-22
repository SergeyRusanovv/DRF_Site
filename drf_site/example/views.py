import random
from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from example.permissions import IsAdminOrReadOnly
from example.models import (
    Subject, Attempt, Answer,
    Student, Testing, Question
)
from example.serializers import (
    SubjectSerializer, AnswerSerializer,
    StudentSerializer, TestingSerializer,
    AttemptSerializer, QuestionSerializer
)


class PaginationClass(PageNumberPagination):
    """
    Кастомный класс pagination
    """
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 1000


@extend_schema(description="Полный CRUD для модели Subject")
class SubjectApiViewSet(viewsets.ModelViewSet):
    """
    Viewset для получения всех вопросов
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = PaginationClass

    # def get_queryset(self):
    #     return Subject.objects.all()[:2]  # возвращать первые 2 записи

    @extend_schema(
        summary="Delete subject",
        responses={
            404: OpenApiResponse(description="No subject for id"),
            200: "Done"
        }
    )
    def destroy(self, *args, **kwargs):
        """Удаление вопроса"""
        return super().destroy(*args, **kwargs)

    @extend_schema(
        summary="Create subject",
        responses={
            404: OpenApiResponse(description="No subject for id"),
            200: SubjectSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        """Создание вопроса"""
        return super().create(*args, **kwargs)

    @extend_schema(
        summary="Update subject by id",
        responses={
            404: OpenApiResponse(description="No subject for id"),
            200: SubjectSerializer
        }
    )
    def partial_update(self, *args, **kwargs):
        """Частичное обновление вопроса"""
        return super().partial_update(*args, **kwargs)

    @extend_schema(
        summary="Update all info for subject by id",
        responses={
            404: OpenApiResponse(description="No subject for id"),
            200: SubjectSerializer
        }
    )
    def update(self, *args, **kwargs):
        """Обновление всего вопроса"""
        return super().update(*args, **kwargs)

    @extend_schema(
        summary="Get subject by id",
        responses={
            404: OpenApiResponse(description="No subject for id"),
            200: SubjectSerializer
        }
    )
    def retrieve(self, *args, **kwargs):
        """Получение одного вопроса"""
        return super().retrieve(*args, **kwargs)

    @extend_schema(
        summary="Get all subjects",
        responses={
            404: OpenApiResponse(description="No subjects"),
            200: SubjectSerializer
        }
    )
    def list(self, *args, **kwargs):
        """Получение всех вопросов"""
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get random subject",
        responses={
            404: OpenApiResponse(description="No subjects"),
            200: SubjectSerializer
        }
    )
    @action(methods=["GET"], detail=False)
    def get_random(self, request: Request) -> Response:
        """
        Получить рандомный вопрос из базы данных
        """
        random_int: int = random.choice([num for num in range(1, 4)])
        random_subject = Subject.objects.get(pk=random_int)
        return Response({"random_subject": SubjectSerializer(random_subject).data})


class AnswerApiView(APIView):
    """
    Ответы
    """
    @extend_schema(
        summary="Get all answers",
        responses={
            404: OpenApiResponse(description="Unknown error"),
            200: AnswerSerializer
        }
    )
    def get(self, request: Request) -> Response:
        """
        Получаем все ответы
        """
        ret = Answer.objects.all()
        return Response({"data": AnswerSerializer(ret, many=True).data})

    @extend_schema(
        summary="Add new answer",
        responses={
            404: OpenApiResponse(description="Validation error"),
            201: AnswerSerializer
        }
    )
    def post(self, request: Request) -> Response:
        """
        Добавляем ответ
        """
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_answer = Answer(
            text=request.data["text"],
            is_correct=request.data["is_correct"],
            question=request.data["question"]
        )
        return Response({"new_answer": AnswerSerializer(new_answer).data})


class StudentApiView(APIView):
    """
    Студенты
    """

    @extend_schema(
        summary="Get all students",
        responses={
            404: OpenApiResponse(description="No students"),
            200: StudentSerializer
        }
    )
    def get(self, request: Request) -> Response:
        """
        Получаем всех студентов
        """
        ret = Student.objects.all()
        return Response({"data": StudentSerializer(ret, many=True).data})

    @extend_schema(
        summary="Create student",
        responses={
            404: OpenApiResponse(description="Validation error"),
            201: StudentSerializer
        }
    )
    def post(self, request: Request) -> Response:
        """
        Добавляем студента
        """
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"new_student": serializer.data})

    @extend_schema(
        summary="Update student by id",
        responses={
            404: OpenApiResponse(description="No student by id"),
            200: StudentSerializer
        }
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        Обновляем существующего студента
        """
        pk = kwargs.get("pk", None)
        if pk is None:
            return Response({"error": "PUT method is not allowed"})
        try:
            instance = Student.objects.get(pk=pk)
        except:
            return Response({"error": "Objects does not exist"})

        serializer = StudentSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response({"update_student": serializer.data})


class AttemptView(generics.ListCreateAPIView):
    """
    Класс для получения всех попыток и добавления новой
    """
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    permission_classes = IsAuthenticatedOrReadOnly,  # добавлять только авторизованные или только читать
    pagination_class = PaginationClass

    @extend_schema(
        summary="Create attempt",
        responses={
            404: OpenApiResponse(description="Validation error"),
            201: AttemptSerializer
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    @extend_schema(
        summary="Get all attempts",
        responses={
            404: OpenApiResponse(description="No attempts"),
            200: AttemptSerializer
        }
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class TestingListApiView(generics.ListCreateAPIView):
    """
    Класс для получения всех результатов тестирования и добавления нового результата
    """
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer
    pagination_class = PaginationClass

    @extend_schema(
        summary="Create testing",
        responses={
            404: OpenApiResponse(description="Validation error"),
            201: TestingSerializer
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    @extend_schema(
        summary="Get all testings",
        responses={
            404: OpenApiResponse(description="No testings"),
            200: TestingSerializer
        }
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

class QuestionDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Вопросы. Полный CRUD
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = IsAdminOrReadOnly,
    pagination_class = PaginationClass

    @extend_schema(
        summary="Update question",
        responses={
            404: OpenApiResponse(description="Validation error"),
            201: QuestionSerializer
        }
    )
    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs)

    @extend_schema(
        summary="Update partial question",
        responses={
            404: OpenApiResponse(description="No testing by id"),
            201: QuestionSerializer
        }
    )
    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)

    @extend_schema(
        summary="Get all questions",
        responses={
            404: OpenApiResponse(description="No testing by id"),
            200: QuestionSerializer
        }
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @extend_schema(
        summary="Delete question",
        responses={
            404: OpenApiResponse(description="No testing by id"),
            200: QuestionSerializer
        }
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
