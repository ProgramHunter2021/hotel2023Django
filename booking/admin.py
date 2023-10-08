from django.contrib import admin
from .models import *
from linebot.models import *
# Register your models here.

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('rt_id', 'rt_name', 'rt_price')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('r_id', 'r_type')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('o_id', 'o_user')

@admin.register(BookingRoom)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('order', 'room', 'booked_date')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('t_number', 't_amount', 't_method', 't_date', 't_status', 'order')