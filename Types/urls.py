from django.urls import path
from . import views

app_name = 'Types'
urlpatterns = [
    path('', views.display_types_view, name='display'),
    path('<str:s_type>/', views.display_types_view, name='display'),
]
