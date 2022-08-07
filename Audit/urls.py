from django.urls import path
from .views import (
        EntityList, 
        EntityUpdate, 
        EntityDelete,
        AuditHome, 
        RelationUpdate,
        RelationDelete,
        RelationList,
        TypeList,
        TypeUpdate, 
        TypeDelete, 
        TripleList, 
        TripleUpdate,
        TripleDelete
)

app_name = 'Audit'
urlpatterns = [
    path('home/', AuditHome.as_view(), name='audit_home'),
    path('Entity/list/', EntityList.as_view(), name='entity_list'),
    path('Entity/<pk>/update/', EntityUpdate.as_view(), name='entity_update_list'),
    path('Entity/<pk>/delete/', EntityDelete.as_view(), name='entity_delete'),
    
    path('Relation/list/', RelationList.as_view(), name='relation_list'),
    path('Relation/<pk>/update/', RelationUpdate.as_view(), name='relation_update_list'),
    path('Relation/<pk>/delete/', RelationDelete.as_view(), name='relation_delete'),

    path('Type/list/', TypeList.as_view(), name='type_list'),
    path('Type/<pk>/update/', TypeUpdate.as_view(), name='type_update_list'),
    path('Type/<pk>/delete/', TypeDelete.as_view(), name='type_delete'),

    path('Triple/list/', TripleList.as_view(), name='triple_list'),
    path('Triple/<pk>/update/', TripleUpdate.as_view(), name='triple_update_list'),
    path('Triple/<pk>/delete/', TripleDelete.as_view(), name='triple_delete'),
]
