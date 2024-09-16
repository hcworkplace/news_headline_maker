from django.db import models

# Create your models here.
class testModel1(models.Model):
    text = models.CharField(max_length=11)

class testModel2(models.Model):
    text = models.CharField(max_length=11)
    num = models.IntegerField(max_length=10)