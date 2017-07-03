from pydojo import *
# CREATE GAME DISPLAY
screen(1280, 720)

hero = Actor('example_asset/characters/stickman/kamae_idle')
hero.loadfolder('example_asset/characters/stickman/kisami_tsuki')
hero.loadfolder('example_asset/characters/stickman/mae_geri')
hero.loadfolder('example_asset/characters/stickman/yoko_geri')
hero.loadfolder('example_asset/characters/stickman/age_uke')
hero.loadfolder('example_asset/characters/stickman/gedan_barai')
hero.loadfolder('example_asset/characters/stickman/hit_body')
hero.action = 'kamae idle'
hero.rotate('flip')
hero.speed = 0
hero.setx(100)

# Clone scale bug?
# hero.scale(2)
print hero.size, hero.rect
enemy = clone(hero)
enemy.setx(600)
enemy.scale(2)

print hero.size, hero.rect, enemy.rect, enemy.size

print 'IN GAME DICT DEBUG'

enemy2 = clone(hero)
enemy2.setx(1000)
enemy2.scale(0.5)

instructions = Text("press A or D to move, J-K-L to attack, U-I-O to defend!", color=CYAN)

print hero.animations
print hero.animation

# MAIN LOOP
while True:

    # print hero.costumes_by_name['age_uke\\age_uke_013']['image'] is enemy.costumes_by_name['age_uke\\age_uke_013'][
    #     'image']

    enemy.play('kisami_tsuki')
    enemy2.play('mae_geri')

    if anykeydown():
        instructions.hide()

    hero.forward(hero.speed)

    # Movement Control
    if key(D):
        hero.point(90)
    if key(A):
        hero.point(-90)

    # Action Control
    if keydown(J):
        hero.action = 'kisami tsuki'
        print hero.action + '!'
    if keydown(K):
        hero.action = 'mae geri'
        print hero.action + '!'
    if keydown(L):
        hero.action = 'yoko geri'
        print hero.action + '!'
    if keydown(U):
        hero.action = 'age uke'
        print hero.action + '!'
    if keydown(I):
        hero.action = 'gedan barai'
        print hero.action + '!'
    if keydown(O):
        hero.action = 'gedan barai'
        print hero.action + '!'

    if hero.action == 'kamae idle':
        hero.speed = 0
        hero.play('kamae_idle')
    elif hero.action == 'kisami tsuki':
        hero.speed = 5
        hero.play('kisami_tsuki', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'
    elif hero.action == 'mae geri':
        hero.speed = 7
        hero.play('mae_geri', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'
    elif hero.action == 'yoko geri':
        hero.speed = 5
        hero.play('yoko_geri', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'
    elif hero.action == 'age uke':
        hero.speed = -3
        hero.play('age_uke', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'
    elif hero.action == 'gedan barai':
        hero.speed = -5
        hero.play('gedan_barai', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'
    elif hero.action == 'hit body':
        hero.speed = -1
        hero.play('hit_body', fps=80, loop=False)
        if hero.animation['state'] == 'ended':
            hero.action = 'kamae idle'

    # UPDATE SCREEN
    update()
