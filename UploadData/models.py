from django.db import models

# Create your models here.

class Triple(models.Model):
    entityA = models.CharField(max_length=255)
    entityB = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)

class Verified(models.Model):
    entityA = models.CharField(max_length=255)
    entityB = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    def __str__(self):
        return '{} --> {} --> {}'.format(self.entityA,self.relation,self.entityB)
