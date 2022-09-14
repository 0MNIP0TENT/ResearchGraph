import django_filters
from users.models import Triple, Entity, SemanticType, Relation

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
