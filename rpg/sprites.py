
from config import *
import math

global screen


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey('black')
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, screen):

        self.screen = screen
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.facing = 'down'

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.char_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.animation_loop = 1

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.draw_healthbar(player_health)

        self.down_animations = [self.game.char_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.char_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.char_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.char_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.char_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.char_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.char_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.char_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.char_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.char_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.char_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.char_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def movement(self):
        keys = pygame.key.get_pressed()
        release = True
        if keys[pygame.K_LEFT] and release:
            release = False
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed

            self.x_change -= player_speed +2
            self.facing = 'left'

        if keys[pygame.K_RIGHT] and release:
            release = False
            for sprite in self.game.all_sprites:
                sprite.rect.x -= player_speed

            self.x_change += player_speed+2
            self.facing = 'right'

        if keys[pygame.K_UP] and release:
            release = False
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed

            self.y_change -= player_speed+2
            self.facing = 'up'

        if keys[pygame.K_DOWN] and release:
            release = False
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed

            self.y_change += player_speed+2
            self.facing = 'down'
        release = True

    def collide_enemy(self, direction, player_health):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.enemy, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.rect.x = self.rect.x - 32
                    player_health -= 15
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += 32

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    self.rect.x = self.rect.x + 32
                    player_health -= 15
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= 32

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.enemy, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.rect.y = self.rect.y - 32
                    player_health -= 15
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += 32

                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    self.rect.y = self.rect.y + 32
                    player_health -= 15
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= 32

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += player_speed

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= player_speed

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed

    def update(self):
        self.draw_healthbar(player_health)
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_enemy('x', player_health)
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_enemy('y', player_health)
        self.collide_blocks('y')
        self.draw_healthbar(player_health)
        
        self.x_change = 0
        self.y_change = 0
        pygame.display.update()

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.char_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.game.char_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.game.char_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.game.char_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def draw_healthbar(self, player_health):
        health = (player_health/200*100/3.5)
        rect = self.rect
        pygame.draw.rect(self.screen, 'black', ((rect.x - 1, rect.y - 14), (34, 10)))
        pygame.draw.rect(self.screen, grey, ((rect.x, rect.y-13), (32, 8)))
        pygame.draw.rect(self.screen, 'red', ((rect.x+2, rect.y - 12), (28, 6)))
        pygame.draw.rect(self.screen, 'green', ((rect.x + 2, rect.y - 12), (health, 6)))
        if player_health <= 0:
            pygame.quit()
            exit()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, screen):

        self.screen = screen
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.enemy
        self.animation_loop = 0
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.facing = 'down'
        self.x_change = 0
        self.y_change = 0

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        surface = pygame.image.load('/home/leo/code/rpg/images/sight.png')
        surface = pygame.transform.scale(surface, (96*2+32, 96*2+32))
        self.sight = surface.get_rect(center=(self.rect.x, self.rect.y))

    def animate(self):

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.char_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.game.char_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.game.char_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.game.char_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def esight(self):
        surface = pygame.image.load('/home/leo/code/rpg/images/sight.png')
        surface = pygame.transform.scale(surface, (96*2+32, 96*2+32))
        self.sight = surface.get_rect(center=(self.rect.x, self.rect.y))

    def move(self):
        if self.sight.colliderect(self.game.player.rect):
            x_dis = (self.sight.x/self.game.player.rect.x)
            y_dis = (self.sight.y/self.game.player.rect.y)
            print(x_dis, y_dis)

    def update(self):
        self.esight()
        self.move()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terr_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = None
        self.rect = None

    def grass(self):
        self.image = self.game.terr_spritesheet.get_sprite(352, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def cliffl(self):
        self.image = self.game.terr_spritesheet.get_sprite(986, 288, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def cliffd(self):
        self.image = self.game.terr_spritesheet.get_sprite(986, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def desert_ground(self):
        self.image = self.game.terr_spritesheet.get_sprite(64, 160, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def rock(self):
        self.image = self.game.terr_spritesheet.get_sprite(32, 32, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def green_ground(self):
        self.image = self.game.terr_spritesheet.get_sprite(32, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
