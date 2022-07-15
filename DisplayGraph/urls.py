from django.urls import path
from . import views

app_name = 'DisplayGraph'
urlpatterns = [
    path('Verified/', views.display_verified_graph_view, name='display_verified'),
    path('UnVerified/', views.display_unverified_graph_view, name='display_unverified'),
]
