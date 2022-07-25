from django.urls import path
from .views import AuditList, AuditUpdate

app_name = 'Audit'
urlpatterns = [
    path('list/', AuditList.as_view(), name='audit_list'),
    path('<pk>/update/', AuditUpdate.as_view(), name='update_list'),
]
