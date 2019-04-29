from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from commodity.models import Goods
from userinfo.models import *
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
# Create your views here.
class UserForm():
    username=forms.CharField(label="用户名",max_length=50)
    upassword=forms.CharField(label="密码",max_length=200)
    email = forms.CharField(label="邮箱",max_length=50)
    phone = forms.CharField(label='手机号',max_length=20)

def index(request):
    goods  = Goods.objects.all()
    username=request.COOKIES.get("username")
    print(username)
    return render(request,'shopstore/index.html',{"goods":goods,"username":username})   
def signup(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['upassword']
            femail = uf.cleaned_data['email']
            fphone = uf.cleaned_data['phone']
            #添加到数据库
            usern=UserInfo.objects.create(username= username,upassword=password,email=femail,phone=fphone)
            if usern:
                response=HttpResponseRedirect('shopstore/index.html')
                response.set_cookie('username',username,3600)
                return response
            else:
                'shopstore/signup.html'
    else:
        uf = UserForm()
    return render_to_response('shopstore/signup.html',{'uf':uf}, context_instance=RequestContext(req))
def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            upasswd=form.cleaned_data["upassword"]
            havepe=UserInfo.objects.filter(uname=username).filter(upassword=upasswd)
            if havepe:
                response=HttpResponseRedirect('shopstore/index.html')
                response.set_cookie('username',username,3600)
                return response
            else:    
                return render(request,"shopstore/signup.html",{"havepe":havepe}) 
    return render_to_response('shopstore/index.html',{'form':form},context_instance=RequestContext(request))