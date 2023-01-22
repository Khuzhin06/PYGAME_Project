import pygame
from dop_def import load_image
PURCHASES = [False, False, False, False, False, False]
FPS = 50
SIZE = WIDTH, HEIGHT = 768, 768
FONT_NAME = pygame.font.match_font('arial')
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
magazine_group = pygame.sprite.Group()


tile_images = {
    'wall': load_image('desk.png'),
    'empty': load_image('floor.png')
}
player_image = load_image('mar.png')
enemy_image = load_image('enemy.png')

tile_width = tile_height = 128


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_magazine(name, pngname, corx, cory):
    name.image = load_image(pngname)
    name.rect = name.image.get_rect()
    name.rect.x = corx
    name.rect.y = cory


def who(who):
    with open('who.txt', mode='w', encoding="utf8") as file:
        file.write(who)
        file.close()


def magazine():
    artur = elisey = genka = kolya = leha = Vovan = 0
    pngnames = ["artur.png", "elisey.png", "genka.png", "kolya.png", "leha.png", 'Vovan.png']
    names = [artur, elisey, genka, kolya, leha, Vovan]
    x = 0
    n = 0
    for i in range(len(names)):
        names[i] = pygame.sprite.Sprite()
        if i <= 2:
            load_magazine(names[i], pngnames[i], 10 + x, 10)
            x += 135
        if i > 2:
            load_magazine(names[i], pngnames[i], 10 + n, 180)
            n += 135
        magazine_group.add(names[i])

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break
                # sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     break


        with open('coins.txt', mode='r', encoding="utf8") as file:
            for line in file:
                coins = line
        with open('characters.txt', mode='r', encoding="utf8") as file:
            char = file.readlines()
            if not char:
                char = ['']
            # print(char)
        screen.fill('black')
        draw_text(screen, '1)Артур: 1500 очков', 13, 80, 155)
        draw_text(screen, '2)Елисей: 1500 очков', 13, 215, 158)
        draw_text(screen, '3)Генадий: 1500 очков', 13, 350, 170)
        draw_text(screen, '4)Колян: 1500 очков', 13, 80, 310)
        draw_text(screen, '5)Лёха: 1500 очков', 13, 215, 310)
        draw_text(screen, '6)Вован: 1500 очков', 13, 350, 310)
        draw_text(screen, 'Количество очков:' + coins, 20, WIDTH - 650, HEIGHT - 75)
        draw_text(screen, 'Нажмите на цифру 1-6, чтобы купить нужного вам персонажа.', 20, 260, HEIGHT - 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            PURCHASES[0] = True
            who('1')
        if keys[pygame.K_2]:
            PURCHASES[1] = True
            who('2')
        if keys[pygame.K_3]:
            PURCHASES[2] = True
            who('3')
        if keys[pygame.K_4]:
            PURCHASES[3] = True
            who('4')
        if keys[pygame.K_5]:
            PURCHASES[4] = True
            who('5')
        if keys[pygame.K_6]:
            PURCHASES[5] = True
            who('6')
        for i in range(6):
            if PURCHASES[i] == True:
                if str(i) not in char[0]:
                    if int(coins) >= 1500:
                        with open('characters.txt', mode='a', encoding="utf8") as file:
                            file.write(str(i))
                        with open('coins.txt', mode='w', encoding="utf8") as file:
                            file.write(str(int(coins) - 1500))
                            file.close()
                    PURCHASES[i] = False
        magazine_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
