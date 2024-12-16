"""A module containing Ball classes for the pool game simulation"""
import math
from config import (
    CREAM,
    BALL_MASS,
    BALL_RADIUS,
    GRAVITY,
    SLIDING_FRICTION_COEF,
    BALL_BALL_RESTITUTION,
    BALL_RAIL_RESTITUTION,
    MIN_SPEED_PX_S,
)


class Ball:
    """
    Ball class for simulating the pool game.

    Attributes:
        turtle: The turtle object used for drawing.
        physics: A dictionary containing the ball's position and velocity.
        properties: A dictionary containing the ball's number and color.
    """
    def __init__(self, pos, velocity, info, turtle):
        """
        Initialize a ball with size, position, velocity, color, and number.

        Parameters:
            pos (tuple): Initial position of the ball (x, y).
            velocity (tuple): Initial velocity of the ball (vx, vy).
            info (tuple): Contains the ball's number and color.
            turtle (Turtle): The turtle object used for drawing.

        Modifies:
            self.physics: Sets initial position and velocity.
            self.properties: Sets the ball's number and color.
        """
        self.turtle = turtle
        # Group physics attributes
        self.physics = {
            'pos': pos,
            'velocity': velocity
        }
        # Group ball properties
        self.properties = {
            'number': info[0],
            'color': info[1]
        }

    @property
    def x(self):
        """
        Get the x-coordinate of the ball's position.

        Returns:
            float: The x-coordinate of the ball's position.
        """
        return self.physics['pos'][0]

    @x.setter
    def x(self, x):
        """
        Set the x-coordinate of the ball's position.

        Modifies:
            self.physics['pos'][0]: Updates the x-coordinate of the ball's position.
        """
        self.physics['pos'][0] = x

    @property
    def y(self):
        """
        Get the y-coordinate of the ball's position.

        Returns:
            float: The y-coordinate of the ball's position.
        """
        return self.physics['pos'][1]

    @y.setter
    def y(self, y):
        """
        Set the y-coordinate of the ball's position.

        Modifies:
            self.physics['pos'][1]: Updates the y-coordinate of the ball's position.
        """
        self.physics['pos'][1] = y

    @property
    def vx(self):
        """
        Get the x-component of the ball's velocity.

        Returns:
            float: The x-component of the ball's velocity.
        """
        return self.physics['velocity'][0]

    @vx.setter
    def vx(self, vx):
        """
        Set the x-component of the ball's velocity.

        Modifies:
            self.physics['velocity'][0]: Updates the x-component of the ball's velocity.
        """
        self.physics['velocity'][0] = vx

    @property
    def vy(self):
        """
        Get the y-component of the ball's velocity.

        Returns:
            float: The y-component of the ball's velocity.
        """
        return self.physics['velocity'][1]

    @vy.setter
    def vy(self, vy):
        """
        Set the y-component of the ball's velocity.

        Modifies:
            self.physics['velocity'][1]: Updates the y-component of the ball's velocity.
        """
        self.physics['velocity'][1] = vy

    @property
    def number(self):
        """
        Get the ball's number.

        Returns:
            int: The number of the ball.
        """
        return self.properties['number']

    @property
    def color(self):
        """
        Get the ball's color.

        Returns:
            str: The color of the ball.
        """
        return self.properties['color']

    @property
    def size(self):
        """
        Get the size or radius of the ball.

        Returns:
            float: The radius of the ball.
        """
        return BALL_RADIUS

    @property
    def mass(self):
        """
        Get the mass of the ball.

        Returns:
            float: The mass of the ball.
        """
        return BALL_MASS

    def draw(self):
        """
        Draw the ball on the table.

        Modifies:
            Uses turtle to draw the ball on the canvas.
        """
        self.turtle.hideturtle()
        self.turtle.pensize(3)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - BALL_RADIUS)
        self.turtle.color(self.color)
        self.turtle.fillcolor(self.color)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(BALL_RADIUS)
        self.turtle.end_fill()
        self._draw_inner_number()
        self.turtle.pensize(0)

    def _draw_inner_number(self):
        """
        Draw the number on the ball.

        Modifies:
            Uses turtle to draw the number on the ball.
        """
        inner_white_radius = BALL_RADIUS * 0.5
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - inner_white_radius)
        self.turtle.pendown()
        self.turtle.color(CREAM)  # Cream color
        self.turtle.begin_fill()
        self.turtle.circle(inner_white_radius)
        self.turtle.end_fill()

        # Draw the number in the center
        self.turtle.penup()
        self.turtle.goto(
            self.x + (BALL_RADIUS * 0.1245),
            self.y - (BALL_RADIUS * 0.575)
        )
        self.turtle.color("black")
        font_size = int(BALL_RADIUS / 1.4)  # Slightly smaller font size
        self.turtle.write(
            str(self.number),
            align="center",
            font=("Helvetica",
                  font_size,
                  "bold")
        )

    def distance(self, other):
        """Calculate the distance to another ball"""
        return math.sqrt((other.y - self.y) ** 2 + (other.x - self.x) ** 2)

    def bounce_off_horizontal_rail(self, canvas_width):
        """
        Handle collisions with the horizontal edges of the table.

        Parameters:
            canvas_width (float): The width of the canvas.

        Modifies:
            self.x: Adjusts position if collision occurs.
            self.vx: Adjusts velocity based on collision.
        """
        # Apply COR between ball and rail
        if self.x - BALL_RADIUS < -canvas_width:
            self.x = -canvas_width + BALL_RADIUS
            self.vx = -BALL_RAIL_RESTITUTION * self.vx
        elif self.x + BALL_RADIUS > canvas_width:
            self.x = canvas_width - BALL_RADIUS
            self.vx = -BALL_RAIL_RESTITUTION * self.vx

    def bounce_off_vertical_rail(self, canvas_height):
        """
        Handle collisions with the vertical edges of the table.

        Parameters:
            canvas_height (float): The height of the canvas.

        Modifies:
            self.y: Adjusts position if collision occurs.
            self.vy: Adjusts velocity based on collision.
        """
        # Apply COR between ball and rail
        if self.y - BALL_RADIUS < -canvas_height:
            self.y = -canvas_height + BALL_RADIUS
            self.vy = -BALL_RAIL_RESTITUTION * self.vy
        elif self.y + BALL_RADIUS > canvas_height:
            self.y = canvas_height - BALL_RADIUS
            self.vy = -BALL_RAIL_RESTITUTION * self.vy

    def bounce_off(self, other):
        """
        Handle ball-to-ball collisions with energy preservation.

        Parameters:
            other (Ball): The other ball involved in the collision.

        Modifies:
            self.vx, self.vy: Adjusts velocity based on collision.
            other.vx, other.vy: Adjusts velocity of the other ball.
        """
        dx = other.x - self.x
        dy = other.y - self.y
        dist = self.distance(other)
        if dist == 0:  # Prevent division by zero
            return

        # Unit normal vector
        nx = dx / dist
        ny = dy / dist

        # Relative velocity
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        vn = dvx * nx + dvy * ny  # Normal velocity

        if vn > 0:  # Balls moving away
            return

        # Compute impulse
        e = BALL_BALL_RESTITUTION
        impulse = -(1 + e) * vn / (1 / self.mass + 1 / other.mass)

        # Apply impulse
        self.vx -= impulse * nx / self.mass
        self.vy -= impulse * ny / self.mass
        other.vx += impulse * nx / other.mass
        other.vy += impulse * ny / other.mass
        # playsound("collision.mp3")

    def move(self, dt):
        """
        Update the ball's position and velocity with friction.

        Parameters:
            dt (float): Time step for the movement.

        Modifies:
            self.x, self.y: Updates position based on velocity.
            self.vx, self.vy: Updates velocity based on friction.
        """
        friction_force = (1 + SLIDING_FRICTION_COEF) * self.mass * GRAVITY
        speed = self._speed()
        if speed > 0:
            # Calculate direction
            dx = self.vx / speed
            dy = self.vy / speed
            # Calculate frictional acceleration
            ax = -friction_force / self.mass * dx
            ay = -friction_force / self.mass * dy
            # Update velocities
            self.vx += ax * dt
            self.vy += ay * dt
            # Stop ball if velocity falls below threshold
            if self._speed() < MIN_SPEED_PX_S:
                self.vx, self.vy = 0, 0
        else:  # Ball is not moving at the first place
            self.vx, self.vy = 0, 0

        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def _speed(self):
        """
        Calculate the speed of the ball.

        Returns:
            float: The current speed of the ball.
        """
        return math.sqrt(self.vx**2 + self.vy**2)

    def is_moving(self):
        """
        Check if the ball is moving.

        Returns:
            bool: True if the ball is moving, False otherwise.
        """
        return self.vx != 0 or self.vy != 0

    def __str__(self):
        """
        Return a string representation of the ball's state.

        Returns:
            str: A string describing the ball's number, position, and speed.
        """
        out = f"Ball {self.number}: Pos=({self.x:.2f}, {self.y:.2f})"
        out += f", Spd=({self.vx:.2f}, {self.vy:.2f})"
        return out


class CueBall(Ball):
    """
    Inheritance class for cue ball.

    Attributes:
        Inherits all attributes from Ball.
    """

    def draw(self):
        """
        Draw the cue ball.

        Modifies:
            Uses turtle to draw the cue ball on the canvas.
        """
        self.turtle.hideturtle()
        self.turtle.pensize(3)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - BALL_RADIUS)
        self.turtle.color(self.color)
        self.turtle.fillcolor(self.color)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(BALL_RADIUS)
        self.turtle.end_fill()
        self.turtle.pensize(0)


class StripeBall(Ball):
    """
    Inheritance class for stripe ball.

    Attributes:
        __stripe_color: The color of the stripe on the ball.
        Inherits all attributes from Ball.
    """

    def __init__(self, pos, velocity, info, turtle):
        """
        Initialize a stripe ball with position, velocity, color, and stripe color.

        Parameters:
            pos (tuple): Initial position of the ball (x, y).
            velocity (tuple): Initial velocity of the ball (vx, vy).
            info (tuple): Contains the ball's number, color, and stripe color.
            turtle (Turtle): The turtle object used for drawing.

        Modifies:
            self.__stripe_color: Sets the stripe color.
        """
        super().__init__(pos, velocity, info, turtle)
        self.__stripe_color = info[2]  # Get stripe color from info tuple

    def draw(self):
        """
        Draw the striped ball.

        Modifies:
            Uses turtle to draw the striped ball on the canvas.
        """
        self.turtle.hideturtle()
        self.turtle.pensize(3)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - BALL_RADIUS)
        self.turtle.color(self.color)  # Cream base
        self.turtle.fillcolor(self.color)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(BALL_RADIUS)
        self.turtle.end_fill()

        self._draw_stripe()
        self._draw_inner_number()
        self.turtle.pensize(0)

    def _draw_stripe(self):
        """
        Draw the stripe on the ball.

        Modifies:
            Uses turtle to draw the stripe on the ball.
        """
        stripe_radius = BALL_RADIUS * 0.8
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - stripe_radius)
        self.turtle.pendown()
        self.turtle.color(self.__stripe_color, self.__stripe_color)
        self.turtle.begin_fill()
        self.turtle.circle(stripe_radius)
        self.turtle.end_fill()
