from django.contrib import admin
from .models import Type, AuditTriple

# Register your models here.
admin.site.register(Type)
admin.site.register(AuditTriple)
