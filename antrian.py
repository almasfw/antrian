# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:59:42 2020

@author: Almas Fauzia
"""

import random
import queue

QUEUE_SIZE = 7


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
dropped = []

# the first customer is arriving and entering the server when the system starts
custArrive += 1
print(f'Customer{str(custArrive)} is coming to the system. Time: {str(time)}')
newEvent = Event('arrival')
listOfEvents.append(newEvent)
print(f'Next {newEvent.eventType} in {str(newEvent.rate)}')

custServiced += 1
print(f'Customer{str(custServiced)} is served.')
newEvent = Event('service')
listOfEvents.append(newEvent)
print(f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')

# initialize queue
q = queue.Queue(QUEUE_SIZE)

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
            print(
                f'Customer{str(custArrive)} is coming to the system. Time: {str(time)}')

            # if there is no queue, the new customer will be straight to the server
            if custArrive == custServiced:
                print(f'Customer{str(custServiced)} is served.')
                q.get_nowait()
        except Exception as e:
            print(
                f"Queue is full, Customer{str(custArrive)} dropped. Time: {str(time)}")
            dropped.append(custArrive)
    else:
        time += temp.rate
        newEvent = Event('service')
        listOfEvents.remove(temp)
        listOfEvents = decrease_rate(temp, listOfEvents)
        if custServiced not in dropped:
            print(
                f'Customer{str(custServiced)} is leaving. Time: {str(time)}')
            # if the next customer have arrived, the next customer is entering the server
            if not q.empty():
                custServiced = q.get_nowait()
                print(f'Customer{str(custServiced)} is served.')

    listOfEvents.append(newEvent)
    if (newEvent.eventType == 'arrival'):
        print(f'Next {newEvent.eventType} in {str(newEvent.rate)} \n')
    else:
        print(
            f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')
    i += 1
    haventArrived = False
