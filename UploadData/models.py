from django.db import models

# Create your models here.

class SemanticType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Entity(models.Model):
    name = models.CharField(max_length=255)
    semantic_type = models.ManyToManyField(SemanticType)

    def __str__(self):
        return self.name 

class Relation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Triple(models.Model):
    entityA = models.OneToOneField(Entity,on_delete=models.DO_NOTHING,related_name='entA')
    entityB = models.OneToOneField(Entity,on_delete=models.DO_NOTHING,related_name='entB')
    relation = models.OneToOneField(Relation,on_delete=models.DO_NOTHING,related_name='rel')

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)

class Verified(models.Model):
    entityA = models.CharField(max_length=255)
    entityB = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)
