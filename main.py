import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = 20
DELTA_ANGLE = FOV / NUM_RAYS
SCREEN_DIST = (WIDTH // 2) / math.tan(FOV / 2)
SCALE = WIDTH // NUM_RAYS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Map settings
MAP_SIZE = 10
TILE_SIZE = 50
MINI_MAP_SCALE = 0.2  # Scale for the minimap
MINI_TILE_SIZE = int(TILE_SIZE * MINI_MAP_SCALE)

maze = [
    "########################################################",
    "#         ###############    ########      ########",
    "# ##### # ############### ########################",
    "#       # ############                 ########",
    "##  # # # ###                  ########################",
    "#     # # #    #########       ######        #####",
    "# ## #        #########        ########################",
    "#   # ###################                   #######",
    "#         ###############    ############ #############",
    "#######################################################"
]

# Player settings
player_x, player_y = 150, 150
player_angle = 0
player_speed = 3
rotation_speed = 0.05

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Maze Game")

# Draw the scaled-down 2D map and player
def draw_mini_map():
    # Draw map tiles
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            if tile == "#":
                pygame.draw.rect(
                    screen, BLUE,
                    (
                        col_idx * MINI_TILE_SIZE,
                        row_idx * MINI_TILE_SIZE,
                        MINI_TILE_SIZE,
                        MINI_TILE_SIZE
                    )
                )
    # Draw player
    player_mini_x = int(player_x * MINI_MAP_SCALE)
    player_mini_y = int(player_y * MINI_MAP_SCALE)
    pygame.draw.circle(screen, GREEN, (player_mini_x, player_mini_y), 5)

# Cast rays for 3D effect
def cast_rays():
    start_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        for depth in range(1, MAX_DEPTH * TILE_SIZE, 5):
            target_x = player_x + depth * math.cos(angle)
            target_y = player_y + depth * math.sin(angle)

            col, row = int(target_x // TILE_SIZE), int(target_y // TILE_SIZE)

            if 0 <= col < len(maze[0]) and 0 <= row < len(maze):
                if maze[row][col] == "#":
                    depth *= math.cos(player_angle - angle)
                    proj_height = SCREEN_DIST / (depth / TILE_SIZE)
                    color = (255 - min(255, depth), 255 - min(255, depth // 2), 255)
                    pygame.draw.rect(
                        screen, color,
                        (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
                    )
                    break

# Main game loop
def main():
    global player_x, player_y, player_angle
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            next_x = player_x + player_speed * math.cos(player_angle)
            next_y = player_y + player_speed * math.sin(player_angle)
            col, row = int(next_x // TILE_SIZE), int(next_y // TILE_SIZE)
            if maze[row][col] != "#":
                player_x = next_x
                player_y = next_y
        if keys[pygame.K_s]:
            next_x = player_x - player_speed * math.cos(player_angle)
            next_y = player_y - player_speed * math.sin(player_angle)
            col, row = int(next_x // TILE_SIZE), int(next_y // TILE_SIZE)
            if maze[row][col] != "#":
                player_x = next_x
                player_y = next_y
        if keys[pygame.K_a]:
            next_x = player_x - player_speed * math.sin(player_angle)
            next_y = player_y + player_speed * math.cos(player_angle)
            col, row = int(next_x // TILE_SIZE), int(next_y // TILE_SIZE)
            if maze[row][col] != "#":
                player_x = next_x
                player_y = next_y
        if keys[pygame.K_d]:
            next_x = player_x + player_speed * math.sin(player_angle)
            next_y = player_y - player_speed * math.cos(player_angle)
            col, row = int(next_x // TILE_SIZE), int(next_y // TILE_SIZE)
            if maze[row][col] != "#":
                player_x = next_x
                player_y = next_y
        if keys[pygame.K_LEFT]:
            player_angle -= rotation_speed
        if keys[pygame.K_RIGHT]:
            player_angle += rotation_speed

        # Drawing
        screen.fill(BLACK)
        cast_rays()
        if keys[pygame.K_m]:  # Only draw minimap and player when 'M' key is held down
            draw_mini_map()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
