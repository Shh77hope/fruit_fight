import pygame as pg
from pygame.locals import *
import random
import os
from pathlib import Path
os.chdir(Path(__file__).parent)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
FPS = 60
pg.display.set_caption('fruit_game')
map = pg.transform.scale(pg.image.load('murder_place.png').convert(),(WIDTH,HEIGHT))
menu_art = pg.transform.scale(pg.image.load('bg_menu.png').convert(),(WIDTH,HEIGHT))
pause_art = pg.transform.scale(pg.image.load('ss.png').convert(),(WIDTH,HEIGHT))
score_font = pg.font.Font('Kenney Pixel.ttf',48)
big_font = pg.font.Font('Kenney Mini.ttf',82)
textX = 10
textY = 10

white = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)

Betty = pg.transform.scale(pg.image.load('Betty.png').convert(), (100,132))
Lila = pg.transform.scale(pg.image.load('Lila.png').convert(), (125,146))
Zoe = pg.transform.scale(pg.image.load('Zoe.png').convert(), (140,129))
Nora = pg.transform.scale(pg.image.load('Nora.png').convert(), (109,155))
Isabelle = pg.transform.scale(pg.image.load('Isabelle.png').convert(), (140,124))
character_list = [Betty,Lila,Zoe,Nora,Isabelle]
#p1, p2 = random.sample(character_list, k=2)
p1 = Zoe
p2 = Betty

speed_a = 12 if p1 == Betty else 10
speed_b = 12 if p2 == Betty else 10

class Player1(pg.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = p1
        self.surf.set_colorkey((0,255,0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(WIDTH/4,HEIGHT/4))

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -speed_a)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, speed_a)
        if pressed_keys[K_a]:
            self.rect.move_ip(-speed_a, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(speed_a, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
playera = Player1()

class Player2(pg.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = p2
        self.surf.set_colorkey((0,255,0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(WIDTH-WIDTH/4,HEIGHT-HEIGHT/4))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed_b)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed_b)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed_b, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed_b, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
playerb = Player2()

class Fruit(pg.sprite.Sprite):
    def __init__(self):
        super(Fruit, self).__init__()
        self.surf = pg.transform.scale(pg.image.load('fruit.png').convert(), (46,48))
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                random.randint(23, WIDTH-23),
                random.randint(24, HEIGHT-24),
            )
        )
fruit = Fruit()

class Fish(pg.sprite.Sprite):
    def __init__(self):
        super(Fish, self).__init__()
        self.surf = pg.transform.scale(pg.image.load('fish.png').convert(), (120,60))
        self.surf.set_colorkey((0,255,0),RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                random.randint(60, WIDTH-60),
                random.randint(30, HEIGHT-30),
            )
        )
fish = Fish()

class Scythe(pg.sprite.Sprite):
    def __init__(self):
        super(Scythe, self).__init__()
        self.surf = pg.transform.scale(pg.image.load('scythe.png').convert(), (650,530))
        self.surf.set_colorkey((0,255,0),RLEACCEL)
        self.rect = self.surf.get_rect(center=(-350,(HEIGHT/2)))

    def update(self, pressed_keys):
        if pressed_keys[K_c]:
            self.rect.move_ip(30, 0)
            if self.rect.centerx >= (WIDTH/2):
                self.kill()
scythe = Scythe()

ff = pg.sprite.Group()
ff.add(fruit)
fs = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(fruit)
all_sprites.add(scythe)
all_sprites.add(playera)
all_sprites.add(playerb)

def startgame():
    score_valuea = 0
    score_valueb = 0

    def a_score(x,y):
        box = pg.Rect(0,0, 165, 50)
        pg.draw.rect(screen,(0,0,0), box)
        score = score_font.render('Score: ' + str(score_valuea),True,(255,255,255))
        screen.blit(score, score.get_rect(center = box.center))
    def b_score(x,y):
        box = pg.Rect((WIDTH-165),0, 165, 50)
        pg.draw.rect(screen,(0,0,0), box)
        score = score_font.render('Score: ' + str(score_valueb),True,(255,255,255))
        screen.blit(score, score.get_rect(center = box.center))

    def Winner():
        wbox = pg.Rect((WIDTH/2),(HEIGHT/4),600,100)
        wbox.center = wbox.topleft
        pg.draw.rect(screen,(0,0,0),wbox)
        pg.draw.rect(screen,(255,255,255),wbox, 2)
        if winner == 'Player A Won!':
            game_over_surface = big_font.render(
                winner, True, (255,245,0))
        if winner == 'Player B Won!':
            game_over_surface = big_font.render(
                winner, True, (255,60,0))
        game_over_rect = game_over_surface.get_rect(center = wbox.center)
        screen.blit(game_over_surface, game_over_rect)
        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        startgame()

    running = True
    while running:
        screen.blit(map,(0,0))
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    pause()
        
        pressed_keys = pg.key.get_pressed()
        playera.update(pressed_keys)
        playerb.update(pressed_keys)
        scythe.update(pressed_keys)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        fruit_collide = pg.sprite.spritecollideany(playera, ff)
        if fruit_collide:
            fruit_collide.kill()
            score_valuea += 1
            new_fruit = Fruit()
            ff.add(new_fruit)
            all_sprites.add(new_fruit)
            if score_valuea == 5 or score_valuea == 15:
                new_fish = Fish()
                fs.add(new_fish)
                all_sprites.add(new_fish)
        if p1 == Zoe:
            fish_collide = pg.sprite.spritecollideany(playera, fs)
            if fish_collide:
                fish_collide.kill()
                score_valuea += 1

        fruit_collide = pg.sprite.spritecollideany(playerb, ff)
        if fruit_collide:
            fruit_collide.kill()
            score_valueb += 1
            new_fruit = Fruit()
            ff.add(new_fruit)
            all_sprites.add(new_fruit)
            if score_valueb == 5 or score_valueb == 15:
                new_fish = Fish()
                fs.add(new_fish)
                all_sprites.add(new_fish)
        if p2 == Zoe:
            fish_collide = pg.sprite.spritecollideany(playerb, fs)
            if fish_collide:
                fish_collide.kill()
                score_valueb += 1
        
        a_score(textX,textY)
        b_score(textX,textY)
        if score_valuea >= 20:
            winner = 'Player A Won!'
            Winner()
        if score_valueb >= 20:
            winner = 'Player B Won!'
            Winner()

        pg.display.flip()
        clock.tick(FPS)

def pause():
    screen.blit(pause_art,(0,0))
    running = True
    while running:
        pause_menu = pg.Rect(WIDTH/2,HEIGHT/2,1000,250)
        pause_menu.center = pause_menu.topleft
        pg.draw.rect(screen,white,pause_menu)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(mouse):
                    menu()
                if resume_button.collidepoint(mouse):
                    running = False

        mouse = pg.mouse.get_pos()

        menu_button = pg.Rect(WIDTH/2-225,HEIGHT/2,400,100)
        menu_button.center = menu_button.topleft
        text = big_font.render('MENU' , True , white)
        if menu_button.collidepoint(mouse):
            pg.draw.rect(screen,color_light,menu_button)
        else:
            pg.draw.rect(screen,color_dark,menu_button)
        screen.blit(text, text.get_rect(center = menu_button.center))

        resume_button = pg.Rect(WIDTH/2+225,HEIGHT/2,400,100)
        resume_button.center = resume_button.topleft
        text = big_font.render('RESUME' , True , white)
        if resume_button.collidepoint(mouse):
            pg.draw.rect(screen,color_light,resume_button)
        else:
            pg.draw.rect(screen,color_dark,resume_button)
        screen.blit(text, text.get_rect(center = resume_button.center))

        pg.display.update()

def menu():
    while True:
        screen.blit(menu_art,(0,0))
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse):
                    startgame()
                if quit_button.collidepoint(mouse):
                    pg.quit()
                    quit()

        mouse = pg.mouse.get_pos()
        
        start_button = pg.Rect(WIDTH/4,HEIGHT-(HEIGHT/3),550,100)
        start_button.center = start_button.topleft
        text = big_font.render('START GAME' , True , white)
        if start_button.collidepoint(mouse):
            pg.draw.rect(screen,color_light,start_button)
        else:
            pg.draw.rect(screen,color_dark,start_button)
        screen.blit(text, text.get_rect(center = start_button.center))

        quit_button = pg.Rect(WIDTH-(WIDTH/4),HEIGHT-(HEIGHT/3),550,100)
        quit_button.center = quit_button.topleft
        text = big_font.render('QUIT' , True , white)
        if quit_button.collidepoint(mouse):
            pg.draw.rect(screen,color_light,quit_button)
        else:
            pg.draw.rect(screen,color_dark,quit_button)
        screen.blit(text, text.get_rect(center = quit_button.center))

        pg.display.update()
menu()
