from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from commodity.models import Goods
from userinfo.models import UserInfo,Adress
from cartinfo.models import Order
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
    print(userinfo.values())
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
                return HttpResponseRedirect("/login")
        except:
            print("erro")
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

    flag=req.GET['flag']
    if flag=='user':
        form = changeuserinfoform(initial={'uname':userinfo['uname'],'email':userinfo['email'],'phone':userinfo['phone']})
        # form = changeuserinfoform()
        return render(req,'shopstore/changeinfo.html',{"username":username,'userinfo':userinfo,'form':form})
    if flag=='address':
        try:
            addresinfo=Adress.objects.filter(id=userinfo['addr_id']).values()[0]
            form = changeadsinfoform(initial={'name':addresinfo['aname'],'ads':addresinfo['ads'],'zipcode':addresinfo['zipcode'],'adsphone':addresinfo['phone']})
            return render(req,'shopstore/changeinfo.html',{"username":username,'form':form})
        except:
            username=req.COOKIES.get("username")
            form = changeadsinfoform()
            return HttpResponseRedirect("/addads")

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
        addr_id=Adress.objects.filter(aname=name).values()[0]['id']
        userinfo.update(addr=addr_id)
        return HttpResponseRedirect('/userinfo')
    form = changeadsinfoform()
    return render(req,'shopstore/addads.html',{"username":username,'form':form})


# #添加关联many to many
# b.auther.add(p)

# #去除关联
# b.auther.remove(p)

# #返回所有作者
# b.auther.all()
from django.views.decorators.csrf import csrf_exempt
import json
import time
@csrf_exempt
# crsf 装饰器
def order(req):
    username=req.COOKIES.get("username")
    if req.method=="POST":
        commodity=json.loads(req.body)
        order=Order()
        order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) \
        + str(time.time()).replace('.', '')[-7:]
        order.orderNo=order_no
        acotnum=0
        acount=0
        for key in commodity:
            acotnum+=int(commodity[key]['num'])
            acount+=int(commodity[key]['num'])*float(commodity[key]['price'])
            try:
                print(Goods.objects.get(id=commodity[key]['id']))
                order.goods.add(Goods.objects.get(id=commodity[key]['id']))
                print(order.goods)
            except:
                pass
        order.acot=acotnum
        order.acount=acount
        order.user=UserInfo.objects.get(uname=username)
        order.save()
        order=Order.objects.get(orderNo=order_no)
        print(order.user,order.goods)
        ok={'ok':'success'}
        return HttpResponse(json.dumps(ok),content_type='application/json')
    else:
        return render(req,'shopstore/cartinfo.html',{"username":username})

def myorder(req):
    username=req.COOKIES.get("username")
    userid=UserInfo.objects.get(uname=username).id
    orders=Order.objects.filter(user_id=userid)
    
    print(orders)
    return render(req,'shopstore/order.html',{"orders":orders,"username":username})
