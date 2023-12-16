from django.forms import model_to_dict
from rest_framework import generics
from example.models import Subject
from example.serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


# class SubjectApiView(generics.ListAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer

class SubjectApiView(APIView):
    def get(self, request: Request) -> Response:
        lst = Subject.objects.all().values()
        return Response({"subjects": list(lst)})

    def post(self, request: Request) -> Response:
        subj_new = Subject.objects.create(
            title=request.data["title"]
        )
        return Response({"subject": model_to_dict(subj_new)})
