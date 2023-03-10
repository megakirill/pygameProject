import os
import pygame



def load_image_start(name, colorkey=None):
    fullname = os.path.join('data_for_menu', name)
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

def menu():
    pygame.init()
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('2d game')
    screen.fill((221, 160, 221))

    #pygame.draw.rect(screen, (152, 251, 152), (350, 300, 300, 100))

    pygame.display.flip()

    # Подгрузка картинок с текстом

    text = pygame.image.load('data_for_menu/text.png')
    text = pygame.transform.scale(text, (300, 75))
    text_a = text.get_rect(bottomright=(645, 400))

    hero = pygame.image.load('data_for_menu/hero.png')
    hero = pygame.transform.scale(hero, (60, 60))

    screen.blit(hero, (200, 500))
    screen.blit(text, text_a)
    pygame.display.flip()
    running = True
    while running:
        screen.blit(text, text_a)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # При наведении кнокпи с текстом выделяются
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 325 and pos[1] <= 400:
                    running = False
                    screen.fill((221, 160, 221))
                    menu = load_image_start('menu.png', (171, 214, 54))
                    menu_a = menu.get_rect(bottomright=(765, 200))
                    screen.blit(menu, menu_a)

                    easy = load_image_start('easy.png')
                    easy_a = easy.get_rect(bottomright=(650, 300))
                    screen.blit(easy, easy_a)

                    medium = load_image_start('medium.png')
                    medium_a = easy.get_rect(bottomright=(650, 450))
                    screen.blit(medium, medium_a)

                    hard = load_image_start('hard.png')
                    hard_a = easy.get_rect(bottomright=(650, 600))
                    screen.blit(hard, hard_a)
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 325 and pos[1] <= 400:
                    text = pygame.image.load('data_for_menu/mouse_text.png')
                    text = pygame.transform.scale(text, (300, 75))
                    text_a = text.get_rect(bottomright=(645, 400))
                    screen.blit(text, text_a)
                else:
                    text = pygame.image.load('data_for_menu/text.png')
                    text = pygame.transform.scale(text, (300, 75))
                    text_a = text.get_rect(bottomright=(645, 400))
        pygame.display.flip()
    level = ''
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 210 and pos[1] <= 300:
                    running = True
                    screen.fill((221, 160, 221))
                    level = 'easy'
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 350 and pos[1] <= 450:
                    running = True
                    screen.fill((221, 160, 221))
                    level = 'medium'
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 500 and pos[1] <= 600:
                    running = True
                    screen.fill((221, 160, 221))
                    level = 'hard'
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 210 and pos[1] <= 300:
                    easy = load_image_start('mouse_easy.png')
                    easy_a = easy.get_rect(bottomright=(650, 300))
                    screen.blit(easy, easy_a)
                else:
                    easy = load_image_start('easy.png')
                    easy_a = easy.get_rect(bottomright=(650, 300))
                    screen.blit(easy, easy_a)
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 350 and pos[1] <= 450:
                    medium = load_image_start('mouse_medium.png')
                    medium_a = easy.get_rect(bottomright=(650, 450))
                    screen.blit(medium, medium_a)
                else:
                    medium = load_image_start('medium.png')
                    medium_a = easy.get_rect(bottomright=(650, 450))
                    screen.blit(medium, medium_a)
                if pos[0] >= 340 and pos[0] <= 645 and pos[1] >= 500 and pos[1] <= 600:
                    hard = load_image_start('mouse_hard.png')
                    hard_a = easy.get_rect(bottomright=(650, 600))
                    screen.blit(hard, hard_a)
                else:
                    hard = load_image_start('hard.png')
                    hard_a = easy.get_rect(bottomright=(650, 600))
                    screen.blit(hard, hard_a)
        pygame.display.flip()
    return level


# создание послесмертного меню
def finish_menu(screen):
    pygame.draw.rect(screen, (192, 64, 0), (400, 200, 175, 245))
    # отрисовка меню
    f1 = pygame.font.Font(None, 25)
    text1 = f1.render('Меню', True,
                      (252, 168, 159))
    f2 = pygame.font.Font(None, 25)
    text2 = f1.render('Играть заново', True,
                      (252, 168, 159))
    f3 = pygame.font.Font(None, 25)
    text3 = f1.render('Выйти в меню', True,
                      (252, 168, 159))
    f4 = pygame.font.Font(None, 25)
    text4 = f1.render('Выйти из игры', True,
                      (252, 168, 159))

    screen.blit(text1, (467, 235))
    screen.blit(text4, (428, 370))
    pygame.display.flip()
    while True:
        pygame.draw.rect(screen, (192, 64, 0), (400, 200, 175, 245))
        f1 = pygame.font.Font(None, 25)
        text1 = f1.render('Меню', True,
                          (252, 168, 159))
        # Отрисовка текста кнопок
        screen.blit(text1, (467, 235))
        screen.blit(text2, (427, 290))
        screen.blit(text3, (427, 330))
        screen.blit(text4, (428, 370))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                # При наведении на кнопку она загорается, красиво
                if pos[0] > 425 and pos[1] > 286 and pos[0] < 549 and pos[1] < 307:
                    f2 = pygame.font.Font(None, 25)
                    text2 = f1.render('Играть заново', True,
                                      (255, 216, 212))
                else:
                    f2 = pygame.font.Font(None, 25)
                    text2 = f1.render('Играть заново', True,
                                      (252, 168, 159))
                if pos[0] > 426 and pos[1] > 330 and pos[0] < 547 and pos[1] < 347:
                    f3 = pygame.font.Font(None, 25)
                    text3 = f1.render('Выйти в меню', True,
                                      (255, 216, 212))
                else:
                    f3 = pygame.font.Font(None, 25)
                    text3 = f1.render('Выйти в меню', True,
                                      (252, 168, 159))
                if pos[0] > 426 and pos[1] > 370 and pos[0] < 553 and pos[1] < 384:
                    f4 = pygame.font.Font(None, 25)
                    text4 = f1.render('Выйти из игры', True,
                                      (255, 216, 212))
                else:
                    f4 = pygame.font.Font(None, 25)
                    text4 = f1.render('Выйти из игры', True,
                                      (252, 168, 159))
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Проверка на нажатие кнопки
                if pos[0] > 426 and pos[1] > 370 and pos[0] < 553 and pos[1] < 384:
                    # выход из игры
                    pygame.quit()
                if pos[0] > 425 and pos[1] > 286 and pos[0] < 549 and pos[1] < 307:
                    # по нажатию кнопки игра возобновляется
                    return -1
        pygame.display.flip()