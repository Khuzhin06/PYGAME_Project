import pygame
import sys, os

FPS = 50
SIZE = WIDTH, HEIGHT = 800, 700
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# основной персонаж
player = level = None


class Board:
    # создание поля
    def __init__(self, size=(0, 0), danger=None, exits=None, furniture_free=True,
                 except_cell=(), map=0):
        self.map = map
        self.danger = danger
        self.except_cell = except_cell
        self.furniture_free = furniture_free
        self.size = size
        self.exits = exits
        self.width = self.size[0]
        self.height = self.size[1]
        self.board = [
            [0] * self.size[0] for _ in range(self.size[1])
        ]
        # значения по умолчанию
        self.cell_size = 40
        self.left = (WIDTH - (self.cell_size * self.width)) // 2
        self.top = (HEIGHT - (self.cell_size * self.height)) // 2

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        if not self.furniture_free:
            self.furniture(screen)
        for x in range(self.left, self.width * self.cell_size + self.left, self.cell_size):
            for y in range(self.top, self.height * self.cell_size + self.top, self.cell_size):
                if ((x - self.left) // self.cell_size, (y - self.top) // self.cell_size) not in self.except_cell:
                    pygame.draw.rect(
                        screen,
                        (190, 190, 190),
                        (x, y, self.cell_size, self.cell_size),
                        width=1
                    )
        self.walls(screen)

    def walls(self, screen):
        if self.exits:
            for i, j in self.exits.keys():
                spots = [(self.cell_size * i[0] + self.left, self.top + i[1] * self.cell_size),
                         (self.cell_size * (i[0] + 1) + self.left,
                          self.top + i[1] * self.cell_size),
                         (self.cell_size * (i[0] + 1) + self.left + 20, self.top + i[1] * self.cell_size - 80),
                         (self.cell_size * i[0] + self.left - 20, self.top + i[1] * self.cell_size - 80)]

                if j == 3:
                    spots = [(
                        self.cell_size * i[0] + self.left, self.top + i[1] * self.cell_size),
                        (self.cell_size * (i[0] + 1) + self.left,
                         self.top + i[1] * self.cell_size),
                        (self.cell_size * (i[0] + 1) + self.left + 20,
                         self.top + i[1] * self.cell_size + 80),
                        (
                            self.cell_size * i[0] + self.left - 20,
                            self.top + i[1] * self.cell_size + 80)]
                elif j == 4:
                    spots = [(self.left + i[0] * self.cell_size, self.top + i[1] * self.cell_size),
                             (self.left + i[0] * self.cell_size,
                              self.top + (i[1] - 1) * self.cell_size),
                             (self.left + i[0] * self.cell_size - 80, self.top + (i[1] - 1) * self.cell_size - 20),
                             (self.left + i[0] * self.cell_size - 80, self.top + i[1] * self.cell_size + 20)]
                elif j == 2:
                    spots = [(self.left + i[0] * self.cell_size, self.top + i[1] * self.cell_size),
                             (self.left + i[0] * self.cell_size,
                              self.top + (i[1] - 1) * self.cell_size),
                             (self.left + i[0] * self.cell_size + 80, self.top + (i[1] - 1) * self.cell_size - 20),
                             (self.left + i[0] * self.cell_size + 80, self.top + i[1] * self.cell_size + 20)]
                # проход(дверь)
                pygame.draw.polygon(screen, 'white',
                                    spots, 0)

    def furniture(self, screen):
        # парты и стулья
        for j in range(0, 9, 3):
            for i in range(0, 10, 2):
                pygame.draw.rect(screen, 'brown', (200 + (i * self.cell_size), 190 + (j * self.cell_size), 40, 80), 0)
                pygame.draw.rect(screen, 'brown',
                                 (200 + (i * self.cell_size) - 20, 190 + (j * self.cell_size) + 5, 20, 30), 0)
                pygame.draw.rect(screen, 'brown',
                                 (200 + (i * self.cell_size) - 20, 190 + (j * self.cell_size) + 45, 20, 30), 0)

        # доска на стене
        pygame.draw.polygon(screen, 'green', [(self.width * self.cell_size + self.left + 80, self.top + 80),
                                              (self.width * self.cell_size + self.left + 80, self.top + 320),
                                              (self.width * self.cell_size + self.left + 20, self.top + 320 - 60),
                                              (self.width * self.cell_size + self.left + 20, self.top + 80 + 60)], 0)


slovarik = [Board(size=(15, 4),
                  exits={((0, 2), 4): -1, ((0, 3), 4): -1, ((15, 3), 2): 3, ((15, 1), 2): 3, ((15, 2), 2): 3,
                         ((15, 4), 2): 3, ((7, 4), 3): 1, ((10, 4), 3): 2}, map=0),
            Board(size=(14, 10), exits={((12, 0), 1): 0}, furniture_free=False, map=1),
            Board(size=(14, 10), exits={((1, 0), 1): 0}, furniture_free=False, map=2),
            Board(size=(14, 4),
                  exits={((0, 1), 4): 0, ((0, 2), 4): 0, ((0, 3), 4): 0, ((0, 4), 4): 0, ((14, 3), 2): 5,
                         ((14, 1), 2): 5, ((14, 2), 2): 5, ((14, 4), 2): 5,
                         ((10, 4), 3): 4, ((7, 0), 1): 9, ((8, 0), 1): 9}, map=3),
            Board(size=(5, 10), exits={((2, 0), 1): 3}, map=4),
            Board(size=(14, 4),
                  exits={((0, 1), 4): 3, ((0, 2), 4): 3, ((0, 3), 4): 3, ((0, 4), 4): 3, ((14, 3), 2): 8,
                         ((14, 2), 2): 8, ((3, 4), 3): 6, ((8, 4), 3): 7}, map=5),
            Board(size=(7, 10), exits={((3, 0), 1): 5}, map=6),
            Board(size=(14, 10), exits={((1, 0), 1): 5}, furniture_free=False, map=7),
            Board(size=(8, 7), exits={((0, 2), 4): 5, ((0, 3), 4): 5, ((6, 7), 3): 10}, map=8,
                  except_cell=((0, 4), (0, 5), (0, 6), (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6),
                               (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6)))
            ]
board = [slovarik[5]]


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


player_image = load_image('mar.png')

tile_width = tile_height = 40


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5 + board[0].left - tile_width, tile_height * pos_y + board[0].top - tile_height)


def get_level_tile(row, col):
    if row >= 0 and row < len(level):
        if col >= 0 and col < len(level[0]):
            return level[row][col]
    return None


def player_move(keys):
    row, col = player.pos_y, player.pos_x
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if get_level_tile(row, col - 1) == '$':
            main(slovarik[board[0].exits[((col - 1, row), 4)]])
        elif get_level_tile(row, col - 1) == '.':
            level[row][col] = '.'
            level[row][col - 1] = '@'
            player.pos_x -= 1
            player.rect.x -= tile_width
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        if get_level_tile(row - 1, col) == '$':
            main(slovarik[board[0].exits[((col - 1, row - 1), 1)]])
        elif get_level_tile(row - 1, col) == '.':
            level[row][col] = '.'
            level[row - 1][col] = '@'
            player.pos_y -= 1
            player.rect.y -= tile_height
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if get_level_tile(row + 1, col) == '$':
            main(slovarik[board[0].exits[((col - 1, row), 3)]])
        elif get_level_tile(row + 1, col) == '.':
            level[row][col] = '.'
            level[row + 1][col] = '@'
            player.pos_y += 1
            player.rect.y += tile_height
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if get_level_tile(row, col + 1) == '$':
            main(slovarik[board[0].exits[((col, row), 2)]])
        elif get_level_tile(row, col + 1) == '.':
            level[row][col] = '.'
            level[row][col + 1] = '@'
            player.pos_x += 1
            player.rect.x += tile_width


def load_level():
    filename = "maps/" + f'map{board[0].map}.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    temp = list(map(lambda x: x, level_map))
    return [list(row) for row in temp]


def generate_level(level):
    new_player, x, y = None, None, None
    playerx, playery = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                playerx, playery = x, y

    if playerx and playery:
        new_player = Player(playerx, playery)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def main(doska):
    global player, level, board
    board[0] = doska
    level = load_level()
    player, level_x, level_y = generate_level(level)

    running = True
    while running:
        screen.fill('black')
        if not board[0].danger:
            board[0].render(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player_move(keys)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    main(slovarik[5])
    terminate()
