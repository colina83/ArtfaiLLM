from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm
# Create your views here.

def home(request):
    if request.method == "POST":
        form = SearchForm(request.POST)        
        if form.is_valid():
            search = form.cleaned_data['search']
            print(search)            
    else:
        form = SearchForm()    
    return render(request, "home.html", {'form': form})