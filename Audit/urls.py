from django.urls import path
from .views import (
    AuditTripleList,
    AuditTripleUpdate,
    AuditTypeCreate,
    UserTripleView,
    GroupsView,
)
app_name = 'Audit'
urlpatterns = [
     
    path('AuditTriple/List/', AuditTripleList.as_view(), name='audit_triple_list'),
    path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', AuditTripleUpdate.as_view(), name='audit_triple_update'),

    path('UserTripleView/List/', UserTripleView.as_view(), name='audit_user_triple_list'),
    path('Groups/', GroupsView.as_view(), name='audit_groups'),
]
