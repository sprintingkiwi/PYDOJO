# -*- coding: utf-8 -*-
from __future__ import print_function
from pydojo.main import *
#import pickle

width=800
height=600

screen(width, height)

click = load("click")
hit = load("hit")
#data = pickle.load(open("savedata.p", "rb"))
a=Text("init: " + str(hit) + " su " + str(click))

while True:
    update()
    
