import pygame
import random
import math
from pygame import mixer 
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 500))

#window title
pygame.display.set_caption("Adventure Begins")

#icon
icon = pygame.image.load('demon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('background.png')
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#Player
player_img = pygame.image.load('glow_bow.png')
playerX = 400
playerY = 400
playerX_change = 0


enemy_img = pygame.image.load('demon.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4
for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)

#GAME OVER TEXT
game_over_font = pygame.font.Font('freesansbold.ttf', 100)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text,(300, 225))
#Enemies
def enemy(x, y):
    screen.blit(enemy_img, (x, y))
def player(x, y):
    screen.blit(player_img, (x, y))

#arrow
arrow_img = pygame.image.load('arrow.png')
arrowX = 0
arrowY = 400
arrowX_change = 0
arrowY_change = 15
arrow_state = "ready" #ready - you can't see the bullet on the screen
                       #fire - The bullet is currently moving
def shoot_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrow_img, (x + 2 , y + 9))
def isCollision(arrowX, arrowY, enemyX, enemyY):
    distance = math.sqrt( math.pow(arrowX - enemyX, 2) + math.pow(arrowY - enemyY, 2) )
    return distance < 27 #collision occurs if distance < 15 pixels


#game loop
running = True
while running:
    #RGB = Red, Green, Blue 
    # screen.fill((100, 55, 40))
    #background image
    screen.blit(background, (0, 0))
    #event input checkpoint
    for event in pygame.event.get():
        #close window -> quit game in terminal
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            #leftward movement
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            #rightward movement
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            #bullet fire  
            if event.key == pygame.K_SPACE: 
                #shoot the bullet only if it is "ready" i.e. on the screen
                if arrow_state is "ready":
                    arrow_sound = mixer.Sound('laser.wav')
                    arrow_sound.play()
                    #Get the curent X-coord of the spaceship
                    shoot_arrow(playerX, arrowY) 
                    arrowX = playerX 
        #key released 
        if event.type == pygame.KEYUP:
            #if the released key was a right or left arrow key 
            #then stop moving the player(bow) 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    #new X-coord of player
    playerX += playerX_change
    #Checking for boundaries of spaceship so that it doesnt go out
    if playerX <= 0:
        playerX = 0
    elif playerX >= 800 - 64:
        playerX = 736

    
    for i in range(num_of_enemies):
        #GAME OVER
        if enemyY[i] > 370 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break 

        enemyX[i] += enemyX_change[i]

        #moving enemy downwards if it hits the window boundary

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 800 - 64:
            enemyX[i] = -1
            enemyY[i] += enemyY_change[i]
        #collision
        collision = isCollision(arrowX, arrowY, enemyX[i], enemyY[i] )
        if collision and arrow_state == "fire":
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            arrow_Y = 400
            arrow_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        #blitting enemy[i]
        enemy(enemyX[i], enemyY[i]) 
    #arrow movement 
    if arrowY <= 0:
        arrowY = 400
        arrow_state = "ready"
     #shooting arrow movement 
    if arrow_state == "fire":
        shoot_arrow(arrowX, arrowY)
        arrowY -= arrowY_change
    

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
