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

        return qs.filter(user=self.request.user).prefetch_related('semantic_type')

class EntityUpdate(UpdateView):
    model = Entity 
    fields = [
      "name",
      "semantic_type",
    ]

    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['semantic_type'].queryset = SemanticType.objects.filter(user=self.request.user) 
        return form

    def get_success_url(self):
        return reverse('Audit:entity_list')

class EntityCreate(CreateView):
    model = Entity
    
    template_name = 'users/entity_create.html'

    fields = [
      "name",
      "semantic_type",
    ] 

    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['semantic_type'].queryset = SemanticType.objects.filter(user=self.request.user) 
        return form

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

    template_name = 'users/relation_create.html'

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

    template_name = 'users/type_create.html'

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

    # filter results based on the user
    def get_queryset(self):
       # original qs
       qs = super().get_queryset() 
       return qs.filter(user=self.request.user).select_related('entityA','relation','entityB')

    # add form
    def get_context_data(self, **kwargs):
        context = super(TripleList, self).get_context_data(**kwargs)
        context['filter'] = TripleFilter(self.request.GET,queryset=self.get_queryset(),request=self.request)
        return context

class TripleCreate(CreateView):
    model = Triple

    template_name = 'users/triple_create.html'

    fields = [
      "entityA",
      "relation",
      "entityB",
    ] 
    
    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['entityA'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['relation'].queryset = Relation.objects.filter(user=self.request.user) 
        form.fields['entityB'].queryset = Entity.objects.filter(user=self.request.user) 
        return form

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

    def get_success_url(self):
        return reverse('Audit:triple_list')

class TripleDelete(DeleteView):
    model = Triple 

    def get_success_url(self):
        return reverse('Audit:triple_list')
