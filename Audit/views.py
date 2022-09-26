from django.views.generic.list import ListView
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView,CreateView
from .models import AuditTriple, Type
from users.models import CustomUser
from .filters import  AuditTripleFilter
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

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

        # get user and other group user
        group = self.request.user.groups.all()
        users = CustomUser.objects.filter(groups__name=group[0])
        other_user = [u for u in users if u != self.request.user][0]
        
        # get user's triples
        a = AuditTriple.objects.filter(user=self.request.user)
        b = AuditTriple.objects.filter(user=other_user)
        
        # make set
        a_set = set([(trip.entityA, trip.relation, trip.entityB) for trip in a])
        b_set = set([(trip.entityA, trip.relation, trip.entityB) for trip in b])
        
        # calculate union and intersection
        intersection = len((a_set & b_set))
        union = len((a_set | b_set))
        
        # calulate simularity
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
