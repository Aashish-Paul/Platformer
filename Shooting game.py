from time import sleep

import pygame
import random


pygame.init()
pygame.font.init()
font1 = pygame.font.SysFont('freesansbold.ttf',40)
walls = [(70, 0, 50, 360),(160, 260, 50, 360),(250, 0, 50, 360),(340, 260, 50, 360),(430, 0, 50, 360),(520, 260, 50, 360), (610, 0, 50, 360)]
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0, 0)
GREEN = (0,255,0)
PURPLE = (128,0,128)
BROWN = (150,75,0)
coins = [(130, 0, 30, 30), (290, 560, 30, 30)]
score = 0
text1 = font1.render('You Win!', True, (RED))
textrect1 = text1.get_rect()
textrect1.center = (400, 300)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Game')
player_speed = 10
x = 10
y = 50
h_x = 800
h_y = 600
hazards = [[180, 200, 20, 20, 3 , 2], [380, 100,20, 20,  2, -3],[181, 200, 20, 20, 3 , 2], [381, 100,20, 20,  2, -3],[182, 200, 20, 20, 3 , 2], [382, 100,20, 20,  2, -3]

]
levels = [{'walls':[(70, 0, 50, 360),(160, 260, 50, 360)],
           'coins':[(130, 0, 30, 30), (290, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3 , 2], [380, 100,20, 20,  2, -3]],
           'goal':(700, 520)},
          {'walls':[(70, 0, 50, 360),(160, 260, 50, 360),(250, 0, 50, 360),(340, 260, 50, 360),(430, 0, 50, 360)],
           'coins':[(130, 0, 30, 30), (290, 560, 30, 30),(400, 0, 30, 30), (550, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3 , 2], [380, 100,20, 20,  2, -3],[90, 120, 20, 20, 3 , 2], [360, 250,20, 20,  2, -3],[400, 50, 20, 20, 3 , 2], [80, 100,20, 20,  2, -3]],
           'goal':(700, 520)},
          {'walls': [(70, 0, 360, 50), (160, 260,360, 50), (250, 0, 360, 50), (340, 260, 360, 50), (430, 0, 360, 50)],
           'coins': [(130, 0, 30, 30), (290, 560, 30, 30), (400, 0, 30, 30), (550, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3, 2], [380, 100, 20, 20, 2, -3], [90, 120, 20, 20, 3, 2],
                       [360, 250, 20, 20, 2, -7]],
           'goal': (700, 520)},
          {'walls': [(70, 0, 360, 50), (160, 260,360, 50), (250, 0, 360, 50), (340, 260, 360, 50), (430, 0, 360, 50),(520, 260, 50, 360)],
           'coins': [(130, 0, 30, 30), (290, 560, 30, 30), (400, 0, 30, 30), (550, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3, 2], [380, 100, 20, 20, 2, -3], [90, 120, 20, 20, 3, 2],
                       [360, 250, 20, 20, 2, -7], [400, 50, 20, 20, 3, 7]],
           'goal': (700, 520)},
          {'walls': [(70, 0, 360, 50), (160, 260,360, 50), (250, 0, 360, 50), (340, 260, 360, 50), (430, 0, 360, 50),(520, 260, 50, 360),(160, 360, 50, 360)],
           'coins': [(130, 0, 30, 30), (290, 560, 30, 30), (400, 0, 30, 30), (550, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3, 2], [380, 100, 20, 20, 2, -3], [90, 120, 20, 20, 3, 2],
                       [360, 250, 20, 20, 2, -7], [400, 50, 20, 20, 3, 7], [80, 100, 20, 20, 2, -7]],
           'goal': (700, 520)},
          {'walls': [(70, 0, 360, 50), (160, 260,360, 50), (250, 0, 360, 50), (340, 260, 360, 50), (430, 0, 360, 50),(520, 260, 50, 360),(160, 360, 50, 360),(400,150,150,50),(650,130,150,50),(45,260,50,150)],
           'coins': [(130, 0, 30, 30), (290, 560, 30, 30), (400, 0, 30, 30), (550, 560, 30, 30)],
           'hazards': [[180, 200, 20, 20, 3, 2], [380, 100, 20, 20, 2, -3], [90, 120, 20, 20, 3, 2],
                       [360, 250, 20, 20, 2, -7], [400, 50, 20, 20, 3, 7], [80, 100, 20, 20, 2, -7],[70, 240, 20, 20, 2, -7]],
           'goal': (700, 520)}
          ]
g_x = 700
g_y = 520
text3 = font1.render('Your Score is!', True, (RED))
textrect3 = text3.get_rect()
textrect3.center = (400, 330)
current_level = 0
# Main game loop
running = True
while running:
    level = levels[current_level]
    walls = level['walls']
    coins = level['coins']
    hazards = level['hazards']
    g_x, g_y = level['goal']

    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] :
                x += player_speed
                if x > WIDTH - 20:
                    x = WIDTH - 20
        if keys[pygame.K_a] :
                x -= player_speed
                if x < 0 :
                    x = 0
        if keys[pygame.K_s] :
                y += player_speed
                if y > HEIGHT - 20:
                    y = HEIGHT - 20
        if keys[pygame.K_w] :
                y -= player_speed
                if y < 0:
                    y = 0
        if keys[pygame.K_UP]:
            player_speed += 10
            if x > WIDTH - 20:
                x = WIDTH - 20
        if keys[pygame.K_DOWN]:
            player_speed -= 10
            if x > WIDTH - 20:
                x = WIDTH - 20

    pygame.draw.rect(screen, RED, (x, y, 20, 20))
    player_rect = pygame.Rect(x, y, 20, 20)
    goal_rect = pygame.Rect(g_x, g_y, 60, 60)
    for hazard in hazards:
        hazard[0] += hazard[4]
        hazard[1] += hazard[5]


        hazard_rect = pygame.Rect(hazard[0], hazard[1], hazard[2], hazard[3])
        if hazard[0] <= 0 or hazard[0] + hazard[2] >= WIDTH:
            hazard[4] =  -hazard[4]
        if hazard[1] <= 0 or hazard[1] + hazard[3] >= HEIGHT:
            hazard[5] = -hazard[5]
        if player_rect.colliderect(hazard_rect):
            print('You have hit a hazard!')
            x = 10
            y = 50
    for hazard in hazards:
        pygame.draw.rect(screen, PURPLE, (hazard[0], hazard[1], hazard[2], hazard[3]))



    for coin in coins:
        pygame.draw.rect(screen, BROWN, coin)
    coins_collected = []
    #coins#
    for coin in coins:
        coin_rect = pygame.Rect(coin)
        if player_rect.colliderect(coin_rect):
            score += 10
            coins_collected.append(coin)

    for coin in coins:
        if coin in coins_collected:
            coins.remove(coin)


    text2 = font1.render(f"Score: {score}",True, (BLACK))
    textrect2 = text2.get_rect()
    textrect2.center = (60, 550)
    screen.blit(text2, textrect2)

    #collision with maze walls#
    for wall in walls:
        wall_rect = pygame.Rect(wall)
        if player_rect.colliderect(wall_rect):
            x = 10
            y = 50

    pygame.draw.rect(screen, GREEN, (g_x, g_y, 60, 60) )  # Outer boundary

    for wall in walls:
        pygame.draw.rect(screen, BLACK, wall)
#player rect touches goal rect#

    if player_rect.colliderect(goal_rect):
        current_level += 1
        if current_level == len(levels):
            text3 = font1.render(f'Your Score is {score}!', True, (RED))
            screen.blit(text1, textrect1)
            screen.blit(text3, textrect3)
            pygame.display.flip()
            pygame.time.wait(2000)
            running  = False
        else:
            print(f'Level {current_level} complete!, Moving to the next level...')
            x = 10
            y = 50
    pygame.display.flip()
    clock.tick(30)

pygame.quit()


print(score)