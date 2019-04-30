from django.db import models

# Create your models here.
class Adress(models.Model):
    aname = models.CharField('收货人',max_length=50,null=False,default="null")
    ads = models.CharField('地址',max_length=300,null=False,default="null")
    phone = models.CharField('电话',max_length=20,null=False,default="null")
    
 
    def __str__(self):
        return self.aname
class UserInfo(models.Model):
    uname = models.CharField('用户名',max_length=50,null=False,unique=True)
    upassword = models.CharField('密码',max_length=200,null=False)
    email = models.CharField('邮箱',max_length=50,null=True)
    phone = models.CharField('手机号',max_length=20,null=False)
    time = models.DateTimeField('注册时间',auto_now=True)
    isban = models.BooleanField('是否禁用',default=False)
    isdelete = models.BooleanField('删除',default=False)
    addr = models.ForeignKey(Adress,on_delete=models.CASCADE,to_field="id",null=True)
 
    def __str__(self):
        return self.uname
 
