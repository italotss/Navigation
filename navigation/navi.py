import pygame
from collections import deque
import random


pygame.init()
screen = pygame.display.set_mode((1000, 400))
clock = pygame.time.Clock()
running = True

# Grid settings
GRID_STEP = 50  # Size of each grid cell
GRID_COLOR = (200, 200, 200)  # Light gray color for grid lines
BG_COLOR = (255, 255, 255)  # White background

# Store filled squares and circles
filled_squares = set()
blue_circles = []  # List of blue circle positions (starts)
red_circles = []   # List of red circle positions (goals)
next_circle_is_blue = True  # Flag to alternate between blue and red
paths = []  # Store computed paths

def fill_square_at_mouse(mouse_pos):
    """Fill the grid square at the mouse position"""
    mouse_x, mouse_y = mouse_pos
    # Find which grid square was clicked
    grid_x = (mouse_x // GRID_STEP) * GRID_STEP
    grid_y = (mouse_y // GRID_STEP) * GRID_STEP
    # Only add if there's no circle at this position
    if (grid_x, grid_y) not in blue_circles and (grid_x, grid_y) not in red_circles:
        filled_squares.add((grid_x, grid_y))

def fill_circle_at_mouse(mouse_pos):
    """Draw a circle in the middle of the grid square at the mouse position"""
    global next_circle_is_blue
    
    mouse_x, mouse_y = mouse_pos
    # Find which grid square was clicked
    grid_x = (mouse_x // GRID_STEP) * GRID_STEP
    grid_y = (mouse_y // GRID_STEP) * GRID_STEP
    
    # Only add if there's no square at this position
    if (grid_x, grid_y) not in filled_squares:
        if next_circle_is_blue:
            if (grid_x, grid_y) not in blue_circles:
                blue_circles.append((grid_x, grid_y))
                next_circle_is_blue = False
        else:
            if (grid_x, grid_y) not in red_circles:
                red_circles.append((grid_x, grid_y))
                next_circle_is_blue = True

def bfs_pathfind(start, goal):
    """BFS pathfinding from start to goal, avoiding filled squares"""
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path
        
        # Check 8 neighbors (up, down, left, right, and 4 diagonals)
        for dx, dy in [(0, GRID_STEP), (0, -GRID_STEP), (GRID_STEP, 0), (-GRID_STEP, 0),
                       (GRID_STEP, GRID_STEP), (GRID_STEP, -GRID_STEP), 
                       (-GRID_STEP, GRID_STEP), (-GRID_STEP, -GRID_STEP)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check bounds and obstacles
            if (0 <= neighbor[0] < 1000 and 0 <= neighbor[1] < 400 and 
                neighbor not in visited and neighbor not in filled_squares):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []  # No path found

def compute_all_paths():
    """Compute paths for all blue-red circle pairs"""
    global paths
    paths = []
    for i in range(min(len(blue_circles), len(red_circles))):
        path = bfs_pathfind(blue_circles[i], red_circles[i])
        if path:
            paths.append(path)

def generate_random_pairs():
    """Generate random pairs of blue and red circles"""
    global next_circle_is_blue
    num_pairs = random.randint(2, 5)
    
    for _ in range(num_pairs):
        # Find random valid positions for blue circle
        while True:
            grid_x = random.randint(0, 19) * GRID_STEP
            grid_y = random.randint(0, 7) * GRID_STEP
            if ((grid_x, grid_y) not in filled_squares and 
                (grid_x, grid_y) not in blue_circles and 
                (grid_x, grid_y) not in red_circles):
                blue_circles.append((grid_x, grid_y))
                break
        
        # Find random valid position for red circle
        while True:
            grid_x = random.randint(0, 19) * GRID_STEP
            grid_y = random.randint(0, 7) * GRID_STEP
            if ((grid_x, grid_y) not in filled_squares and 
                (grid_x, grid_y) not in blue_circles and 
                (grid_x, grid_y) not in red_circles):
                red_circles.append((grid_x, grid_y))
                break
    
    # Keep flag in sync (should be True if equal number of blue/red)
    next_circle_is_blue = len(blue_circles) == len(red_circles)
    compute_all_paths()

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                fill_square_at_mouse(event.pos)
            elif event.button == 3:  # Right mouse button
                fill_circle_at_mouse(event.pos)
                compute_all_paths()  # Recompute paths when circle is added
            elif event.button == 2:  # Middle mouse button
                generate_random_pairs()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # Draw vertical grid lines
    for x in range(0, 1000, GRID_STEP):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, 400))
    
    # Draw horizontal grid lines
    for y in range(0, 400, GRID_STEP):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (1000, y))

    # Draw all filled squares
    for grid_x, grid_y in filled_squares:
        pygame.draw.rect(screen, (0, 0, 0), [grid_x + 1, grid_y + 1, GRID_STEP - 1, GRID_STEP - 1])

    # Draw paths
    for path in paths:
        for i in range(len(path) - 1):
            x1 = path[i][0] + GRID_STEP // 2
            y1 = path[i][1] + GRID_STEP // 2
            x2 = path[i + 1][0] + GRID_STEP // 2
            y2 = path[i + 1][1] + GRID_STEP // 2
            pygame.draw.line(screen, (0, 255, 0), (x1, y1), (x2, y2), 3)

    # Draw all blue circles (starts)
    for grid_x, grid_y in blue_circles:
        center_x = grid_x + GRID_STEP // 2
        center_y = grid_y + GRID_STEP // 2
        pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), GRID_STEP // 3)

    # Draw all red circles (goals)
    for grid_x, grid_y in red_circles:
        center_x = grid_x + GRID_STEP // 2
        center_y = grid_y + GRID_STEP // 2
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), GRID_STEP // 3)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()