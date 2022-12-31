import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((1260, 680))
background = pygame.image.load('background_final.png')
instruct_font = pygame.font.Font('freesansbold.ttf', 70 )

 #GAME WON TEXT
game_won_font = pygame.font.Font('freesansbold.ttf', 60)
#game exit font
game_exit_font = pygame.font.Font('freesansbold.ttf', 20)
frame_image = pygame.image.load('frame.png')
def frame(x, y):
	screen.blit(frame_image, (x, y))
def isCorrectLevel(x, y):
	return 519 < x < 527 and 253 < y < 261
def game_won_text():
	won_text = game_won_font.render("YOU'VE RESTORED THE FRAME!", True, (250, 250, 250))
	screen.blit(won_text, (200, 215))
def game_exit_text():
	exit_text = game_exit_font.render("PRESS ENTER TO CONTINUE!", True, (240,240,240))
	screen.blit(exit_text, (300, 275))

	#frame
	# frame_image = pygame.image.load('frame.png')
	#frame coordinates
	
frameX = random.randint(0, 1000)
frameY = random.randint(0, 500)
frameX_change = 0
frameY_change = 0

pygame.display.set_caption("Pick the frame")
	
screen.blit(frame_image, (frameX, frameY))
event_allowed = "yes"
running = True
while running:
	screen.blit(background, (0, 0))
	if event_allowed == "yes":	
		pygame.draw.rect(screen, (0, 0, 0), (523, 257, 64, 53))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event_allowed == "yes":	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					frameX_change = -1
				if event.key == pygame.K_RIGHT:
					frameX_change = +1
				if event.key == pygame.K_DOWN:
					frameY_change = +1
				if event.key == pygame.K_UP:
					frameY_change = -1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					frameX_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					frameY_change = 0	
	if event_allowed == "yes":	
		frameX += frameX_change
		frameY += frameY_change
		frame(frameX, frameY)
	
	#GAME WON
	if isCorrectLevel(frameX, frameY):
		# screen.blit(background, (0, 0))
		game_won_text()
		event_allowed = "no"
		# game_exit_text()
		
		# for event in pygame.event.get():
		# 	if event.type == pygame.KEYDOWN:
		# 		running = False
	pygame.display.update()




