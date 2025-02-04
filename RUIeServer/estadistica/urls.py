from django.urls import path
from . import views

urlpatterns = [
     path('', views.estadistica, name="estadistica"),
     path('buscar/', views.busqueda, name="busqueda"),
     path('reincidencia/', views.reincidencia, name="reincidente"),

#    Consultas en ajax
     path('buscar_rescate/', views.buscar_reincidente_ajax, name='buscar_rescate'),
     path('reincidentes_dia/', views.reincidentes_xdia_ajax, name='reincidencia'),

     path("pdf/", views.generar_pdf, name="generar_pdf"),
]