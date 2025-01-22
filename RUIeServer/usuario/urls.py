
from django.urls import path, include
from usuario import views

urlpatterns = [
    path('validar/', views.login_user),
]
