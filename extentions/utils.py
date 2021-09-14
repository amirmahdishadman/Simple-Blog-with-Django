from . import jalali
from django.utils import timezone



def persian_number_converter(mystr):
    numbers={
        "0":"۰",
        "1":"۱",
        "2":"۲",
        "3":"۳",
        "4":"۴",
        "5":"۵",
        "6":"۶",
        "7":"۷",
        "8":"۸",
        "9":"۹",
    }
    for e,p in numbers.items():
        mystr = mystr.replace(e,p)
    return mystr







def jalali_converter(time):
    time=timezone.localtime(time)
    month={
        "1":"فروردین",
        "2":"اردیبهشت",
        "3":"خرداد",
        "4":"تیر",
        "5":"مرداد",
        "6":"شهریور",
        "7":"مهر",
        "8":"آبان",
        "9":"آذر",
        "10":"دی",
        "11":"بهمن",
        "12":"اسفند" ,  
    }
    min=time.minute
    if(int(time.minute))<10:
        min="0"+str(time.minute)


    h=time.hour
    if(int(time.hour))<10:
        h="0"+str(time.hour)


    time_to_str="{},{},{}".format(time.year,time.month,time.day)
    time_to_tuple=jalali.Gregorian(time_to_str).persian_tuple()
    output="{} {} {}, ساعت {}:{}".format(
    time_to_tuple[2],
    month[str(time_to_tuple[1])],
    time_to_tuple[0],
    h,
    min
    )
    return persian_number_converter(output)