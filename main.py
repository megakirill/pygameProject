import os
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2d game')

# функция загрузки изображения
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


# сторона плитки
tile_size = 50
# закончилась ли игра
game_over = False


class Player():
    def __init__(self, x, y):
        # список для картинок персонажа, направленных в правую сторону
        self.right_imgs = []
        # список для картинок персонажа, направленных в левую сторону
        self.left_imgs = []
        # индекс картинки, которую нужно выбрать (для анимации)
        self.img_index = 0
        # контроль скорости смены картинок в анимации
        self.speed_control = 0
        for num in range(1, 5):
            player_img_r = load_image(f'pers{num}.png', 'black')
            player_img_r = pygame.transform.scale(player_img_r, (40, 40))
            player_img_l = pygame.transform.flip(player_img_r, True, False)
            self.right_imgs.append(player_img_r)
            self.left_imgs.append(player_img_l)
        self.ghost_img = load_image('ghost.png', 'black')
        self.ghost_img = pygame.transform.scale(self.ghost_img, (30, 40))

        self.player_img = self.right_imgs[self.img_index]
        self.rect = self.player_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_width = self.player_img.get_width()
        self.player_height = self.player_img.get_height()

        self.velocity_y = 0
        # проверка на то, в какую сторону смотрит персонаж (по умолчанию: вправо)
        self.is_right = True
        self.is_jumped = False

    def update(self, game_over):
        delta_x = 0
        delta_y = 0

        if game_over == False:
            # обработка нажатий клавиш движения
            event = pygame.key.get_pressed()

            if event[pygame.K_LEFT]:
                delta_x -= 5
                self.speed_control += 1
                self.is_right = False
            if event[pygame.K_RIGHT]:
                delta_x += 5
                self.speed_control += 1
                self.is_right = True
            if event[pygame.K_SPACE] and self.is_jumped == False:
                self.velocity_y -= 13
                self.is_jumped = True
            if event[pygame.K_SPACE] == False:
                self.is_jumped = False
            if event[pygame.K_LEFT] == False and event[pygame.K_RIGHT] == False:
                self.speed_control = 0
                self.img_index = 0
                if self.is_right:
                    self.player_img = self.right_imgs[0]
                else:
                    self.player_img = self.left_imgs[0]

            # добавление анимации персонажу
            if self.speed_control > 7:
                self.speed_control = 0
                self.img_index += 1
                if self.img_index >= 4:
                    self.img_index = 0
                if self.is_right:
                    self.player_img = self.right_imgs[self.img_index]
                if self.is_right == False:
                    self.player_img = self.left_imgs[self.img_index]

            # гравитация
            self.velocity_y += 1
            if self.velocity_y > 10:
                self.velocity_y = 10
            delta_y += self.velocity_y

            # проверка на пересечения/взаимодействия
            for tile in level.tile_list:
                # проверка по x-у
                if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.player_width, self.player_height):
                    delta_x = 0

                # проверка по y-ку
                if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.player_width, self.player_height):
                    if self.velocity_y < 0:
                        delta_y = tile[1].bottom - self.rect.top
                        self.velocity_y = 0
                    elif self.velocity_y >= 0:
                        delta_y = tile[1].top - self.rect.bottom
                        self.velocity_y = 0

            # проверка на взаимодействия с мобами
            if pygame.sprite.spritecollide(self, mob_group, False):
                game_over = True

            # проверка на взаимодействия с шипами
            if pygame.sprite.spritecollide(self, spikes_group, False):
                game_over = True

            # обновление координат
            self.rect.x += delta_x
            self.rect.y += delta_y

            # контроль того чтобы персонаж не выходил за пределы экрана
            if self.rect.right > width:
                self.rect.right = width
                delta_x = 0
            if self.rect.left < 0:
                self.rect.left = 0
                delta_x = 0
            if self.rect.bottom > height:
                self.rect.bottom = height
                delta_y = 0
        elif game_over:
            self.player_img = self.ghost_img
            if self.rect.y > 200:
                self.rect.y -= 5
        screen.blit(self.player_img, self.rect)

        return game_over


# создание монстра
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('mob.png', 'white')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = 1
        self.control_move = 0

    def update(self):
        # движения монстра
        self.rect.x += self.move_speed
        self.control_move += 1
        if abs(self.control_move) > 50:
            self.move_speed *= -1
            self.control_move *= -1


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('spike.png', 'black')
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# класс для создания уровня
class Level():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = load_image('chocoMid.png', 'black')
        dirt_img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
        grass_img = load_image('chocoCenter.png')
        grass_img = pygame.transform.scale(grass_img, (tile_size, tile_size))
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img_rect = dirt_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (dirt_img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img_rect = dirt_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (grass_img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    mob = Mob(col_count * tile_size, row_count * tile_size + 13)
                    mob_group.add(mob)
                if tile == 4:
                    spikes = Spikes(col_count * tile_size, row_count * tile_size + 25)
                    spikes_group.add(spikes)
                col_count += 1
            row_count += 1

    def create(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# список с элементами для создания уровня
# 0 - пустая клетка, 1 - клетка с землей, 2 - клетка с грязью, 3 - монстр
level_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 1, 2, 4, 4, 4, 4, 4, 4, 2, 1, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]

player = Player(100, height - 175)
mob_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
level = Level(level_data)

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

    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((128, 166, 255))
    screen.blit(sun, (20, 20))
    screen.blit(cloud, (100, 20))
    screen.blit(cloud2, (500, 80))
    screen.blit(cloud3, (800, 50))
    screen.blit(cloud4, (200, 50))
    level.create()
    if game_over == False:
        mob_group.update()
    mob_group.draw(screen)
    spikes_group.draw(screen)

    game_over = player.update(game_over)

    pygame.display.update()
pygame.quit()
