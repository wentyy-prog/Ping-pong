from pygame import *
from random import *
init()
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,player_size_x,player_size_y):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(player_size_x,player_size_y)).convert_alpha()
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
        self.mask = mask.from_surface(self.image)
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Ball(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed,player_size_x,player_size_y,player_speed_y):
        super().__init__(player_image,player_x,player_y,player_speed,player_size_x,player_size_y)
        self.player_speed_y=player_speed_y
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.player_speed_y
        if self.rect.x >1280 or self.rect.y>960:
            self.rect.y=300
            self.rect.x=300


class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
    def update_two(self):
        keys=key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed



window = display.set_mode((1280,960))
display.set_caption("Пинг-понг")
ping_pong=transform.scale(image.load('beatch.png'),(1920, 1080))

racket_first=Player('racket.png',50,350,2,150,250)
racket_second=Player('racket.png',1100,350,2,150,250)

ball=Ball('ball.png',randint(10,1100),randint(10,60),1,40,40,1)


count_1=0
count_2=0
font1=font.SysFont('Arial',35)
font2=font.SysFont('Arial',100)
first=font1.render("1 игрок: "+str(count_1),1,(0,209,13))
second=font1.render("2 игрок: "+str(count_2),1,(0,209,13))

victory_1=font2.render('FIRST WIN!',True,(0,255,100))
victory_2=font2.render('SECOND WIN!',True,(0,255,100))
mixer.music.load('background.wav')
mixer.music.set_volume(0.05)
mixer.music.play()

first_group=sprite.Group()
second_group=sprite.Group()
first_group.add(racket_first)
second_group.add(racket_second)

rebound=mixer.Sound('ball.mp3')
win=mixer.Sound('win.wav')
win.set_volume(0.05)
finish=False
game = True
while game:
    for e in event.get():
        if e.type ==QUIT:
            game=False
        if e.type==KEYDOWN:
            if e.key==K_r:
                racket_first=Player('racket.png',50,350,2,150,250)
                racket_second=Player('racket.png',1100,350,2,150,250)
                ball=Ball('ball.png',randint(10,1100),randint(10,60),1,40,40,1)
                count_1=0
                count_2=0
                first=font1.render("1 игрок: "+str(count_1),1,(0,209,13))
                second=font1.render("2 игрок: "+str(count_2),1,(0,209,13))

                mixer.music.play()
                finish=False

    if finish!=True:
        window.blit(ping_pong,(0,0))
        window.blit(first,(10,10))
        window.blit(second,(1130,10))

        ball.reset()
        ball.update()
        racket_first.reset()
        racket_first.update()
        racket_second.reset()
        racket_second.update_two()
        if count_1==5:
            window.blit(victory_1,(400,400))
            finish=True
            win.play()
            mixer.music.stop()
        if count_2==5:
            window.blit(victory_2,(400,400))
            finish=True
            win.play()
            mixer.music.stop()

        if  sprite.spritecollide(ball,second_group,False,sprite.collide_mask) or sprite.spritecollide(ball,first_group,False,sprite.collide_mask):
            ball.speed*=-1

        if ball.rect.y>=960 or ball.rect.y <=10:
            ball.player_speed_y*=-1

        if ball.rect.x>=1280 or ball.rect.x<=10:
            ball.speed*=-1

        if sprite.spritecollide(ball,first_group,False,sprite.collide_mask) or sprite.spritecollide(ball,second_group,False,sprite.collide_mask):
            rebound.play()

        if ball.rect.x == 1280:
            count_1+=1
            first=font1.render("1 игрок: "+str(count_1),1,(0,209,13))
            window.blit(first,(10,10))

        if ball.rect.x ==10:
            count_2+=1
            second=font1.render("2 игрок: "+str(count_2),1,(0,209,13))
            window.blit(second,(1130,10))

        
    display.update()