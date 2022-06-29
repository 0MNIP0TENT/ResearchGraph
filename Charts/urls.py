from django.urls import path
from . import views

app_name = 'Charts'
urlpatterns = [
    path('degree/', views.display_degree_view, name='degree'),
    path('relation/', views.display_relation_view, name='relation'),
    path('out-relations/', views.display_out_relations_view, name='out_relations'),
]
