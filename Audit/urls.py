from django.urls import path
from .views import (
    AuditTripleList,
    AuditTripleUpdate,
    AuditTypeCreate,
    UserTripleView,
    AuditTripleDetailView,
    ListDatasets,
    DeleteDataset,
    GroupsView,
    get_simularity,
    audit_triples,
    admin_view_triples,
    CommentView,
)
app_name = 'Audit'
urlpatterns = [

    # urls for everyone 
    path('Groups/', GroupsView.as_view(), name='audit_groups'),

    # urls for auditors
    path('AuditTriple/List/', audit_triples, name='audit_triple_list'),
    path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', AuditTripleUpdate.as_view(), name='audit_triple_update'),

    # urls for admins
    path('UserTripleView/List/',admin_view_triples, name='audit_user_triple_list'),
    path('UserComments/',CommentView.as_view(), name='audit_comments'),
    path('<pk>/', AuditTripleDetailView.as_view(), name='audit_triple_detail'),

    path('delete/dataset/<pk>/', DeleteDataset.as_view(), name='audit_delete_dataset'),
    path('list/dataset/', ListDatasets.as_view(), name='audit_list_datasets'),

]
