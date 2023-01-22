import sys
import os
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def money(skoko):
    with open('coins.txt', mode='r', encoding="utf8") as file:
        for line in file:
            coins = line
    with open('coins.txt', mode='w', encoding="utf8") as file:
        file.write(str(int(coins) + skoko))
        file.close()


hero = {'1': 'kolya1.png',
        '2': 'elisey1.png',
        '3': 'genka1.png',
        '4': 'artur1.png',
        '5': 'leha1.png',
        '6': 'Vova1.png'}


def who_now():
    with open('who.txt', mode='r', encoding="utf8") as file:
        for line in file:
            return hero[line]
