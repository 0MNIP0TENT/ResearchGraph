from django import forms
from .models import Dataset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from Audit.fields import ListTextWidget

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

class AuditFunctionalForm(forms.Form):
    verified_choices = (
        ('Unknown', 'Unknown'),
        ('True', 'True'),
        ('False', 'False'),
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super(AuditFunctionalForm,self).__init__(*args, **kwargs)

        self.relation_qs = AuditTriple.objects.filter(user=self.request.user).values_list('relation').distinct()

        self.fields['relation'] = forms.CharField(required=False)
        self.fields['relation'].widget = ListTextWidget(self.relation_qs, 'relation_list')
        self.fields['relation'].queryset = AuditTriple.objects.filter(user=self.request.user).distinct()
            
        self.fields['entityA'] =  forms.CharField(required=False)
        self.fields['entityB'] =  forms.CharField(required=False)


    helper = FormHelper()
    helper.form_method = 'GET'

    # seems to work without defining these
    # helper.form_action = reverse_lazy('Audit/AuditTriple/List/')
    # helper.form_action = 'index'

    # submit
    helper.add_input(Submit('submit', 'Submit'))

    # fields
    # user = ForeignKey(get_user_model(),on_delete=models.CASCADE,default='')

    dataset = forms.ModelChoiceField(required=False, queryset=Dataset.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    #relation_qs = AuditTriple.objects.values_list('relation').distinct()
    #relation = forms.CharField(required=False, widget=ListTextWidget(relation_qs, 'relation_list'))
    #relation = forms.CharField(required=False )
    #entityA = forms.CharField(required=False)
    #entityB = forms.CharField(required=False)
    verified = forms.ChoiceField(choices=verified_choices, widget=forms.Select(attrs={'class': 'form-control'}))

