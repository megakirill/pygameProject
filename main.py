import os
import random
import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        line_counter = 0
        for j in range(self.height):
            for i in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + (self.cell_size * i), self.top + (self.cell_size * line_counter),
                                  self.cell_size,
                                  self.cell_size), 1)
            line_counter += 1

    def on_click(self, cell):
        print(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        else:
            print(cell)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2d game')
board = Board(10, 8)
board.set_view(0, 0, 100)
# декор
sun = load_image('sunc.png', 'black')
sun = pygame.transform.scale(sun, (150, 150))
cloud = load_image('cloud.png', 'white')
cloud = pygame.transform.scale(cloud, (120, 120))
cloud2 = load_image('cloud2.png', 'white')
cloud2 = pygame.transform.scale(cloud2, (200, 150))
cloud3 = load_image('cloud3.png', 'white')
cloud3 = pygame.transform.scale(cloud3, (150, 120))
cloud4 = load_image('cloud4.png', 'white')
cloud4 = pygame.transform.scale(cloud4, (200, 150))
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((128, 166, 255))
    screen.blit(sun, (20, 20))
    screen.blit(cloud, (100, 20))
    screen.blit(cloud2, (500, 80))
    screen.blit(cloud3, (800, 50))
    screen.blit(cloud4, (200, 50))
    board.render(screen)
    pygame.display.update()
pygame.quit()
