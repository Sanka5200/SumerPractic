from django.shortcuts import render, redirect
from .models import  Baza
from .forms import BazaForm

def book_home(request):
    book=Baza.objects.order_by("-date")
    return render(request, 'book/book_home.html', {'book':book})

def create(request):
    error=""
    if request.method == 'POST':
        form = BazaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error="Ошибка заполнения"
    form = BazaForm()
    data = {
        'form':form,
        'error':error
    }
    return render(request, 'book/create.html', data)