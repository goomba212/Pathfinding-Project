import pygame
sw, sh = 800, 480
clock = pygame.time.Clock()
player_health = 200
button_shape = [(0, 0), (100, 0), (130, 50), (0, 50), (0, 45)]
tile_size = 32
player_speed = 3
player_layer = 4
enemy_layer = 3
ground_layer = 1
block_layer = 2
green = (0, 155, 0)
grey = (200, 200, 200)
tilemap = [

    '          BBBBBBBBBBBBBBBBBB....BB',
    '          B.....................BB',
    '          B.....................BB',
    '          B.....................BB',
    'CBBBBBBBBBB.....BBBBBBBBBBBBBBBB',
    'CB.....,,................B',
    'CB....E.,,.....,,,.......B',
    'CBBBBBB............B...BBB',
    'CB..........P............B',
    'CB...,,..................B',
    'CB........B........E.....B',
    'CB..,,....B.......,,.....B',
    'CB...,,...BBBBBB.........B',
    'CB..................,....B',
    'CBBBBB.............,,,...B',
    'CB.....,,............,,..B',
    'CB..E,,,......BBBB....E.,B',
    'CB.................,,....B',
    'CBBBBBBBBBBBBBBBBBBBBBBBBB',
    '.FFFFFFFFFFFFFFFFFFFFFFFF.',
]
print(len(tilemap))
