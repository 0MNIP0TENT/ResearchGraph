from django import forms
from .models import AuditTriple

class AuditTripleForm(forms.ModelForm):
    class Meta:
        model = AuditTriple
        fields = ('verified',)
