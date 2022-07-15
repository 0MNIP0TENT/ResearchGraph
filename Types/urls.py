from django.urls import path
from . import views

app_name = 'Types'
urlpatterns = [
    path('Verified/', views.display_verified_types_view, name='display_verified'),
    path('Verified/<str:s_type>/', views.display_verified_types_view, name='display_verified'),

    path('UnVerified/', views.display_unverified_types_view, name='display_unverified'),
    path('UnVerified/<str:s_type>/', views.display_unverified_types_view, name='display_unverified'),
]
