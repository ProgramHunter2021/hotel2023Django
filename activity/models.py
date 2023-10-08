from django.db import models

# Create your models here.

class ActivityType(models.Model):
    at_id = models.CharField(max_length=40, unique=True, primary_key= True)
    at_name = models.CharField(max_length= 50,blank= True, null= True)
    comment = models.TextField(blank= True, null= True)

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % (self.at_name)

class Activities(models.Model):
    a_id = models.CharField(max_length=40, unique=True, primary_key= True)
    a_name = models.CharField(max_length= 50,blank= True, null= True)
    a_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
    a_img = models.TextField(blank= True, null= True)
    a_phone = models.CharField(max_length= 20, blank=True, null= True)
    a_date = models.TextField(blank= True, null= True)
    a_address = models.TextField(blank= True, null= True)
    a_price = models.TextField(blank= True, null= True)
    a_organizer = models.TextField(blank= True, null= True)
    a_url = models.TextField(blank= True, null= True)
    comment = models.TextField(blank= True, null= True)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s" % (self.a_name)