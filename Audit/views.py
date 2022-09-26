from django.views.generic.list import ListView
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from users.models import Entity, Relation, SemanticType, Triple, CustomUser
from .models import AuditTriple, Type
from .filters import TripleFilter, EntityFilter, RelationFilter, SemanticTypeFilter, AuditTripleFilter
from django.db.models import prefetch_related_objects, Prefetch
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

class EntityList(ListView):
    model = Entity  
 
    # add form
    def get_context_data(self, **kwargs):
        context = super(EntityList, self).get_context_data(**kwargs)
        context['filter'] = EntityFilter(self.request.GET,queryset=self.get_queryset())
        user_set = set()
        other_users_set = set()

        for obj in Entity.objects.filter(user=self.request.user):
           user_set.add(obj.name)

        for obj in Entity.objects.exclude(user=self.request.user):
           other_users_set.add(obj.name)

        context['simularity'] = len(user_set & other_users_set)/len(user_set | other_users_set)
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
      "verified",
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
        user_set = set()
        other_users_set = set()

        for obj in Relation.objects.filter(user=self.request.user):
           user_set.add(obj.name)

        for obj in Relation.objects.exclude(user=self.request.user):
           other_users_set.add(obj.name)

        context['simularity'] = len(user_set & other_users_set)/len(user_set | other_users_set)
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
      "verified",
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
        user_set = set()
        other_users_set = set()

        for obj in SemanticType.objects.filter(user=self.request.user):
           user_set.add(obj.name)

        for obj in SemanticType.objects.exclude(user=self.request.user):
           other_users_set.add(obj.name)

        context['simularity'] = len(user_set & other_users_set)/len(user_set | other_users_set)
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
      "verified",
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

        user_set = set()
        other_users_set = set()

        for obj in Triple.objects.filter(user=self.request.user).select_related('entityA','relation','entityB'):
           user_set.add((obj.entityA.name,obj.relation.name,obj.entityB.name))

        for obj in Triple.objects.exclude(user=self.request.user).select_related('entityA','relation','entityB'):
           other_users_set.add((obj.entityA.name,obj.relation.name,obj.entityB.name))

        context['simularity'] = len(user_set & other_users_set)/len(user_set | other_users_set)

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
      "verified",
    ]

    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['entityA'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['relation'].queryset = Relation.objects.filter(user=self.request.user) 
        form.fields['entityB'].queryset = Entity.objects.filter(user=self.request.user) 
        return form

    def get_success_url(self):
        return reverse('Audit:triple_list')

class TripleDelete(DeleteView):
    model = Triple 

    def get_success_url(self):
        return reverse('Audit:triple_list')  

class AuditTripleList(ListView):
    model = AuditTriple 
    template_name = 'audit_triple_list.html'

    # filter results based on the user
    def get_queryset(self):
       # original qs
       qs = super().get_queryset() 
       return qs.filter(user=self.request.user).prefetch_related('entityA_types','entityB_types')

    # add form
    def get_context_data(self, **kwargs):
        context = super(AuditTripleList, self).get_context_data(**kwargs)
        context['filter'] = AuditTripleFilter(self.request.GET,queryset=self.get_queryset(),request=self.request)

        # get simularity
        group = self.request.user.groups.all()
        users = CustomUser.objects.filter(groups__name=group[0])
        other_user = [u for u in users if u != self.request.user][0]

        a = AuditTriple.objects.filter(user=self.request.user)
        b = AuditTriple.objects.filter(user=other_user)
#        a = AuditTriple.objects.filter(user=self.request.user).values_list('entityA','entityA_types','relation','entityB')
#        b = AuditTriple.objects.filter(user=other_user).values('entityA','entityA_types','relation','entityB')
        # get the types of the entitys
#        at = [x.entityA_types.values_list('name') for x in a] 
#        bt = [x.entityB_types.all() for x in a] 
         


#        a_set = set()
#        b_set = set()

        
#        for obj in a:
#            ad = obj.entityA_types.values('name')
#            enta_types = tuple([name['name'] for name in ad])
#            entb_types = tuple([name['name'] for name in obj.entityB_types.values('name')])
#            a_set.add((obj.entityA,enta_types,obj.relation, obj.entityB, entb_types))
#
#        for obj in b:
#            enta_types = tuple([name['name'] for name in obj.entityA_types.values('name')])
#            entb_types = tuple([name['name'] for name in obj.entityB_types.values('name')])
#            b_set.add((obj.entityA,enta_types,obj.relation,obj.entityB, entb_types))
#

        a_set = set([(trip.entityA, trip.relation, trip.entityB) for trip in a])
        b_set = set([(trip.entityA, trip.relation, trip.entityB) for trip in b])

        intersection = len((a_set & b_set))
        union = len((a_set | b_set))

        context['simularity'] = round(intersection / union,2) 
        return context

class AuditTripleUpdate(UpdateView):
    model = AuditTriple
    template_name = 'audit_triple_form.html'
    fields = [
      "entityA",
      "entityA_types",
      "relation",
      "entityB",
      "entityB_types",
    ]

    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        query = Type.objects.filter(user=self.request.user)
      #  form.fields['entityA'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['entityA_types'].queryset = Type.objects.filter(user=self.request.user) 
      #  form.fields['relation'].queryset = Relation.objects.filter(user=self.request.user) 
      #  form.fields['entityB'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['entityB_types'].queryset = Type.objects.filter(user=self.request.user) 
        return form

    # if updated make verified False
    def form_valid(self,form):
        form.instance.verified = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:audit_triple_list')

class AuditTypeCreate(CreateView):
    model = Type

    template_name = 'audit_type_create.html'

    fields = [
      "name",
    ]

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Audit:audit_triple_list')
