from django.db import models
import uuid
from django.contrib.auth import get_user_model

# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=255,)

    def __str__(self):
        return self.name 

class Type(models.Model):

    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,default='')
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

    class Meta:
        ordering = ('name',)

class AuditTriple(models.Model):

    id = models.UUIDField(
    
        primary_key=True,
        default=uuid.uuid4,
        editable=False

    ) 

    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)

    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,default='')

    entityA = models.CharField(max_length=255)
    entityA_types = models.ManyToManyField(Type,blank=True,related_name="entityA_types")

    relation = models.CharField(max_length=255)

    entityB = models.CharField(max_length=255)
    entityB_types = models.ManyToManyField(Type,blank=True,related_name="entityB_types")

    comment = models.TextField(blank=True,null=True,verbose_name="comments",help_text="Enter a optional reason for un verifing")

    verified = models.BooleanField(default=True)

    class Meta:
        ordering = ('relation',)

    def __str__(self):
        return self.entityA + '----' + self.relation + '---->' + self.entityB 
