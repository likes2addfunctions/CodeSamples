# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 17:37:34 2018

@author: g
"""

import random
import csv

## gets event titles from google form csv export
def getEvents(row):
    events = []
    for i in range(4):
        question = row[i+2]
        startInd = question.find("[")
        endInd = question.find("]")
        event = question[startInd+1:endInd]
        events.append(event)
    return events
    
## builds dictionary of staff preferences from google form csv export
def getStaffPrefsFromCSV(CSVPath):
    staffPrefs = {}
    with open(CSVPath) as csvFile:
        csvreader = csv.reader(csvFile)
        rowCount = 0
        for row in csvreader:
            if rowCount == 0:
                events = getEvents(row)
                rowCount += 1
            else:
                name = row[1]
                prefs = {}
                for i in range(4):
                    prefs[events[i]] = int(row[i+2])
                staffPrefs[name] = prefs
    return(staffPrefs)

## returns events in order of most requested.
def orderEvents(staff):
    eventCounts = {}
    for member in staff:
        prefs = staff[member]
        for event in prefs:
            rank = prefs[event]
            if event in eventCounts:
                eventCounts[event] = eventCounts[event] + rank
            else:
                eventCounts[event] = rank
    return(sorted(eventCounts, key = lambda x : eventCounts[x]))

## returns a list of all staff 
def getStaffForEventAndRank(staff,event,rank,assignmentCounts,maxAssignments):
    rankPool = []
    for member in staff:
        if staff[member][event] == rank:
            if member in assignmentCounts:
                #print(member,assignmentCounts[member])
                if assignmentCounts[member] < maxAssignments:
                    rankPool.append(member)
                else:
                    1
                    #print("x", member)
            else:
                rankPool.append(member)
    return(rankPool)
    
## returns segments of staffPool by number of assignments.
def segmentStaffPoolByNumOfAssignments(staffPool, assignmentCounts, maxAssignments):
    segments = []
    for i in range(maxAssignments):
        segment = []
        for member in staffPool:
            if member in assignmentCounts:
                if assignmentCounts[member] == i:
                    segment.append(member)
                else:
                    pass
            elif i == 0:
                segment.append(member)
        segments.append(segment)
    return segments
                
def assignEvents(staff,events,maxAssignments):
    ## dictionary to keep track of how many duties have been assigned to any staff member 
    assignmentCounts = {}
    def updateAssignmentCounts(cand):
        if cand in assignmentCounts:
            assignmentCounts[cand] += 1
        else:
            assignmentCounts[cand] = 1
    
    ## dictionary to keep track of even assignments
    assignments = {}
    
    ##Assign staff to most popular events first
    orderedEvents = orderEvents(staff)
    for event in orderedEvents:
        
        ##number of staff needed for event
        numStaff = events[event]
        
        assignedStaff = []
        staffPool = []
        rank = 1
        ##make pool 
        #for rank in range (len(events)+1):
        while numStaff > 0 and rank < len(events)+1:
            
            ## get staff who ranked event at current rank
            bigstaffPool = getStaffForEventAndRank(staff,event,rank,assignmentCounts,maxAssignments)
            ## break up by number of events already assigned
            segments = segmentStaffPoolByNumOfAssignments(bigstaffPool,assignmentCounts,maxAssignments)
            ## add staff to event assignment list starting with least events already assigned
            for staffPool in segments:
            # if less or equal to number of staff than needed for event add all to duty list and adjust num of staff needed
                if len(staffPool) <= numStaff:
                    for member in staffPool:
                        if not member in assignedStaff:
                            updateAssignmentCounts(member)
                            assignedStaff.append(member)
                    numStaff = numStaff - len(staffPool)
            ## if more staff than needed pick randomly 
                elif len(staffPool) > numStaff and numStaff > 0:
                    for k in range(numStaff):
                        randind = random.randrange(len(staffPool))
                        cand = staffPool.pop(randind)
                        if not cand in assignedStaff:
                            assignedStaff.append(cand)
                            updateAssignmentCounts(cand)
                    numStaff = 0
            rank += 1
            #print(assignedStaff)
                    
            
        assignments[event]= assignedStaff
    print(assignmentCounts)
    return(assignments)
    
def writeAssignmentsToCSV(assignments):
    with open ("AdjuntDuties.csv", 'w') as csvFile:
        csvwriter = csv.writer(csvFile)
        for event in assignments:
            eventAssignment = [event] + assignments[event]
            csvwriter.writerow(eventAssignment)
        
    
if __name__ == "__main__":
    ##key = event name, val = num of staff required for event
    events = {"dance":2, "game":4,"show": 2, "play":1}
#    
#    ##key = event name, val = prefrence of duty
#    sue =  {"dance":4, "game":1,"show": 2, "play":3}
#    john = {"dance":4, "game":1,"show": 2, "play":3}
#    mike = {"dance":4, "game":1,"show": 2, "play":3}
#    jill = {"dance":1, "game":3,"show": 4, "play":2}
#    
#    staff = {"sue":sue,"john":john,"mike":mike,"jill":jill}
    csvPath = "Adjunct Duty Sign Up (Responses) - Form Responses 1(1).csv"
    
    staff = getStaffPrefsFromCSV(csvPath)

    assignments = assignEvents(staff,events,3)
    for event in assignments:            
        print(event, assignments[event])
    writeAssignmentsToCSV(assignments)
    
                
        
    