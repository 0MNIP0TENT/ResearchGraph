from django.urls import path
from . import views

app_name = 'Entitys'
urlpatterns = [
    path('', views.display_entitys_view, name='display'),
    path('<str:entity>/', views.display_entitys_view, name='display'),
]
