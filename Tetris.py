import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()  # initialize the font module

# GLOBALS VARIABLES
width = 800
height = 700
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 20 height per block
blockSize = 30

# top left position of the actual play area, position to start to draw box and check collision
top_left_x = (width - playWidth) // 2
top_left_y = height - playHeight

# SHAPE FORMATS, represent all the shapes
# S has two different orientations, rotations
# 0 represents where the block actually exist
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

# Z has two different orientations, rotations
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

# I has two different orientations, rotations
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

# O has one orientation, rotation
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

# J has four different orientations, rotations
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

# L has four different orientations, rotations
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

# T has four different orientations, rotations
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# list of all possible shapes
shapes = [S, Z, I, O, J, L, T]
# list of all possible colors
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


# data structure of this game, represent the pieces
class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  #number from 0-3


def create_grid(locked_positions={}):
    # create one list for every row in the grid
    # (0, 0, 0) represents black
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    # iterate through the grid to check if it corresponds to the lock-pos
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []  # generate a list of position
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)  # get the one row in the list
        for j, column in enumerate(row):
            if column == '0':  # if the position is part of the block
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        # move everything left and up
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # take all the element in the list to a one dimensional list
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # when the y position is on grid
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:  # if the block is going over the grid
            return True  # lost the game
    return False


# randomly pick one shape from the list
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + playWidth / 2 - (label.get_width() / 2), top_left_y + playHeight / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    start_x = top_left_x
    start_y = top_left_y

    for i in range(row):
        # horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (start_x, start_y + i * blockSize),
                         (start_x + playWidth, start_y + i * blockSize))
        for j in range(col):
            # vertical lines
            pygame.draw.line(surface, (128, 128, 128), (start_x + j * blockSize, start_y),
                             (start_x + j * blockSize, start_y + playHeight))


# check if row is complete and needs to clear and shift every other row above down by inc
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):  # iterate through the grid from the bottom
        row = grid[i]
        if (0, 0, 0) not in row:  # if a row has no black
            inc += 1  # number of rows to shift down
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  # delete from the locked positions
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key  # getting x y positions in each key locations
            if y < ind:  # if the y value is above the current index of the row removing
                newKey = (x, y+inc)  # increment the y value to shift down
                # rewrite the locked, same color value as the last key, and equal to the newKey position
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    start_x = top_left_x + playWidth + 50
    start_y = top_left_y + playHeight / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (start_x + j * blockSize, start_y + i * blockSize, blockSize, blockSize), 0)

    surface.blit(label, (start_x + 10, start_y - 30))


def update_score(nscore):
    score = max_score()

    with open('score.txt', 'w')as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('score.txt', 'r')as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def draw_window(surface, score=0, last_score=0):
    surface.fill((0, 0, 0))
    # Tetris Title
    # pygame.font.init()  # initialize the font
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS by Kerry', 1, (255, 255, 255))

    # print it on the screen
    surface.blit(label, (top_left_x + playWidth / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + playWidth + 50
    start_y = top_left_y + playHeight / 2 - 100

    surface.blit(label, (start_x + 20, start_y + 150))

    # high score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    start_x = top_left_x - 200
    start_y = top_left_y + 200

    surface.blit(label, (start_x + 20, start_y + 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # draw rectangles on each row and col
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * blockSize, top_left_y + i * blockSize, blockSize, blockSize), 0)

    # Draw the grid of the actual game
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, playWidth, playHeight), 5)  # border size of 5
    # pygame.display.update()


def main(win):
    last_score = max_score()
    global grid

    locked_positions = {}  # (x,y):(255, 0, 0)  position:color
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    level_time = 0
    score = 0

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # increase in time gradually
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01

        # piece falling timing
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the user press x, close the game
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # move block left
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    # check if the position is valid
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                # move block right
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                # rotate the block
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1%len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1%len(current_piece.shape)

                # move block down
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

            shape_pos = convert_shape_format(current_piece)

            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]  # current iteration
                if y > -1:  # not above the screen
                    grid[y][x] = current_piece.color

            # if piece hit the ground
            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color

                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                score += clear_rows(grid, locked_positions)*10

            draw_window(win, score, last_score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

            # check if the user lose, if the blocks exceed the top
            if check_lost(locked_positions):
                draw_text_middle("You LOST!!!", 80, (255, 255, 255), win)
                pygame.display.update()
                pygame.time.delay(2000)
                run = False
                update_score(score)

    pygame.display.update()
    pygame.time.delay(2000)


def main_menu(win):
    run = True
    while run:  # enter the game
        win.fill((0, 0, 0))  # fill the screen with black
        draw_text_middle('Press any key to begin', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user click the x button, quit the game
                run = False
            if event.type == pygame.KEYDOWN:  # if anykey is being pressed, start the game
                main(win)

    pygame.quit()


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris by Kerry")
main_menu(win)  # start game
