### I did not see a file structure attached, so I designed this to
### run in the same file as the trip_data.csv file.

import csv
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

start = time.clock()

def get_date_range(date1,date2):
    datestr1 = str(date1.month) + "/" + str(date1.day) + "/" + str(date1.year)
    day1 = datetime.datetime.strptime(datestr1, "%m/%d/%Y")
    datestr2 = str(date2.month) + "/" + str(date2.day) + "/" + str(date2.year)
    day2 = datetime.datetime.strptime(datestr2, "%m/%d/%Y")
    if day1 == day2:
        return [day1]
    if day1 < day2:
        start = day1
        end = day2
    else:
        start = day2
        end = day1
    daterange = []
    while start < end:
        daterange.append(start)
        start = start + datetime.timedelta(1)
    daterange.append(end)
    return daterange

def generate_report():
    k = -1
    bike_durations = {}
    bike_rentals = {}
    round_trips = 0
    trips_by_date = {}
    weekend_trips = 0
    weekday_trips = 0
    day_dict = {}
    for j in range(1,8):
        day_dict[j] = [[],[]]
    with open('201508_trip_data.csv') as csvfile:
        data_table = csv.reader(csvfile)
        for entry in data_table:
            startTerminal = entry[4]
            endTerminal = entry[7]
            bikeID = entry[8]
            tripDuration = entry[1]

## collect data for most use bike
            if k > -1:

                try:
                    bike_durations[bikeID] = bike_durations[bikeID]+ float(tripDuration)
                except:
                    bike_durations[bikeID] = float((tripDuration))
                try:
                    bike_rentals[bikeID] = bike_rentals[bikeID]+ 1
                except:
                    bike_rentals[bikeID] = 1

## collect data for number of daily trips
                startDate = datetime.datetime.strptime(entry[2], "%m/%d/%Y %H:%M")
                endDate = datetime.datetime.strptime(entry[5], "%m/%d/%Y %H:%M")
                daterange = get_date_range(startDate,endDate)
                for date in daterange:
                    try:
                        trips_by_date[date] = trips_by_date[date]+ 1
                    except:
                        trips_by_date[date] = 1
                    

                
## collect data for prop of round trips
                if startTerminal == endTerminal:
                    round_trips = round_trips + 1
            k = k + 1

### analysis for most bike time used
    most_used_time = 0
    most_used_bike = 0
    for entry in bike_durations:
        if bike_durations[entry] > most_used_time:
            most_used_time = bike_durations[entry]
            most_used_bike = entry
    print "Bike number ", most_used_bike, " saw the most use at ", most_used_time, " seconds."
    most_rentals = 0
    most_rented_bike = 0
    for entry in bike_rentals:
        if bike_rentals[entry] > most_rentals:
            most_rentals = bike_rentals[entry]
            most_rented_bike = entry
    print "Bike number ", most_rented_bike, " saw the most rentals at ", most_rentals, " rentals."

### anlysis for likelihood of round trips. It is assumed that each ride is independent and that the sample size is over 1000 rides,
### with at least this many rides the sampling distribution is essentially normal and using the test statistic cutoff of +/- 3
### corresponds to a significnace level of about .05. 
    rtProp = float(round_trips)/k
    testStat = (rtProp - .5)/(np.sqrt(.5 *(1-.5)/k))
    if abs(testStat) > 3:
        if rtProp < .5:
            print "Riders are significantly more likely to not make round trips"
        else:
            print "Riders are significantly more likely to make round trips"
            
    else:
        print "This data does not reflect a significant difference preference of round to one-way trips"
    print "Round trips were made ", rtProp * 100, " percent of the time"
    print "for a test statistic of ", testStat

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
    print "there were ", weekend_trips, " trips taken on the weekend and ", weekday_trips, " trips taken on the weekdays."

###Display Graph of number of trips by date, different makers for different days of the week

    fig = plt.figure()
    Monday = plt.plot(day_dict[1][0],day_dict[1][1], 'g^', label = 'Monday')
    Tuesday = plt.plot(day_dict[2][0],day_dict[2][1], 'b^', label = 'Tuesday')
    Wednesday = plt.plot(day_dict[3][0],day_dict[3][1], 'm^', label = 'Wednesday')
    Thursday = plt.plot(day_dict[4][0],day_dict[4][1], 'r^', label = 'Thursday')
    Friday = plt.plot(day_dict[5][0],day_dict[5][1], 'y^', label = 'Friday')
    Saturday = plt.plot(day_dict[6][0],day_dict[6][1], 'ko', label = 'Saturday')
    Sunday = plt.plot(day_dict[7][0],day_dict[7][1], 'co', label = 'Sunday')
    plt.legend(bbox_to_anchor=(0., 1., 1., .01), loc=3, ncol=4, mode="expand", borderaxespad=0.)
    end = time.clock()
    print end - start
    plt.show()
    fig.savefig("RidersByDay.png")
    plt.close()



            

    
    

generate_report()

end = time.clock()
print end - start


### Further Analysis:

### Difference in round trips:  There appears to be a very significant difference in the likelihood of riders to make round-trips.
### In particular they are much less likely to not make round trips. This is likely due to people using the bikes for commute
### rather than for pleasure.

### Difference in Weekday vs. Weekend Usage: The data shows that almot 3.5 times as many bikes are used on weekdays than on weekends.
### This further supports the idea that these bikes are mainly being used for commute, presumably to and from work. 

### Business Ramifications: It would be useful to increase business on the weekends and/or encourage riders to use the bikes for
### pleasure riding/excercise as well as for the commute they already use them for.  One solution might be to advertise and offer "nicer"
### touring or mountin bikes that people could rent, perhaps for a slightly higher price. 










    


