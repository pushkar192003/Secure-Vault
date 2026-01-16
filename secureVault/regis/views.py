from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def register_view(request):
    return render(request, 'regis/register.html')
def login_view(request):
     return render(request, 'regis/login.html')
def logout_view(request):
     return HttpResponse("Login page")
