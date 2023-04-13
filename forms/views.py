from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from .models import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Create your views here.


def make_string_date(date, hours, minutes, ampm):
    output = ""
    if ampm == "PM":
        hours += 12
    else:
        if len(str(hours)) != 2:
            hours = "0" + str(hours)
    output = str(date)[0:10] + " " + str(hours) + \
        ":" + str(minutes) + ":00"
    return output


def take_end_date(date_string, hours, minutes):
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    adjust = timedelta(hours=hours, minutes=minutes)
    adjusted_date = date+adjust
    return str(adjusted_date)


# base
def get_multiple_days(date_string, days, limit):
    # print(limit)
    output = []
    DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    output.append(str(date))
    one_day = timedelta(days=1)
    if (len(output) == limit):
        return output
    while (True):
        for DAY in DAYS:
            date = date + one_day
            for day in days:
                if DAY == day:
                    output.append(str(date))
                    if (len(output) == limit):
                        return output


# by date date
def get_multiple_days_end(date_string, days, limit_date, recur_options):
    output = []
    adjust = timedelta(hours=23, minutes=59, seconds=59)
    limit_date = limit_date+adjust
    # print(days)
    DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    date = datetime.strptime(
        date_string, "%Y-%m-%d  %H:%M:%S").replace(tzinfo=None)
    output.append(str(date))
    one_day = timedelta(days=1)
    # print(limit_date)
    # print(date)
    if ((limit_date-date).days < 0):
        return output
    if (recur_options == "daily"):
        while (True):
            date = date+one_day
            if ((limit_date-date).days < 0):
                # print(limit_date-date)
                return output
            else:
                output.append(str(date))
    elif (recur_options == "weekly"):
        while (True):
            date = date+one_day
            # print("date: " + str(date))
            i = date.weekday()
            if (DAYS[i] in days):
                if ((limit_date-date).days < 0):
                    # print(limit_date-date)
                    return output
                else:
                    output.append(str(date))
    elif (recur_options == "biweekly"):
        date_added_counter = DAYS.index(date.strftime("%a").lower())+2
        print("day: " + date.strftime("%a").lower())
        print("initial dac: " + str(date_added_counter))
        skip_week = False
        while (True):
            date = date+one_day
            print("date do be processed: " + str(date))
            i = date.weekday()
            if (date_added_counter > 6):
                if (skip_week):
                    skip_week = False
                else:
                    skip_week = True
                date_added_counter = 0
            print("dac: " + str(date_added_counter))
            print("skip week: " + str(skip_week))
            if ((DAYS[i] in days) and not (skip_week)):
                if ((limit_date-date).days < 0):
                    # print(limit_date-date)
                    return output
                else:
                    output.append(str(date))
            date_added_counter += 1
    else:  # if Monthly
        one_month = relativedelta(months=1)
        while (True):
            date = date+one_month
            if ((limit_date-date).days < 0):
                # print(limit_date-date)
                return output
            else:
                output.append(str(date))


# by occurence
def get_multiple_days_occur(date_string, days, limit_occur, recur_options):
    # print(limit_occur)
    output = []
    DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    output.append(str(date))
    one_day = timedelta(days=1)
    if (len(output) == limit_occur):
        return output
    if (recur_options == "daily"):
        print("Daily, limit=" + str(limit_occur))
        for i in range(limit_occur-1):
            date = date+one_day
            output.append(str(date))
            print("Added: " + str(date))
        return output
    elif (recur_options == "weekly"):
        while (True):
            date = date+one_day
            i = date.weekday()
            if (DAYS[i] in days):
                if (len(output) == limit_occur):
                    return output
                else:
                    output.append(str(date))
    elif (recur_options == "biweekly"):
        date_added_counter = DAYS.index(date.strftime("%a").lower())+2
        # print("day: " + date.strftime("%a").lower())
        # print("initial dac: " + str(date_added_counter))
        skip_week = False
        while (True):
            date = date+one_day
            i = date.weekday()
            if (date_added_counter > 6):
                if (skip_week):
                    skip_week = False
                else:
                    skip_week = True
                date_added_counter = 0
            if ((DAYS[i] in days) and not (skip_week)):
                if (len(output) == limit_occur):
                    return output
                else:
                    output.append(str(date))
            date_added_counter += 1
    else:  # monthly
        one_month = relativedelta(months=1)
        for i in range(limit_occur-1):
            date = date+one_month
            output.append(str(date))
        return output


def calculate_limit_by_date(start, end, days):
    limit = 0
    # start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    # end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    # result = end_date-start_date
    result = end-start
    limit = result.days + 1

    return limit

#
# def calculate_limit_by_occur(days, start, occurences):
#    limit = 0
#    limit = int(occurences/len(days))
#    # print("occur/len = " + str(limit))
#    DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
#    start_date_weekday = DAYS[start.weekday()]
#    if start_date_weekday not in DAYS:
#        # print("added 1 to limit")
#        limit += 1
#    return limit


def db_string_to_datetimearray(str):
    output = []
    temp = str.split(",")
    for date in temp:
        print(date)
        output.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return output


def index(request):
    if request.method == 'POST':
        if ('button1' in request.POST):
            print("Hello")
            dates = Testz.objects.get(id=4).start_date_string_array
            print(dates)
            datetimes = db_string_to_datetimearray(dates)
            form = AddressFormModel(request.POST)
            print(datetimes)
        else:
            form = AddressFormModel(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data.get("start_date")
                start_hours = int(form.cleaned_data.get("start_hour"))
                start_minutes = form.cleaned_data.get("start_minute")
                duration_hours = form.cleaned_data.get("duration_hour")
                duration_minutes = form.cleaned_data.get("duration_minute")
                ampm = form.cleaned_data.get("ampm")
                start_str = make_string_date(
                    start_date, start_hours, start_minutes, ampm)
                end_str = take_end_date(
                    start_str, int(duration_hours), int(duration_minutes))
                form.date_string = start_str

                recur_check = form.cleaned_data.get("recur_check")
                if (recur_check):
                    sun = form.cleaned_data.get("sun")
                    mon = form.cleaned_data.get("mon")
                    tue = form.cleaned_data.get("tue")
                    wed = form.cleaned_data.get("wed")
                    thu = form.cleaned_data.get("thu")
                    fri = form.cleaned_data.get("fri")
                    sat = form.cleaned_data.get("sat")
                    recur_days = []
                    if (sun):
                        recur_days.append("sun")
                    if (mon):
                        recur_days.append("mon")
                    if (tue):
                        recur_days.append("tue")
                    if (wed):
                        recur_days.append("wed")
                    if (thu):
                        recur_days.append("thu")
                    if (fri):
                        recur_days.append("fri")
                    if (sat):
                        recur_days.append("sat")

                    recur_options = form.cleaned_data.get("recur_options")
                    end_date_check = form.cleaned_data.get("end_date_check")
                    occurences_check = form.cleaned_data.get(
                        "occurences_check")
                    limit = 0
                    multiple_start = []
                    multiple_end = []

                    if (end_date_check):
                        end_recur_date = form.cleaned_data.get("end_date")
                        # limit = calculate_limit_by_date(start_date, end_recur_date)
                        multiple_start = get_multiple_days_end(
                            start_str, recur_days, end_recur_date.replace(tzinfo=None), recur_options)
                        multiple_end = get_multiple_days_end(
                            end_str, recur_days, end_recur_date.replace(tzinfo=None), recur_options)

                    elif (occurences_check):
                        occurences = form.cleaned_data.get("occurences")
                        # limit = calculate_limit_by_occur(
                        #    recur_days, start_date, int(occurences))
                        limit = int(occurences)
                        limit_occur = int(occurences)
                        multiple_start = get_multiple_days_occur(
                            start_str, recur_days, limit_occur, recur_options)
                        multiple_end = get_multiple_days_occur(
                            end_str, recur_days, limit_occur, recur_options)

                    # multiple_start = get_multiple_days(
                    #    start_str, recur_days, limit)
                    # multiple_end = get_multiple_days(
                    #    end_str, recur_days, limit)
                # db_entry = Testz()
                # db_entry.start_date_string_array = ','.join(multiple_start)
                # db_entry.end_date_string_array = ','.join(multiple_end)
                # db_entry.recur_check = form.cleaned_data.get('recur_check')
                # db_entry.save()
                if (recur_check):
                    return render(request, 'home.html',
                                  {'form': form,
                                   'recur_check': recur_check,
                                   'multiple_start': multiple_start,
                                   'multiple_end': multiple_end,
                                   'multiple_dates': zip(multiple_start, multiple_end, range(1, 1+len(multiple_start)))})
                return render(request, 'home.html',
                              {'form': form,
                               'recur_check': recur_check,
                               'start_str': start_str,
                               'end_str': end_str})
    else:
        form = AddressFormModel()

    return render(request, 'home.html', {'form': form})
