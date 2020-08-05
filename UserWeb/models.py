from django.db import models

# Create your models here.
class Users(models.Model):

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)+" ------- "+str(self.password)

class FeedbackUser(models.Model):

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)+" ------- "+str(self.password)