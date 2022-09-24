from django.urls import path
from . import views

app_name = 'Entities'
urlpatterns = [
    path('Verified/', views.display_verified_entitys_view, name='display_verified'),
    path('Verified/<str:entity>/', views.display_verified_entitys_view, name='display_verified'),

    path('UnVerified/', views.display_unverified_entitys_view, name='display_unverified'),
    path('UnVerified/<path:entity>/', views.display_unverified_entitys_view, name='display_unverified'),
]
