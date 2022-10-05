from django.contrib import admin
from .models import Type, AuditTriple, Dataset

# Register your models here.
admin.site.register(Type)
admin.site.register(AuditTriple)
admin.site.register(Dataset)
