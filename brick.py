import pygame
import sys
import random
import time
import os

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Path to audio files
audio_path = os.path.join(os.path.dirname(__file__), 'audio')

# Load sound effects
start_sound = pygame.mixer.Sound(os.path.join(audio_path, 'start.mp3'))
brick_sound = pygame.mixer.Sound(os.path.join(audio_path, 'brick.mp3'))
power_sound = pygame.mixer.Sound(os.path.join(audio_path, 'power.mp3'))
death_sound = pygame.mixer.Sound(os.path.join(audio_path, 'death.mp3'))
win_sound = pygame.mixer.Sound(os.path.join(audio_path, 'win.mp3'))

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
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

PARTICLE_COUNT = 10  # Number of particles per brick

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
            pygame.mixer.Sound.play(brick_sound)

        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                self.speed_y = -self.speed_y
                brick.hit_points -= 1
                pygame.mixer.Sound.play(brick_sound)
                if brick.hit_points <= 0:
                    bricks.remove(brick)
                    powerup = self.create_powerup(brick.rect)
                    if powerup:
                        powerups.append(powerup)
                    create_particles(brick.rect)
                else:
                    brick.update_color()
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
        self.hit_points = 3 if color == BLUE else 2 if color == RED else 1
        self.update_color()

    def update_color(self):
        if self.hit_points == 3:
            self.color = BLUE
        elif self.hit_points == 2:
            self.color = RED
        elif self.hit_points == 1:
            self.color = GREEN

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

# Particle class
class Particle:
    def __init__(self, x, y, color, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.life = 100

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.life -= 1

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

# Initialize particles
particles = []

# Timer
start_time = 0
end_time = 0

# Score
score = 0

# Lives
lives = LIVES

# Audio mute status
audio_muted = False

# Game states
START = 0
PLAYING = 1
PAUSED = 2
END = 3
INSTRUCTIONS = 4
game_state = START

def draw_start_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    text = font.render("Press SPACE to Start", True, WHITE)
    SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    pygame.display.flip()

def draw_instructions_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 35)
    instructions = [
        "Instructions:",
        "1. Use LEFT and RIGHT arrow keys to move the paddle.",
        "2. Press SPACE to start the game.",
        "3. Break all the bricks to win.",
        "4. Collect power-ups for special abilities.",
        "5. Avoid missing the ball with your paddle.",
        "Press BACKSPACE to go back."
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 50 + i * 40))
    pygame.display.flip()

def draw_paused_screen():
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Paused. Press P to Resume", True, WHITE)
    SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    pygame.display.flip()

def draw_end_screen(won):
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    if won:
        text = font.render("Congratulations! You Won!", True, WHITE)
    else:
        text = font.render("Game Over. You Lost.", True, WHITE)
    SCREEN.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, (SCREEN_HEIGHT - text.get_height()) // 2))
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2 + 60))
    pygame.display.flip()

def create_particles(brick_rect):
    for _ in range(PARTICLE_COUNT):
        speed_x = random.randint(-5, 5)
        speed_y = random.randint(-5, 5)
        particle = Particle(brick_rect.centerx, brick_rect.centery, random.choice(COLORS), speed_x, speed_y)
        particles.append(particle)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == START:
                    start_time = time.time()
                    pygame.mixer.Sound.play(start_sound)
                    game_state = PLAYING
                elif game_state == END:
                    # Restart the game
                    paddle = Paddle()
                    balls = [Ball(paddle)]
                    bricks = [Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, COLORS[(row + col) % len(COLORS)]) for row in range(BRICK_ROWS) for col in range(BRICK_COLUMNS)]
                    powerups = []
                    particles = []
                    score = 0
                    lives = LIVES
                    game_state = START
            elif event.key == pygame.K_p and game_state == PLAYING:
                game_state = PAUSED
            elif event.key == pygame.K_p and game_state == PAUSED:
                game_state = PLAYING
            elif event.key == pygame.K_m:
                audio_muted = not audio_muted
                pygame.mixer.music.set_volume(0 if audio_muted else 1)
            elif event.key == pygame.K_i and game_state == START:
                game_state = INSTRUCTIONS
            elif event.key == pygame.K_BACKSPACE and game_state == INSTRUCTIONS:
                game_state = START
            elif event.key == pygame.K_ESCAPE and game_state == PLAYING:
                game_state = PAUSED

    if game_state == START:
        draw_start_screen()
    elif game_state == INSTRUCTIONS:
        draw_instructions_screen()
    elif game_state == PLAYING:
        SCREEN.fill(BLACK)
        paddle.move()
        paddle.update()
        paddle.draw()
        for ball in balls[:]:
            if ball.move(paddle, bricks, powerups):
                balls.remove(ball)
                if not balls:
                    lives -= 1
                    if lives > 0:
                        balls.append(Ball(paddle))
                    else:
                        game_state = END
                        end_time = time.time()
                        pygame.mixer.Sound.play(death_sound)
                        break
            ball.update()
            ball.draw()
        for brick in bricks:
            brick.draw()
        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle.rect):
                if powerup.powerup_type == 'extra_life':
                    lives += 1
                else:
                    for ball in balls:
                        ball.apply_powerup(powerup.powerup_type)
                    paddle.apply_powerup(powerup.powerup_type)
                powerups.remove(powerup)
                pygame.mixer.Sound.play(power_sound)
            elif powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)
            powerup.draw()
        for particle in particles[:]:
            particle.move()
            if particle.life <= 0:
                particles.remove(particle)
            particle.draw()
        score = (BRICK_ROWS * BRICK_COLUMNS - len(bricks)) * 10
        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
        SCREEN.blit(text, (20, 20))
        if not bricks:
            game_state = END
            end_time = time.time()
            pygame.mixer.Sound.play(win_sound)
        pygame.display.flip()
    elif game_state == PAUSED:
        draw_paused_screen()
    elif game_state == END:
        draw_end_screen(not bricks)
    clock.tick(60)
