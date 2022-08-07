from django.views.generic.list import ListView
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from users.models import Entity, Relation, SemanticType, Triple 
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

class EntityList(ListView):
    model = Entity

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(user=self.request.user)

class EntityUpdate(UpdateView):
    model = Entity 
    fields = [
      "name",
      "semantic_type",
    ]

    def get_success_url(self):
        return reverse('Audit:entity_list')

class EntityDelete(DeleteView):
    model = Entity

    def get_success_url(self):
        return reverse('Audit:entity_list')

class RelationList(ListView):
    model = Relation
    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class RelationUpdate(UpdateView):
    model = Relation 
    fields = [
      "name",
    ] 

    def get_success_url(self):
        return reverse('Audit:relation_list')

class RelationDelete(DeleteView):
    model = Relation

    def get_success_url(self):
        return reverse('Audit:relation_list')

class TypeList(ListView):
    model = SemanticType

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class TypeUpdate(UpdateView):
    model = SemanticType
    fields = [
      "name",
    ]

    def get_success_url(self):
        return reverse('Audit:type_list')

class TypeDelete(DeleteView):
    model = SemanticType 

    def get_success_url(self):
        return reverse('Audit:type_list')

class TripleList(ListView):
    model = Triple 

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class TripleUpdate(UpdateView):
    model = Triple
    fields = [
      "entityA",
      "relation",
      "entityB",
    ]

    def get_success_url(self):
        return reverse('Audit:triple_list')

class TripleDelete(DeleteView):
    model = Triple 

    def get_success_url(self):
        return reverse('Audit:triple_list')
