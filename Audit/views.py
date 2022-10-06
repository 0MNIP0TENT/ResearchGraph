from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from .models import AuditTriple, Type, Dataset
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from .filters import  AuditTripleFilter, AuditUserTripleFilter

# used to redirect login on certain pages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserTripleView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/login/' 
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

    #return JsonResponse({'group_data':group_data,'simularity_dict':simularity_dict})
    return JsonResponse({'group_data':group_data,'simularity_dict':simularity_dict})



class AuditTripleList(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/login/' 
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

        return context

def audit_triples(request):
    context = {}

    triple_filter = AuditTripleFilter(
        request.GET,
        queryset=AuditTriple.objects.filter(user=request.user)
    )

    paginated_triple_filter = Paginator(triple_filter.qs,50)

    context['triple_filter'] = triple_filter 
    page_number = request.GET.get('page')
    page_obj = paginated_triple_filter.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request,'audit_triple_list.html',context=context)

class AuditTripleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/login/' 
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

class AuditTypeCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/login/' 
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

class ListDatasets(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/login/' 
    model = Dataset
    template_name = 'audit_list_datasets.html'

class DeleteDataset(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/login/' 
    model = Dataset
    template_name = 'audit_dataset_confirm_delete.html'

    def get_success_url(self):
        return reverse('Audit:audit_list_datasets')
