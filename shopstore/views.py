from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from commodity.models import Goods
from userinfo.models import *
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
# Create your views here.
class UserForm(forms.Form):
    username=forms.CharField(label="用户名",max_length=50)
    upassword=forms.CharField(label="密码",max_length=200)
class loginform(forms.Form):
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
    form= loginform()
    ifsuccess=False
    if req.method == 'POST':
        form = loginform(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['upassword']
            femail = uf.cleaned_data['email']
            fphone = uf.cleaned_data['phone']
            #添加到数据库
            usern=UserInfo.objects.create(username= username,upassword=password,email=femail,phone=fphone)
            print(usern)
            if usern:
                response=HttpResponseRedirect('shopstore/index.html')
                response.set_cookie('username',username,3600)
                return response
            else:
                ifsuccess=False
                return render(req,'shopstore/signup.html',{"form":form,'ifsuccess':ifsuccess})

    return render(req,'shopstore/signup.html',{"form":form,'ifsuccess':ifsuccess})
def login(request):
    havepe=False
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            username=form.cleaned_data["username"]
            upasswd=form.cleaned_data["upassword"]
            print(username,upasswd)
            havepe=UserInfo.objects.filter(uname=username).filter(upassword=upasswd)
            print(havepe)
            if havepe:
                response=HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                return response
            else:  
                form = UserForm()  
                havepe=True
                return render(request,"shopstore/login.html",{"havepe":havepe,"form":form}) 
    return render(request,'shopstore/login.html',{"havepe":havepe,"form":form})
def logout(req):
    response = HttpResponseRedirect('/')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response
