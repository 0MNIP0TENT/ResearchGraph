from django.contrib import admin
from .models import Triple, Entity, Relation
from .models import Verified, SemanticType

# Register your models here.
admin.site.register(Triple)
admin.site.register(Verified)
admin.site.register(Entity)
admin.site.register(SemanticType)
admin.site.register(Relation)
