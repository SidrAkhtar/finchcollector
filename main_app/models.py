from os import DirEntry
from django.db import models
# Import the reverse function
from django.urls import reverse

# Create your models here.
MEALS = (
   ('B', 'Breakfast'),
   ('L', 'Lunch'),
   ('D', 'Dinner'),
)

class Finch(models.Model):
   name = models.CharField(max_length=100)
   family = models.CharField(max_length=100)
   habitat = models.CharField(max_length=200)
   diet = models.TextField(max_length=250)
   price = models.CharField(max_length=50)
   lifespan = models.CharField(max_length=100)

   def __str__(self):
      return f'{self.name} ({self.id})'

class Feeding(models.Model):
   date = models.DateField('Feeding Date')
   meal = models.CharField(
      max_length=1,
      choices=MEALS,
      default=MEALS[0][0]
      )
   finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

   def __str__(self):
      # Nice method for obtaining the friendly value of a Field.choice
      return f"{self.get_meal_display()} on {self.date}"

   class Meta:
      ordering = ['-date']

   def get_absolute_url(self):
      return reverse('detail', kwargs={'finch_id': self.id})