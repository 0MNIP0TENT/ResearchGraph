from django.urls import path
from . import views

app_name = 'Charts'
urlpatterns = [
    path('degree/Verified', views.display_verified_degree_view, name='degree_verified'),
    path('relation/Verified', views.display_verified_relation_view, name='relation_verified'),
    path('out-relations/Verified', views.display_verified_out_relations_view, name='out_relations_verified'),

    path('degree/UnVerified', views.display_unverified_degree_view, name='degree_unverified'),
    path('relation/UnVerified', views.display_unverified_relation_view, name='relation_unverified'),
    path('out-relations/UnVerified', views.display_unverified_out_relations_view, name='out_relations_unverified'),
]
