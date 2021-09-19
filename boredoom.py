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
pygame.display.set_caption('BoreDoom v3.5')
boredoom_icon = pygame.image.load('data/images/boredoom.png').convert()
boredoom_icon.set_colorkey((0, 0, 0))
pygame.display.set_icon(boredoom_icon)

# Tile Stuff -------------------------------------------------------------- #
tile_size = 16
test_img = pygame.image.load('data/images/test_img.png').convert()
test_img.set_colorkey((255, 0, 255))

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

# Other Stuff ------------------------------------------------------------- #
bg_color = (76, 64, 102)
touching_floor = 1
framerate = 60
screen_shake = 0
game_map_level = ()
framerate = 60
coord_map = [0, 0]
click = False

# Main menu Loop -------------------------------------------------------------- #
def main_menu():
    global click
    global framerate
    global game_map_level
    bg_color = (76, 64, 102)
    while True:
        screen.fill(bg_color)

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.image.load('data/images/buttons/level_select.png').convert()
        button_1.set_colorkey((0, 0, 0))
        button_2 = pygame.image.load('data/images/buttons/exit.png').convert()
        button_2.set_colorkey((0, 0, 0))
        button_3 = pygame.image.load('data/images/buttons/options.png').convert()
        button_3.set_colorkey((0, 0, 0))
        button_1_rect = pygame.Rect(380, 300, 200, 50)
        button_2_rect = pygame.Rect(380, 450, 200, 50)
        button_3_rect = pygame.Rect(380, 375, 200, 50)
        if button_1_rect.collidepoint((mx, my)):
            if click:
                level_select()
        if button_2_rect.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_3_rect.collidepoint((mx, my)):
            if click:
                options()
        screen.blit(pygame.transform.scale(button_1, (200, 50)), (380, 300))
        screen.blit(pygame.transform.scale(button_3, (200, 50)), (380, 375))
        screen.blit(pygame.transform.scale(button_2, (200, 50)), (380, 450))

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
    wait = 0
    while running:
        screen.fill(bg_color)
        wait += 1

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.image.load('data/images/buttons/fps_60.png').convert()
        button_1.set_colorkey((0, 0, 0))
        button_2 = pygame.image.load('data/images/buttons/fps_75.png').convert()
        button_2.set_colorkey((0, 0, 0))
        button_3 = pygame.image.load('data/images/buttons/menu.png').convert()
        button_3.set_colorkey((0, 0, 0))
        button_1_rect = pygame.Rect(380, 100, 200, 50)
        button_2_rect = pygame.Rect(380, 200, 200, 50)
        button_3_rect = pygame.Rect(380, 300, 200, 50)
        if button_1_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    framerate = 60
                    running = False
                    wait = 0
        if button_2_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    framerate = 75
                    running = False
                    wait = 0
        if button_3_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    running = False
                    wait = 0
        screen.blit(pygame.transform.scale(button_1, (200, 50)), (380, 100))
        screen.blit(pygame.transform.scale(button_2, (200, 50)), (380, 200))
        screen.blit(pygame.transform.scale(button_3, (200, 50)), (380, 300))

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

# Options menu Loop ----------------------------------------------------------- #
def level_select():
    global click
    global game_map_level
    global coord_map
    bg_color = (76, 64, 102)
    running = True
    wait = 0
    while running:
        screen.fill(bg_color)
        wait += 1

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.image.load('data/images/buttons/level_1.png').convert()
        button_1.set_colorkey((0, 0, 0))
        button_2 = pygame.image.load('data/images/buttons/level_2.png').convert()
        button_2.set_colorkey((0, 0, 0))
        button_3 = pygame.image.load('data/images/buttons/menu.png').convert()
        button_3.set_colorkey((0, 0, 0))
        button_1_rect = pygame.Rect(380, 100, 200, 50)
        button_2_rect = pygame.Rect(380, 200, 200, 50)
        button_3_rect = pygame.Rect(380, 300, 200, 50)
        if button_1_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    game_map_level = 'data/game_map'
                    coord_map[0] = 64
                    coord_map[1] = 118
                    game()
                    wait = 0
        if button_2_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    game_map_level = 'data/game_map_2'
                    coord_map[0] = 64
                    coord_map[1] = 234
                    game()
                    wait = 0
        if button_3_rect.collidepoint((mx, my)):
            if wait > 13:
                if click:
                    running = False
                    wait = 0
        screen.blit(pygame.transform.scale(button_1, (200, 50)), (380, 100))
        screen.blit(pygame.transform.scale(button_2, (200, 50)), (380, 200))
        screen.blit(pygame.transform.scale(button_3, (200, 50)), (380, 300))

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
    global screen_shake, test_sound_timer, touching_floor, framerate

    # Player Stuff ------------------------------------------------------------ #
    moving_right = False
    moving_left = False
    player_y_momentum = 0
    air_timer = 0
    true_scroll = [0, 0]
    e.load_animations('data/images/entities/')
    player = e.entity(coord_map[0], coord_map[1], 11, 13, 'player')
    running = True
    double_jump = 0

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

    game_map = load_map(game_map_level)

    while running:
        display.fill(bg_color)

        # Scroll Stuff ---------------------------------------------------- #
        true_scroll[0] += (player.x - true_scroll[0] - 120) / 20
        true_scroll[1] += (player.y - true_scroll[1] - 75) / 5
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
            if touching_floor == 1:
                player.set_action('idle')
            if touching_floor == 0:
                if player_movement[1] > 0:
                    player.set_action('fall')
                if player_movement[1] < 0:
                    player.set_action('jump')
        if player_movement[0] > 0:
            player.set_flip(False)
            if touching_floor == 1:
                player.set_action('run')
            if touching_floor == 0:
                if player_movement[1] > 0:
                    player.set_action('fall')
                if player_movement[1] < 0:
                    player.set_action('jump')
        if player_movement[0] < 0:
            player.set_flip(True)
            if touching_floor == 1:
                player.set_action('run')
            if touching_floor == 0:
                if player_movement[1] > 0:
                    player.set_action('fall')
                if player_movement[1] < 0:
                    player.set_action('jump')
        if touching_floor == 0:
            if player_movement[1] > 0:
                player.set_action('fall')
            if player_movement[1] < 0:
                player.set_action('jump')

        # Sound stuff ----------------------------------------------------- #
        if test_sound_timer > 0:
            test_sound_timer -= 1

        # Collision stuff ------------------------------------------------- #
        collision_types = player.move(player_movement, tile_rects)

        if collision_types['bottom']:
            double_jump = 0
            touching_floor = 1
            player_y_momentum = 1
            air_timer = 0
            if player_movement[0] != 0:
                if test_sound_timer == 0:
                    test_sound_timer = 12
                    random.choice(test_sound).play()
        else:
            if collision_types['top']:
                player_y_momentum = 0
            air_timer += 1
            touching_floor = 0

        if double_jump == 2:
            double_jump += 1
            player_y_momentum = -5.75
            jump_sound.play()

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
                    double_jump += 1
                    if air_timer < 6:
                        player_y_momentum = -5.75
                        touching_floor = 0
                        jump_sound.play()
                if event.key == K_ESCAPE:
                    # pygame.mixer.music.fadeout(1000)
                    running = False
                if event.key == K_e:
                    screen_shake = 30
                if event.key == K_q:
                    framerate = 10
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_q:
                    framerate = 60

        if screen_shake > 0:
            screen_shake -= 1

        screen.blit(pygame.transform.scale(display, WIN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(framerate)

main_menu()
