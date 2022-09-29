from django.views.generic.list import ListView
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView,CreateView
from .models import AuditTriple, Type
from users.models import CustomUser
from django.contrib.auth.models import Group
from .filters import  AuditTripleFilter, AuditUserTripleFilter
  
# Create your views here.

class UserTripleView(ListView):
    model = AuditTriple
    template_name = 'audit_user_triple_list.html'

    def get_queryset(self):
       # original qs
       return super().get_queryset().filter().select_related('user')

    # add filter form
    def get_context_data(self, **kwargs):
        context = super(UserTripleView, self).get_context_data(**kwargs)
        context['filter'] = AuditUserTripleFilter(self.request.GET,queryset=self.get_queryset(),request=self.request)

        return context

class GroupsView(TemplateView):
    template_name = "audit_groups.html"

    def get_context_data(self, **kwargs):
        context = super(GroupsView,self).get_context_data()
        group_user_dict = {group.name: group.user_set.values_list('id', flat=True) for group in Group.objects.all()}
        simularity = []
        for group in group_user_dict:
            # There are 2 users per group
            user1, user2 = group_user_dict[group]  
            
            # initial queries
            a = AuditTriple.objects.filter(user=user1).values_list('entityA','relation','entityB','verified')
            b = AuditTriple.objects.filter(user=user2).values_list('entityA','relation','entityB','verified')

            a_set = set() 
            b_set = set() 

            for trip in a:
              a_set.add((trip[0],trip[1],trip[2],trip[3])) 

            for trip in b:
              b_set.add((trip[0],trip[1],trip[2],trip[3])) 

            simularity.append(round(len(a_set&b_set)/len(a_set|b_set)*100,2))

        group_data = list(zip(group_user_dict.keys(),simularity))
        context['group_data'] = group_data

        return context

def get_simularity(request):
    group_user_dict = {group.name: group.user_set.values_list('id', flat=True) for group in Group.objects.all()}
    simularity = []
    for group in group_user_dict:
        # There are 2 users per group
        user1, user2 = group_user_dict[group]  
             
        # initial queries
        a = AuditTriple.objects.filter(user=user1).values_list('entityA','relation','entityB','verified')
        b = AuditTriple.objects.filter(user=user2).values_list('entityA','relation','entityB','verified')

        a_set = set() 
        b_set = set() 

        for trip in a:
            a_set.add((trip[0],trip[1],trip[2],trip[3])) 

        for trip in b:
            b_set.add((trip[0],trip[1],trip[2],trip[3])) 

        simularity.append(round(len(a_set&b_set)/len(a_set|b_set)*100,2))

    group_data = dict(zip(group_user_dict.keys(),simularity))

    return JsonResponse({'group_data':group_data})



class AuditTripleList(ListView):
    model = AuditTriple 
    template_name = 'audit_triple_list.html'

    # filter results based on the user
    def get_queryset(self):
       # original qs
       qs = super().get_queryset() 
       return qs.filter(user=self.request.user).prefetch_related('entityA_types','entityB_types')

    # add filter form
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
        context['simularity'] = round(intersection / union * 100,2) 
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
      "verified",
    ]

    # override get_form to make only the users data available
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        query = Type.objects.filter(user=self.request.user)
      #  form.fields['entityA'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['entityA_types'].queryset = query 
      #  form.fields['relation'].queryset = Relation.objects.filter(user=self.request.user) 
      #  form.fields['entityB'].queryset = Entity.objects.filter(user=self.request.user) 
        form.fields['entityB_types'].queryset = query
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
