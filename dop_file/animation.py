import sys

import pygame
from pygame.constants import QUIT, K_ESCAPE, KEYDOWN


# pygame.constants необходим для создания условия выхода из цикла


# далее создаем функцию my_animation, принимающая следующие аргументы
# w1, h1 - количество спрайтов в строке и столбце изображения,
# k - это общее количество кадров в изображении,
# fps - количество кадров в секунду, name - название и путь к изображению,
# position - положение анимации на игровом экране.

def my_animation(w1, h1, k, fps, name, position):
    # список для хранения кадров и таймер
    frames = []
    timer = pygame.time.Clock()

    # создаем экран и загружаем изображение в переменную sprite,
    # установив методом convert_alpha необходимую прозрачность
    scr = pygame.display.set_mode((300, 300), 0, 32)
    sprite = pygame.image.load("kostic 2.0.jpg".format(name)).convert_alpha()

    # находим длину, ширину изображения и размеры каждого кадра
    width, height = sprite.get_size()
    w, h = width / w1, height / h1

    # счетчик положения кадра на изображении
    row = 0

    # итерация по строкам
    for j in range(int(height / h)):
        # производим итерацию по элементам строки
        for i in range(int(width / w)):
            # добавляем  в список отдельные кадры
            frames.append(sprite.subsurface(pygame.Rect(i * w, row, w, h)))
        # смещаемся на высоту кадра, т.е. переходим на другую строку
        row += int(h)

    # счетчик
    counter = 0

    while True:
        # условие выхода из цикла - нажатие клавиши ESCAPE
        for evt in pygame.event.get():
            if evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE):
                sys.exit()
        # заполняем игровое поле красным цветом и методом blit вырисовываем на поверхности

        scr.fill((0, 0, 0))
        scr.blit(frames[counter], position)

        # счетчик используемый как индекс в списке увеличивается до того как не превысит
        counter = (counter + 1) % k

        # обновляем экран
        pygame.display.update()
        timer.tick(fps)


if __name__ == "__main__":
    x = float(input("Fps:"))
    my_animation(4, 3, 12, x, "image", (90, 90))
