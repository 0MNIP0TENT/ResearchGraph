from django.urls import path
from .views import EntityList, EntityUpdate, AuditHome, RelationUpdate, RelationList,TypeList,TypeUpdate, TripleList, TripleUpdate

app_name = 'Audit'
urlpatterns = [
    path('home/', AuditHome.as_view(), name='audit_home'),
    path('Entity/list/', EntityList.as_view(), name='entity_list'),
    path('Entity/<pk>/update/', EntityUpdate.as_view(), name='entity_update_list'),
    
    path('Relation/list/', RelationList.as_view(), name='relation_list'),
    path('Relation/<pk>/update/', RelationUpdate.as_view(), name='relation_update_list'),

    path('Type/list/', TypeList.as_view(), name='type_list'),
    path('Type/<pk>/update/', TypeUpdate.as_view(), name='type_update_list'),

    path('Triple/list/', TripleList.as_view(), name='triple_list'),
    path('Triple/<pk>/update/', TripleUpdate.as_view(), name='triple_update_list'),
]
