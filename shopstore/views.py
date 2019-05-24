from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from commodity.models import Goods
from userinfo.models import UserInfo,Adress
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
# Create your views here.
class UserForm(forms.Form):
    username=forms.CharField(label="用户名",max_length=50)
    upassword=forms.CharField(label='密码',widget=forms.PasswordInput())


class loginform(forms.Form):
    username=forms.CharField(label="用户名",max_length=50)
    upassword=forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.CharField(label="邮箱",max_length=50)
    phone = forms.CharField(label='手机号',max_length=20)


class changeuserinfoform(forms.Form):
    uname=forms.CharField(label="用户名",max_length=50)
    email = forms.CharField(label="邮箱",max_length=50)
    phone = forms.CharField(label='手机号',max_length=20)


class changeadsinfoform(forms.Form):
    name=forms.CharField(label="收货人",max_length=50)
    ads=forms.CharField(label="地址",max_length=50)
    zipcode=forms.CharField(label="邮编",max_length=50)
    adsphone=forms.CharField(label="收货手机号码",max_length=50)





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
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['upassword']
            femail = form.cleaned_data['email']
            fphone = form.cleaned_data['phone']
            #添加到数据库
            isuser=UserInfo.objects.filter(uname=username)
            if isuser:
                form= loginform()
                ifsuccess=True
                return render(req,'shopstore/signup.html',{"form":form,'ifsuccess':ifsuccess})
            else:
                usern=UserInfo.objects.create(uname= username,upassword=password,email=femail,phone=fphone)
            print(usern)
            if usern:
                response=HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                return response
            else:
                ifsuccess=True
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
                response.set_cookie('username',username,604800)
                return response
            else:  
                form = UserForm()  
                havepe=True
                return render(request,"shopstore/login.html",{"havepe":havepe,"form":form}) 
    return render(request,'shopstore/login.html',{"havepe":havepe,"form":form})



def logout(req):
    response = HttpResponseRedirect('/cartinfo')
    #清理cookie里保存username
    response.delete_cookie("commodity")
    response.delete_cookie('username')
    return response

def cartinfo(req):
    username=req.COOKIES.get("username")
    return render(req,'shopstore/cartinfo.html',{"username":username})


def userinfo(req):
    username=req.COOKIES.get("username")
    userinfo=UserInfo.objects.filter(uname=username)
    return render(req,'shopstore/userinfo.html',{"username":username,'userinfo':userinfo})



def changeinfo(req):
    username=req.COOKIES.get("username")
    userinfo=UserInfo.objects.filter(uname=username)
    if req.method=="POST":
        print(req.POST)
        try:
            if req.POST['uname']:
                funame=req.POST["uname"]
                femail=req.POST["email"]
                fphone=req.POST["phone"]
                UserInfo.objects.filter(uname=username).update(uname=funame,email=femail,phone=fphone)
        except:
            pass
        try:
            if req.POST['ads']:
                print('hi')
                faname=req.POST["name"]
                fads=req.POST["ads"]
                fzipcode=req.POST["zipcode"]
                fadsphone=req.POST["adsphone"]
                userinfo=userinfo.values()[0]
                print(userinfo)
                Adress.objects.filter(id=userinfo['addr_id']).update(aname=faname,ads=fads,zipcode=fzipcode,phone=fadsphone)
        except:
            pass
        userinfo=UserInfo.objects.filter(uname=username)
        return render(req,'shopstore/userinfo.html',{"username":username,'userinfo':userinfo})
    userinfo=userinfo.values()[0]
    addresinfo=Adress.objects.filter(id=userinfo['addr_id']).values()[0]
    flag=req.GET['flag']
    if flag=='user':
        form = changeuserinfoform(initial={'uname':userinfo['uname'],'email':userinfo['email'],'phone':userinfo['phone']})
        # form = changeuserinfoform()
        return render(req,'shopstore/changeinfo.html',{"username":username,'userinfo':userinfo,'form':form})
    if flag=='address':
        form = changeadsinfoform(initial={'name':addresinfo['aname'],'ads':addresinfo['ads'],'zipcode':addresinfo['zipcode'],'adsphone':addresinfo['phone']})
        return render(req,'shopstore/changeinfo.html',{"username":username,'form':form})
    userinfo=UserInfo.objects.filter(uname=username)
    return render(req,'shopstore/userinfo.html',{"username":username,'userinfo':userinfo})

def addads(req):

    username=req.COOKIES.get("username")
    userinfo=UserInfo.objects.filter(uname=username)
    if req.method=="POST":
        faname=req.POST["name"]
        fads=req.POST["ads"]
        fzipcode=req.POST["zipcode"]
        fadsphone=req.POST["adsphone"]
        name=Adress.objects.create(aname=faname,ads=fads,zipcode=fzipcode,phone=fadsphone)
        addr_id=Adress.objects.filter(aname=name)
    form = changeadsinfoform()
    return render(req,'shopstore/addads.html',{"username":username,'form':form})

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
# crsf 装饰器
def order(req):
    if req.method=="POST":
        commodity=json.loads(req.body)
        print(commodity)
        ok={'ok':'success'}
        return HttpResponse(json.dumps(ok),content_type='application/json')
    else:
        return HttpResponse("fail")
