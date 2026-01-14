from django.urls import path
from . import views
urlpatterns = [
    path('thread-proof/', views.proof_by_thread_view),
    path('question-2/', views.question_two_view, name='question_2'),
    path('question-3/', views.question_three_view, name='question_3'),
    path('question-4/', views.question_four_view, name='question_4'),
]