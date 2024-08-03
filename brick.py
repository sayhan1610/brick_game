import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# Paddle variables
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball variables
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = -5

# Brick variables
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 30

# Initialize paddle
paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize ball
ball = pygame.Rect(paddle.x + PADDLE_WIDTH // 2, paddle.y - BALL_SIZE, BALL_SIZE, BALL_SIZE)

# Initialize bricks
bricks = []
brick_colors = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)
        brick_colors.append(COLORS[(row + col) % len(COLORS)])

# Timer
start_time = 0
end_time = 0

# Game states
START = 0
PLAYING = 1
END = 2
game_state = START

def draw_start_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Press SPACE to Start", True, WHITE)
    SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    pygame.display.flip()

def draw_end_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    time_elapsed = end_time - start_time
    text = font.render(f"Game Over! Time: {time_elapsed:.2f} seconds", True, WHITE)
    SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    pygame.display.flip()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == START:
                game_state = PLAYING
                start_time = time.time()
            if event.key == pygame.K_SPACE and game_state == END:
                game_state = START
                # Reset game
                paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
                ball = pygame.Rect(paddle.x + PADDLE_WIDTH // 2, paddle.y - BALL_SIZE, BALL_SIZE, BALL_SIZE)
                bricks = []
                brick_colors = []
                for row in range(BRICK_ROWS):
                    for col in range(BRICK_COLUMNS):
                        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
                        bricks.append(brick)
                        brick_colors.append(COLORS[(row + col) % len(COLORS)])

    if game_state == START:
        draw_start_screen()

    if game_state == PLAYING:
        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.right += PADDLE_SPEED

        # Handle ball movement
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            BALL_SPEED_X = -BALL_SPEED_X
        if ball.top <= 0:
            BALL_SPEED_Y = -BALL_SPEED_Y

        # Ball collision with paddle
        if ball.colliderect(paddle):
            BALL_SPEED_Y = -BALL_SPEED_Y

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                BALL_SPEED_Y = -BALL_SPEED_Y
                index = bricks.index(brick)
                bricks.remove(brick)
                brick_colors.pop(index)

        # Ball goes out of bounds
        if ball.bottom >= SCREEN_HEIGHT:
            game_state = END
            end_time = time.time()

        # Drawing
        SCREEN.fill(BLACK)
        pygame.draw.rect(SCREEN, WHITE, paddle)
        pygame.draw.ellipse(SCREEN, WHITE, ball)
        for brick, color in zip(bricks, brick_colors):
            pygame.draw.rect(SCREEN, color, brick)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    if game_state == END:
        draw_end_screen()

pygame.quit()
sys.exit()
