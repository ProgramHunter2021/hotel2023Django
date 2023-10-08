
from django.db import models
from django.db.models.fields.related import ForeignKey

from hotelbot.models import *
# Create your models here.

class RoomType(models.Model):
    rt_id = models.CharField(max_length=50, unique=True, primary_key= True)
    rt_name = models.CharField(max_length=255)
    rt_price = models.IntegerField(default=0)
    rt_limit = models.IntegerField(default=2)
    rt_image = models.TextField(blank= True, null= True)
    rt_description = models.TextField(blank= True, null= True)
    comment = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s" % (self.rt_name, self.rt_price)
    
room_status = (('open', 'open'),('closed', 'closed'))

class Room (models.Model):
    r_id = models.CharField(max_length=50, unique=True, primary_key= True)
    r_key = models.CharField(max_length=100, unique=True)
    r_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    r_status = models.CharField(max_length=10, choices=room_status)
    r_users = models.ManyToManyField(Users,blank=True)
    comment = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s" % (self.r_id, self.r_type.rt_name)

order_status = (('1', '未付訂'),('2', '已付訂'),('3', '全付清'),('4', '結案'),('5','已取消'))

class Order(models.Model):
    o_id = models.CharField(max_length=50, unique=True, primary_key= True)
    o_user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=False)
    o_roomtype = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    o_date = models.DateTimeField(default=timezone.now)  
    o_status = models.CharField(max_length=10, choices=order_status)
    comment = models.TextField(blank= True, null= True)
    
    def __str__(self):
        # return "Order: %s" % (self.o_date)
        return "%s, (%s)%s" % (self.o_date.date(), self.o_user.lineid, self.o_user.name)

class BookingRoom(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    booked_date = models.DateTimeField()
    comment = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s, %s" % (self.order, self.room, self.booked_date.date())

class Transactions(models.Model):
    t_number = models.TextField()
    t_amount = models.IntegerField(default=0)
    t_method = models.CharField(max_length=50)
    t_date = models.DateTimeField()
    t_status = models.BooleanField(default=False)
    t_invoicetype = models.CharField(max_length=50, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank= True, null= True)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s, %s, %s, %s" % (self.t_number, self.t_amount, self.t_date, self.order)