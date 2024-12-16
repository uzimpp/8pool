# Pool Game Simulator

## Project Title
Physics-Based Pool Game Simulation

## Description
A realistic pool game simulator implementing accurate physics for ball collisions, friction, and cue stick mechanics. Built with Python and Turtle graphics, it offers an engaging experience with realistic ball movements and game rules.

---

## Overview
The **Pool Game Simulator** combines physics simulation with interactive gameplay. Players use a cue stick to strike balls, considering angles, power, and ball interactions. The game features realistic physics including elastic collisions, friction, and momentum conservation.

---

## Features

### Core Mechanics
- **Physics Simulation:**
  - Elastic collisions between balls
  - Rail bounces with energy loss
  - Rolling friction on cloth
  - Realistic cue ball mechanics

### Game Elements
- **Player Control:**
  - Intuitive cue stick aiming
  - Power adjustment system
  - Shot preview guidelines
- **Visual Elements:**
  - Realistic pool table rendering
  - Numbered and striped balls
  - Dynamic cue stick visualization
  - Smooth animations

---

## Installation & Setup

### Prerequisites
- Python 3.x
- Turtle graphics (built-in)

### Steps
1. **Clone Repository:**
```bash
git clone [repository-url]
```

2. **Navigate to Project:**
```bash
cd pool
```

3. **Run Setup Script:**
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

---

## Controls
- **A/D:** Rotate cue stick (counter-clockwise/clockwise)
- **W/S:** Adjust shot power (increase/decrease)
- **Space:** Execute shot
- **Enter:** Restart after winning
- **Cancel:** Quit after winning

---

## Physics Implementation

### Physical Properties
Based on [Dr. Dave's Billiards Physics](https://billiards.colostate.edu/faq/physics/physical-properties/):

```python
# Core Constants
BALL_RADIUS = 12px        # 2.25 inches
BALL_MASS = 0.17kg        # 6 oz
SLIDING_FRICTION = 0.2    # Cloth friction
BALL_RESTITUTION = 0.96   # Collision elasticity
```

### Key Physics Concepts

1. **Ball Movement and Friction:**
   - Balls move according to their velocity, which is updated every frame.
   - Friction is applied to simulate the slowing effect of the table cloth, calculated as `F(friction) = μmg`, where `μ` is the friction coefficient, `m` is the ball mass, and `g` is gravity.

2. **Collision Dynamics:**
   - **Elastic Collisions:** When balls collide, their velocities are updated using the coefficient of restitution (e ≈ 0.96), ensuring energy conservation.
   - **Rail Bounces:** Balls bounce off table edges with some energy loss, modeled by a lower restitution coefficient for rail collisions.

3. **Pocket Detection:**
   - Balls are checked for proximity to pockets. If a ball is close enough, it is considered pocketed and removed from play.
   - The cue ball is repositioned if pocketed, simulating a scratch.

4. **Cue Stick Mechanics:**
   - The cue stick's angle and power are adjustable, affecting the direction and speed of the cue ball.
   - The shot power determines the velocity imparted to the cue ball, with a maximum speed limit to ensure realistic gameplay.

5. **Table Dimensions:**
   - Length: 9ft (900px)
   - Width: 4.5ft (450px)
   - Scale: 1ft = 100px

---

## Project Architecture

### Core Components
- **`PoolGame`:** 
  - Main game controller managing game states and user interactions
  - Handles game loop, input processing, and display updates
  - Coordinates interactions between all other components

- **`Ball` Family:** 
  - Base class implementing physics-based ball behavior
  - `CueBall`: Special white ball that players strike directly
  - `StripeBall`: Implements striped ball visuals (numbers 9-15)
  - Handles movement, collisions, and visual rendering

- **`CueStick`:** 
  - Manages cue stick positioning, power, and shooting mechanics
  - Provides visual feedback for aiming and power
  - Handles shot execution and animation

- **`Table`:** 
  - Renders the pool table surface and pockets
  - Manages pocket collision detection
  - Tracks pocketed balls and handles ball removal

- **`PhysicsEngine`:** 
  - Implements core physics calculations:
    - Ball-to-ball collisions using coefficient of restitution
    - Rail bounces with energy loss
    - Friction and velocity calculations
  - Updates ball positions and velocities

- **`Handler`:** 
  - Manages intersection calculations for:
    - Ball-to-rail collisions
    - Ball-to-ball collisions
    - Guide line projections
  - Provides utility functions for collision detection

### Class Relationships
```mermaid
[Your existing class diagram here]
```

### Key Interactions
1. **Shot Execution:**
   - Player adjusts `CueStick` angle and power
   - `CueStick` transfers momentum to `CueBall`
   - `PhysicsEngine` calculates resulting velocities

2. **Collision Handling:**
   - `PhysicsEngine` detects collisions
   - `Handler` calculates intersection points
   - `Ball` objects update their velocities

3. **Game State Management:**
   - `PoolGame` monitors ball positions and velocities
   - `Table` checks for pocketed balls
   - Game state updates based on remaining balls

---

## Game Rules
1. **Basic Rules:**
   - Strike the cue ball to pocket numbered balls
   - Win by pocketing all balls except cue ball
   - Scratch results in cue ball repositioning

2. **Ball Colors:**
   - Solids: 1-7 (yellow, blue, red, purple, orange, green, brown)
   - Black: 8
   - Stripes: 9-15 (matching solid colors)
   - Cue: White

---

## Testing & Quality
- Fully compliant with Pylint
- Check code quality:
```bash
pylint src/*.py
```

### Known Issues
- [List any known bugs or limitations]

---

## Project Structure
```
pool/
├── src/
│   ├── poolgame.py    # Main controller
│   ├── ball.py        # Ball physics
│   ├── cuestick.py    # Cue mechanics
│   ├── table.py       # Table handling
│   ├── physic.py      # Physics engine
│   ├── handler.py     # Collision detection
│   ├── config.py      # Constants
│   └── display.py     # Display management
└── README.md
```

---

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Open pull request

---

## License
MIT License - See LICENSE file for details