from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch

# Create your views here.
# Define the home view
def home(request):
   return render(request, 'home.html')

def about(request):
   return render(request, 'about.html')

def finches_index(request):
   finches = Finch.objects.all()
   return render(request, 'finches/index.html', { 
      'finches': finches 
      })

def finches_detail(request, finch_id):
   finch = Finch.objects.get(id=finch_id)
   return render(request, 'finches/detail.html', {
      'finch': finch
      })

class FinchCreate(CreateView):
   model = Finch
   fields = '__all__'
   # success_url = '/finches/' --- used "get_absolute_url" method in models.py

class FinchUpdate(UpdateView):
   model = Finch
   fields = ['family', 'habitat', 'diet', 'price', 'lifespan']

class FinchDelete(DeleteView):
   model = Finch
   success_url = '/finches/'