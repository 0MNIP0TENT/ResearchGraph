from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from .models import AuditTriple, Type, Dataset
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from .filters import  AuditTripleFilter, AuditUserTripleFilter, CommentFilter 
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

# used to redirect login on certain pages
from django.contrib.auth.mixins import LoginRequiredMixin

#forms imports
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from Audit.fields import ListTextWidget

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

    def get_context_data(self):
        context = super(GroupsView,self).get_context_data()
        group_user_dict = {group.name: group.user_set.values_list('id', flat=True) for group in Group.objects.all()}
        simularity_dict = dict()

        a_set = set() 
        b_set = set() 

        for dataset in Dataset.objects.all():
            simularity_list = []
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

                simularity_list.append(round(len(a_set&b_set)/len(a_set|b_set)*100,2))

                # clear set for next group
                a_set.clear()
                b_set.clear()

                simularity_dict[dataset] = simularity_list

            group_data = list(zip(group_user_dict.keys(),simularity_list))
            context['group_data'] = group_data
            context['simularity_dict'] = simularity_dict

        return context

def get_simularity(request):
    # NOT IN USE
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

class AuditTripleModelForm(ModelForm):
    # NOT IN USE
    class Meta:
        model = AuditTriple
        fields = ['dataset','relation','entityA','entityB','verified']
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.layout = Layout(
            HTML('<h1> hiiiiii </h1>'),
            Field('dataset'),
            Field('relation'),
            Field('entityA'),
            Field('entityB'),
            Field('verified'),
            Submit('submit','Submit', css_class='btn-success')
        )
        return helper

class AuditTripleList(LoginRequiredMixin, ListView):
    # NOT IN USE
    login_url = '/accounts/login/login/' 
    model = AuditTriple 
    template_name = 'audit_triple_list.html'
   # form_class = AuditTripleModelForm

    # filter results based on the user
    def get_queryset(self):
       # original qs
       qs = super().get_queryset() 

       return qs.filter(user=self.request.user).select_related('user','dataset')
       #return qs.filter(user=self.request.user).prefetch_related('entityA_types','entityB_types').select_related('dataset')

    # add filter form
    def get_context_data(self, **kwargs):
        context = super(AuditTripleList, self).get_context_data(**kwargs)
        context['triple_filter'] = triple_filter 
        paginated_triple_filter = Paginator(triple_filter.qs,50)
        context = {'form': AuditFunctionalForm(request=selfrequest)}
        page_number = self.request.GET.get('page')
        page_obj = paginated_triple_filter.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class AuditFunctionalForm(forms.Form):
    verified_choices = (
        ('Unknown', 'Unknown'),
        ('True', 'True'),
        ('False', 'False'),
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super(AuditFunctionalForm,self).__init__(*args, **kwargs)

        self.relation_qs = AuditTriple.objects.filter(user=self.request.user).values_list('relation').distinct()

        self.fields['relation'] = forms.CharField(required=False)
        self.fields['relation'].widget = ListTextWidget(self.relation_qs, 'relation_list')
        self.fields['relation'].queryset = AuditTriple.objects.filter(user=self.request.user).distinct()
            
        self.fields['entityA'] =  forms.CharField(required=False)
        self.fields['entityB'] =  forms.CharField(required=False)


    helper = FormHelper()
    helper.form_method = 'GET'

    # seems to work without defining these
    # helper.form_action = reverse_lazy('Audit/AuditTriple/List/')
    # helper.form_action = 'index'

    # submit
    helper.add_input(Submit('submit', 'Submit'))

    # fields
    # user = ForeignKey(get_user_model(),on_delete=models.CASCADE,default='')


    dataset = forms.ModelChoiceField(required=False, queryset=Dataset.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    #relation_qs = AuditTriple.objects.values_list('relation').distinct()
    #relation = forms.CharField(required=False, widget=ListTextWidget(relation_qs, 'relation_list'))
    #relation = forms.CharField(required=False )
    #entityA = forms.CharField(required=False)
    #entityB = forms.CharField(required=False)
    verified = forms.ChoiceField(choices=verified_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    
     
def audit_triples(request):
    context = {}

    if not request.user.is_authenticated:
        raise PermissionDenied

    triple_filter = AuditTripleFilter(
        request.GET,
        queryset=AuditTriple.objects.filter(user=request.user).select_related('dataset')
    )

    paginated_triple_filter = Paginator(triple_filter.qs,50)
    context = {'form': AuditFunctionalForm(request=request)}
    context['triple_filter'] = triple_filter 
    page_number = request.GET.get('page')
    page_obj = paginated_triple_filter.get_page(page_number)
    context['page_obj'] = page_obj
    
    return render(request,'audit_triple_list.html',context=context)

def audit_triple_cards(request):
    context = {}

    if not request.user.is_authenticated:
        raise PermissionDenied

    triple_filter = AuditTripleFilter(
        request.GET,
        queryset=AuditTriple.objects.filter(user=request.user).select_related('dataset')
    )

    paginated_triple_filter = Paginator(triple_filter.qs,25)
    context = {'form': AuditFunctionalForm(request=request)}
    context['triple_filter'] = triple_filter 
    page_number = request.GET.get('page')
    page_obj = paginated_triple_filter.get_page(page_number)
    context['page_obj'] = page_obj
    
    return render(request,'audit_triple_cards.html',context=context)

def admin_view_triples(request):
    context = {}

    if not request.user.is_staff:
        raise PermissionDenied

    triple_filter = AuditUserTripleFilter(
        request.GET,
        queryset=AuditTriple.objects.all()
    )

    paginated_triple_filter = Paginator(triple_filter.qs,50)

    context['triple_filter'] = triple_filter 
    page_number = request.GET.get('page')
    page_obj = paginated_triple_filter.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request,'audit_user_triple_list.html',context=context)

def admin_view_triple_cards(request):
    context = {}

    if not request.user.is_staff:
        raise PermissionDenied

    triple_filter = AuditUserTripleFilter(
        request.GET,
        queryset=AuditTriple.objects.all().select_related('user')
    )

    paginated_triple_filter = Paginator(triple_filter.qs,25)

    context = {'form': AuditFunctionalForm(request=request)}
    context['triple_filter'] = triple_filter 
    page_number = request.GET.get('page')
    page_obj = paginated_triple_filter.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request,'audit_user_triple_cards.html',context=context)

class AuditTripleUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/accounts/login/login/' 
    model = AuditTriple
    template_name = 'audit_triple_form.html'
    fields = [
      "entityA",
      "relation",
      "entityB",
      "comment",
      #"verified",
    ]

    # if updated make verified False
    def form_valid(self,form):
        form.instance.verified = False
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next','/')

# Detail view for admins to view comments
class AuditTripleDetailView(DetailView):
    model = AuditTriple
    template_name = 'audit_triple_detail.html'

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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class DeleteDataset(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/login/' 
    model = Dataset
    template_name = 'audit_dataset_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('Audit:audit_list_datasets')

class CommentView(LoginRequiredMixin, ListView):
    model = AuditTriple
    template_name = 'audit_comments.html'
    login_url = '/accounts/login/login/' 

    def get_queryset(self): 
        qs = super(CommentView, self).get_queryset()
        return qs.exclude(comment='').select_related('dataset','user').order_by('user')

    def get_context_data(self):
        context = super(CommentView, self).get_context_data()
        context['filter'] = CommentFilter(
            self.request.GET,
            queryset=self.get_queryset(),
            request=self.request
        )
        paginated_comment_filter = Paginator(context['filter'].qs,10)
        page_number = self.request.GET.get('page')
        page_obj = paginated_comment_filter.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class DifferenceView(LoginRequiredMixin, ListView):
    model = AuditTriple
    template_name = 'audit_differences.html'
    login_url = '/accounts/login/login/' 

    # Overwrite the queryset to return the unverified triples of the logged in user.
    def get_queryset(self):
        qs = super(DifferenceView, self).get_queryset()
        return qs.filter(user=self.request.user,verified=False).select_related('user')

    def get_context_data(self):
        context = super(DifferenceView, self).get_context_data()

        # users only have one group
        group = self.request.user.groups.all()[0]
         
        # get the name of the other group memeber
        other_group_member = get_user_model().objects.filter(
            groups__name=group).exclude(username=self.request.user.username) 
        
        # get search params for the other groups user
        entityA_list = self.get_queryset().values_list('entityA') 
        relation_list = self.get_queryset().values_list('relation') 
        entityB_list = self.get_queryset().values_list('entityB') 

        # only one other group member
        other_list = AuditTriple.objects.filter(
            user=other_group_member[0],
            entityA__in=entityA_list,
            relation__in=relation_list,
            entityB__in=entityB_list
        ).select_related('user','dataset') 

        context['other_list'] = other_list
        return context
