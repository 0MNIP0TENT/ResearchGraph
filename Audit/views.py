from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from users.models import UserDataset
from django.views.generic.edit import UpdateView
from users.models import Entity
  
# Create your views here.

class AuditHome(TemplateView): 
    template_name = 'audit_home.html'

class EntityList(ListView):
    model = Entity

class EntityUpdate(UpdateView):
    model = Entity 
    fields = [
      "name",
    ]
    success_url = '/'

