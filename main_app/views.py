from django.shortcuts import render

class Finch: 
   def __init__(self, name, family, habitat, diet, price, lifespan):
      self.name = name
      self.family = family
      self.habitat = habitat
      self.diet = diet
      self.price = price
      self.lifespan = lifespan

finches = [
   Finch('Blue Finch', 'Thraupidae', 'Dry Savannah', 'Seeds, insects and plant matter', '$20-$40', '5-10 years'),
   Finch('Purple Finch', 'Fringillidae', 'Suburbs, groves, and woods', 'Seeds(of elm, and ash and so on), berries, small fruits, buds,  insects', '$55-$150', '5-9 years on average'),
]


# Create your views here.
# Define the home view
def home(request):
   return render(request, 'home.html')

def about(request):
   return render(request, 'about.html')

def finches_index(request):
   return render(request, 'finches/index.html', { 
      'finches': finches 
      })