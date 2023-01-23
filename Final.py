import pygame
import sys, os
SIZE = WIDTH, HEIGHT = 768, 768
screen = pygame.display.set_mode(SIZE)


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


def you_win():
    youwin = pygame.transform.scale(load_image('You Win.jpg'), (WIDTH, HEIGHT))
    screen.blit(youwin, (0, 0))
    pygame.display.set_caption('Финал')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.flip()


if __name__ == '__main__':
    you_win()