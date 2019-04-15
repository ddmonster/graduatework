from django.shortcuts import render
from django.http import HttpResponse
from commodity.models import Goods
# Create your views here.

def index(request):
    goods  = Goods.objects.all()
    print(goods[0].picture)
    return render(request,'shopstore/index.html',{"goods":goods})   
def login(request):
    return render(request,"shopstore/login.html")         
