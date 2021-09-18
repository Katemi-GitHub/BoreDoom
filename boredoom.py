import pygame
import sys
import random
import data.engine as e
clock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Window essentials ----------------------------------------------------------- #
WIN_SIZE = 960, 520
surface = (960 / 4, 520 / 4)
screen = pygame.display.set_mode(WIN_SIZE, 0, 32)
display = pygame.Surface(surface)
pygame.display.set_caption('BoreDoom v3.4')
boredoom_icon = pygame.image.load('data/images/boredoom.png').convert()
boredoom_icon.set_colorkey((0, 0, 0))
pygame.display.set_icon(boredoom_icon)

# Font ------------------------------------------------------------------------ #
font = pygame.font.SysFont(None, 32)
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Stuff ----------------------------------------------------------------------- #
framerate = 60
click = False

# Main menu Loop -------------------------------------------------------------- #
def main_menu():
    global click
    global framerate
    bg_color = (76, 64, 102)
    while True:
        screen.fill(bg_color)
        draw_text('Main Menu Beta v3.4', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.image.load('data/images/start.png').convert()
        button_1.set_colorkey((0, 0, 0))
        button_2 = pygame.image.load('data/images/options.png').convert()
        button_2.set_colorkey((0, 0, 0))
        button_1_rect = pygame.Rect(50, 100, 200, 50)
        button_2_rect = pygame.Rect(50, 200, 200, 50)
        if button_1_rect.collidepoint((mx, my)):
            if click:
                game()
        if button_2_rect.collidepoint((mx, my)):
            if click:
                options()
        screen.blit(pygame.transform.scale(button_1, (200, 50)), (50, 100))
        screen.blit(pygame.transform.scale(button_2, (200, 50)), (50, 200))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(framerate)

# Options menu Loop ----------------------------------------------------------- #
def options():
    global click
    global framerate
    bg_color = (76, 64, 102)
    running = True
    while running:
        screen.fill(bg_color)
        draw_text('Options Beta v3.4 (To do...)', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                framerate = 60
        if button_2.collidepoint((mx, my)):
            if click:
                framerate = 75
        if button_3.collidepoint((mx, my)):
            if click:
                main_menu()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(framerate)

# Game Loop ------------------------------------------------------------------- #
def game():
    running = True
    # Tile Stuff -------------------------------------------------------------- #
    tile_size = 16
    test_img = pygame.image.load('data/images/test_img.png').convert()
    test_img.set_colorkey((255, 0, 255))

    # Player Stuff ------------------------------------------------------------ #
    moving_right = False
    moving_left = False
    player_y_momentum = 0
    air_timer = 0
    player_jump = 0
    true_scroll = [0, 0]
    e.load_animations('data/images/entities/')
    player = e.entity(64, 118, 10, 13, 'player')

    # Sound Stuff ------------------------------------------------------------- #
    jump_sound = pygame.mixer.Sound('data/audio/jump.wav')
    test_sound = [pygame.mixer.Sound('data/audio/test_0.mp3'),
                  pygame.mixer.Sound('data/audio/test_1.mp3'),
                  pygame.mixer.Sound('data/audio/test_2.mp3')]
    test_sound[0].set_volume(0.4)
    test_sound[1].set_volume(0.4)
    test_sound[2].set_volume(0.4)
    test_sound_timer = 0

    # pygame.mixer.music.load('data/audio/music.wav')
    # pygame.mixer.music.play(-1)

    # Map Stuff --------------------------------------------------------------- #
    def load_map(path):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    game_map = load_map('data/game_map')

    # Other Stuff ------------------------------------------------------------- #
    bg_color = (76, 64, 102)
    touching_floor = 1
    framerate = 60
    screen_shake = 0

    while running:
        display.fill(bg_color)

        # Scroll Stuff ---------------------------------------------------- #
        true_scroll[0] += (player.x - true_scroll[0] - 120) / 20
        true_scroll[1] += (player.y - true_scroll[1] - 75) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        if screen_shake:
            scroll[0] += random.randint(0, 8) - 4
            scroll[1] += random.randint(0, 8) - 4

        # Tile thingy things ---------------------------------------------- #
        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(test_img, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                x += 1
            y += 1

        # Player movement ------------------------------------------------- #
        player_movement = [0, 0]
        if moving_right == True:
            player_movement[0] += 2.75
        if moving_left == True:
            player_movement[0] -= 2.75
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 5.75:
            player_y_momentum = 5.75

        if player_movement[0] == 0:
            player.set_action('idle')
        if player_movement[0] > 0:
            player.set_action('run')
            player.set_flip(False)
        if player_movement[0] < 0:
            player.set_action('run')
            player.set_flip(True)
        if player_y_momentum > 0:
            if touching_floor == 0:
                true_scroll[1] += (player.y - true_scroll[1] + 75) / 75

        # Sound stuff ----------------------------------------------------- #
        if test_sound_timer > 0:
            test_sound_timer -= 1

        # Collision stuff ------------------------------------------------- #
        collision_types = player.move(player_movement, tile_rects)

        if collision_types['bottom']:
            touching_floor = 1
            player_y_momentum = 0
            air_timer = 0
            player_jump = 0
            if player_movement[0] != 0:
                if test_sound_timer == 0:
                    test_sound_timer = 12
                    random.choice(test_sound).play()
        else:
            if collision_types['top']:
                player_y_momentum = 0
            if player_jump == 1:
                player.set_action('jump')
            air_timer += 1

        player.change_frame(1)
        player.display(display, scroll)

        for event in pygame.event.get():  # Event loop ------------------------ #
            if event.type == QUIT:
                # pygame.mixer.music.fadeout(1000)
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_SPACE:
                    if air_timer < 6:
                        player_jump = 1
                        player_y_momentum = -5.75
                        touching_floor = 0
                        jump_sound.play()
                if event.key == K_ESCAPE:
                    # pygame.mixer.music.fadeout(1000)
                    running = False
                if event.key == K_e:
                    screen_shake = 30
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False

        if screen_shake > 0:
            screen_shake -= 1

        screen.blit(pygame.transform.scale(display, WIN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(framerate)

main_menu()
