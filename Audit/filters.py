import django_filters
from django.db import models
from django import forms
from users.models import Triple, Entity, SemanticType, Relation

class TripleFilter(django_filters.FilterSet):
    class Meta:
        model = Triple
        fields = {'entityA','entityB','relation'}
    #    exclude = ['user']
       
class EntityFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Entity
        exclude = ['semantic_type','user']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for entities'}

class RelationFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Relation
        exclude = ['user']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for relations'}

class SemanticTypeFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = SemanticType
        exclude = ['user']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form.fields['name'].label='Name'
        self.form.fields['name'].widget.attrs = {'placeholder':'search for semantic types'}
