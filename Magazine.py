import pygame
import sys, os

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
# основной персонаж
player = level = None


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


tile_images = {
    'wall': load_image('desk.png'),
    'empty': load_image('floor.png')
}
player_image = load_image('mar.png')
enemy_image = load_image('enemy.png')

tile_width = tile_height = 128


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = enemy_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


def get_level_tile(row, col):
    if row >= 0 and row < len(level):
        if col >= 0 and col < len(level[0]):
            return level[row][col]
    return None


def player_move(keys, txt, player):
    row, col = player.pos_y, player.pos_x
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if get_level_tile(row, col - 1) == '.':
            level[row][col] = '.'
            level[row][col - 1] = txt
            player.pos_x -= 1
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        if get_level_tile(row - 1, col) == '.':
            level[row][col] = '.'
            level[row - 1][col] = txt
            player.pos_y -= 1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if get_level_tile(row + 1, col) == '.':
            level[row][col] = '.'
            level[row + 1][col] = txt
            player.pos_y += 1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if get_level_tile(row, col + 1) == '.':
            level[row][col] = '.'
            level[row][col + 1] = txt
            player.pos_x += 1


def load_level(filename):
    filename = "maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    temp = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return [list(row) for row in temp]


def generate_level(level):
    new_player, x, y = None, None, None
    playerx, playery = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                playerx, playery = x, y
            elif level[y][x] == ']':
                Tile('empty', x, y)
                enemyx, enemyy = x, y

    if playerx and playery:
        new_player = Player(playerx, playery)
    if enemyy and enemyx:
        enemy = Enemy(enemyx, enemyy)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, enemy, enemyx, enemyy


def start_screen():
    intro_text = ["СБЕЖАТЬ ИЗ ШКОЛЫ",
                  "171 Edition",
                  "",
                  "Правила игры:",
                  "Нажмите на любую клавишу на клавиатуре, чтобы начать игру",
                  "Нажмите на любую клавишу на мышке, чтобы открыть магазин"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 5, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                magazine()
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global player, level, enemy
    level = load_level("map2.txt")
    player, level_x, level_y, enemy, enemy_x, enemy_y = generate_level(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                print(keys)
                player_move(keys, '@', player)
                player_move(keys, ']', enemy)


        screen.fill('white')
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


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
            if event.type == pygame.QUIT:
                running = False
                break

        with open('coins.txt', mode='r', encoding="utf8") as file:
            for line in file:
                coins = line
        screen.fill('black')
        draw_text(screen, '1)Артур: 1500 очков', 13, 80, 155)
        draw_text(screen, '2)Елисей: 1500 очков', 13, 215, 158)
        draw_text(screen, '3)Генадий: 1500 очков', 13, 350, 170)
        draw_text(screen, '4)Колян: 1500 очков', 13, 80, 310)
        draw_text(screen, '5)Лёха: 1500 очков', 13, 215, 310)
        draw_text(screen, '6)Вован: 1500 очков', 13, 350, 310)
        draw_text(screen, 'Количество очков:' + coins, 20, WIDTH - 120, HEIGHT - 50)
        draw_text(screen, 'Нажмите на цифру 1-6, чтобы купить нужного вам персонажа.', 20, 260, HEIGHT - 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            PURCHASES[0] = True
        if keys[pygame.K_2]:
            PURCHASES[1] = True
        if keys[pygame.K_3]:
            PURCHASES[2] = True
        if keys[pygame.K_4]:
            PURCHASES[3] = True
        if keys[pygame.K_5]:
            PURCHASES[4] = True
        if keys[pygame.K_6]:
            PURCHASES[5] = True
        magazine_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    main()
    terminate()