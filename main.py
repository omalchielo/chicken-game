import pygame
import random
import sys
import time
from tinydb import TinyDB, Query

prev = ""


class Cross(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("snd/gun.wav")
        self.gunshot.set_volume(0.1)

    def shoot(self):
        pygame.sprite.spritecollide(cross, chicken_group, True)
        print(pygame.sprite.spritecollide(cross, chicken_group, True))
        self.gunshot.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Chicken(pygame.sprite.Sprite):
    def __init__(self, picture, x, y):
        super().__init__()
        random_number = random.randint(50, 250)
        self.image = pygame.transform.scale(pygame.image.load(picture), (random_number, random_number))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = [x, y]


def check_number(text):
    _ = ""

    for i in str(text):
        if i.isnumeric():
            _ += i
    return _


def make_text(i, color, size_x, size_y, size_text):
    sys_font = pygame.font.Font("fnt/font_p.ttf", size_text)
    sys_text = sys_font.render(i, True, color)
    sys_text_rect = sys_text.get_rect()
    sys_text_rect.center = (size_x, size_y)
    screen.blit(sys_text, sys_text_rect)


pygame.init()
stop = True
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
cas = 0
start = True
while stop:
    cas += 0.1
    pygame.draw.line(screen, (0, 0, 0), (0, 50), (cas, 50), 5)
    if start is True:
        font = pygame.font.Font("fnt/font_p.ttf", 50)
        input_box = pygame.Rect(425, 71, 140, 40)
        color = pygame.Color("grey13")
        chicken_group = pygame.sprite.Group()
        cross = Cross("img/cross.png")
        cross_group = pygame.sprite.Group()
        cross_group.add(cross)
        clock = pygame.time.Clock()
        bg = pygame.image.load("img/farm.png")
        pygame.mouse.set_visible(True)
        base_font = pygame.font.Font(None, 60)
        done = False
        prev = ""
        user_text = ''
        hits = 0
        count_x = 0
        count_y = 0
        shot_alr = 0
        kills = 0
        missed_b = 0
        lives = 5
        kills_lives = 0
        cas = 0
        fps = 60
        screen.blit(bg, (0, 0))
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += (event.unicode).upper()

            screen.blit(bg, (0, 0))
            make_text(f"ENTER YOUR NAME: ", color, 250, 100, 50)
            txt_surface = font.render(user_text, True, color)
            width_text = max(200, txt_surface.get_width() + 10)
            input_box.w = width_text
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
            clock.tick(60)

        pygame.mouse.set_visible(False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shot_alr += 1
            cross.shoot()
    if str(prev) != str(chicken_group):
        if prev != "":
            count_x = int(check_number(str(prev)))
            count_y = int(check_number(str(chicken_group)))
            kills += (count_x - count_y)
            if count_x - count_y > 1:
                double_kill = pygame.mixer.Sound("snd/double.wav")
                double_kill.set_volume(0.1)
                double_kill.play()

            kills_lives += 1

        if int(check_number(str(chicken_group))) < 3:
            while int(check_number(str(chicken_group))) < 3:
                new_target = Chicken("img/chicken.png", random.randint(100, width - 100),
                                     random.randint(100, height - 100))
                chicken_group.add(new_target)
        prev = str(chicken_group)
    alive = (lives - (shot_alr - kills_lives))

    if alive <= 0 or cas >= width:
        screen.blit(bg, (0, 0))
        make_text(f"YOU LOST!", (0, 0, 0), width // 2, height // 2 - 250, 100)
        make_text(f"YOU GOT: {str(kills)} KILLS!", (0, 0, 0), width // 2, height // 2 - 150, 70)
        pygame.mouse.set_visible(True)
        make_text(f"PRESS SPACE IF YOU WANT TO PLAY AGAIN", (0, 0, 0), width // 2, height // 2 - 50, 60,)
        db = TinyDB(r"vysledky.json")
        x = {user_text: kills}
        seznam = {}
        User = Query()

        db.insert(x)

        y = []
        list_best = []

        for i in db.all():
            y.append(i)

        for _ in y:
            for i in _.items():
                seznam[int(i[1])] = i[0]

        make_text(f"LEADERBORD", (0, 0, 0), width // 2, height // 2 + 50, 60)
        seznam = dict(sorted(seznam.items(), reverse=True))
        nu = 1
        lenght = 50
        for i in seznam.items():
            lenght += 50
            make_text(f"{nu} - {i[1]} {i[0]}", (0, 0, 0), width // 2, height // 2 + lenght, 60)
            nu += 1
            if nu >= 4:
                break
        pygame.display.update()
        user_text = ""
        no = True
        while no:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                no = False

        pygame.display.update()
        start = True
        kills = 0
        lives = 5
    if start is False:
        make_text(f"lives: {str(alive)}", (0, 0, 0), 900, 25, 50,)
        make_text(f"kills: {str(kills)}", (0, 0, 0), 75, 25, 50,)

        pygame.display.update()
        screen.blit(bg, (0, 0))
        chicken_group.draw(screen)
        cross_group.draw(screen)
        cross_group.update()
        clock.tick(240)

pygame.quit()
