import math
import copy
from config import (
    MAX_SPEED_PX_S,
    OFFSET,
    CUESTICK_HANDLE_COLOR,
    CUESTICK_LENGTH,
    CUESTICK_THICKNESS,
    CUESTICK_SHAFT_COLOR,
    CUESTICK_TIP_COLOR,
)


class CueStick:
    """Class representing the cue stick."""
    def __init__(self, cueball, myturtle):
        """Initialize the cue stick."""
        self.cueball = cueball  # Reference to the cue ball
        self.angle = 180        # Initial aiming angle
        self.offset = OFFSET    # Distance between cue stick and cue ball
        self.power = 0          # Shot power
        self.shot_position = None  # Store the last position after shooting
        self.shot_angle = None     # Store the angle of the last shot

        # Turtle setup
        self.turtle = myturtle
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.hideturtle()

    def draw(self, x, y, angle_rad):
        """Draw the cue stick dynamically, tapering towards the middle."""
        # Define widths for each section
        widths = {
            'tip': CUESTICK_THICKNESS / 1.125,
            'middle': CUESTICK_THICKNESS,
            'butt': CUESTICK_THICKNESS * 1.75
        }
    
        # Calculate main positions
        positions = {
            'tip': (
                x + (self.offset * math.cos(angle_rad)),
                y + (self.offset * math.sin(angle_rad))
            ),
            'middle': (
                x + (self.offset + CUESTICK_LENGTH/2) * math.cos(angle_rad),
                y + (self.offset + CUESTICK_LENGTH/2) * math.sin(angle_rad)
            ),
            'butt': (
                x + (self.offset + CUESTICK_LENGTH) * math.cos(angle_rad),
                y + (self.offset + CUESTICK_LENGTH) * math.sin(angle_rad)
            )
        }
    
        # Calculate midbut position
        midbut = (
            (positions['butt'][0] + 1.5 * positions['middle'][0]) / 2.5,
            (positions['butt'][1] + 1.5 * positions['middle'][1]) / 2.5
        )
    
        # Calculate corners for each section
        corners = {}
        for section, (pos_x, pos_y) in positions.items():
            width = widths[section]
            corners[section] = {
                'left': (
                    pos_x - width * math.sin(angle_rad),
                    pos_y + width * math.cos(angle_rad)
                ),
                'right': (
                    pos_x + width * math.sin(angle_rad),
                    pos_y - width * math.cos(angle_rad)
                )
            }
    
        # Draw the cue stick
        self._draw_tip(*positions['tip'], angle_rad)
        # Draw handle
        self.turtle.penup()
        self.turtle.goto(*midbut)
        self.turtle.pendown()
        self.turtle.color(CUESTICK_HANDLE_COLOR)
        self.turtle.begin_fill()
        self._draw_section(
            midbut,
            corners['middle']['left'],
            corners['butt']['left'],
            corners['butt']['right'],
            corners['middle']['right']
        )
        self.turtle.end_fill()
        # Draw shaft
        self.turtle.color(CUESTICK_SHAFT_COLOR)
        self.turtle.begin_fill()
        self._draw_section(
            midbut,
            corners['middle']['left'],
            corners['tip']['left'],
            corners['tip']['right'],
            corners['middle']['right']
        )
        self.turtle.end_fill()
        self.turtle.penup()

    def _draw_section(self, start_pos, *points):
        """Helper method to draw a section of the cue stick."""
        self.turtle.goto(*start_pos)
        for point in points:
            self.turtle.goto(*point)
        self.turtle.goto(*start_pos)

    def _draw_tip(self, tip_x, tip_y, angle_rad):
        """Draw a small tip at the end of the cue stick."""
        x = tip_x + (CUESTICK_THICKNESS / 2 * math.cos(angle_rad))
        y = tip_y + (CUESTICK_THICKNESS / 2 * math.sin(angle_rad))
        self.turtle.goto(x, y)
        self.turtle.color(CUESTICK_TIP_COLOR)  # Cue stick tip
        self.turtle.setheading(self.angle + 90)  # Adjust to face the cue ball
        self.turtle.begin_fill()
        self.turtle.circle(CUESTICK_THICKNESS)  # Small circle tip
        self.turtle.end_fill()

    def _rotate(self, angle):
        """Rotate the cue stick around the cue ball."""
        self.angle += angle
        self.angle %= 360  # Keep the angle within 0-360 degrees
        print(self)
        self._update_position()

    def _power(self, power):
        """Adjust the cue stick's power and offset."""
        if 0 <= self.power + power <= 100:
            self.power += power
            self.offset += power / 10
            print(self)
            self._update_position()

    def shoot(self):
        """Shoot the cue ball and freeze the cue stick's position."""
        # simulate the cue stick moving toward the cue ball
        self.shooting_animation()
        # Save state
        self.shot_position = [self.cueball.x, self.cueball.y]
        self.shot_angle = self.angle
        # Hit the ball
        angle_rad = math.radians(self.angle)
        velocity = (self.power / 100) * MAX_SPEED_PX_S
        self.cueball.vx = -velocity * math.cos(angle_rad)  # Update cue ball velocity
        self.cueball.vy = -velocity * math.sin(angle_rad)
        print(f"Shoot with {self.power}% power, at angle of {self.angle} degree")
    
    def shooting_animation(self):
        """Animate the cue stick pulling back and then shooting forward."""
        original_offset = self.offset  # Save the initial offset
        pull_back_distance = original_offset * (0.2 + self.power / 500)  # Scale pull-back with power
    
        # Pull-back animation
        for _ in range(10):  # 10 steps for pull-back
            self.offset = original_offset + (pull_back_distance * (_ / 10))  # Smooth pull back
            self._update_position()  # Redraw cue stick
            self.turtle.getscreen().update()  # Refresh the screen
            self.turtle.getscreen().ontimer(lambda: None, 20)  # Small delay for smoothness
    
        # Forward shooting animation
        for _ in range(50):  # 30 steps for shooting forward
            self.offset = original_offset + pull_back_distance * (1 - _ / 30)  # Gradually return to impact
            self._update_position()  # Redraw cue stick
            self.turtle.getscreen().update()  # Refresh the screen
            self.turtle.getscreen().ontimer(lambda: None, 10)  # Small delay for smoothness
    
        # Clear the cue stick drawing upon impact
        self.turtle.clear()
    
        # Restore the original offset and set shot position
        self.offset = original_offset
        self.shot_position = [self.cueball.x, self.cueball.y]
        self.shot_angle = self.angle

    def _update_position(self):
        """Update the position of the cue stick dynamically."""
        self.turtle.clear()
        if self.shot_position:
            x, y = self.shot_position
            angle_rad = math.radians(self.shot_angle)
        else:
            x, y = self.cueball.x, self.cueball.y
            angle_rad = math.radians(self.angle)
        self.draw(x, y, angle_rad)

    def reset(self):
        """Reset the cue stick to follow the cue ball again."""
        self.shot_position = None  # Clear static position
        self.shot_angle = None     # Clear shot angle
        self.angle = 270           # Reset angle for aiming
        self.power = 0             # Reset power for next shot
        self.offset = OFFSET       # Reset distance
        self._update_position()    # Dynamically follow the cue ball
    def __str__(self):
        return f"Current power {self.power}, Current angle {self.angle}"