
from django.shortcuts import render
from django.urls import path

# 
def index_view(request):
    return render(request, 'affiliate/index.html')
