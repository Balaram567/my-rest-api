from django.urls import path
from .import views

urlpatterns=[
    path('api/poll', views.poll, name='game'),
    path('api/detail/<int:id>/', views.detail, name='game'),
    path('api/class/api', views.PollApiView.as_view()),
    path('api/class/detail/<int:id>/', views.PollApiDetail.as_view()),
    path('api/class/login', views.LoginView.as_view())
]
