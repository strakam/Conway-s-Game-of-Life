# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
window_size = 1280
square_size = 20
grid_size = window_size // square_size
fps = 60
simulate_fps = 10
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
running = True

# constants
ALIVE = 1
DEAD = 0
LEFTMOUSEBUTTON = 0

# colors
fg = (150, 150, 150)
fg_grid = (50, 50, 50)
bg = (30, 30, 30)

show_grid = True
simulate = False


def empty_grid():
    return [[DEAD] * grid_size for _ in range(grid_size)]


# function to generate evenly spaced lines forming a grid
def generate_grid(spacing):
    for i in range(0, window_size, spacing):
        pygame.draw.line(screen, fg_grid, (i, 0), (i, window_size))
        pygame.draw.line(screen, fg_grid, (0, i), (window_size, i))


def draw_square(x, y):
    r = pygame.Rect(x * square_size, y * square_size, square_size, square_size)
    pygame.draw.rect(screen, fg, r)


def snap_to_grid(pos):
    # max() and min() to prevent out of bounds
    pos = (max(0, min(pos[0], window_size - 1)), max(0, min(pos[1], window_size - 1)))
    return pos[0] // square_size, pos[1] // square_size


def get_neighbors_count(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + i >= 0 and x + i < grid_size and y + j >= 0 and y + j < grid_size:
                if i != 0 or j != 0:
                    count += cell_grid[x + i][y + j] == ALIVE
    return count


# Conway's Game of Life
def get_next_state(x, y):
    alive_neighbors = get_neighbors_count(x, y)
    if cell_grid[x][y] == ALIVE:
        if alive_neighbors < 2 or alive_neighbors > 3:
            return DEAD
        return ALIVE
    else:
        if alive_neighbors == 3:
            return ALIVE
        return DEAD


cell_grid = empty_grid()  # initialize grid
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:  # toggle grid
                show_grid = not show_grid
            if event.key == pygame.K_s:  # toggle simulation
                simulate = not simulate
            if event.key == pygame.K_r and not simulate:  # reset grid
                cell_grid = empty_grid()

        elif event.type == pygame.MOUSEBUTTONDOWN and not simulate:  # click to toggle cell state
            x, y = snap_to_grid(event.pos)
            cell_grid[x][y] = ALIVE if (cell_grid[x][y] == DEAD) else DEAD
        elif event.type == pygame.MOUSEMOTION and not simulate:  # drag to draw (LEFTMOUSEBUTTON -> ALIVE, else -> DEAD)
            if any(event.buttons):
                x, y = snap_to_grid(event.pos)
                cell_grid[x][y] = ALIVE if event.buttons[LEFTMOUSEBUTTON] else DEAD

    # draw background and grid
    screen.fill(bg)
    if show_grid:
        generate_grid(square_size)

    if simulate:
        new_generation = empty_grid()
        for x in range(grid_size):
            for y in range(grid_size):
                new_generation[x][y] = get_next_state(x, y)
        cell_grid = new_generation

    for x in range(grid_size):
        for y in range(grid_size):
            if cell_grid[x][y] == ALIVE:
                draw_square(x, y)

    pygame.display.flip()  # update the display
    if simulate:
        clock.tick(simulate_fps)  # limits FPS
    else:
        clock.tick(fps)

pygame.quit()
