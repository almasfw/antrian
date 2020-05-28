# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:59:42 2020

@author: Almas Fauzia
"""

import random


class Event:
    def __init__(self, eventType):
        self.eventType = eventType
        self.rate = random.random()
        # if eventType == arrival, rate is the time needed until the next customer arrives
        # if eventType == service, rate is the time needed for server to serve the customer that is in it


def decrease_rate(tempEvent, listOfEvents):
    for event in listOfEvents:
        event.rate -= tempEvent.rate
        print(f"Remaining {event.eventType} time: {str(event.rate)}")
    return listOfEvents


listOfEvents = []
custArrive = 0
custServiced = 0
time = 0
haventArrived = False

eventBin = []
timestamp = []
eventTrack = []

# the first customer is arriving and entering the server when the system starts
custArrive += 1
print(f'Customer{str(custArrive)} datang pada detik ke {str(time)}.')
newEvent = Event('arrival')
listOfEvents.append(newEvent)
print(f'Next {newEvent.eventType} in {str(newEvent.rate)}')

custServiced += 1
print(f'Customer{str(custServiced)} masuk ke server pada detik ke {str(time)}.')
newEvent = Event('service')
listOfEvents.append(newEvent)
print(f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')

n = 10
i = 0
while i < n:
    # take the first coming event from queue
    temp = sorted(listOfEvents, key=lambda event: event.rate, reverse=False)[0]

    j = 0
    # search for an arrival event if temp is service event but the next customer have not arrived yet
    while (temp.eventType == 'service') & (custArrive < custServiced) & (j < (len(listOfEvents)-1)):
        print('Next customer have not arrived yet.')
        haventArrived = True
        j += 1
        temp = sorted(listOfEvents, key=lambda event: event.rate)[j]

    eventBin.append(temp)

    # execute the event
    if temp.eventType == 'arrival':
        custArrive += 1
        time += temp.rate
        print(f'Customer{str(custArrive)} datang pada detik ke {str(time)}.')
        newEvent = Event('arrival')
        listOfEvents.remove(temp)

        # if the arrival happens because of other than haventArrived situation
        if not haventArrived:
            listOfEvents = decrease_rate(temp, listOfEvents)

        # if there is no queue, the new customer will be straight to the server
        if custArrive == custServiced:
            print(f'Customer {str(custServiced)} masuk ke server.')
    else:
        time += temp.rate
        print(f'Customer{str(custServiced)} pergi pada detik ke {str(time)}.')
        newEvent = Event('service')
        listOfEvents.remove(temp)
        listOfEvents = decrease_rate(temp, listOfEvents)
        custServiced += 1
        # if the next customer have arrived, the next customer is entering the server
        if custArrive >= custServiced:
            print(f'Customer{str(custServiced)} masuk ke server.')

    listOfEvents.append(newEvent)
    if (newEvent.eventType == 'arrival'):
        print(f'Next {newEvent.eventType} in {str(newEvent.rate)} \n')
    else:
        print(
            f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')
    i += 1
    haventArrived = False
