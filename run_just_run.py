import pygame
import sys, os

FPS = 50
SIZE = WIDTH, HEIGHT = 704, 768
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# основной персонаж
player = level = enemy = None


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
    'floor': load_image('desk1.png'),
    'wall1': load_image('wall4.png'),
    'door': load_image('door.png'),
    'wall': load_image('walling.png'),
    'empty': load_image('floor1.png')
}
player_image = load_image('Vova.png')
enemy_image = load_image('enemy1.png')

tile_width = tile_height = 64


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
    if keys == 'lose':
        return '['
    elif keys == 'left':
        if get_level_tile(row, col - 1) == '.':
            level[row][col] = '.'
            level[row][col - 1] = txt
            player.pos_x -= 1
        if get_level_tile(row, col - 1) == ']' or get_level_tile(row, col - 1) == 'H':
            return get_level_tile(row, col - 1)
    elif keys == 'up':
        if get_level_tile(row - 1, col) == '.':
            level[row][col] = '.'
            level[row - 1][col] = txt
            player.pos_y -= 1
        if get_level_tile(row - 1, col) == ']' or get_level_tile(row - 1, col) == 'H':
            return get_level_tile(row - 1, col)
    elif keys == 'down':
        if get_level_tile(row + 1, col) == '.':
            level[row][col] = '.'
            level[row + 1][col] = txt
            player.pos_y += 1
        if get_level_tile(row + 1, col) == ']' or get_level_tile(row + 1, col) == 'H':
            return get_level_tile(row + 1, col)
    elif keys == 'right':
        if get_level_tile(row, col + 1) == '.':
            level[row][col] = '.'
            level[row][col + 1] = txt
            player.pos_x += 1
        if get_level_tile(row, col + 1) == ']' or get_level_tile(row, col + 1) == 'H':
            return get_level_tile(row, col + 1)
    return False


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
    playerx, playery, enemyy, enemyx = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('floor', x, y)
            elif level[y][x] == '1':
                Tile('wall1', x, y)
            elif level[y][x] == 'H':
                Tile('door', x, y)
            elif level[y][x] == 'h':
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


def enemy_move(enemy, player):
    if (abs(enemy.pos_x - player.pos_x) == 1 and abs(enemy.pos_y - player.pos_y) == 0) or \
            (abs(enemy.pos_x - player.pos_x) == 0 and abs(enemy.pos_y - player.pos_y) == 1) or \
            (abs(enemy.pos_x - player.pos_x) == 1 and abs(enemy.pos_y - player.pos_y) == 1):
        return 'lose'
    if enemy.pos_x < player.pos_x and get_level_tile(enemy.pos_y, enemy.pos_x + 1) == '.':
        return 'right'
    if enemy.pos_y > player.pos_y and (
            get_level_tile(enemy.pos_y - 1, enemy.pos_x) == '.' or get_level_tile(enemy.pos_y - 1, enemy.pos_x) == '@'):
        return 'up'
    if enemy.pos_y < player.pos_y and (
            get_level_tile(enemy.pos_y + 1, enemy.pos_x) == '.' or get_level_tile(enemy.pos_y + 1, enemy.pos_x) == '@'):
        return 'down'
    if enemy.pos_x > player.pos_x and (
            get_level_tile(enemy.pos_y, enemy.pos_x - 1) == '.' or get_level_tile(enemy.pos_y, enemy.pos_x - 1) == '@'):
        return 'left'
    if enemy.pos_x == player.pos_x:
        return 'left'
    if enemy.pos_y == player.pos_y:
        return 'up'


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

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
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global player, level, enemy
    level = load_level("map2.txt")
    player, level_x, level_y, enemy, enemy_x, enemy_y = generate_level(level)
    true = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    true = player_move('left', '@', player)
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    true = player_move('right', '@', player)
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    true = player_move('up', '@', player)
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    true = player_move('down', '@', player)
                false = player_move(enemy_move(enemy, player), ']', enemy)
                if true == ']' or false == '[':
                    print('bye')
                    return False
                if true == 'H':
                    print('win')
                    return True
        screen.fill('white')
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    main()
    terminate()