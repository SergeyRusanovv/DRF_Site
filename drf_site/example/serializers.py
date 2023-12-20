import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from example.models import Subject, Student, Testing, Attempt, Question


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "title",


class AnswerSerializer(serializers.Serializer):
    text = serializers.CharField()
    is_correct = serializers.BooleanField()
    question = serializers.ReadOnlyField(source="question.text")  # relations - FK


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):  # срабатывает при вызове метода serializer.save() во view
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):  # instance - обьект модели Student
        instance.name = validated_data.get("name", instance.name)  # если полей больше, то прописывать их также
        instance.save()
        return instance


class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = "__all__"


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


##########################################
### example work with Serializer class ###
##########################################


class Model:
    def __init__(self, text, is_correct, question):
        self.text = text
        self.is_correct = is_correct
        self.question = question


class ExSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=512)
    is_correct = serializers.BooleanField()
    question = serializers.IntegerField()


def encode():
    model = Model("Test text", True, 10)
    model_sr = ExSerializer(model)
    print(model_sr.data, type(model_sr.data), sep="\n")
    json = JSONRenderer().render(model_sr.data)
    print(json)


def decode():
    stream = io.BytesIO(b'{"text":"Test text","is_correct":true,"question":10}')
    data = JSONParser().parse(stream)
    serializer = ExSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
