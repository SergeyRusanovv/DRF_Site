"""
URL configuration for drf_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from example.views import (
    SubjectApiViewSet, AnswerApiView,
    StudentApiView, TestingListApiView,
    AttemptView, QuestionDetailApiView
)
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r"subject", SubjectApiViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),  # http://127.0.0.1:8000/api/v1/subjetct/

    # path("api/v1/subjects/", SubjectApiViewSet.as_view({"get": "list"})),
      # ключ - метод который вызывается, значение - метод вызывается из viewset
    # path("api/v1/subjects/<int:pk>/", SubjectApiViewSet.as_view({"put": "update"})),

    path("api/v1/answers/", AnswerApiView.as_view()),
    path("api/v1/students/", StudentApiView.as_view()),
    path("api/v1/students/<int:pk>/", StudentApiView.as_view()),
    path("api/v1/testings/", TestingListApiView.as_view()),
    path("api/v1/testings/<int:pk>/", TestingListApiView.as_view()),
    path("api/v1/attempts/", AttemptView.as_view()),
    path("api/v1/questions/<int:pk>/", QuestionDetailApiView.as_view()),
]


admin.site.site_header = "Панель администратирования моделей для DRF сайта"  # заголовок в админке сайта
admin.site.index_title = "Список приложений и  моделей"  # подзаголовок в админке сайта
