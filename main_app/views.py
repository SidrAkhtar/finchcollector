from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy
from .forms import FeedingForm

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
   # instantiate FeedingForm to be rendered in the template
   feeding_form = FeedingForm()
   return render(
      request, 
      'finches/detail.html',
      {
         'finch': finch,
         'feeding_form': feeding_form
      }
   )

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

def add_feeding(request, finch_id):
   # create a ModelForm instance using the data in request.POST
   form = FeedingForm(request.POST)
   # validate the form
   if form.is_valid():
      # don't save the form to the db until it
      # has the cat_id assigned
      new_feeding = form.save(commit=False)
      new_feeding.finch_id = finch_id
      new_feeding.save()
   return redirect('detail', finch_id=finch_id)


class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'