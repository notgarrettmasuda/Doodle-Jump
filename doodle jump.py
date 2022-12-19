import pygame
import os
import random

pygame.init()
os.chdir('C:/users/garre/OneDrive/Documents/My Code/My Projects/doodle jump')

clock = pygame.time.Clock()
FPS = 60

#screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650

#show screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen title
pygame.display.set_caption('doodle jump')

#fonts
font = pygame.font.SysFont('Arial', 26)

#colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#images
#jumper
jumper_img = pygame.image.load(os.path.join("img", "jumper.png")).convert_alpha()
jumper_w = jumper_img.get_width()
jumper_h = jumper_img.get_height()
jumper_img = pygame.transform.scale(jumper_img, (jumper_w * 0.1, jumper_h * 0.1))
#tiles
g_rectangle_img = pygame.image.load(os.path.join("img", "g rectangle.jpg")).convert_alpha()
g_rect_w = g_rectangle_img.get_width()
g_rect_h = g_rectangle_img.get_height()
g_rectangle_img = pygame.transform.scale(g_rectangle_img, (g_rect_w * 0.1, g_rect_h * 0.1))
r_rectangle_img = pygame.image.load(os.path.join("img", "r rectangle.png")).convert_alpha()
r_rect_w = r_rectangle_img.get_width()
r_rect_h = r_rectangle_img.get_height()
r_rectangle_img = pygame.transform.scale(r_rectangle_img, (r_rect_w * 0.1, r_rect_h * 0.1))

#game variables
line = pygame.draw.line(screen, GREEN, (0, 550), (500, 550))

#text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Jumper(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.image = jumper_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_jump = False
        self.jumping = False
        self.jump_count = 15
        self.gravity = 1
        self.jumps = 0
    #handles jumper movement
    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - 10 > 0:
            self.rect.x -= 10
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + 10 + self.image.get_width() < SCREEN_WIDTH:
            self.rect.x += 10
        
        #jump mechanic
        if self.is_jump == False:
            self.rect.y += 2 * self.gravity
            if line.colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()) and self.jumps == 0 \
                or pygame.sprite.spritecollide(jumper, tile_group, False):
                self.is_jump = True
                self.rect.y == 2
                self.jumps += 1
                self.jumping = True
                
        else:   
            if self.jump_count >= 5:
                self.rect.y -= 25
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 15
                if self.gravity <= 5:
                    if self.jumps % 5 == 0:
                        self.gravity += 0.5
                else:
                    self.gravity = 5

    
    def draw(self):
        screen.blit(self.image, self.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #changes tile position
    def update(self):
        self.rect.x = random.randint(30, 400)
        self.rect.y = random.randint(200, 350)

    #draws tile on screen
    def draw(self):
        screen.blit(self.image, self.rect)

tile_group = pygame.sprite.Group()
fake_tile_group = pygame.sprite.Group()

#class instances
jumper = Jumper(250, 500)
tile = Tile(g_rectangle_img, 250, 500)
fake_tile = Tile(r_rectangle_img, 900, 900)

tile_group.add(tile)
fake_tile_group.add(fake_tile)

#game loop
run = True
while run:
    #framerate
    clock.tick(FPS)
    screen.fill(BLACK)
    if jumper.jumps == 0:
        pygame.draw.line(screen, GREEN, (0, 550), (500, 550))

    draw_text('Jumps: ' + f'{jumper.jumps}', font, GREEN, 0, 0)
    tile.draw()
    jumper.draw()
    fake_tile.draw()
    #main game instances
    if jumper.jumping == True:
        tile.kill()
        tile_group.empty()
        tile.update()
        tile.draw()
        tile_group.add(tile)
        jumper.jumping = False
        if jumper.jumps >= 30:
            fake_tile.kill()
            fake_tile_group.empty()
            fake_tile.update()
            fake_tile.draw()
            fake_tile_group.add(fake_tile)

    #detects game over
    if jumper.rect.y >= 650:
        draw_text('GAME OVER', font, RED, (SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT / 2)

    #game event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys_pressed = pygame.key.get_pressed()
    jumper.movement(keys_pressed)
    
    pygame.display.update()
pygame.quit()