from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    pass

class SemanticType(models.Model):
    # DO_NOTHING makes so if a Entity is deleted the semantic types will remain
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

    class Meta:
        ordering = ('name',)

class Entity(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=255,null=True)
    semantic_type = models.ManyToManyField(SemanticType,blank=True)
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name 

class Relation(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name 

class Triple(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    entityA = models.ForeignKey(Entity,on_delete=models.SET_NULL,null=True,related_name='entA')
    entityB = models.ForeignKey(Entity,on_delete=models.SET_NULL,null=True,related_name='entB')
    relation = models.ForeignKey(Relation,on_delete=models.SET_NULL,null=True,related_name='rel')

    class Meta:
        ordering = ('relation',)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)

class UserDataset(models.Model):
    dataset = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    entityA = models.CharField(max_length=255)
    entityB = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)

