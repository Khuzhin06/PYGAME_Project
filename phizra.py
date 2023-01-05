import pygame


FPS = 50  # количество кадров в секунду
SIZE = WIDTH, HEIGHT = 720, 420


class PHIZRA:
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
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.cell_size_x = cell_size * 3
        self.cell_size_y = cell_size // 3

    def render(self,  screen):
        end_x = self.width * self.cell_size_x + self.left
        end_y = self.height * self.cell_size_y + self.top
        for x in range(self.left, end_x, self.cell_size_x):
            for y in range(self.top, end_y, self.cell_size_y):
                pygame.draw.rect(
                    screen,
                    'white',
                    (x, y, self.cell_size_x, self.cell_size_y),
                    width=1
                )


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def phizra():
    pygame.display.set_caption('Клетчатое поле начало')
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    running = True

    # поле 5 на 7
    board = PHIZRA(3, 15)
    board.set_view(0, 0, 80)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        draw_text(screen, str('Заполните поле полностью белым'), 35, WIDTH / 2, 570)

        screen.fill('black')
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    phizra()
    pygame.quit()
