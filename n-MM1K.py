# -*- coding: utf-8 -*-
"""
Created on Sat May 30 2020

Module for n*M/M/1/K queue problem, with the assumption that each queue share the same pool

@author: Almas Fauzia
         Gregorius Aria Neruda
         Rayhan Naufal Ramadhan
"""

import random
import queue
import math
import csv

# Global variables
exp_dist_lambda = 0.5

# maximum amount of customer inside queue (K-1), set to `0` if infinite
QUEUE_SIZE = 7

QUEUES = 3  # the amount of M/M/1 queues (n)
dropped = []
queues = []
servers = []

listOfEvents = []
eventsOnHold = []  # list to store events on-hold
custArrive = 0
custServiced = 0
n = 50
i = 0
time = 0
haventArrived = False

# build .csv file to save the log
file = open('logN-MM1K.csv', 'w', newline='')
writer = csv.writer(file)


class Event:
    def __init__(self, eventType, queue_label):
        self.eventType = eventType
        self.rate = CDF_inverse(random.random())
        self.queue_label = queue_label  # denotes which M/M/1
        # if eventType == arrival, rate is the time needed until the next customer arrives
        # if eventType == service, rate is the time needed for server to serve the customer that is in it


def decrease_rate(tempEvent, listOfEvents):
    for event in listOfEvents:
        event.rate -= tempEvent.rate
        # writer.writerow([f'[Time: {str(time)}] Remaining {event.eventType} time in Queue {event.queue_label}: {str(event.rate)}'])
    return listOfEvents


# function to calculate rate from exponential distribution
def CDF_inverse(CDF):
    return -1 * math.log(1-CDF) / exp_dist_lambda


def init_queue(queue_label):
    global custArrive
    global custServiced
    global time
    global n
    global i
    global listOfEvents

    i += 1
    custArrive = i
    queues[queue_label].put_nowait(custArrive)
    n -= 1
    writer.writerow([f'[Time: {str(time)}] Customer{str(custArrive)} is entering Queue {queue_label}.'])
    newEvent = Event('arrival', queue_label)
    listOfEvents.append(newEvent)
    # writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} for Queue {queue_label} in {str(newEvent.rate)}'])

    custServiced = queues[queue_label].get_nowait()
    servers[queue_label].put_nowait(custServiced)
    writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Queue {queue_label}.'])
    newEvent = Event('service', queue_label)
    listOfEvents.append(newEvent)
    # writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} for Queue {queue_label} in {str(newEvent.rate)}'])


def start_queue(queue_label, temp):
    global custArrive
    global custServiced
    global time
    global n
    global i
    global listOfEvents
    global haventArrived
    global dropped

    if temp.eventType == 'arrival':
        i += 1
        custArrive = i
        time += temp.rate
        listOfEvents.remove(temp)

        # if the arrival happens because of other than haventArrived situation
        if not haventArrived:
            listOfEvents = decrease_rate(temp, listOfEvents)
        newEvent = Event('arrival', queue_label)
        try:
            queues[queue_label].put_nowait(custArrive)
            writer.writerow([f'[Time: {str(time)}] Customer{str(custArrive)} is entering Queue {queue_label}.'])
            # if there is no queue, the new customer will be straight to the server
            if queues[queue_label].qsize() == 1 and not servers[queue_label].full():
                custServiced = queues[queue_label].get_nowait()
                servers[queue_label].put_nowait(custServiced)
                writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Queue {queue_label}.'])
        except Exception:
            writer.writerow([f'[Time: {str(time)}] Queue is full, Customer{str(custArrive)} is dropped from Queue {queue_label}.'])
            dropped.append(custArrive)
    else:
        time += temp.rate
        newEvent = Event('service', queue_label)
        listOfEvents.remove(temp)
        listOfEvents = decrease_rate(temp, listOfEvents)
        custServiced = servers[queue_label].get_nowait()
        writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is leaving Queue {queue_label}.'])
        # if the next customer have arrived, the next customer is entering the server
        if not queues[queue_label].empty():
            custServiced = queues[queue_label].get_nowait()
            servers[queue_label].put_nowait(custServiced)
            writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Queue {queue_label}.'])

    listOfEvents.append(newEvent)
    # if (newEvent.eventType == 'arrival'):
    #     writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} for Queue {queue_label} in {str(newEvent.rate)}'])
    # else:
    #     writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} for Queue {queue_label} in {str(newEvent.rate)}'])

    n -= 1
    haventArrived = False


def main():
    for i in range(QUEUES):
        queues.append(queue.Queue(QUEUE_SIZE))
        servers.append(queue.Queue(1))
        init_queue(i)

    while n > 0:
        # restore events
        for event in eventsOnHold:
            eventsOnHold.remove(event)
            listOfEvents.append(event)

        # take the first coming event from queue
        temp = sorted(listOfEvents, key=lambda event: event.rate)[0]
        # search for an arrival event if temp is service event but the next customer have not arrived yet
        while (temp.eventType == 'service') & (queues[temp.queue_label].empty()) & (servers[temp.queue_label].empty()):
            # writer.writerow([f'[Time: {str(time)}] Next customer have not arrived yet in Queue {temp.queue_label}.'])
            haventArrived = True

            eventsOnHold.append(temp)
            listOfEvents.remove(temp)
            temp = sorted(listOfEvents, key=lambda event: event.rate)[0]

        start_queue(temp.queue_label, temp)


if __name__ == '__main__':
    main()
