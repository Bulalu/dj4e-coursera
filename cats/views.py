from django.shortcuts import render, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Breed, Cat

# Create your views here.

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields ="__all__"
    success_url = reverse_lazy('cats:all')


class CatList(LoginRequiredMixin, View):

    def get(self,request):
        mc = Cat.objects.all
        al = Breed.objects.all().count
        ctx= {'cat_list':mc, 'breed_count': al}
        return render(request, 'cats/cat_list.html', ctx)
    


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields ="__all__"
    success_url = reverse_lazy('cats:all')
    



class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields ="__all__"
    success_url = reverse_lazy('cats:all')


class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields ="__all__"
    success_url = reverse_lazy('cats:all')


class BreedList(LoginRequiredMixin, View):

    def get(self,request):
        mc = Breed.objects.all()
        ctx = {'breed_list': mc}
        return render(request,'cats/breed_list.html', ctx)
    
   


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields ="__all__"
    success_url = reverse_lazy('cats:all')



class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields ="__all__"
    success_url = reverse_lazy('cats:all')


