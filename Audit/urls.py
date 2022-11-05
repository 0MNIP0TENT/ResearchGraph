from django.urls import path
from . import views 

app_name = 'Audit'
urlpatterns = [

    # urls for everyone 
    path('Groups/', views.GroupsView.as_view(), name='audit_groups'),
    path('UserComments/',views.CommentView.as_view(), name='audit_comments'),
    path('GroupComparisons/',views.GroupComparisons.as_view(), name='audit_comparisons'),

    # urls for auditors
    path('AuditTripleList/', views.audit_triples, name='audit_triple_list'),
    path('AuditTripleCards/', views.audit_triple_cards, name='audit_triple_cards'),
    #path('AuditType/create/', AuditTypeCreate.as_view(), name='audit_type_create'),
    path('AuditTriple/<uuid:pk>/Update/', views.AuditTripleUpdate.as_view(), name='audit_triple_update'),

    # urls for admins
    path('UserTripleViewList/',views.UserTripleViewList.as_view(), name='audit_user_triple_list'),
    path('UserTripleViewCards/', views.UserTripleView.as_view(), name='audit_user_triple_cards'),
    path('<pk>/', views.AuditTripleDetailView.as_view(), name='audit_triple_detail'),

    path('delete/dataset/<pk>/', views.DeleteDataset.as_view(), name='audit_delete_dataset'),
    path('list/dataset/', views.ListDatasets.as_view(), name='audit_list_datasets'),

]
