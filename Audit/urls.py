from django.urls import path
from .views import (
    AuditTripleUpdate,
    AuditTypeCreate,
    AuditTripleDetailView,
    ListDatasets,
    DeleteDataset,
    GroupsView,
    audit_triples,
    admin_view_triples,
    CommentView,
    audit_triple_cards,
    admin_view_triple_cards,
    DifferenceView,
)
app_name = 'Audit'
urlpatterns = [

    # urls for everyone 
    path('Groups/', GroupsView.as_view(), name='audit_groups'),
    path('UserComments/',CommentView.as_view(), name='audit_comments'),
    path('GroupDifferences/',DifferenceView.as_view(), name='audit_differences'),

    # urls for auditors
    path('AuditTripleList/', audit_triples, name='audit_triple_list'),
    path('AuditTripleCards/', audit_triple_cards, name='audit_triple_cards'),
    path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', AuditTripleUpdate.as_view(), name='audit_triple_update'),

    # urls for admins
    path('UserTripleViewList/',admin_view_triples, name='audit_user_triple_list'),
    path('UserTripleViewCards/',admin_view_triple_cards, name='audit_user_triple_cards'),
    path('<pk>/', AuditTripleDetailView.as_view(), name='audit_triple_detail'),

    path('delete/dataset/<pk>/', DeleteDataset.as_view(), name='audit_delete_dataset'),
    path('list/dataset/', ListDatasets.as_view(), name='audit_list_datasets'),

]
