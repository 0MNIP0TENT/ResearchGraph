import django_filters
from .models import AuditTriple

class AuditTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('relation','entityA','entityB','verified')

    # overriding init to pass the request object to the filter   
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        queries = AuditTriple.objects.filter(user=kwargs['request'].user)
        self.form.fields['relation'].queryset = queries 
        self.form.fields['entityA'].queryset =  queries
       # self.form.fields['entityA_types'].queryset = entities 
        self.form.fields['entityB'].queryset = queries 
       # self.form.fields['entityB_types'].queryset = entities 

class AuditUserTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('user','relation','entityA','entityB','verified')

#    # overriding init to pass the request object to the filter   
#    def __init__(self,*args,**kwargs):
#        super().__init__(*args,**kwargs)
#        queries = AuditTriple.objects.filter(user=kwargs['request'].user)
#        self.form.fields['relation'].queryset = queries 
#        self.form.fields['entityA'].queryset =  queries
#       # self.form.fields['entityA_types'].queryset = entities 
#        self.form.fields['entityB'].queryset = queries 
#       # self.form.fields['entityB_types'].queryset = entities 
