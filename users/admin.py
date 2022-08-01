from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserDataset, Triple, Entity, SemanticType, Relation

from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserDataset)
admin.site.register(Triple)
admin.site.register(Entity)
admin.site.register(SemanticType)
admin.site.register(Relation)
