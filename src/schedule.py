#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 13:09:36 2018

@author: fuadaghazada
"""

import datetime

class Scheduler:

    def __init__(self, sch_day, sch_month, sch_year, sch_hour, sch_min):

        self.sch_state = False

        self.sch_day = sch_day
        self.sch_month = sch_month
        self.sch_year = sch_year

        self.sch_hour = sch_hour
        self.sch_min = sch_min

        self.sch_date = datetime.date(self.sch_year, self.sch_month, self.sch_day)

        self.sch_time = datetime.time(self.sch_hour, self.sch_min)

    def start(self):

        if self.sch_state == False:
            self.sch_state = True

    def stop(self):

        if self.sch_state == True:
            self.sch_state = False

    def check(self):

        # 0 - passed
        # 1 - in time
        # 2 - continue

        if self.sch_state == True:
            if self.sch_date > self.currentDate():

                return 2

            elif self.sch_date == self.currentDate():

                if self.sch_time > self.currentTime():
                    return 2
                elif self.sch_time.hour == self.currentTime().hour and self.sch_time.minute == self.currentTime().minute:

                    self.stop()

                    return 1
                else:
                    return 0

            else:
                return 0

    def hasTimeArrived(self):
        return self.check() == 1

    def hasTimePassed(self):
        return self.check() == 0

    def timeContinue(self):
        return self.check() == 2

    def currentDate(self):

        current_date_time = datetime.datetime.now()

        day = current_date_time.day
        month = current_date_time.month
        year = current_date_time.year

        return datetime.date(year, month, day)

    def currentTime(self):

        current_date_time = datetime.datetime.now()

        hours = current_date_time.hour
        minutes = current_date_time.minute
        seconds = current_date_time.second

        return datetime.time(hours, minutes, seconds)
