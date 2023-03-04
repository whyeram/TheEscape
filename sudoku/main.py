import pygame
import requests

pygame.init()
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']


grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
original_grid_element_colour = (52, 31, 151)
background_colour = (245, 245, 220)
buffer = 2
correct = "no"
#screen
screen = pygame.display.set_mode((940, 670))
#instructions font
instruct_font = pygame.font.Font('freesansbold.ttf', 20)
#GAME WON TEXT
game_won_font = pygame.font.Font('freesansbold.ttf', 60)
def game_won_text():
    won_text = game_won_font.render("ONTO THE NEXT!", True, (255, 0, 0))
    screen.blit(won_text,(210, 305))
#iNCORRECT TEXT
incorrect_font = pygame.font.Font('freesansbold.ttf', 40)
def incorrect_text():
    incorrect_text = incorrect_font.render("OOPS! NOT THERE YET!", True, (255, 0, 0))
    screen.blit(incorrect_text,(230, 310))
def instructions(x, y):
	instruct = instruct_font.render("PRESS ENTER TO SUBMIT", True, (0, 0, 0))
	screen.blit(instruct, (x, y))
def insert(screen, position):
	#font
	value = 0
	i, j = position[1], position[0]
	myfont = pygame.font.SysFont('Comic Sans MS', 35)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if grid_original[i][j] != 0:
					return
				#checking for 0
				if event.key == 48: 
					grid[i][j] = event.key - 48
					pygame.draw.rect(screen, background_colour, (200 + position[0] * 60 + buffer, 65 + position[1] * 60 + buffer, 60 - 2*buffer, 60 - 2*buffer))
					pygame.display.update()

				#checking for valid input
				if 0 < event.key - 48 < 10: 
					pygame.draw.rect(screen, background_colour, (200 + position[0] * 60 + buffer, 65 + position[1] * 60 + buffer, 60 - 2*buffer, 60 - 2*buffer))
					value = myfont.render(str(event.key - 48), True, (0, 0, 0))
					screen.blit(value, (215 + position[0] * 60 , position[1] * 60 + 71))
					grid[i][j] = event.key - 48
					pygame.display.update()
					return
				return
def is_not_full(board):
    for row in board:
        for num in row:
            if num == 0:
                return True
    return False

def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool'''

    for i in range(9):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  # make sure it isn't the same number we're checking for by comparing coords
            return False

    for j in range(9):
        if board[pos[0]][j] == num and (pos[0], j) != pos:  # Same row but not same number
            return False

    start_i = pos[0] - pos[0] % 3  # ex. 5-5%3 = 3 and thats where the grid starts
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):  # adds i and j as needed to go from start of grid to where we need to be
            if board[start_i + i][start_j + j] == num and (start_i + i,
                    start_j + j) != pos:
                return False
    return True
def is_correct(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
            elif not valid(board, (i, j), board[i][j]):
                return False      
    return True



def main():

	#initialising pygame
	pygame.init()

	#Window title
	pygame.display.set_caption("Sudoku")

	#background
	background = pygame.image.load('background.png')
	#blitting background image on screen
	screen.blit(background, (0, 0))
	#sudoku background rectangle 
	pygame.draw.rect(screen, background_colour, (200, 65, 540, 540))
	#font
	myfont = pygame.font.SysFont('Comic Sans MS', 35)

	for i in range(0, 10):
		thickness =1
		if i % 3 == 0:
			thickness = 3
		pygame.draw.line(screen, (0, 0, 0), (200 + 60*i, 65), (200 + 60*i, 605), thickness )
		pygame.draw.line(screen, (0, 0, 0), (200, 65 + 60*i ), (740, 65 + 60*i ), thickness )
	pygame.display.update()
	for i in range(0, len(grid[0])):
		for j in range(0, len(grid[0])):
			if 0 < grid[i][j] < 10:
				value = myfont.render(str(grid[i][j]), True, original_grid_element_colour)
				screen.blit(value, ((j + 1) * 60 + 160, (i + 1) * 60 + 12))
	
	running = True
	#event input checkpoint
	while running:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pos = pygame.mouse.get_pos()
				insert(screen, ((pos[0] - 200 )// 60, (pos[1] - 65) // 60))
				print(grid)
			# close window -> quit game in terminal
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and is_correct(grid):
				correct = "yes"
				game_won_text()
				running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not is_correct(grid):
				correct = "no"
				incorrect_text()
		instructions(650, 40)
		pygame.display.update()

	return
main()


