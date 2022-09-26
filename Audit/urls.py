from django.urls import path
from .views import (
    AuditHome, 
    AuditTripleList,
    AuditTripleUpdate,
    AuditTypeCreate,
)
app_name = 'Audit'
urlpatterns = [
    path('home/', AuditHome.as_view(), name='audit_home'),
     
    path('AuditTriple/List/', AuditTripleList.as_view(), name='audit_triple_list'),
    path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', AuditTripleUpdate.as_view(), name='audit_triple_update'),
]
