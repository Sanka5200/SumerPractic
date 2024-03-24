from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('admin', views.admin, name='admin'),
    path('writetous', views.writetous, name='writetous'),
]