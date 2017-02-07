### Portfolio Note
# This is a tool to run the google finance data capture tool every
# minute during market hours.

import os
import datetime
import time
import holidays

us_holidays = holidays.UnitedStates()

def marketopenhelp(date,daynum,hour,minute):
    
    if date in us_holidays:
        print "markets closed."
        return 0
    if daynum in range(6, 8):
        print "markets closed."
        return 0
    if hour in range (7,14):
        return 1
    if hour == 6:
        if minute > 29:
            return 1
        else:
            return 0
        
    print "markets closed."
    return 0

def marketopen():
    d = datetime.datetime.now()
    date = time.strftime("%m /%d/%Y")
    daynum = d.isoweekday()
    hour = d.hour
    minute = d.minute
    return marketopenhelp(date,daynum,hour,minute)
    
    

def timetoopen():
    d = datetime.datetime.now()
    hour = d.hour
    if hour > 8:
        waittime = ((24-hour)+5)*3600
    elif hour < 6:
        waittime = max(3600,(5-hour)*3600)
    else:
        waittime = 60
    print "waiting", waittime, "seconds"
    return waittime

while 1:
    if marketopen():
        try:
            execfile("google finance data capture sql.py")
            time.sleep(60)
        except:
            time.sleep(60)
    else:
        waittime = timetoopen()
        time.sleep(waittime)
