# Brick Breaker Game

## Overview

Brick Breaker is a classic arcade-style game where players control a paddle to bounce a ball and break bricks. The game features various power-ups, sound effects, and dynamic gameplay elements to keep players engaged.

## Features

- **Paddle Movement**: Use the LEFT and RIGHT arrow keys to move the paddle.
- **Brick Breaking**: Bounce the ball off the paddle to break bricks of different colors and hit points.
- **Power-Ups**: Collect power-ups that offer special abilities or enhancements.
- **Particles**: Visual effects when bricks are destroyed.
- **Sound and Music**: Includes sound effects for interactions and background music.
- **Scoring**: Earn points based on the number of bricks destroyed.
- **Lives**: Keep track of lives and restart the game if all lives are lost.

## Getting Started

### Requirements

- Python 3.x
- Pygame library

You can install Pygame using pip if you haven't already:

```bash
pip install pygame
```

### Installation

1. Clone or download the repository.
2. Place your audio files (e.g., `start.mp3`, `brick.mp3`, `power.mp3`, `death.mp3`, `win.mp3`, and `background_music.mp3`) in an `audio` directory within the project folder.

### Running the Game

Navigate to the directory where the script is located and run:

```bash
python brick.py
```

## Controls

- **SPACE**: Start or restart the game.
- **LEFT Arrow**: Move the paddle left.
- **RIGHT Arrow**: Move the paddle right.
- **P**: Pause or resume the game.
- **M**: Mute or unmute the audio.
- **I**: View instructions.
- **BACKSPACE**: Go back to the start screen from instructions.
- **ESC**: Pause the game.

## Game States

- **START**: The initial screen where you press SPACE to start the game.
- **INSTRUCTIONS**: Displays how to play the game.
- **PLAYING**: The main gameplay state.
- **PAUSED**: The game is paused.
- **END**: The game has ended, displaying the result.

## Classes

### `Paddle`

Manages the paddle's position and its interactions with power-ups.

### `Ball`

Handles the ball's movement, collisions, and power-up effects.

### `Brick`

Represents a brick with varying hit points and colors.

### `PowerUp`

Represents power-ups that fall from broken bricks and provides special abilities.

### `Particle`

Visual effects that occur when a brick is destroyed.

## Audio Files

Ensure you have the following audio files in the `audio` directory:

- `start.mp3`: Sound played when the game starts.
- `brick.mp3`: Sound played when a brick is hit.
- `power.mp3`: Sound played when a power-up is collected.
- `death.mp3`: Sound played when the player loses all lives.
- `win.mp3`: Sound played when the player wins.
- `background_music.mp3`: Music played in the background during the game.

## Troubleshooting

- **Audio Issues**: Ensure audio files are correctly placed and named in the `audio` directory.
- **Performance**: If the game runs slowly, try adjusting the game loop's `clock.tick` value.

## Contributing

Feel free to fork the repository and submit pull requests with improvements or fixes. Ensure any changes are well-tested and documented.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy breaking bricks and collecting power-ups! 🚀🎮
