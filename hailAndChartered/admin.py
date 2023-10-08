from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import hailOption, charteredOption, chartered_order

class hailOptionAdmin(ImportExportModelAdmin):
    list_display = ('id','agencyName','agencyNumber','agencyUrl','imgUrl','onOff',)
    ordering = ('id',)

class charteredOptionAdmin(ImportExportModelAdmin):
    list_display = ('id','carType','carImgUrl','chtdStartPrice','chtdAlldayPrice',\
                    'timeOutPrice','onOff',)
    ordering = ('id',)

class charteredOrderAdmin(ImportExportModelAdmin):
    list_display = ('id','pub_datetime','userId','appointmentDate','carType','passengerAmount',\
                    'chtd_time','total_cost','questNote', 'transaction_id','paid')
    ordering = ('id',)

admin.site.register(hailOption, hailOptionAdmin)
admin.site.register(charteredOption, charteredOptionAdmin)
admin.site.register(chartered_order, charteredOrderAdmin)