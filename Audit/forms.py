from django import forms
from .models import AuditTriple

class AuditTripleForm(forms.ModelForm):
    class Meta:
        model = AuditTriple
        fields = ('verified',)

class AuditUpdateForm(forms.ModelForm):
    entityA = forms.CharField(disabled=True)
    relation = forms.CharField(disabled=True)
    entityB = forms.CharField(disabled=True)
    class Meta:
        model = AuditTriple
        fields = ('entityA','relation','entityB','comment',)
