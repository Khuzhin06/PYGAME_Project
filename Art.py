import pygame

FPS = 50
SIZE = WIDTH, HEIGHT = 560, 610
FONT_NAME = pygame.font.match_font('arial')


class Art:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [
            [0] * width for _ in range(height)
        ]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.win = False
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top

        self.cell_size = cell_size

    def render(self, screen):
        end_x = self.width * self.cell_size + self.left
        end_y = self.height * self.cell_size + self.top
        self.win = True
        for x in range(self.left, end_x, self.cell_size):
            col = (x - self.left) // self.cell_size
            for y in range(self.top, end_y, self.cell_size):
                row = (y - self.top) // self.cell_size
                if self.board[row][col] == 0:
                    width = 1
                    self.win = False
                elif self.board[row][col] == 1:
                    width = 0
                else:
                    raise Exception("Что-то пошло не так. В клетке поля хранится не 0 или 1")
                pygame.draw.rect(
                    screen,
                    'white',
                    (x, y, self.cell_size, self.cell_size),
                    width=width
                )

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is None:
            # Пользователь нажал мимо поля, поэтому ничего не делать
            return
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        mx, my = mouse_pos
        if mx <= self.left or mx >= self.width * self.cell_size + self.left:
            return
        if my <= self.top or my >= self.height * self.cell_size + self.top:
            return

        column = (mx - self.left) // self.cell_size
        row = (my - self.top) // self.cell_size
        return row, column

    def on_click(self, cell):
        print(cell)
        row, col = cell
        for i in range(7):
            for j in range(7):
                if row == i or col == j:
                    if self.board[i][j] == 0:
                        self.board[i][j] = 1
                    elif self.board[i][j] == 1:
                        self.board[i][j] = 0
                    else:
                        raise Exception("Что-то пошло не так. В клетке поля хранится не 0 или 1")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def art():
    pygame.display.set_caption('художник')
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    running = True

    # поле 5 на 7
    board = Art(7, 7)
    board.set_view(0, 0, 80)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        if board.win:
            running = False
        screen.fill('black')
        draw_text(screen, str('Заполните поле полностью белым'), 35, WIDTH / 2, 570)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    art()
    pygame.quit()
