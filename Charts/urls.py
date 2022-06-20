from django.urls import path
from . import views

app_name = 'Charts'
urlpatterns = [
    path('', views.display_charts_view, name='display'),
]
