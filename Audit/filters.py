import django_filters
from .models import AuditTriple
from django.contrib.auth import get_user_model

class AuditTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('dataset','relation','entityA','entityB','verified')

# for admin users
class AuditUserTripleFilter(django_filters.FilterSet):

    choices = get_user_model().objects.exclude(is_staff=True).values_list('id','username')
    user = django_filters.ChoiceFilter(choices=choices)
    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('dataset','dataset','user','relation','entityA','entityB','verified')

class CommentFilter(django_filters.FilterSet):

    choices = get_user_model().objects.exclude(is_staff=True).values_list('id','username')
    user = django_filters.ChoiceFilter(choices=choices)
    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('user','relation','entityA','entityB',)

