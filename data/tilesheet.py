import pygame


class Tilesheet:
    def __init__(self, filename, width, height, rows, cols):
        image = pygame.image.load(filename).convert()
        image.set_colorkey((255, 0, 255))
        self.tile_table = []
        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, rows):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))

    def get_tile(self, x, y):
        return self.tile_table[x][y]

    def draw(self, screen):
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x * 16, y * 16))
