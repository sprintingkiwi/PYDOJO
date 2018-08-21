# -*- coding: utf-8 -*-
# from __future__ import print_function
from pydojo.main import *
# import pickle

width=800
height=600

screen(width, height)

a = Actor()
testo=Text("3 click, poi ti mostro il punteggio")

timer = Timer(1750)

click = 0
hit =   0

while True:
    if timer.get():
        a.gorand()
        a.show()

    if a.click():
        hit+=1
        a.hide()
    
    if MOUSE.leftdown:
        click+=1
        
    update()
    #if data["click"] > 2:
       # pickle.dump( data, open( "savedata.p", "wb"),protocol=2 )
       # execute("sulfrum_savedata_b.py")
       # quit()

    if click > 2:
        save(hit, "hit")
        save(click, "click")
        execute("example_savedata_b.py")
        quit()
        
    if keydown(D):
        #print(data["click"], data["hit"])
        pass
