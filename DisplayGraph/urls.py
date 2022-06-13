from django.urls import path
from . import views

app_name = 'DisplayGraph'
urlpatterns = [
    path('', views.display_graph_view, name='display'),
]
