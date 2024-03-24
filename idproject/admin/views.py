from django.shortcuts import render
from .models import  Baza

def book_home(request):
    return render(request, 'admin.html')