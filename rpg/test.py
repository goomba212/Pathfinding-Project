import pygame

sw, sh = 600, 600
screen = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()
x, y = 0, 0
button_shape = ((0+x, 0+y), (100+x, 0+y), (130+x, 50+y), (0+x, 50+y), (0+x, 45+y))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill('black')

    x, y = 100, 100
    button_shape = ((0 + x, 0 + y), (100 + x, 0 + y), (130 + x, 50 + y), (0 + x, 50 + y), (0 + x, 45 + y))
    pygame.draw.polygon(screen, 'green', (button_shape))
    pygame.display.update()
    clock.tick(60)
