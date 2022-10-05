import django_filters
from .models import AuditTriple
from django.forms import Select

class AuditTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('dataset','relation','entityA','entityB','verified')

    # overriding init to pass the request object to the filter   
   # def __init__(self,*args,**kwargs):
   #     super().__init__(*args,**kwargs)
   #    # datasets = set(AuditTriple.objects.values_list('dataset').distinct())
   #    # choices = []
       # [choices.append((name[0],name[0])) for name in datasets]
   #     queries = AuditTriple.objects.filter(user=kwargs['request'].user)
   #     self.form.fields['dataset'].widget = Select(choices=choices) 
   #     self.form.fields['relation'].queryset = queries 
   #     self.form.fields['entityA'].queryset =  queries
   #    # self.form.fields['entityA_types'].queryset = entities 
   #     self.form.fields['entityB'].queryset = queries 
       # self.form.fields['entityB_types'].queryset = entities 

# for admin users
class AuditUserTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('dataset','dataset','user','relation','entityA','entityB','verified')

    # overriding init to pass the request object to the filter   
  #  def __init__(self,*args,**kwargs):
  #      super().__init__(*args,**kwargs)
  #      datasets = set(AuditTriple.objects.values_list('dataset').distinct())
  #      choices = []
  #      [choices.append((name[0],name[0])) for name in datasets]
  #      self.form.fields['dataset'].widget = Select(choices=choices) 
  #      queries = AuditTriple.objects.filter(user=kwargs['request'].user)
  #      self.form.fields['relation'].queryset = queries 
  #      self.form.fields['entityA'].queryset =  queries
  #     # self.form.fields['entityA_types'].queryset = entities 
  #      self.form.fields['entityB'].queryset = queries 
  #     # self.form.fields['entityB_types'].queryset = entities 
