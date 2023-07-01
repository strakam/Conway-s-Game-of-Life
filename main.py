# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
window_size = 1280
square_size = 20
fps = 60
simulate_fps = 10
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
running = True

fg = (150, 150, 150)
fg_grid = (50, 50, 50)
bg = (30, 30, 30)

show_grid = True
simulate = False

cell_grid = [[0 for i in range(window_size//square_size)] for j in range(window_size//square_size)]

# function to generate evenly spaced lines forming a grid
def generate_grid(spacing):
    grid = []
    for i in range(0, window_size, spacing):
        pygame.draw.line(screen, fg_grid, (i, 0), (i, window_size))
        pygame.draw.line(screen, fg_grid, (0, i), (window_size, i))

def draw_square(x, y, size):
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, fg, r)

def get_pos():
    pos = pygame.mouse.get_pos()
    return pos[0] // square_size, pos[1] // square_size


def get_neighbors_count(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (x+i >= 0 and x+i < len(cell_grid) and y+j >= 0 and y+j < len(cell_grid)):
                if (i != 0 or j != 0):
                    count += cell_grid[x+i][y+j]
    return count

# Conway's Game of Life
def get_next_state(x,y):
    alive_neighbors = get_neighbors_count(x,y)
    # if this cell is alive
    if cell_grid[x][y] == 1:
        if alive_neighbors < 2 or alive_neighbors > 3:
            return 0
        return 1
    # if this cell is dead
    else:
        if alive_neighbors == 3:
            return 1
        return 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for keypress of 'g' to toggle grid
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_grid = not show_grid
            if event.key == pygame.K_s:
                simulate = not simulate
        # check for click and get mouse position
        if event.type == pygame.MOUSEBUTTONDOWN and not simulate:
            pos = get_pos()
            cell_grid[pos[0]][pos[1]] ^= 1

    # draw line
    screen.fill(bg)
    if show_grid:
        generate_grid(square_size)

    if simulate:
        new_generation = [[0 for i in range(window_size//square_size)] for j in range(window_size//square_size)]
        for i in range(len(cell_grid)):
            for j in range(len(cell_grid)):
                if simulate:
                    new_generation[i][j] = get_next_state(i,j)
        cell_grid = new_generation

    for i in range(len(cell_grid)):
        for j in range(len(cell_grid)):
            if cell_grid[i][j] == 1:
                draw_square(i*square_size, j*square_size, square_size)

    pygame.display.flip()  # update the display
    if simulate:
        clock.tick(simulate_fps)  # limits FPS
    else:
        clock.tick(fps)

pygame.quit()
