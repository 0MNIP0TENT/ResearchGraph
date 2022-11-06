from django.contrib import admin
from .models import Type, AuditTriple, Dataset

# Register your models here.

@admin.register(AuditTriple)
class AuditAdmin(admin.ModelAdmin): 
    exclude = ('entityA_types','entityB_types',)
    list_display = ('dataset','user','entityA','relation','entityB','verified',)
    list_filter = ('user','relation','entityA','entityB','verified',)

admin.site.register(Type)
admin.site.register(Dataset)
