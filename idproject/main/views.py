from django.shortcuts import render
def index(request):
    return render(request, 'main/index.html')
def about(request):
    return render(request, 'main/about.html')
def writetous(request):
    return render(request, 'main/writetous.html')
def admin(request):
    return render(request, '127.0.0.1:8000/admin')