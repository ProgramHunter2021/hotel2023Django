from django.db import models
from django.utils import timezone

# 叫車清單
class hailOption(models.Model):
    agencyName = models.CharField(max_length=50)   #車行名
    agencyNumber = models.CharField(max_length=10,blank=True, null=True)  #車行電話
    agencyUrl = models.URLField(blank=True, null=True)  #網址
    imgUrl = models.URLField(blank=True, null=True)  #圖片網址
    onOff = models.BooleanField(default=True) #開關

# 包車清單
class charteredOption(models.Model):
    carType = models.CharField(max_length=50)   #車種
    carImgUrl = models.URLField(blank=True, null=True)  #圖片網址  
    chtdStartPrice = models.PositiveIntegerField(default=3000) #半天價
    chtdAlldayPrice = models.PositiveIntegerField(default=4500) #全天價
    timeOutPrice = models.PositiveIntegerField(default=400) #超時價/小時
    onOff = models.BooleanField(default=True) #開關

# 包車預約紀錄
class chartered_order(models.Model):
    pub_datetime = models.DateTimeField(default=timezone.now)   #登錄時間
    userId = models.CharField(max_length=40, blank=True, null=True)   #官方內建ID
    appointmentDate = models.DateTimeField(blank=True, null=True)    #預約日期
    carType = models.CharField(max_length=50)   #預約車型
    passengerAmount = models.PositiveIntegerField(default=2)    #乘客數
    chtd_time = models.CharField(max_length=30) #包車總時間
    total_cost = models.IntegerField(default=0)  #消費總金額
    questNote = models.CharField(max_length=100, blank=True, null=True)    #客戶特殊需求
    transaction_id = models.CharField(max_length=50, blank=True, null=True) #使用LinePay時, 串接官方的回傳值
    paid = models.BooleanField(default=False) #繳費與否
    
    class Meta:
        ordering = ('-appointmentDate',)