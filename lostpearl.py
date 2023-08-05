from random import *
from pygame import *
win_height = 700
win_width = 500
window=display.set_mode((700,500))
clock = time.Clock()
FPS=60
display.set_caption("LostPearl")
background=transform.scale(image.load("f.png"),(win_height,win_width))
preview=transform.scale(image.load("preview.png"),(win_height,win_width))
window.blit(background,(0,0))
sharks =sprite.Group()
ink=sprite.Group()
pearls=sprite.Group()
fishes=sprite.Group()
font.init()
fontl=font.Font(None, 36)
lost=0
total=0
lifes=4
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, height, weight):
        super().__init__()
        self.image=transform.scale(image.load(player_image), (height,weight))
        self.speed=player_speed
        self.rect = self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total<5 and lost<3 and lifes>0:
            keys_pressed=key.get_pressed()
            if keys_pressed[K_w] and self.rect.y >5:
                self.rect.y -=self.speed
            if keys_pressed[K_s] and self.rect.y <395:
                self.rect.y +=self.speed
        
class Enemy(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.x-=self.speed
        
class Bullet(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.x+=self.speed
            
class Heal(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.x-=self.speed

class Pearl(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.x-=self.speed
        
octopus =Player('octopus.png', 10, 250,4, 130,150)
font.init()
font = font.SysFont('Arial', 54)
win = font.render('YOU WIN!', True, (255,0,0))
lose = font.render('YOU LOSE!', True, (255,0,0))
death=font.render('YOU DIED!', True, (169,0,0))
knowledge=font.render('нажми E чтобы стрелять', True, (255,205,0))
game=True
finish = False
mixer.init()
mixer.music.load('sound.ogg')
mixer.music.play()

wait=120
wait2=120
wait0=240
wait3=360
n=300
a=900
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
    while n!=0:
        window.blit(preview,(0,0))
        display.update()
        n-=1
    window.blit(background,(0,0))
    octopus.reset()
    octopus.update()
    if finish!=True:
        while a!=0:
            window.blit(knowledge,(150,150))
            display.update()
            a-=1
        if wait==0:
            wait=120
            sharks.add(Enemy('shark.png', 750,randint(5,390), 4,200,100))
        else:
            wait-=1
        if wait0==0:
            wait0=240
            pearls.add(Pearl('pearl.png', 750,randint(5,390), 3,60,60))
        else:
            wait0-=1
        if wait3==0:
            wait3=360
            fishes.add(Heal('fish.png', 750,randint(5,390),4,100,70))
        else:
            wait3-=1
        sharks.draw(window)
        pearls.draw(window)
        fishes.draw(window)
        ink.draw(window)
        for e in event.get():
            if e.type == QUIT:
                game=False
            elif e.type == KEYDOWN:
                if e.key==K_e:
                    ink.add(Bullet('ink.png', octopus.rect.x+20, octopus.rect.y, 7,80,80))
        text_lose=fontl.render("lost:"+str(lost), 1,(255,255,255))
        text_win=fontl.render("total:"+str(total),1,(255,255,255))
        text_lifes=fontl.render(str(lifes),1,(255,0,0))
        window.blit(text_lose,(2,2))
        window.blit(text_win,(2,30))
        window.blit(text_lifes,(680,1))
    if total==5:
        window.blit(win,(200,200))
        finish=True
        if wait2 == 0:
            wait2 = 120
            lost=0
            total=0
            lifes=4
            finish=False
        else:
            wait2-=1
    if lost==3:
        finish=True
        window.blit(lose,(200,200))
        if wait2 == 0:
            wait2 = 120
            lost=0
            total=0
            lifes=4
            finish=False
        else:
            wait2-=1
    if lifes==0:
        finish=True
        window.blit(death,(200,200))
        if wait2 == 0:
            wait2 = 120
            lost=0
            lifes=4
            total=0
            finish=False
        else:
            wait2-=1
    sprite_list=sprite.spritecollide(octopus, pearls,True)
    sprite_list2=sprite.spritecollide(octopus, fishes,True)
    sprite_list3=sprite.spritecollide(octopus, sharks,True)
    sprite_list4=sprite.groupcollide(ink, sharks,True,True)
    for f in sprite_list2: 
        lifes+=1
    for s in sprite_list: 
        total+=1
    for d in sprite_list3: 
        lifes-=1
    sharks.update()
    ink.update()
    fishes.update()
    pearls.update()
    
    display.update()
    clock.tick(FPS)