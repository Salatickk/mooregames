from pygame import *
from random import *
from time import time as timer


# from pygame import sprite

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(Gamesprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 500:

            self.rect.y = 0
            self.rect.x = randint(80, 620)

window = display.set_mode((700, 500))
display.set_caption("Caption")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
player = Player("rocket.png", 5, 420, 80,180,10)


bullets = sprite.Group()
monsters = sprite.Group()
collides = sprite.groupcollide(monsters,bullets, True, True)
win_width = 700
win_height = 500
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 80, 80, 50,randint(1,5))

    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(30, win_width - 30,),-40, 80,50,randint( 1,3))
    asteroids.add(asteroid)

font.init()
font = font.Font(None, 36)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render("YOU LOSE", True, (255, 215, 0))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
image_asteroid = 'asteroid.png'
game = True
clock = time.Clock()
FPS = 60
finish = False
score = 0
lost = 0
max_lost = 3
goal = 10
num_fire = 0
life = 3
rel_time = False
while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
                if num_fire <5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire > 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if finish != True:
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), 80, 80, 50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -=1
        if life ==0 or lost >= max_lost:

            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        score1 = font.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(score1,(10,20))
        lose_condition = font.render('Потрачено:' + str(lost), 1, (255, 255, 255))
        window.blit(lose_condition, (10, 50))
        if life == 3:
            life_color = (250,0,0)
        if life == 2:
            life_color = (0,250,0)
        if life == 1:
            life_color = (0,0,250)

        text_life = font.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))

        player.update()
        player.reset()
        asteroids.update()
        asteroids.draw(window)

        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        collide = sprite.groupcollide(monsters,bullets, True, True)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload = font.render("We're reloading", 1 , (155,0,0))
                window.blit(reload, (250,400))
            else:
                num_fire = 0
                rel_time = False

        display.update()
    else:
        score = 0
        lost = 0

        rel_time = False

        for a in asteroids:
            a.kill()
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(80, 620), 80, 80, 50,randint(1,5))
            monsters.add(monster)
    time.delay(50)