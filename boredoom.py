import pygame
import sys
import data.engine as e
Clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()

# Window essentials -----------------------------------------------------------
WIN_SIZE = 960, 520
screen = pygame.display.set_mode(WIN_SIZE, 0, 32)
display = pygame.Surface((480, 260))
pygame.display.set_caption('BoreDoom v0.1')
boredoom_icon = pygame.image.load('data/images/boredoom.png').convert()
boredoom_icon.set_colorkey((0, 0, 0))
pygame.display.set_icon(boredoom_icon)

# Tile Stuff ------------------------------------------------------------------
tile_size = 32
test_img = pygame.image.load('data/images/test_img.png').convert()
test_img.set_colorkey((255, 0, 255))
tile_index = {1: test_img}

# Map Stuff -------------------------------------------------------------------
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

# Player Stuff ----------------------------------------------------------------
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]
e.load_animations('data/images/entities/')
player = e.entity(100, 100, 9, 12, 'player')

# Other Stuff -----------------------------------------------------------------
bg_color = (76, 64, 102)
player_jump = 0

while True:  # While loop
    display.fill(bg_color)

    # Scroll Stuff ------------------------------------------------------------
    true_scroll[0] += (player.x-true_scroll[0]-152)/20
    true_scroll[1] += (player.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # Tile thingy things ------------------------------------------------------
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(test_img, (x * tile_size, y * tile_size))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1

    # Player movement ---------------------------------------------------------

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 3
    if moving_left:
        player_movement[0] -= 3
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 5:
        player_y_momentum = 5

    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_action('run')
        player.set_flip(False)
    if player_movement[0] < 0:
        player.set_action('run')
        player.set_flip(True)

    collision_types = player.move(player_movement, tile_rects)

    if collision_types['bottom']:
        player_y_momentum = 0
        air_timer = 0
        player_jump = 0
    else:
        air_timer += 1

    if player_jump == 1:
        player.set_action('jump')

    player.change_frame(1)
    player.display(display, scroll)

    for event in pygame.event.get():  # Event loop ----------------------------
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 6:
                    player_y_momentum = -7
                    player_jump = 1
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WIN_SIZE), (0, 0))
    pygame.display.update()
    Clock.tick(60)
