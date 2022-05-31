from django.urls import path
from . import views

app_name = 'Relations'
urlpatterns = [
    path('', views.display_relations_view, name='display'),
    path('<str:relation>/', views.display_relations_view, name='display'),
]
