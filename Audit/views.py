from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from .models import AuditTriple, Type, Dataset
from users.models import CustomUser
from django.contrib.auth.models import Group
from .filters import  AuditTripleFilter, AuditUserTripleFilter
  
# Create your views here.

class UserTripleView(ListView):
    model = AuditTriple
    template_name = 'audit_user_triple_list.html'

    def get_queryset(self):
       # original qs
       return super().get_queryset().filter().select_related('user','dataset')

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
        simularity_dict = dict()

        a_set = set() 
        b_set = set() 
        for dataset in Dataset.objects.all():
            simularity = []
            # There are 2 users per group
            for group in group_user_dict:
                user1, user2 = group_user_dict[group]  
            
                # initial queries
                a = AuditTriple.objects.filter(user=user1,dataset=dataset).values_list('entityA','relation','entityB','verified')
                b = AuditTriple.objects.filter(user=user2,dataset=dataset).values_list('entityA','relation','entityB','verified')

                for trip in a:
                  a_set.add((trip[0],trip[1],trip[2],trip[3])) 

                for trip in b:
                  b_set.add((trip[0],trip[1],trip[2],trip[3])) 

                simularity.append(round(len(a_set&b_set)/len(a_set|b_set)*100,2))

                # clear set for next group
                a_set.clear()
                b_set.clear()

                simularity_dict[dataset] = simularity

        group_data = list(zip(group_user_dict.keys(),simularity))
        context['group_data'] = group_data
        context['simularity_dict'] = simularity_dict

        return context

def get_simularity(request):
    group_user_dict = {group.name: group.user_set.values_list('id', flat=True) for group in Group.objects.all()}
    simularity_dict = dict()
    a_set = set() 
    b_set = set() 
    for dataset in Dataset.objects.all():
        simularity = []
        for group in group_user_dict:

            # There are 2 users per group
            user1, user2 = group_user_dict[group]  

            # initial queries
            a = AuditTriple.objects.filter(user=user1,dataset=dataset).values_list('entityA','relation','entityB','verified')
            b = AuditTriple.objects.filter(user=user2,dataset=dataset).values_list('entityA','relation','entityB','verified')

            for trip in a:
                a_set.add((trip[0],trip[1],trip[2],trip[3])) 

            for trip in b:
                b_set.add((trip[0],trip[1],trip[2],trip[3])) 

            simularity.append(round(len(a_set&b_set)/len(a_set|b_set)*100,2))
            # clear set for next group
            a_set.clear()
            b_set.clear()

        group_data = dict(zip(group_user_dict.keys(),simularity))
        simularity_dict[dataset.name] = simularity
    print('simdict',simularity_dict)


    #return JsonResponse({'group_data':group_data,'simularity_dict':simularity_dict})
    return JsonResponse({'group_data':group_data,'simularity_dict':simularity_dict})



class AuditTripleList(ListView):
    model = AuditTriple 
    template_name = 'audit_triple_list.html'

    # filter results based on the user
    def get_queryset(self):
       # original qs
       qs = super().get_queryset() 

       return qs.filter(user=self.request.user).select_related('user','dataset')
       #return qs.filter(user=self.request.user).prefetch_related('entityA_types','entityB_types').select_related('dataset')

    # add filter form
    def get_context_data(self, **kwargs):
        context = super(AuditTripleList, self).get_context_data(**kwargs)
        context['filter'] = AuditTripleFilter(self.request.GET,queryset=self.get_queryset(),request=self.request)

     #   # get user and other group user
     #   group = self.request.user.groups.all()
     #   users = CustomUser.objects.filter(groups__name=group[0])
     #   other_user = [u for u in users if u != self.request.user][0] 
     #   a = list()
     #   b = list()
     #   
     #   # get user's triples
     #   a = AuditTriple.objects.filter(user=self.request.user).values_list('dataset','entityA','relation','entityB','verified')
     #   b = AuditTriple.objects.filter(user=other_user).values_list('dataset','entityA','relation','entityB','verified')

     #   a_set = set()
     #   b_set = set()
     #   
     #   # make set
     #   for trip in a: 
     #       a_set.add((trip[0],trip[1],trip[2],trip[3],trip[4])) 
     #   
     #   for trip in b: 
     #       b_set.add((trip[0],trip[1],trip[2],trip[3],trip[4])) 

     #   # calculate union and intersection
     #   intersection = len((a_set & b_set))
     #   union = len((a_set | b_set))
     #   
     #   # calulate simularity
     #   context['simularity'] = round(intersection / union * 100,2) 
        return context

class AuditTripleUpdate(UpdateView):
    model = AuditTriple
    template_name = 'audit_triple_form.html'
    fields = [
      "entityA",
      "relation",
      "entityB",
      "verified",
    ]

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

class ListDatasets(ListView):
    model = Dataset
    template_name = 'audit_list_datasets.html'

class DeleteDataset(DeleteView):
    model = Dataset
    template_name = 'audit_dataset_confirm_delete.html'

    def get_success_url(self):
        return reverse('Audit:audit_list_datasets')
