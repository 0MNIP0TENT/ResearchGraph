
from django.urls import path
from . import views

app_name = 'UploadData'
urlpatterns = [
    path('', views.upload_data_view, name='upload'),
]
