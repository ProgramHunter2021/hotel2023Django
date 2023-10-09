from .models import *
import time
import datetime

class MyDateTime:
    def __init__(self, yyyy_mm_dd):
        year, month, day = yyyy_mm_dd.split('-')
        self.main_datetime = datetime.datetime(int(year), int(month), int(day))

    def date(self):
        return self.main_datetime.date()

    def date_time(self):
        return self.main_datetime

    def time(self):
        return self.main_datetime.time()

    def add_day(self, day_num):
        return self.main_datetime + datetime.timedelta(days=day_num)

    # 取得天數
    def comprise_between(self, bound_my_datetime):
        return abs((bound_my_datetime.main_datetime - self.main_datetime).days)+1
    
    print(comprise_between)

    # 取得整列, 開始日期到結束日期的所有日期, 不包含結束日期
    def comprise_everyday(self, bound_my_datetime):
        everyday_list=[]
        for day_counter in range(self.comprise_between(bound_my_datetime)):
            curr_datetime = self.add_day(day_counter)
            everyday_list.append(curr_datetime.date())
        return everyday_list

    print(comprise_everyday)

    def __str__(self):
        return str(self.main_datetime)

# region 房間查詢Class

class EmptyRoomTypeHistogram:
    def __total_room_num(self):
        target_room_type = RoomType.objects.filter(rt_name=self.room_type_name).first()
        return len(Room.objects.filter(r_type=target_room_type))

    def __curr_booking_room_list(self):
        target_room_type = RoomType.objects.get(rt_name=self.room_type_name)
        target_rooms = Room.objects.filter(r_type=target_room_type)
        from_datetime = self.from_date.date_time()
        to_datetime = self.to_date.date_time()
        return BookingRoom.objects.filter(room__in=target_rooms, booked_date__range=(from_datetime, to_datetime))

    def __init__(self, room_type, str_from_date='', str_to_date=''):
        self.limit_days = 100
        if str_from_date and not str_to_date:
            self.room_type_id = room_type.rt_id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_from_date)

            self.histogram = 0
            self.histogram = self.__total_room_num()

            for curr_booking in self.__curr_booking_room_list():
                self.histogram -= 1
                if self.histogram < 0:
                    self.histogram = 0

        elif str_from_date and str_to_date:
            self.room_type_id = room_type.rt_id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_to_date)

            self.curr_range_days = abs(self.from_date.comprise_between(self.to_date))
            if self.curr_range_days > self.limit_days:
                return
            #initial
            range_days = self.from_date.comprise_everyday(self.to_date)

            self.histogram = {}
            for everyday in range_days:
                self.histogram[everyday.year] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month][everyday.day] = self.__total_room_num()

            #set value
            for curr_booking in self.__curr_booking_room_list():
                year  = curr_booking.over_night_date.year
                month = curr_booking.over_night_date.month
                day   = curr_booking.over_night_date.day

                if year in self.histogram and month in self.histogram[year] and day in self.histogram[year][month]:
                    self.histogram[year][month][day] -= 1
                    if self.histogram[year][month][day] < 0:
                       self.histogram[year][month][day] = 0

class BookingUnit:
    #room:yyyy_mm_dd:yyyy_mm_dd
    def __init__(self, str_room_from_data_to_data):
        print(str_room_from_data_to_data)
        self.roomtype_id, from_date, to_date = str_room_from_data_to_data.split(':')
        self.from_datetime = MyDateTime(from_date)
        print(self.from_datetime)
        self.to_datetime = MyDateTime(to_date)
        print(self.to_datetime)

    def total_day(self):
        return self.from_datetime.comprise_between(self.to_datetime)

    def every_night(self):
        return self.from_datetime.comprise_everyday(self.to_datetime)

def getFreeRoom(str_roomtype, str_from_date='', str_to_date=''):
    lst_free_room = []
    lst_Booked = []
    from_date = MyDateTime(str_from_date)
    to_date = MyDateTime(str_to_date)
    if from_date.comprise_between(to_date) == 1:
        lst_Booked = BookingRoom.objects.filter(booked_date = str_from_date).all()
    else:
        lst_Booked = BookingRoom.objects.filter(booked_date__in = from_date.comprise_everyday(to_date)).all()
    print(lst_Booked)
    
    all_rooms_of_type = Room.objects.filter(r_type__rt_name = str_roomtype).all()
    lst_booked_room = []
    if not lst_Booked:
        return all_rooms_of_type
    else:
        for booked in lst_Booked:
            lst_booked_room.append(booked.room)
        for room in all_rooms_of_type:
            if room in lst_booked_room:
                continue
            else:
                lst_free_room.append(room)
        return lst_free_room

# endregion