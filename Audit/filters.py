import django_filters
from users.models import Triple, Entity, SemanticType, Relation
from .models import AuditTriple

class TripleFilter(django_filters.FilterSet):

    class Meta:
        model = Triple
        fields = ('relation','entityA','entityB','verified')

    # overriding init to pass the request object to the filter   
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        entities = Entity.objects.filter(user=kwargs['request'].user)
        self.form.fields['relation'].queryset = Relation.objects.filter(user=kwargs['request'].user)
        self.form.fields['entityA'].queryset = entities 
        self.form.fields['entityB'].queryset = entities 

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


class EntityFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Entity
        exclude = ['semantic_type','user']

    # changing field widget attribs 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for entities'}

class RelationFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Relation
        exclude = ['user']

    # changing field widget attribs 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for relations'}

class SemanticTypeFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = SemanticType
        exclude = ['user']

    # changing field widget attribs 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for semantic types'}
