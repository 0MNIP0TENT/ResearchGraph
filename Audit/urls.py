from django.urls import path
from .views import EntityList, EntityUpdate

app_name = 'Audit'
urlpatterns = [
    path('list/', AuditHome.as_view(), name='audit_home'),
    path('list/', EntityList.as_view(), name='entity_list'),
    path('Entity/<pk>/update/', EntityUpdate.as_view(), name='entity_update_list'),
]
