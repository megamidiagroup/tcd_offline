from django.db import models

# Create your models here.
class Profanities(models.Model):
    word = models.CharField(max_length=255, )
    pub_date = models.DateField(auto_now=True)