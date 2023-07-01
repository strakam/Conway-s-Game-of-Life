# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
window_size = 1280
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
running = True

show_grid = True

# function to generate evenly spaced lines forming a grid
def generate_grid(spacing):
    grid = []
    for i in range(0, window_size, spacing):
        pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, window_size))
        pygame.draw.line(screen, (255, 255, 255), (0, i), (window_size, i))

def draw_square(x, y, size):
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, (255, 255, 255), r)

def snap_to_grid(x, y, spacing):
    return (x // spacing) * spacing, (y // spacing) * spacing


squares = []
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
        # check for click and get mouse position
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = snap_to_grid(pos[0], pos[1], 20)
            squares.append(pygame.Rect(pos[0], pos[1], 20, 20))

    # draw line
    screen.fill((0, 0, 0))
    if show_grid:
        generate_grid(20)
    for s in squares:
        pygame.draw.rect(screen, (255, 255, 255), s)

    pygame.display.flip()  # update the display
    clock.tick(60)  # limits FPS to 60

pygame.quit()
