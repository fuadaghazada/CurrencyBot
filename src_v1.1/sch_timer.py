#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 10:53:04 2018

@author: fuadaghazada
"""

from time import sleep


def setTimer(seconds):

    countdown = seconds
    original = countdown
    m = 0

    while countdown >= 60:

        countdown -= 60
        m += 1

    for i in range (original,0,-1):
        if m < 0:
            break
        for i in range(countdown,-2,-1):
            if i % 60 == 0:
                m-=1
            if i == 0:
                break
            print(m," minutes and ",i," seconds")
            sleep(1)
        if m < 0:
            break
        for j in range(59,-1,-1):
            if j % 60 == 0:
                m-=1
            print(m," minutes and ",j," seconds")
            sleep(1)

    return True
