import pygame

FPS = 50  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 800, 700


class Board:
    # создание поля
    def __init__(self, size=(0, 0), loot=None, danger=None, exits=None, furniture_free=True,
                 wall_count=(True, True, True, True), except_cell=()):
        self.danger = danger
        # self.classroom_number = no
        # self.name = name
        if not self.danger:
            self.except_cell = except_cell
            self.furniture_free = furniture_free
            self.size = size
            self.wall_count = wall_count
            # self.loot = loot
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
                spots = [(self.cell_size * (i[0] - 1) + self.left, self.top + i[1] * self.cell_size),
                         (self.cell_size * i[0] + self.left,
                          self.top + i[1] * self.cell_size),
                         (self.cell_size * i[0] + self.left + 20, self.top + i[1] * self.cell_size - 80),
                         (self.cell_size * (i[0] - 1) + self.left - 20, self.top + i[1] * self.cell_size - 80)]

                if j == 3:
                    spots = [(
                        self.cell_size * (i[0] - 1) + self.left, self.top + i[1] * self.cell_size),
                                (self.cell_size * i[0] + self.left,
                                 self.top + i[1] * self.cell_size),
                                (self.cell_size * i[0] + self.left + 20,
                                 self.top + i[1] * self.cell_size + 80),
                                (
                                    self.cell_size * (i[0] - 1) + self.left - 20,
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


# список комнат
slovarik = [Board(size=(15, 4),
                  exits={((0, 2), 4): -1, ((0, 3), 4): -1, ((15, 3), 2): 1, ((15, 1), 2): 1, ((15, 2), 2): 1, ((15, 4), 2): 1,((8, 4), 3): 3, ((11, 4), 3): 4}),
            Board(size=(14, 10), exits={((13, 0), 1): 0}, furniture_free=False),
            Board(size=(14, 10), exits={((2, 0), 1): 0}, furniture_free=False),
            Board(size=(14, 4),
                  exits={((0, 1), 4): 0, ((0, 2), 4): 0, ((0, 3), 4): 0, ((0, 4), 4): 0, ((14, 3), 2): 2, ((14, 1), 2): 2, ((14, 2), 2): 2, ((14, 4), 2): 2,
                         ((11, 4), 3): 5}),
            Board(size=(5, 10), exits={((3, 0), 1): 1}),
            Board(size=(14, 4),
                  exits={((0, 1), 4): 1, ((0, 2), 4): 1, ((0, 3), 4): 1, ((0, 4), 4): 1, ((14, 3), 2): 8, ((14, 2), 2): 8, ((3, 4), 3): 6, ((8, 4), 3): 7}),
            Board(size=(7, 10), exits={((4, 0), 1): 2}),
            Board(size=(14, 10), exits={((2, 0), 1): 2}, furniture_free=False)
            ]


def main():
    pygame.display.set_caption('Клетчатое поле начало')
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    running = True

    board = slovarik[1]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_LEFT:

        screen.fill('black')
        if not board.danger:
            board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()





#Board(size=(8, 10), exits={((2, 10), 3): 1, ((0, 10), 4): 3, ((8, 6), 2): 4, ((8, 7), 2): 4, ((3, 5), 4): 5, (4, 0): 6, (5, 0): 6, (6, 0): 6, (7, 0): 6}
#[#Board(size=(6, 5), exits={((2, 5), 3): -1, ((5, 0), 0): 1}),
            #Board(size=(3, 3), exits={((2, 3), 3): 0, ((2, 0), 0): 2}),
            #Board(size=(8, 10),
                  #exits={((2, 10), 3): 1, ((0, 10), 3): 3, ((8, 6), 2): 4, ((8, 7), 2): 4, ((3, 5), 4): 5, ((4, 0), 0): 6, ((5, 0), 0): 6, ((6, 0), 0): 6,
                         #((7, 0), 0): 6},
                  #except_cell=((3, 9), (4, 9), (5, 9), (6, 9), (7, 0), (7, 1), (7, 2), (7, 3),
                               #(7, 9), (8, 9), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8),
                               #(0, 0), (0, 1), (0, 2), (0, 3),
                               #(0, 4), (0, 5), (1, 0),
                               #(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5))),
            #Board(size=(6, 10), exits={(6, 2): 2}, except_cell=(
                #(3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 5), (5, 6), (5, 7),
                #(5, 8), (5, 9)), ),
            #Board(size=(15, 4),
                  #exits={((0, 2), 4): 2, ((0, 3), 4): 2, ((15, 3), 2): 9, ((15, 1), 2): 9, ((15, 2), 2): 9, ((15, 4), 2): 9, ((8, 4), 3): 7, ((11, 4), 3): 8}),
            #Board(size=(9, 13), except_cell=(
                #(8, 0), (7, 0), (6, 0), (8, 1), (7, 1), (6, 1), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (0, 11),
                #(1, 11), (2, 11), (3, 11), (4, 11),
                #(0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (8, 12), (7, 12), (6, 12), (8, 11), (7, 11), (6, 11)),
                  #exits={(5, 12): 6, (9, 10): 2}),
            #Board(size=(5, 3), exits={(5, 2): 5}),
            #Board(size=(14, 10), exits={((13, 0), 0): 4}, furniture_free=False),
            #Board(size=(14, 10), exits={(2, 0): 4}, furniture_free=False),
            #Board(size=(14, 4),
                  #exits={(0, 1): 4, (0, 2): 4, (0, 3): 4, (0, 4): 4, (14, 3): 11, (14, 1): 11, (14, 2): 11, (14, 4): 11,
                         #(11, 4): 7}),
            #Board(size=(5, 10), exits={(3, 0): 9}),
            #Board(size=(14, 4),
                  #exits={(0, 1): 9, (0, 2): 9, (0, 3): 9, (0, 4): 9, (14, 3): 14, (14, 2): 14, (3, 4): 12, (8, 4): 13}),
            #Board(size=(7, 10), exits={(4, 0): 11}),
            #Board(size=(14, 10), exits={(2, 0): 11}, furniture_free=False),
            #Board(size=(14, 16), except_cell=((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                                              #(0, 13), (0, 14), (0, 15), (1, 13), (1, 14), (1, 15), (2, 13), (2, 14),
                                              #(2, 15), (3, 13), (3, 14), (3, 15), (4, 13), (4, 14), (4, 15),
                                              #(11, 15), (8, 15), (9, 15), (10, 15), (12, 15), (13, 15), (8, 0), (9, 0),
                                              #(10, 0), (11, 0), (12, 0), (13, 0),
                                              #(8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (8, 2), (9, 2),
                                              #(10, 2), (11, 2), (12, 2), (13, 2),
                                              #(8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (8, 4), (9, 4),
                                              #(10, 4), (11, 4), (12, 4), (13, 4)),
                  #exits={(3, 0): 20, (0, 11): 11, (0, 12): 11, (7, 16): 12, (13, 15): 20})
            #]

