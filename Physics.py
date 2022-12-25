import pygame
from random import choice

FPS = 50  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 800, 400
FONT_NAME = pygame.font.match_font('arial')


class Physic:
    # создание поля
    def __init__(self, width):
        self.width = width
        self.board = [
            0 for _ in range(width)
        ]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.live = 3
        self.point = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        end_x = self.width * self.cell_size + self.left
        for x in range(self.left, end_x, self.cell_size):
            col = (x - self.left) // self.cell_size
            pygame.draw.rect(
                screen,
                'white',
                (x, 320, self.cell_size, self.cell_size),
                width=1
            )
            if self.board[col] == 'a':
                pygame.draw.line(
                    screen,
                    'blue',
                    (x + 4, 364),
                    (x + self.cell_size - 8, 320 + self.cell_size - 8),
                    width=2
                )
                pygame.draw.line(
                    screen,
                    'blue',
                    (x + 4, 364),
                    (x + self.cell_size - 8, 328),
                    width=2
                )
            if self.board[col] == 's':
                pygame.draw.line(
                    screen,
                    'yellow',
                    (x - 8 + self.cell_size, 324),
                    (x + self.cell_size // 2, 392),
                    width=2
                )
                pygame.draw.line(
                    screen,
                    'yellow',
                    (x + 8, 324),
                    (x + self.cell_size // 2, 392),
                    width=2
                )
            if self.board[col] == 'w':
                pygame.draw.line(
                    screen,
                    'green',
                    (x - 8 + self.cell_size, 392),
                    (x + self.cell_size // 2, 324),
                    width=2
                )
                pygame.draw.line(
                    screen,
                    'green',
                    (x + 8, 392),
                    (x + self.cell_size // 2, 324),
                    width=2
                )
            if self.board[col] == 'd':
                pygame.draw.line(
                    screen,
                    'red',
                    (x + 75, 364),
                    (x + 8, 320 + self.cell_size - 8),
                    width=2
                )
                pygame.draw.line(
                    screen,
                    'red',
                    (x + 75, 364),
                    (x + 8, 328),
                    width=2
                )
            if self.board[col] == 'Yes':
                pygame.draw.rect(
                    screen,
                    'green',
                    (x, 320, 80, 80),
                )
            elif self.board[col] == 'No':
                pygame.draw.rect(
                    screen,
                    'red',
                    (x, 320, 80, 80),
                )

    def turn_left(self):
        choi = choice(['a', 'w', 'd', 's'])
        if self.board[0] in ('d', 'w', 's', 'a'):
            self.live -= 1
        self.board.pop(0)
        self.board.append(choi)

    def click(self, a):
        if a == self.board[0]:
            self.board[0] = 'Yes'
            self.point += 10
        elif self.board[0] != 0 and self.board[0] != 'Yes' and self.board[0] != 'No':
            self.board[0] = 'No'
            self.live -= 1


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def physic():
    pygame.display.set_caption('химичка')
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    running = True

    # поле 5 на 7
    board = Physic(10)
    board.set_view(0, 320, 80)
    TURN_BOARD_EVENT = pygame.USEREVENT + 1
    TURN_BOARD_TIMER = 1000
    pygame.time.set_timer(TURN_BOARD_EVENT, TURN_BOARD_TIMER)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == TURN_BOARD_EVENT:
                board.turn_left()
                TURN_BOARD_TIMER -= 30
                if TURN_BOARD_TIMER <= 500:
                    TURN_BOARD_TIMER = 500
                pygame.time.set_timer(TURN_BOARD_EVENT, TURN_BOARD_TIMER)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            board.click('a')
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            board.click('d')
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            board.click('w')
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            board.click('s')

        if not board.live:
            running = False
        screen.fill('black')
        # screen.blit(background, background_rect)
        draw_text(screen, str(board.point), 18, WIDTH / 2, 10)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    physic()
    pygame.quit()
