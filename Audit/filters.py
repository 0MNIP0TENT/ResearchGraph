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

# for admin users
class AuditUserTripleFilter(django_filters.FilterSet):

    entityA = django_filters.CharFilter(lookup_expr='startswith')
    entityB = django_filters.CharFilter(lookup_expr='startswith')
    relation = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = AuditTriple
        fields = ('dataset','dataset','user','relation','entityA','entityB','verified')

