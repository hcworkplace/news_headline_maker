from django.db import models

# Create your models here.

class AiClass(models.Model):
    class_num = models.IntegerField()
    lecture = models.CharField(max_length=50)
    class_room = models.CharField(max_length=50)
    students_num = models.IntegerField()

class AiStudents(models.Model):
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=50)
    intro_text = models.TextField()