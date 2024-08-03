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

# Constants
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

BALL_SIZE = 10
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = -5

BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 30

LIVES = 3
SPEED_INCREMENT = 0.5

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.right += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, paddle):
        self.rect = pygame.Rect(paddle.rect.x + PADDLE_WIDTH // 2, paddle.rect.y - BALL_SIZE, BALL_SIZE, BALL_SIZE)
        self.speed_x = INITIAL_BALL_SPEED_X
        self.speed_y = INITIAL_BALL_SPEED_Y

    def move(self, paddle, bricks, brick_colors):
        global game_state, end_time, score

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if self.rect.colliderect(paddle.rect):
            offset = (self.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.speed_x = self.speed_x + offset * 2
            self.speed_y = -self.speed_y

        for brick in bricks[:]:
            if self.rect.colliderect(brick):
                self.speed_y = -self.speed_y
                index = bricks.index(brick)
                bricks.remove(brick)
                brick_colors.pop(index)
                score += 10
                self.increase_speed()
                break

        if self.rect.bottom >= SCREEN_HEIGHT:
            game_state = END
            end_time = time.time()

    def increase_speed(self):
        self.speed_x += SPEED_INCREMENT if self.speed_x > 0 else -SPEED_INCREMENT
        self.speed_y += SPEED_INCREMENT if self.speed_y > 0 else -SPEED_INCREMENT

    def draw(self):
        pygame.draw.ellipse(SCREEN, WHITE, self.rect)

# Brick class
class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

# Initialize paddle and ball
paddle = Paddle()
ball = Ball(paddle)

# Initialize bricks
bricks = []
brick_colors = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, COLORS[(row + col) % len(COLORS)])
        bricks.append(brick)
        brick_colors.append(brick.color)

# Timer
start_time = 0
end_time = 0

# Score
score = 0

# Lives
lives = LIVES

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
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2 + 60))
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    SCREEN.blit(lives_text, ((SCREEN_WIDTH - lives_text.get_width()) // 2, (SCREEN_HEIGHT - lives_text.get_height()) // 2 + 120))
    pygame.display.flip()

def draw_game():
    SCREEN.fill(BLACK)
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(lives_text, (10, 50))
    pygame.display.flip()

def reset_game():
    global paddle, ball, bricks, brick_colors, score, lives
    paddle = Paddle()
    ball = Ball(paddle)
    bricks = []
    brick_colors = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, COLORS[(row + col) % len(COLORS)])
            bricks.append(brick)
            brick_colors.append(brick.color)
    score = 0
    lives = LIVES

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == START:
                game_state = PLAYING
                start_time = time.time()
            if event.key == pygame.K_SPACE and game_state == END:
                reset_game()
                game_state = START

    if game_state == START:
        draw_start_screen()

    if game_state == PLAYING:
        paddle.move()
        ball.move(paddle, bricks, brick_colors)
        draw_game()
        pygame.time.Clock().tick(60)

    if game_state == END:
        if lives > 0:
            lives -= 1
            ball = Ball(paddle)  # Reset ball position
            game_state = PLAYING
        else:
            draw_end_screen()

pygame.quit()
sys.exit()
