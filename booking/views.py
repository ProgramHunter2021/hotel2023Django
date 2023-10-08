from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.forms.models import model_to_dict

from .utils import *
from .models import * 
from hotelbot.RichMenu import *

# Create your views here.

# region WebSite

def index(request):
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)

@csrf_exempt
def booking(request, room_type):
    if request.method == "GET":
        rt = RoomType.objects.filter(rt_name = room_type).first()
        rt = model_to_dict(rt)
        template = get_template('booking_step1.html')
        html = template.render(locals())
        return HttpResponse(html)

def enhanced(request):
    template = get_template('enhanced.html')
    html = template.render(locals())
    return HttpResponse(html)

@csrf_exempt
def query_room(request):
    print("查詢空房")
    today_date = request.GET.get('today', '')
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')

    if today_date:
        histogram=[]
        for room_type in list(models.RoomType.objects.all()):
            histogram_unit = EmptyRoomTypeHistogram(room_type, today_date)
            histogram.append(histogram_unit)

        return render(request, 'BookingList1.html', locals())
    elif from_date and to_date:
        histogram = []
        roomTypes = models.RoomType.objects.all()
        for room_type in list(roomTypes):
            histogram_unit = EmptyRoomTypeHistogram(room_type, from_date, to_date)
            histogram.append(histogram_unit)
        return render(request,'BookingList2.html', locals())
    else:
        return render(request,'BookingList1.html', locals())

# endregion

# region LineBot Liff

def form_searchroom(request):
    template = get_template('form_searchroom.html')
    html = template.render(locals())
    return HttpResponse(html)

def openCodeScaner(request):
    template= get_template('codeScaner.html')
    html = template.render(locals())
    return HttpResponse(html)

def form_Userinfo(request):
    template = get_template('form_userinfo.html')
    html = template.render(locals())
    return HttpResponse(html)

# endregion 