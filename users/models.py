from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    pass

class UserDataset(models.Model):
    dataset = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    entityA = models.CharField(max_length=255)
    entityB = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)
