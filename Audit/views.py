from django.views.generic.list import ListView
from users.models import UserDataset
from django.views.generic.edit import UpdateView
  
# Create your views here.

class AuditList(ListView):
    model = UserDataset

class AuditUpdate(UpdateView):
    model = UserDataset
    fields = [
        "entityA",
        "entityB",
        "relation",
    ]
    success_url = '/'
