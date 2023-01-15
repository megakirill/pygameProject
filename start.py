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

    arrow = pygame.image.load('data_for_menu/i.png')
    arrow = pygame.transform.scale(arrow, (150, 75))
    arrow.set_colorkey((255, 255, 255))
    arrow_left = arrow.get_rect(bottomright=(400, 200))

    #pygame.draw.rect(screen, (152, 251, 152), (350, 300, 300, 100))

    pygame.display.flip()

    text = pygame.image.load('data_for_menu/text.png')
    text = pygame.transform.scale(text, (300, 75))
    text_a = text.get_rect(bottomright=(645, 400))

    hero = pygame.image.load('data_for_menu/hero.png')
    hero = pygame.transform.scale(hero, (60, 60))

    screen.blit(hero, (200, 500))
    screen.blit(arrow, arrow_left)
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
