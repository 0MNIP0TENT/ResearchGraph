from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from users.models import Entity, Relation, SemanticType, Triple 
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

class EntityList(ListView):
    model = Entity

class EntityUpdate(UpdateView):
    model = Entity 
    fields = [
      "name",
    ]
    success_url = '/'

class RelationList(ListView):
    model = Relation

class RelationUpdate(UpdateView):
    model = Relation 
    fields = [
      "name",
    ] 
    success_url = '/'

class TypeList(ListView):
    model = SemanticType

class TypeUpdate(UpdateView):
    model = SemanticType
    fields = [
      "name",
    ]
    success_url = '/'  

class TripleList(ListView):
    model = Triple 

class TripleUpdate(UpdateView):
    model = Triple
    fields = [
      "entityA",
      "relation",
      "entityB",
    ]
    success_url = '/'  
