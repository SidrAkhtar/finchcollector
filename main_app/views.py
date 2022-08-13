import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy, Photo
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
   # Get the toys the finch doesn't have...
   # First, create a list of the toy ids that the finch DOES have
   id_list = finch.toys.all().values_list('id')
   # Now we can query for toys whose ids are not in the list using exclude
   toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
   # instantiate FeedingForm to be rendered in the template
   feeding_form = FeedingForm()
   return render(
      request, 
      'finches/detail.html',
      {
         'finch': finch,
         'feeding_form': feeding_form,
         'toys': toys_finch_doesnt_have
      }
   )

class FinchCreate(CreateView):
   model = Finch
   fields = '__all__'
   # Refactor fields so that 'toys' is not rendered in form
   fields = ['name', 'family', 'habitat', 'diet', 'price', 'lifespan']
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
      # has the finch_id assigned
      new_feeding = form.save(commit=False)
      new_feeding.finch_id = finch_id
      new_feeding.save()
   return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
   # Note that you can pass a toy's id instead of the whole toy object
   finch = Finch.objects.get(id=finch_id)
   finch.toys.add(toy_id)
   # Finch.objects.get(id=finch_id).toys.add(toy_id)
   return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(finch_id)
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

def add_photo(request, finch_id):
   # photo-file will be the "name" attribute on the <input type="file">
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
         bucket = os.environ['S3_BUCKET']
         s3.upload_fileobj(photo_file, bucket, key)
         # build the full url string
         url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
         # we can assign to finch_id or finch (if you have a finch object)
         Photo.objects.create(url=url, finch_id=finch_id)
      except Exception as e:
         print('An error occurred uploading file to S3')
         print(e)
   return redirect('detail', finch_id=finch_id)
