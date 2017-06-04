from pydojo import *
# CREATE GAME DISPLAY
screen(360, 720)

hero = Actor('example_asset/characters/stickman/kamae_idle')
hero.loadfolder('example_asset/characters/stickman/kisami_tsuki')
hero.loadfolder('example_asset/characters/stickman/mae_geri')
hero.action = 'kamae idle'

print hero.costumes
print len(hero.costumes)

# MAIN LOOP
while True:

    print hero.cosnumber

    if keydown(J):
        hero.action = 'kisami tsuki'
        print hero.action + '!'
    if keydown(K):
        hero.action = 'mae geri'
        print hero.action + '!'

    if hero.action == 'kamae idle':
        hero.nextcostume(2, costumes=[0, 23])
    elif hero.action == 'kisami tsuki':
        hero.nextcostume(1, costumes=[24, 47])
        if hero.cosnumber > 46:
            hero.action = 'kamae idle'
    elif hero.action == 'mae geri':
        hero.nextcostume(1, costumes=[60, 71])
        if hero.cosnumber > 70:
            hero.action = 'kamae idle'

    # UPDATE SCREEN
    update()
