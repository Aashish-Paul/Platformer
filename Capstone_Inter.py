#Adding platforms
import pygame
from pygame.locals import *

from os import path
import pickle

from pygame import mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

pygame.init()


 
clock = pygame.time.Clock()
fps = 60

level =0
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define game variables
tile_size = 35

game_over=0

score =0

main_menu=True


#load images
sun_img = pygame.image.load('Sun.png')
bg_img = pygame.image.load('Plat_Bg.png')



ss=pygame.image.load('START.png')
start_img = pygame.transform.scale(ss, (180, 60))
ee=pygame.image.load('EXIT.png')
exit_img = pygame.transform.scale(ee, (180, 60))

restart_img=pygame.image.load('RESTART.png')



font_score = pygame.font.SysFont("Bauhaus 93", 30)
font = pygame.font.SysFont("Bauhaus 93", 70)
white =(255,255,255)
blue =(0,0,255)

#pygame.mixer.music.load('music.wav')
#pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(0.5)
game_fx = pygame.mixer.Sound('game_over.wav')
game_fx.set_volume(0.5)

def draw_text(text, font, text_col, x,y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x,y))




def reset_level(level):
    player.reset(100, screen_height - 110)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    platform_group.empty()
    for i in range(0,8):
        if path.exists(f"L{i}"):
            pickle_in = open(f"L{i}", "rb")
            world_data = pickle.load(pickle_in)

    world = World(world_data)


    return world





class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked= False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action = True
                self.clicked=True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False



        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):

        self.reset(x, y)

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'Character {num}.png')
            img_right = pygame.transform.scale(img_right, (30, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()

        self.dead_image = pygame.image.load('Ghost.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y

        self.vel_y = 0
        self.jumped = False

        self.direction = 0

        self.in_air = True

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()

            # Jumping logic
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True

            if key[pygame.K_SPACE] == False:
                self.jumped = False

            # Moving left and right
            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1

            if key[pygame.K_d]:
                dx += 5
                self.direction = 1
                self.counter += 1

            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0

                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Gravity effect
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            self.in_air = True

            # Collision detection with tiles (platforms)
            for tile in world.tile_list:
                # Check horizontal collisions (left-right)
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Check vertical collisions (up-down)
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Falling or jumping: stop at the top of the platform or surface
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

                        #    check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

                        # game_over.play()
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Update player's position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text("GAME OVER!", font, blue, (screen_width // 2) - 180, (screen_width // 2))
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('Dirt.png')
        grass_img = pygame.image.load('Grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)


                if tile == 3:
                    blob=Enemy(col_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
#4
                if tile==4:
                    platform = Platform(col_count * tile_size, row_count * tile_size,1,0)
                    platform_group.add(platform)

                if tile==5:
                    platform = Platform(col_count * tile_size, row_count * tile_size,0,1)
                    platform_group.add(platform)
                    
                if tile==6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    lava_group.add(lava)

                if tile==7:
                    coin = Coin(col_count * tile_size+ (tile_size//2) , row_count * tile_size + (tile_size//2))
                    coin_group.add(coin) 
                
                if tile==8:
                    exit = Exit(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    exit_group.add(exit) 

                


                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('Blob.png')
        self.img = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_direction=1
        self.move_counter= 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=1
        if abs(self.move_counter) > 40:
            self.move_direction *=-1
            self.move_counter *= -1            

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Lava.png')
        self.image=pygame.transform.scale(img,(tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#1
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Half Grass Block.png')
        self.image=pygame.transform.scale(img,(tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction =1
        self.move_x =move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter +=1
        if abs(self.move_counter) > 40:
            self.move_direction *=-1
            self.move_counter *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Coin.png')
        self.image=pygame.transform.scale(img,(tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('EXIT.png')
        self.image=pygame.transform.scale(img,(tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y        

if path.exists(f"L{level}"):
    pickle_in = open(f"L{level}",'rb')
    world_data = pickle.load(pickle_in)
#world = World(world_data)



lava_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
#2
platform_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()
score_coin = Coin(tile_size//2, tile_size//2)
coin_group.add(score_coin)

world = World(world_data)

player = Player(100, screen_height - 110)



restart_button = Button(screen_width//2 - 50, screen_height//2 +100, restart_img)
start_button = Button(screen_width//2 - 250, screen_height//2 , start_img)
exit_button = Button(screen_width//2 + 50, screen_height//2 , exit_img)



run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:

        world.draw()

        if game_over==0:
            blob_group.update()
            platform_group.update()

            if pygame.sprite.spritecollide(player, coin_group, True):
                score +=1

                coin_fx.play()
            draw_text('X ' + str(score), font_score, white, tile_size+12, 5)



        lava_group.draw(screen)
        blob_group.draw(screen)
#3
        platform_group.draw(screen)
        coin_group.draw(screen)

        exit_group.draw(screen)
        
        game_over = player.update(game_over)
    
        if game_over== -1:
            if restart_button.draw():

                world_data=[]
                world=reset_level(level)
                game_over=0
                score=0

        if game_over == 1:
            level +=1
            if level <= 7:
                world_data=[]
                world=reset_level(level)
                game_over=0
            else:

                draw_text("YOU WIN!", font, blue, (screen_width//2)-110, (screen_width//2))
                if restart_button.draw():
                    level=1
                    world_data=[]
                    world=reset_level(level)
                    game_over=0
                    score=0

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()