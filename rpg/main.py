import pygame.key
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((sw, sh))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('images/Jersey25-Regular.ttf', 32)
        self.running = True

        self.player = None
        self.char_spritesheet = Spritesheet('images/character.png')
        self.terr_spritesheet = Spritesheet('images/terrain.png')
        self.enemy_spritesheet = Spritesheet('images/enemy.png')

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):

                if column == 'B':
                    Block(self, j, i)

                if column == 'P':
                    self.player = Player(self, j, i, self.screen)

                if column == ',':
                    gr = Ground(self, j, i)
                    gr.grass()

                if column == 'E':
                    Enemy(self, j, i, self.screen)

                if column == 'F':
                    gr = Ground(self, j, i)
                    gr.cliffd()

                if column == 'C':
                    gr = Ground(self, j, i)
                    gr.cliffl()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(green)
        self.all_sprites.draw(self.screen)
        self.clock.tick(60)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False


g = Game()
g.new()
g.create_tilemap()
while g.running:
    g.main()

pygame.quit()
sys.exit()
