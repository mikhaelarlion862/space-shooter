#Create your own shooter
from pygame import *
from random import randint
from time import time as timer

#loading font functions separately
font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (0, 255, 0))
lose = font1.render('YOU FAILED!', True, (180, 0, 0))


font2 = font.Font(None, 36)


#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#we need the following images:
img_back = "galaxy.jpg" #game background
img_bullet = "bullet.png" #bullet
img_hero = "rocket.png" #hero
img_enemy = "ufo.png" #enemy
score = 0 #ships destroyed
goal = 10 #how many ships need to be shot down to win
lost = 0 #ships missed
max_lost = 3 #lose if you miss that many

class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #call for the class (Sprite) constructor:
       sprite.Sprite.__init__(self)


       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #every sprite must have the rect property that represents the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #method drawing the character on the window
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       global lost
       #disappears upon reaching the screen edge
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
class Obstacle(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#bullet sprite class  
class Bullet(GameSprite):
   # enemy movement
   def update(self):
       self.rect.y += self.speed
       # disappears upon reaching the screen edge
       if self.rect.y < 0:
           self.kill()
#create a small window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
#creating a group of enemy sprites
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Obstacle('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#main game loop:
run = True #the flag is reset by the window close button

reload_time = False

nun_fire = 0

while run:
   for e in event.get():
       if e.type == QUIT:
           run = False
       
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               if nun_fire < 5 and reload_time == False:
                   nun_fire = nun_fire + 1
                   fire_sound.play()
                   ship.fire()

               if nun_fire >= 5 and reload_time == False:
                   last_time = timer()
                   reload_time = True
 
   if not finish:
       window.blit(background,(0,0))


       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()

       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)

       #reload
       if reload_time == True:
           now_time = timer()

           if now_time - last_time < 1:
               reload = font2.render('Reloading......', 1, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               nun_fire = 0
               reload_time = False
       
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(
               80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

       if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
           finish = True 
           window.blit(lose, (200, 200))

       if score >= goal:
           finish = True
           window.blit(win, (200, 200))

       text = font2.render("Score: " + str(score), 1, (0, 255, 0))
       window.blit(text, (10, 20))

       text_lose = font2.render("Missed: " + str(lost), 1, (255, 0, 0))
       window.blit(text_lose, (10, 50))

       display.update()
   
   else:
       finish = False
       score = 0
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()


       time.delay(3000)
       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

       for i in range(1, 3):
           asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
           asteroids.add(asteroid)
           
      


   time.delay(50)




