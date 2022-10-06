from django.urls import path
from .views import (
    AuditTripleList,
    AuditTripleUpdate,
    AuditTypeCreate,
    UserTripleView,
    ListDatasets,
    DeleteDataset,
    GroupsView,
    get_simularity,
    audit_triples
)
app_name = 'Audit'
urlpatterns = [
     
    path('AuditTriple/List/', audit_triples, name='audit_triple_list'),
    path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', AuditTripleUpdate.as_view(), name='audit_triple_update'),

    path('UserTripleView/List/', UserTripleView.as_view(), name='audit_user_triple_list'),
    path('Groups/', GroupsView.as_view(), name='audit_groups'),
    path('Groups/simularity', get_simularity, name='get_simularity'),

    path('delete/dataset/<pk>/', DeleteDataset.as_view(), name='audit_delete_dataset'),
    path('list/dataset/', ListDatasets.as_view(), name='audit_list_datasets'),
]
