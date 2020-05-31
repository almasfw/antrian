# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:59:42 2020

Module for M/M/1/K queue problem.

@author: Almas Fauzia
         Gregorius Aria Neruda
         Rayhan Naufal Ramadhan
         
"""

import random
import queue
import math
import csv
import sys

# Global variables
exp_dist_lambda = 0.5

# maximum amount of customer inside queue (K-1), server is included, set to `0` if infinite
try:
    QUEUE_SIZE = int(sys.argv[1])
except IndexError:
    print("One argument is missing \n")
    print("usage: python ./MM1K.py <K> \n")
    print("- K  : maximum number of customers in queue (including customer being served) \n")
    sys.exit(1)

listOfEvents = []
custArrive = 0
custServiced = 0
time = 0
haventArrived = False
dropped = []

n = 100
i = 0


class Event:
    def __init__(self, eventType):
        self.eventType = eventType
        self.rate = CDF_inverse(random.random())
        # if eventType == arrival, rate is the time needed until the next customer arrives
        # if eventType == service, rate is the time needed for server to serve the customer that is in it


def decrease_rate(tempEvent, listOfEvents):
    for event in listOfEvents:
        event.rate -= tempEvent.rate
        # writer.writerow([f'[Time: {str(time)}] Remaining {event.eventType} time: {str(event.rate)}'])
    return listOfEvents


# function to calculate rate from exponential distribution
def CDF_inverse(CDF):
    return -1 * math.log(1-CDF) / exp_dist_lambda


# build .csv file to save the log
file = open('logMM1K.csv', 'w', newline='')
writer = csv.writer(file)

# the first customer is arriving and entering the server when the system starts
custArrive += 1
writer.writerow(
    [f'[Time: {str(time)}] Customer{str(custArrive)} is coming to the system.'])
newEvent = Event('arrival')
listOfEvents.append(newEvent)
# writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} in {str(newEvent.rate)}'])

custServiced += 1
writer.writerow(
    [f'[Time: {str(time)}] Customer{str(custServiced)} is served.'])
newEvent = Event('service')
listOfEvents.append(newEvent)
# writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} in {str(newEvent.rate)}.'])

# initialize queue
q = queue.Queue(QUEUE_SIZE)
q.put_nowait(custArrive)

while i < n:
    # take the first coming event from queue
    temp = sorted(listOfEvents, key=lambda event: event.rate, reverse=False)[0]

    j = 0
    # search for an arrival event if temp is service event but the next customer have not arrived yet
    while (temp.eventType == 'service') & (custArrive < custServiced) & (j < (len(listOfEvents)-1)):
        # writer.writerow([f'[Time: {str(time)}] Next customer have not arrived yet.'])
        haventArrived = True
        j += 1
        temp = sorted(listOfEvents, key=lambda event: event.rate)[j]

    # execute the event
    if temp.eventType == 'arrival':
        custArrive += 1
        time += temp.rate
        listOfEvents.remove(temp)
        # if the arrival happens because of other than haventArrived situation
        if not haventArrived:
            listOfEvents = decrease_rate(temp, listOfEvents)
        newEvent = Event('arrival')
        try:
            q.put_nowait(custArrive)
            writer.writerow(
                [f'[Time: {str(time)}] Customer{str(custArrive)} is coming to the system.'])

            # if there is no queue, the new customer will be straight to the server
            if custArrive == custServiced:
                writer.writerow(
                    [f'[Time: {str(time)}] Customer{str(custServiced)} is served.'])
        except Exception as e:
            writer.writerow(
                [f'[Time: {str(time)}] Queue is full, Customer{str(custArrive)} dropped.'])
            dropped.append(custArrive)
    else:
        time += temp.rate
        newEvent = Event('service')
        listOfEvents.remove(temp)
        listOfEvents = decrease_rate(temp, listOfEvents)
        if custServiced not in dropped:
            writer.writerow(
                [f'[Time: {str(time)}] Customer{str(custServiced)} is leaving.'])
            custServiced += 1
            while custServiced in dropped:
                custServiced += 1
            q.get_nowait()
            # if the next customer have arrived, the next customer is entering the server
            if q.empty():
                writer.writerow(
                    [f'[Time: {str(time)}] Customer{str(custServiced)} is served.'])

    listOfEvents.append(newEvent)
    # if (newEvent.eventType == 'arrival'):
    #     writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} in {str(newEvent.rate)}.'])
    # else:
    #     writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} in {str(newEvent.rate)}.'])
    i += 1
    haventArrived = False
