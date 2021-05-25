from django.urls import path
from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MediaApi.as_view()),
    path('movies/<str:id>', views.MediaDetailsApi.as_view())
]