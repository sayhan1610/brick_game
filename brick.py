import pygame
import sys
import random

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
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            bricks.remove(brick)

    # Ball goes out of bounds
    if ball.bottom >= SCREEN_HEIGHT:
        running = False

    # Drawing
    SCREEN.fill(BLACK)
    brick_color = random.choice([RED, GREEN, BLUE])
    pygame.draw.rect(SCREEN, WHITE, paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(SCREEN, brick_color, brick)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
