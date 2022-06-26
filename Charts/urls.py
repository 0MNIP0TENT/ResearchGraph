from django.urls import path
from . import views

app_name = 'Charts'
urlpatterns = [
    path('', views.charts_view, name='charts'),
    path('degree/', views.display_degree_view, name='degree'),
    path('relation/', views.display_relation_view, name='relation'),
]
