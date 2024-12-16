"""Module containing the CueStick class for the pool game simulation."""

import math
from config import (
    MAX_SPEED_PX_S,
    OFFSET,
    BALL_RADIUS,
    PEN_SIZE,
    CUESTICK_HANDLE_COLOR,
    CUESTICK_LENGTH,
    CUESTICK_THICKNESS,
    CUESTICK_SHAFT_COLOR,
    CUESTICK_TIP_COLOR,
    ANGLE_STEP,
)


class CueStick:
    """
    Represents a cue stick used to strike the cue ball in a pool game.

    Attributes:
        # _state (dict): All cue stick state data
            - cueball: Reference to cue ball [GET]
            - angle: Current aiming angle [GET] [SET]
            - offset: Distance from cue ball [GET] [SET]
            - power: Shot power (0-100) [GET] [SET]
            - shot_position: Last position after shooting [GET] [SET]
            - shot_angle: Angle of last shot [GET] [SET]
        + turtle: Turtle object for drawing
    """

    def __init__(self, cueball, myturtle):
        self._state = {
            'cueball': cueball,
            'angle': 180,
            'offset': OFFSET,
            'power': 0,
            'shot_position': None,
            'shot_angle': None
        }
        self.turtle = myturtle
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.hideturtle()

    @property
    def pow(self):
        """
        Get the current shot power.
        """
        return self._state['power']

    @pow.setter
    def pow(self, value):
        """
        Set the shot power, ensuring it stays within limits.
        """
        if 0 <= value <= 100:
            self._state['power'] = value

    @property
    def angle(self):
        """
        Get the current aiming angle of the cue stick.
        """
        return int(self._state['angle'])

    @angle.setter
    def angle(self, value):
        """
        Set the aiming angle, keeping it within 0-360 degrees.
        """
        self._state['angle'] = value % 360

    @property
    def offset(self):
        """
        Get the current distance between the cue stick and the cue ball.
        """
        return self._state['offset']

    @offset.setter
    def offset(self, value):
        """
        Set the offset, ensuring it stays positive.
        """
        if value > 0:
            self._state['offset'] = value
        else:
            raise ValueError("Offset must be greater than zero.")

    @property
    def shot_position(self):
        """
        Get the last position of the cue stick after shooting.
        """
        return self._state['shot_position']

    @shot_position.setter
    def shot_position(self, state):
        """
        Set the last position of the cue stick after shooting.
        """
        self._state['shot_position'] = state

    @property
    def shot_angle(self):
        """
        Get the angle of the last shot.
        """
        return self._state['shot_angle']

    @shot_angle.setter
    def shot_angle(self, val):
        """
        Set the angle of the last shot.
        """
        self._state['shot_angle'] = val

    def draw(self, x, y, angle_rad):
        """
        Draw the cue stick on the screen with a dynamic tapering effect.

        Parameters:
            x (float): The x-coordinate of the cue ball.
            y (float): The y-coordinate of the cue ball.
            angle_rad (float): The angle in radians at which the cue stick is drawn.

        Modifies:
            self.turtle: Updates the visual representation of the cue stick.
        """
        # Define section widths
        widths = {
            'tip': CUESTICK_THICKNESS / 1.125,
            'middle': CUESTICK_THICKNESS,
            'butt': CUESTICK_THICKNESS * 1.75
        }

        # Calculate positions
        positions = {
            'tip': (
                x + self.offset * math.cos(angle_rad),
                y + self.offset * math.sin(angle_rad)
            ),
            'middle': (
                x + (self.offset + CUESTICK_LENGTH / 2) * math.cos(angle_rad),
                y + (self.offset + CUESTICK_LENGTH / 2) * math.sin(angle_rad)
            ),
            'butt': (
                x + (self.offset + CUESTICK_LENGTH) * math.cos(angle_rad),
                y + (self.offset + CUESTICK_LENGTH) * math.sin(angle_rad)
            )
        }

        # Mid / Bottom position for creating cue stick detail
        midbut = (
            (positions['butt'][0] + 1.5 * positions['middle'][0]) / 2.5,
            (positions['butt'][1] + 1.5 * positions['middle'][1]) / 2.5
        )

        # Calculate corners for each section
        corners = {
            section: {
                'left': (
                    pos_x - widths[section] * math.sin(angle_rad),
                    pos_y + widths[section] * math.cos(angle_rad)
                ),
                'right': (
                    pos_x + widths[section] * math.sin(angle_rad),
                    pos_y - widths[section] * math.cos(angle_rad)
                )
            }
            for section, (pos_x, pos_y) in positions.items()
        }

        # Draw the cue stick
        self._draw_tip(*positions['tip'], angle_rad)
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
        """
        Helper method to draw a section of the cue stick.
        """
        self.turtle.goto(*start_pos)
        for point in points:
            self.turtle.goto(*point)
        self.turtle.goto(*start_pos)

    def _draw_tip(self, tip_x, tip_y, angle_rad):
        """
        Draw a small tip at the end of the cue stick.
        """
        x = tip_x + (CUESTICK_THICKNESS / 2 * math.cos(angle_rad))
        y = tip_y + (CUESTICK_THICKNESS / 2 * math.sin(angle_rad))
        self.turtle.goto(x, y)
        self.turtle.color(CUESTICK_TIP_COLOR)
        self.turtle.setheading(self.angle + 90)  # Face the cue ball
        self.turtle.begin_fill()
        self.turtle.circle(CUESTICK_THICKNESS)  # Small circle tip
        self.turtle.end_fill()

    def rotate(self, angle):
        """
        Rotate the cue stick around the cue ball.

        Parameters:
            angle (float): Angle to rotate the cue stick.

        Modifies:
            self.angle: Updates the cue stick's angle.
            self.turtle: Redraws the cue stick at new angle.

        Explanation:
            The rotation is animated smoothly by breaking it into small steps.
            It uses the shortest path to reach the target angle and updates
            the screen after each small rotation to create fluid motion.
        """
        target_angle = (self.angle + angle) % 360  # Keep angle within 0-360

        # Calculate the shortest rotation direction
        delta_angle = (target_angle - self.angle + 540) % 360 - 180
        angle_step = delta_angle / ANGLE_STEP  # Angle increment per step

        for _ in range(ANGLE_STEP):  # Increase steps for smoother rotation
            # Adjust angle increment
            self.angle = (self.angle + angle_step) % 360
            self.update_position()  # Redraw cue stick
            self.turtle.getscreen().update()  # Refresh the screen
            self.turtle.getscreen().ontimer(lambda: None, 10)  # Reduce delay for smoothness
        print(self)
        self.update_position()

    def power(self, power):
        """
        Adjust the cue stick's power and offset.

        Parameters:
            power (float): Power adjustment value.

        Modifies:
            self.power: Updates the shot power.
            self.offset: Adjusts distance from cue ball.
            self.turtle: Redraws the cue stick at new position.
        """
        if 0 <= self.pow + power <= 100:
            self.pow += power
            self.offset += power / 10
            print(self)
            self.update_position()

    def shoot(self):
        """
        Shoot the cue ball and freeze the cue stick's position.

        Modifies:
            self.shot_position: Saves current position.
            self.shot_angle: Saves current angle.
            self._physics['cue_ball'].vx, self._physics['cue_ball'].vy: Updates cue ball velocity.
            self.turtle: Animates the shooting motion.

        Returns:
            None

        Explanation:
            The shooting process involves three main steps:
            1. Pull back animation - cue stick moves away from the ball
            2. Forward stroke animation - cue stick moves toward the ball
            3. Impact calculation - converts power and angle into ball velocity

            The shot power determines both the pull-back distance and the final
            velocity of the cue ball. A power of 0 will result in no shot.
        """
        if self.pow != 0:  # Do nothing if there's no power
            offset = self.offset  # Save initial offset
            # Scale pull-back with power
            pull_back_dist = offset * (self.pow / 50)

            # Animations for pulling back and shooting
            self.pullback_animation(offset, pull_back_dist)
            self.turtle.getscreen().ontimer(lambda: None, 50)  # Small delay
            self.shooting_animation(offset, pull_back_dist)

            # Save shot state
            self.shot_position = [
                self._state['cueball'].x, self._state['cueball'].y]
            self.shot_angle = self.angle

            # Update cue ball velocity
            angle_rad = math.radians(self.angle)
            velocity = (self.pow / 100) * MAX_SPEED_PX_S
            self._state['cueball'].vx = -velocity * math.cos(angle_rad)
            self._state['cueball'].vy = -velocity * math.sin(angle_rad)
        print(f"Shoot with {self.pow}% power, at angle of {self.angle} deg")

    def shooting_animation(self, offset, pull_back_dist):
        """
        Animate the cue stick moving forward to strike the cue ball.

        Parameters:
            offset (float): The initial offset of the cue stick from the cue ball.
            pull_back_dist (float): The distance the cue stick was pulled back.
        """
        i = 0
        while self.offset - BALL_RADIUS - PEN_SIZE > 0:
            # Gradually decrease the offset to simulate forward motion
            self.offset = offset + pull_back_dist * (1 - (i / 20))
            self.update_position()  # Redraw the cue stick at the new position
            self.turtle.getscreen().update()  # Refresh the screen
            self.turtle.getscreen().ontimer(lambda: None, 10)  # delay for smoothness
            i += 1

    def pullback_animation(self, offset, pull_back_dist):
        """
        Animate the cue stick pulling back before shooting.

        Parameters:
            offset (float): The initial offset of the cue stick from the cue ball.
            pull_back_dist (float): The maximum distance the cue stick is pulled back.
        """
        for i in range(125):  # Incremental animation steps
            self.offset = offset + (pull_back_dist * (i / 125))
            self.update_position()  # Redraw cue stick
            self.turtle.getscreen().update()  # Refresh the screen
            self.turtle.getscreen().ontimer(lambda: None, 10)  # Delay for smoothness

    def update_position(self):
        """Update the visual position of the cue stick on the screen."""
        self.turtle.clear()
        if self.shot_position:
            x, y = self.shot_position
            angle_rad = math.radians(self.shot_angle)
        else:
            x, y = self._state['cueball'].x, self._state['cueball'].y
            angle_rad = math.radians(self.angle)
        self.draw(x, y, angle_rad)

    def reset(self):
        """Reset the cue stick to follow the cue ball again."""
        self.shot_position = None  # Clear static position
        self.shot_angle = None  # Clear shot angle
        self.angle = 270  # Reset angle for aiming
        self.pow = 0  # Reset power for next shot
        self.offset = OFFSET  # Reset distance
        self.update_position()  # Dynamically follow the cue ball

    def __str__(self):
        """Return a string representation of the cue stick's current state."""
        return f"Current power {self.pow}, Current angle {self.angle}"
