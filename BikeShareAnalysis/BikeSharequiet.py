### I did not see a file structure attached, so I designed this to
### run in the same file as the trip_data.csv file.

import csv
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from scipy import stats as stats

start = time.clock()

### This function will return a list of dates between the given dates.
def get_date_range(date1,date2):
    datestr1 = str(date1.month) + "/" + str(date1.day) + "/" + str(date1.year)
    day1 = datetime.datetime.strptime(datestr1, "%m/%d/%Y")
    datestr2 = str(date2.month) + "/" + str(date2.day) + "/" + str(date2.year)
    day2 = datetime.datetime.strptime(datestr2, "%m/%d/%Y")
    startday = min(day1,day2)
    endday = max(day1,day2)
    daterange = []
    while startday < endday:
        daterange.append(startday)
        startday = startday + datetime.timedelta(1)
    daterange.append(endday)
    return daterange

### This is the main function that will analyse data.
def generate_report():
    k = -1
    use_by_id = {}
    round_trips = 0
    trips_by_date = {}
    weekend_trips = 0
    weekday_trips = 0
    day_dict = {}
    for j in range(1,8):
        day_dict[j] = [[],[]]

### Parse csv file and identify pertinent data from each entry
    with open('201508_trip_data.csv') as csvfile:
        data_table = csv.reader(csvfile)
        for entry in data_table:
            startTerminal = entry[4]
            endTerminal = entry[7]
            bikeID = entry[8]
            tripDuration = entry[1]

    ### collect data for most used bike
            if k > -1:
                try:
                    use_by_id[bikeID][0] = use_by_id[bikeID][0]+ \
                    float(tripDuration)
                except:
                    use_by_id[bikeID] = [float((tripDuration)),1]
                use_by_id[bikeID][1] = use_by_id[bikeID][1]+ 1

    ### collect data for number of daily trips
                startDate = datetime.datetime.strptime(entry[2], \
                                                       "%m/%d/%Y %H:%M")
                endDate = datetime.datetime.strptime(entry[5], \
                                                     "%m/%d/%Y %H:%M")
                daterange = get_date_range(startDate,endDate)
                for date in daterange:
                    try:
                        trips_by_date[date] = trips_by_date[date]+ 1
                    except:
                        trips_by_date[date] = 1
                                  
    ### collect data for prop of round trips
                if startTerminal == endTerminal:
                    round_trips = round_trips + 1
            k = k + 1

### analysis for most time and most number of rentals
    most_used_time = 0
    most_used_bike = 0
    most_rentals = 0
    most_rented_bike = 0
    for entry in use_by_id:
        if use_by_id[entry][0] > most_used_time:
            most_used_time = use_by_id[entry][0]
            most_used_bike = entry
        if use_by_id[entry][1] > most_rentals:
            most_rentals = use_by_id[entry][1]
            most_rented_bike = entry
  
### anlysis for likelihood of round trips. It is assumed that each ride
### is independent. The test is conducted with significnace level of .05. 
    pval = stats.binom_test(round_trips,k,.5)
  
### Separate trips by day of the week, count weekend vs weekday     
    for entry in trips_by_date:
        j = entry.isoweekday()
        day_dict[j][0] = day_dict[j][0] + [entry]
        day_dict[j][1] = day_dict[j][1] + [trips_by_date[entry]]
    for j in range(1,6):
        for i in day_dict[j][1]:
            weekday_trips = weekday_trips + i
    for j in range(6,8):
        for i in day_dict[j][1]:
            weekend_trips = weekend_trips + i    

### Display Graph of number of trips by date, 
### different makers for different days of the week
    fig = plt.figure()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', \
            'Saturday', 'Sunday']
    icons = ['g^', 'b^', 'm^', 'r^', 'y^', 'ko', 'co']
    for j in range (1,8):
        plt.plot(day_dict[j][0], day_dict[j][1], \
                 icons[j-1] , label = days[j-1])
    plt.legend(bbox_to_anchor=(0., 1., 1., .01), loc=3, ncol=4, \
                 mode="expand", borderaxespad=0.)
    plt.show()
    fig.savefig("BikeShareRidersByDay.png")
    plt.close()

    end = time.clock()

    print "Bike used for longest time:", most_used_bike 
    print "Bike rented most:", most_rented_bike  
    print "Chance one way and round trip are equally likely:", pval
    print "Run time:", end - start

generate_report()