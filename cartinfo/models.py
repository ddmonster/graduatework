from django.db import models

# Create your models here.
from userinfo.models import UserInfo
from commodity.models import Goods
# Create your models here.
# 购物车CartInfo
# id
# user 用户（关联UserInfo）
# goods 商品（关联Goods）
# ccount 数量（数量）
ORDERSTATUS = (
    (1,'已提交',),
    (2,'处理中',),
    (3,'已完成',),
)
class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    good = models.ForeignKey(Goods,on_delete=models.CASCADE)
    ccount = models.IntegerField('数量',db_column='cart_count')
 
    def __str__(self):
        return self.user
# 订单表Order
# id
# orderNo 订单号
# orderdetail(商品，数量，单价，描述)
# adsname 收件人
# adsphone 收件电话
# ads　地址
# user　用户（关联）
# time 时间
# acot 总数
# acount 总价
# orderstatus 状态
class Order(models.Model):
    orderNo = models.CharField('商品编号',max_length=50)
    time = models.DateTimeField(auto_now=True)
    acot = models.IntegerField('总数',null=True)
    acount = models.DecimalField('总价',max_digits=8,decimal_places=2,null=True)
    orderstatus = models.IntegerField('订单',choices=ORDERSTATUS,default=1)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,null=True)
    goods=models.ManyToManyField(Goods,related_name='goods')
    def __str__(self):
        return self.orderNo