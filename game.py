import pygame

# Basic pygame setup
pygame.init()

# Initial screen size
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Gravity system variables
gravity = 800
velocity_y = 0
is_on_ground = False

# Create the window (resizable)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('الواد اللي بينط')

clock = pygame.time.Clock()
running = True
DTime = 0

# Character Animation Setup
PLAYER_SCALE = 2
WALK_SPEED = 300
ANIMATION_SPEED = 0.1

# Image filenames
IDLE_IMAGE = "idle.png"
WALK_FILENAMES = ["walk3.png", "walk4.png"]
JUMP_FILENAME = "jump.png"

# Load and scale images
def load_and_scale(filename):
    img = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(img, (img.get_width() * PLAYER_SCALE, img.get_height() * PLAYER_SCALE))

IDLE_IMAGE = load_and_scale(IDLE_IMAGE)
WALK_ANIMATION = [load_and_scale(f) for f in WALK_FILENAMES]
JUMP_IMAGE = load_and_scale(JUMP_FILENAME)

# Animation state variables
current_state = "idle"
animation_frame_index = 0
animation_timer = 0.0
is_facing_right = True

# Player setup
current_player_image = IDLE_IMAGE
player_rect = current_player_image.get_rect()
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
player_rect.center = (int(player_pos.x), int(player_pos.y))

# Floor properties
FLOOR_HEIGHT = 50
FLOOR_Y = SCREEN_HEIGHT - FLOOR_HEIGHT

# Load background and floor textures
background_original = pygame.image.load("bg.png").convert()
background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

floor_texture_original = pygame.image.load("numboard.png").convert()
floor_texture = pygame.transform.scale(floor_texture_original, (100, FLOOR_HEIGHT))  # tile width 100px

# Function to draw tiled floor
def draw_tiled_floor():
    tiles_needed = SCREEN_WIDTH // floor_texture.get_width() + 1
    for i in range(tiles_needed):
        screen.blit(floor_texture, (i * floor_texture.get_width(), FLOOR_Y))


# Score system setup

score = 0
highest_y = player_rect.centery  # track highest vertical position reached (lowest Y value = higher jump)
font = pygame.font.Font(None, 48)  # default font

# Main Game Loop
while running:
    DTime = clock.tick(60) / 1000

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle window resize
        if event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
            FLOOR_Y = SCREEN_HEIGHT - FLOOR_HEIGHT

        # Jump control
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_SPACE):
            if is_on_ground:
                velocity_y = -600
                is_on_ground = False
                current_state = "jump"
                animation_frame_index = 0
                animation_timer = 0.0

    # Input
    keys = pygame.key.get_pressed()
    is_moving_horizontally = False

    # Movement
    if keys[pygame.K_a]:
        player_rect.x -= WALK_SPEED * DTime
        is_facing_right = False
        is_moving_horizontally = True
    if keys[pygame.K_d]:
        player_rect.x += WALK_SPEED * DTime
        is_facing_right = True
        is_moving_horizontally = True

    # State Update
    if is_on_ground:
        if is_moving_horizontally:
            if current_state != "walk":
                current_state = "walk"
                animation_frame_index = 0
                animation_timer = 0.0
        else:
            current_state = "idle"

    # Physics
    velocity_y += gravity * DTime
    player_rect.y += velocity_y * DTime

    # Floor collision
    if player_rect.bottom > FLOOR_Y:
        player_rect.bottom = FLOOR_Y
        velocity_y = 0
        if not is_on_ground:
            is_on_ground = True
            animation_frame_index = 0
            animation_timer = 0.0
            current_state = "idle" if not is_moving_horizontally else "walk"

    # Horizontal wrapping
    if player_rect.left > SCREEN_WIDTH:
        player_rect.right = 0
    elif player_rect.right < 0:
        player_rect.left = SCREEN_WIDTH

    
    # Score Update (increase when going higher)
  
    if player_rect.centery < highest_y:
        score += int((highest_y - player_rect.centery) / 10)  # increase based on height difference
        highest_y = player_rect.centery  # update new highest point

    # Animation Update
    if current_state == "walk":
        animation_timer += DTime
        if animation_timer >= ANIMATION_SPEED:
            animation_timer = 0.0
            animation_frame_index = (animation_frame_index + 1) % len(WALK_ANIMATION)
        current_player_image = WALK_ANIMATION[animation_frame_index]
    elif current_state == "jump":
        current_player_image = JUMP_IMAGE
    else:
        current_player_image = IDLE_IMAGE

    # Flip sprite if facing left
    if not is_facing_right:
        current_player_image = pygame.transform.flip(current_player_image, True, False)

    # Drawing
    screen.blit(background, (0, 0))
    draw_tiled_floor()
    screen.blit(current_player_image, player_rect)

    # Draw score on top
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

pygame.quit()
