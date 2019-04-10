from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    rang=range(30)
    return render(request,'shopstore/index.html',{"rang":rang})   
def login(request):
    return render(request,"shopstore/login.html")         
