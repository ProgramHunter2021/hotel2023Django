from django.db import models
from hotelbot.models import *

# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=False)
    category = models.TextField(null= True, blank =False)
    service = models.TextField(null= True, blank =False)
    reservation_date = models.DateTimeField(null= True, blank=True)  

    is_canceled = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s, %s" % (self.id, self.user)

class Service_Item(models.Model):

    id = models.IntegerField(primary_key=True)
    category = models.TextField(null= True, blank =False) #服務的種類(SPA，美髮美睫之類的)
    img_url = models.TextField(null= True, blank =False) #服務的圖片
    title = models.TextField(null= True, blank =False) #服務的項目(精油推拿)
    duration = models.TextField(null= True, blank =False) #時長
    description = models.TextField(null= True, blank =False) #介紹
    price = models.TextField(null= True, blank =False) #價格 

    created_on = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s, %s" % (self.category, self.title)