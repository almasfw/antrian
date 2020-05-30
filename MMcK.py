# -*- coding: utf-8 -*-
"""
Created on Sat May 30 2020

Module for M/M/c/K queue problem.

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

SERVERS = 3  # the amount of servers (c)
dropped = []
servers = []

listOfEvents = []
eventsOnHold = []  # list to store events on-hold
custArrive = 0
custServiced = 0
n = 150
i = 0
time = 0
haventArrived = False

# build .csv file to save the log
file = open('logMMcK.csv', 'w', newline='')
writer = csv.writer(file)


class Event:
    def __init__(self):
        self.eventType = None
        self.rate = CDF_inverse(random.random())
        self.server_label = None  # denotes which server

    def arrival(self):
        self.eventType = 'arrival'

    def service(self, server_label):
        self.eventType = 'service'
        self.server_label = server_label
        # if eventType == arrival, rate is the time needed until the next customer arrives
        # if eventType == service, rate is the time needed for server to serve the customer that is in it


def decrease_rate(tempEvent, listOfEvents):
    for event in listOfEvents:
        if event.eventType == 'arrival' or (event.eventType == 'service' and not servers[event.server_label].empty()):
            event.rate -= tempEvent.rate
        # if event.eventType == 'arrival':
        #     writer.writerow([f'[Time: {str(time)}] Remaining {event.eventType} time in Queue: {str(event.rate)}'])
        # else:
        #     writer.writerow([f'[Time: {str(time)}] Remaining {event.eventType} time in Server {str(event.server_label)}: {str(event.rate)}'])
    return listOfEvents


# function to calculate rate from exponential distribution
def CDF_inverse(CDF):
    return -1 * math.log(1-CDF) / exp_dist_lambda


def init_queue(q, server_label):
    global custArrive
    global custServiced
    global time
    global n
    global i
    global listOfEvents

    i += 1
    custArrive = i
    q.put_nowait(custArrive)
    n -= 1
    writer.writerow([f'[Time: {str(time)}] Customer{str(custArrive)} is entering the queue.'])
    newEvent = Event()
    newEvent.arrival()
    listOfEvents.append(newEvent)
    # writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} in {str(newEvent.rate)}'])

    custServiced = q.get_nowait()
    servers[server_label].put_nowait(custServiced)
    writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Server {server_label}.'])
    newEvent = Event()
    newEvent.service(server_label)
    listOfEvents.append(newEvent)
    # writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} for Server {server_label} in {str(newEvent.rate)}'])


def start_queue(q, server_label, temp):
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
        newEvent = Event()
        newEvent.arrival()
        try:
            q.put_nowait(custArrive)
            writer.writerow([f'[Time: {str(time)}] Customer{str(custArrive)} is entering the queue.'])
            # if there is no queue, find empty server
            for server_label in range(len(servers)):
                if q.qsize() == 1 and not servers[server_label].full():
                    custServiced = q.get_nowait()
                    servers[server_label].put_nowait(custServiced)
                    writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Server {server_label}.'])
                    break
        except Exception as e:
            writer.writerow([f'[Time: {str(time)}] Queue is full, Customer{str(custArrive)} is dropped from Queue.'])
            dropped.append(custArrive)
    else:
        time += temp.rate
        newEvent = Event()
        newEvent.service(server_label)
        listOfEvents.remove(temp)
        listOfEvents = decrease_rate(temp, listOfEvents)
        custServiced = servers[server_label].get_nowait()
        writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is leaving Server {server_label}.'])
        # if the next customer have arrived, the next customer is entering the server
        if not q.empty():
            custServiced = q.get_nowait()
            servers[server_label].put_nowait(custServiced)
            writer.writerow([f'[Time: {str(time)}] Customer{str(custServiced)} is being served in Server {server_label}.'])

    listOfEvents.append(newEvent)
    # if (newEvent.eventType == 'arrival'):
    #     writer.writerow([f'[Time: {str(time)}] Next {newEvent.eventType} in {str(newEvent.rate)}'])
    # else:
    #     writer.writerow([f'[Time: {str(time)}] Next completed {newEvent.eventType} for Server {server_label} in {str(newEvent.rate)}'])

    n -= 1
    haventArrived = False


def main():
    q = queue.Queue(QUEUE_SIZE)
    for i in range(SERVERS):
        servers.append(queue.Queue(1))
        init_queue(q, i)

    while n > 0:
        # restore events
        for event in eventsOnHold:
            eventsOnHold.remove(event)
            listOfEvents.append(event)

        # take the first coming event from queue
        temp = sorted(listOfEvents, key=lambda event: event.rate)[0]
        # search for an arrival event if temp is service event but the next customer have not arrived yet
        while (temp.eventType == 'service'):
            if (q.empty()) & (servers[temp.server_label].empty()):
                # writer.writerow([f'[Time: {str(time)}] Next customer have not arrived yet in Queue.'])
                haventArrived = True

                eventsOnHold.append(temp)
                listOfEvents.remove(temp)
                temp = sorted(listOfEvents, key=lambda event: event.rate)[0]
            else:
                break

        start_queue(q, temp.server_label, temp)


if __name__ == '__main__':
    main()
