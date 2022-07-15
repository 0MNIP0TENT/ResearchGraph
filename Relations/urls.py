from django.urls import path
from . import views

app_name = 'Relations'
urlpatterns = [
    path('Verified/', views.display_verified_relations_view, name='display_verified'),
    path('Verified/<str:relation>/', views.display_verified_relations_view, name='display_verified'),

    path('UnVerified/', views.display_unverified_relations_view, name='display_unverified'),
    path('UnVerified/<str:relation>/', views.display_unverified_relations_view, name='display_unverified'),
]
