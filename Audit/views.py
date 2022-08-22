from django.views.generic.list import ListView
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from users.models import Entity, Relation, SemanticType, Triple 
from .filters import TripleFilter, EntityFilter, RelationFilter, SemanticTypeFilter
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

class EntityList(ListView):
    model = Entity  
 
    # add form
    def get_context_data(self, **kwargs):
        context = super(EntityList, self).get_context_data(**kwargs)
        context['filter'] = EntityFilter(self.request.GET,queryset=self.get_queryset())
        return context

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

class EntityCreate(CreateView):
    model = Entity

    fields = [
      "name",
      "semantic_type",
    ] 

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:entity_list')

class EntityDelete(DeleteView):
    model = Entity

    def get_success_url(self):
        return reverse('Audit:entity_list')

class RelationList(ListView):
    model = Relation

    # add form
    def get_context_data(self, **kwargs):
        context = super(RelationList, self).get_context_data(**kwargs)
        context['filter'] = RelationFilter(self.request.GET,queryset=self.get_queryset())
        return context

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class RelationCreate(CreateView):
    model = Relation

    fields = [
      "name",
    ] 

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:relation_list')

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
    
    # add form
    def get_context_data(self, **kwargs):
        context = super(TypeList, self).get_context_data(**kwargs)
        context['filter'] = SemanticTypeFilter(self.request.GET,queryset=self.get_queryset())
        return context

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class TypeCreate(CreateView):
    model = SemanticType

    fields = [
      "name",
    ] 

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:type_list')

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

    # add form
    def get_context_data(self, **kwargs):
        context = super(TripleList, self).get_context_data(**kwargs)
        context['filter'] = TripleFilter(self.request.GET,queryset=self.get_queryset())
        return context

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

class TripleCreate(CreateView):
    model = Triple

    fields = [
      "entityA",
      "relation",
      "entityB",
    ] 

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:triple_list')

class TripleUpdate(UpdateView):
    model = Triple
    fields = [
      "entityA",
      "relation",
      "entityB",
    ]

    # filter results based on the user
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        return qs.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('Audit:triple_list')

class TripleDelete(DeleteView):
    model = Triple 

    def get_success_url(self):
        return reverse('Audit:triple_list')
