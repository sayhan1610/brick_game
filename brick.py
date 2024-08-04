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
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
COLORS = [RED, GREEN, BLUE]
POWERUP_COLORS = {
    'x3_balls': YELLOW,
    'mega_ball': PURPLE,
    'paddle_size': CYAN,
    'speed_boost': RED,
    'reset_speed': ORANGE,
    'extra_life': GREEN
}

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

POWERUP_CHANCE = 0.1  # Chance of a power-up dropping from a brick
POWERUP_FALL_SPEED = 2  # Speed at which power-ups fall

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.original_width = PADDLE_WIDTH
        self.powerup_end_time = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.right += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)

    def apply_powerup(self, powerup_type):
        if powerup_type == 'paddle_size':
            self.rect.width = self.original_width * 2
            self.powerup_end_time = pygame.time.get_ticks() + 10000  # 10 seconds

    def update(self):
        if pygame.time.get_ticks() > self.powerup_end_time:
            self.rect.width = self.original_width

# Ball class
class Ball:
    def __init__(self, paddle, mega_ball=False):
        self.rect = pygame.Rect(paddle.rect.x + PADDLE_WIDTH // 2, paddle.rect.y - BALL_SIZE, BALL_SIZE, BALL_SIZE)
        self.initial_speed_x = INITIAL_BALL_SPEED_X
        self.initial_speed_y = INITIAL_BALL_SPEED_Y
        self.speed_x = self.initial_speed_x
        self.speed_y = self.initial_speed_y
        self.mega_ball = mega_ball
        self.powerup_end_time = 0

    def move(self, paddle, bricks, powerups):
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
            if self.rect.colliderect(brick.rect):
                self.speed_y = -self.speed_y
                bricks.remove(brick)
                powerup = self.create_powerup(brick.rect)
                if powerup:
                    powerups.append(powerup)
                break

        if self.rect.bottom >= SCREEN_HEIGHT:
            return True  # Ball fell off the screen
        return False  # Ball did not fall off the screen

    def create_powerup(self, brick_rect):
        if random.random() < POWERUP_CHANCE:
            powerup_type = random.choice(list(POWERUP_COLORS.keys()))
            return PowerUp(brick_rect.x, brick_rect.y, powerup_type)
        return None

    def increase_speed(self):
        self.speed_x += SPEED_INCREMENT if self.speed_x > 0 else -SPEED_INCREMENT
        self.speed_y += SPEED_INCREMENT if self.speed_y > 0 else -SPEED_INCREMENT

    def draw(self):
        pygame.draw.ellipse(SCREEN, WHITE, self.rect)

    def apply_powerup(self, powerup_type):
        if powerup_type == 'mega_ball':
            self.mega_ball = True
            self.powerup_end_time = pygame.time.get_ticks() + 10000  # 10 seconds
        elif powerup_type == 'speed_boost':
            self.speed_x *= 1.5
            self.speed_y *= 1.5
            self.powerup_end_time = pygame.time.get_ticks() + 10000  # 10 seconds
        elif powerup_type == 'reset_speed':
            self.speed_x = self.initial_speed_x
            self.speed_y = self.initial_speed_y

    def update(self):
        if pygame.time.get_ticks() > self.powerup_end_time:
            self.mega_ball = False

# Brick class
class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

# Power-up class
class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.powerup_type = powerup_type
        self.color = POWERUP_COLORS[powerup_type]

    def move(self):
        self.rect.y += POWERUP_FALL_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

# Initialize paddle and balls
paddle = Paddle()
ball = Ball(paddle)
balls = [ball]

# Initialize bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, COLORS[(row + col) % len(COLORS)])
        bricks.append(brick)

# Initialize power-ups
powerups = []

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
    for ball in balls:
        ball.draw()
    for brick in bricks:
        brick.draw()
    for powerup in powerups:
        powerup.draw()
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(lives_text, (10, 50))
    pygame.display.flip()

def reset_game():
    global paddle, balls, bricks, powerups, score, lives
    paddle = Paddle()
    balls = [Ball(paddle)]
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, COLORS[(row + col) % len(COLORS)])
            bricks.append(brick)
    powerups = []
    score = 0
    lives = LIVES

# Main game loop
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
        paddle.update()
        for ball in balls[:]:
            if ball.move(paddle, bricks, powerups):
                balls.remove(ball)
                score += 10  # Increment score when a ball falls off
        if len(balls) == 0:
            if lives > 0:
                lives -= 1
                ball = Ball(paddle)  # Reset ball position
                balls = [ball]  # Reset balls list
                game_state = PLAYING
            else:
                game_state = END
                end_time = time.time()
        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle.rect):
                if powerup.powerup_type == 'x3_balls':
                    new_ball1 = Ball(paddle)
                    new_ball2 = Ball(paddle)
                    balls.append(new_ball1)
                    balls.append(new_ball2)
                elif powerup.powerup_type == 'extra_life':
                    lives += 2
                else:
                    for ball in balls:
                        ball.apply_powerup(powerup.powerup_type)
                if powerup.powerup_type == 'paddle_size':
                    paddle.apply_powerup(powerup.powerup_type)
                powerups.remove(powerup)
            elif powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)
        draw_game()
        pygame.time.Clock().tick(60)

    if game_state == END:
        draw_end_screen()

pygame.quit()
sys.exit()
