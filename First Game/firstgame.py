import pygame
import random
import math

pygame.init()

win = pygame.display.set_mode((1000, 750))

pygame.display.set_caption("Space Invaders")

#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)

text_x = 20
text_y = 20

#game over text

game_over_font = pygame.font.Font('freesansbold.ttf', 256)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x,y))

def game_over_text(x, y):
    end_text = font.render("GAME OVER", True, (255, 255, 255))
    win.blit(end_text, (450, 375))

#ship 

x = 500
y = 650
x_change = 0
y_change = 0
vel = 30

ship = pygame.image.load('ship.png')
ship = pygame.transform.scale(ship, (64, 64))

def draw_ship(x,y):
    win.blit(ship, (x,y))

#bullet

bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 650
bullet_change = 50
bullet_state = "ready"

def draw_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bullet, (x + 20, y - 40))

#enemies

enemy = []
enemy_x = []
enemy_y = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy.append(pygame.image.load('ghost.png'))
    enemy_x.append(random.randint(0, 800))
    enemy_y.append(random.randint(50, 150))
    enemyX_change.append(30)
    enemyY_change.append(50)

def draw_enemy(x, y, i):
    win.blit(enemy[i], (x,y))

#collisions

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 32:
        return True
    else:
        return False

    
#main loop

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -vel
            if event.key == pygame.K_RIGHT:
                x_change = vel
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = x
                    draw_bullet(bullet_x, bullet_y)

                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            
    x += x_change
    y += y_change

    #boudaries
    
    if x < 0:
        x = 0
    if x > 934:
        x = 934

    win.fill((0,0,0))

    #enemy movement

    for i in range(num_enemies):

        #game over

        if enemy_y[i] > 600:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_text(x, y)
            break
            
        enemy_x[i] += enemyX_change[i]

        if enemy_x[i] <= 0:
            enemyX_change[i] = 30
            enemy_y[i] += enemyY_change[i]
            
        elif enemy_x[i] >= 934:
            enemyX_change[i] = -30
            enemy_y[i] += enemyY_change[i]

        #collisions

        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        
        if collision:
            bullet_y = 650
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 800)
            enemy_y[i] = random.randint(50, 150)

        draw_enemy(enemy_x[i], enemy_y[i], i)

    #bullet movement

    if bullet_y <= 0:
        bullet_y = 650
        bullet_state = "ready"
    
    if bullet_state is "fire":
        draw_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_change
        

    draw_ship(x,y)
    show_score(text_x, text_y)

    pygame.display.update()

pygame.quit()
