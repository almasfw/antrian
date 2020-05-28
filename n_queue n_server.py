# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:59:42 2020

@author: Almas Fauzia
"""

import random
import queue
import math

QUEUE_SIZE = 7
exp_dist_lambda = 0.5


class Event:
    def __init__(self, eventType):
        self.eventType = eventType
        self.rate = CDF_inverse(random.random())
        # if eventType == arrival, rate is the time needed until the next customer arrives
        # if eventType == service, rate is the time needed for server to serve the customer that is in it


def decrease_rate(tempEvent, listOfEvents):
    for event in listOfEvents:
        event.rate -= tempEvent.rate
        print(f"Remaining {event.eventType} time: {str(event.rate)}")
    return listOfEvents


# function to calculate rate from exponential distribution
def CDF_inverse(CDF):
    return -1 * math.log(1-CDF) / exp_dist_lambda
    
def get_min_queue(queue):
    sizes = []
    for q in queue:
        size = q.qsize()
        sizes.append(size)
        
    return sizes.index(min(sizes))

servers = 3    
custArrive = [0 for i in range(servers)]
custServiced = [0 for i in range(servers)]
time = [0 for i in range(servers)]
haventArrived = False
dropped = []
listOfEvents = [[] for i in range(servers)]

# initialize queue
queues = []
for i in range(servers):
    q = queue.Queue(QUEUE_SIZE)    
    queues.append(q)

for i in range(servers):
    # the first customer is arriving and entering the server when the system starts
    custArrive[i] += 1
    print(f'Customer{str(custArrive[i])}{i+1} is coming to the queue {i+1}. Time: {str(time[i])}')
    newEvent = Event('arrival')
    listOfEvents[i].append(newEvent)
    print(f'Next {newEvent.eventType} in {str(newEvent.rate)}')
    
    custServiced[i] += 1
    print(f'Customer{str(custServiced[i])}{i+1} is served.')
    newEvent = Event('service')
    listOfEvents[i].append(newEvent)
    print(f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')


n = 6
i = 0
temp = ['' for i in range(servers)]
while i < n:
    # take the first coming event from queue
    print(f'iterations: {i+1}')
    k = i % servers
    temp[k] = sorted(listOfEvents[k], key=lambda event: event.rate, reverse=False)[0]

    j = 0
    # search for an arrival event if temp is service event but the next customer have not arrived yet
    while (temp[k].eventType == 'service') & (custArrive[k] < custServiced[k]) & (j < (len(listOfEvents[k])-1)):
        print('Next customer have not arrived yet.')
        haventArrived = True
        j += 1
        temp[k] = sorted(listOfEvents[k], key=lambda event: event.rate)[j]

    # execute the event
    if temp[k].eventType == 'arrival':
        custArrive[k] += 1
        time[k] += temp[k].rate
        listOfEvents[k].remove(temp[k])
        # if the arrival happens because of other than haventArrived situation
        if not haventArrived:
            listOfEvents[k] = decrease_rate(temp[k], listOfEvents[k])
        newEvent = Event('arrival')
        try:
            queues[k].put_nowait(custArrive[k])
            print(
                f'Customer{str(custArrive[k])}{k+1} is coming to the queue {k+1}. Time: {str(time[k])}')

            # if there is no queue, the new customer will be straight to the server
            if custArrive[k] == custServiced[k]:
                print(f'Customer{str(custServiced[k])}{k+1} is served in server {k+1}.')
        except Exception as e:
            print(
                f"Queue is full, Customer{str(custArrive[k])} dropped. Time: {str(time[k])}")
            dropped.append(custArrive[k])
    else:
        time[k] += temp[k].rate
        newEvent = Event('service')
        listOfEvents[k].remove(temp[k])
        listOfEvents[k] = decrease_rate(temp[k], listOfEvents[k])
        if custServiced[k] not in dropped:
            print(
                f'Customer{str(custServiced[k])}{k+1} is leaving the server {k+1}. Time: {str(time[k])}')
            # if the next customer have arrived, the next customer is entering the server
            if not queues[k].empty():
                custServiced[k] = queues[k].get_nowait()
                print(f'Customer{str(custServiced[k])}{k+1} is served in server {k+1}.')

    listOfEvents[k].append(newEvent)
    if (newEvent.eventType == 'arrival'):
        print(f'Next {newEvent.eventType} in {str(newEvent.rate)} \n')
    else:
        print(
            f'Next completed {newEvent.eventType} in {str(newEvent.rate)} \n')
    i += 1
    haventArrived = False
