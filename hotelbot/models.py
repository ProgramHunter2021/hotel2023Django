from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
    lineid = models.CharField(max_length=40, unique=True, primary_key= True)    # line用戶ID
    name = models.CharField(max_length=25, blank=True, null=True)            # 姓名
    idnumber = models.CharField(max_length=25, blank=True, null=True)
    nick_name = models.CharField(max_length=30, blank=True, null=True)          # line用戶name
    image_url = models.TextField(blank=True, null=True)                         # line用戶大頭貼
    phone = models.CharField(max_length=20, blank= True, null= True)            # 電話號碼
    address = models.TextField(blank= True, null= True)                         # 地址
    birthday = models.DateField(blank= True, null= True)                        # 生日
    email = models.TextField(blank= True, null= True)                           # 地址
    einvoice = models.CharField(max_length=20, blank= True, null= True)         # 電子發票
    GUInumber = models.CharField(max_length=20,blank= True, null= True)         # 統一編號
    followdate = models.DateTimeField(default=timezone.now)                     # line追蹤時間
    status = models.BooleanField(default=False, verbose_name="封鎖")
    promotable = models.BooleanField(default=False, verbose_name="promotable")
    comment = models.TextField(blank= True, null= True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s, %s" % (self.lineid, self.name)