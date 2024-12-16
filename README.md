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
1. **Collision Dynamics:**
   - Elastic collisions (e ≈ 0.96)
   - Momentum conservation
   - Impulse calculations

2. **Friction Forces:**
   ```
   F(friction) = μmg
   where:
   μ = friction coefficient
   m = ball mass
   g = gravity
   ```

3. **Table Dimensions:**
   - Length: 9ft (900px)
   - Width: 4.5ft (450px)
   - Scale: 1ft = 100px

---

## Project Architecture

### Key Classes
```mermaid
[Your existing class diagram here]
```

### Core Components
- **`PoolGame`:** Main game controller
- **`Ball` Family:** Ball physics and behaviors
- **`CueStick`:** Shot mechanics
- **`Table`:** Table and pocket handling
- **`PhysicsEngine`:** Physics calculations
- **`Handler`:** Collision detection

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