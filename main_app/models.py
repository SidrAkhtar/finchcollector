from os import DirEntry
from django.db import models
# Import the reverse function
from django.urls import reverse

# Create your models here.
class Finch(models.Model):
   name = models.CharField(max_length=100)
   family = models.CharField(max_length=100)
   habitat = models.CharField(max_length=200)
   diet = models.TextField(max_length=250)
   price = models.CharField(max_length=50)
   lifespan = models.CharField(max_length=100)

   def __str__(self):
      return self.name

   def get_absolute_url(self):
      return reverse('detail', kwargs={'finch_id': self.id})