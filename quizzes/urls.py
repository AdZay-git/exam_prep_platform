from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('my/results/', views.my_results, name='my_results'),
    path('<int:pk>/', views.quiz_detail, name='quiz_detail'),
]
