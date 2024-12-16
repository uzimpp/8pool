"""Module containing ball classes for the pool game simulation."""

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
    Base class for all pool balls in the simulation.

    Attributes:
        # _physics (dict): Contains position and velocity data
            - 'pos': [x, y] position coordinates [GET] [SET]
            - 'velocity': [vx, vy] velocity components [GET] [SET]
        # _properties (dict): Contains ball characteristics
            - 'number': Ball number (1-15, None for cue ball) [GET]
            - 'color': RGB color tuple [GET]
        + turtle: Turtle object for drawing

    Modifies:
        - Ball's position and velocity through physics calculations
        - Visual representation through turtle graphics
        - Collision responses with other balls and rails

    Returns:
        None directly, but provides properties for accessing ball state

    Explanation:
        The ball simulates realistic pool physics including:
        - Rolling friction on the table cloth
        - Elastic collisions with other balls
        - Rail bounces with energy loss
        - Automatic stopping when speed becomes negligible
    """

    def __init__(self, pos, velocity, info, turtle):
        """
        Initialize a ball with position, velocity, and visual properties.

        Parameters:
            pos (list): Initial [x, y] position
            velocity (list): Initial [vx, vy] velocity
            info (list): Ball properties [number, color]
            turtle: Turtle graphics object for drawing

        Modifies:
            self._physics: Sets initial position and velocity
            self._properties: Sets ball number and color
            self.turtle: Configures drawing object
        """
        self.turtle = turtle
        self._physics = {
            'pos': pos,
            'velocity': velocity
        }
        self._properties = {
            'number': info[0],
            'color': info[1]
        }

    @property
    def x(self):
        """
        Get the x-coordinate of the ball's position.
        """
        return self._physics['pos'][0]

    @x.setter
    def x(self, x):
        """
        Set the x-coordinate of the ball's position.
        """
        self._physics['pos'][0] = x

    @property
    def y(self):
        """
        Get the y-coordinate of the ball's position.
        """
        return self._physics['pos'][1]

    @y.setter
    def y(self, y):
        """
        Set the y-coordinate of the ball's position.
        """
        self._physics['pos'][1] = y

    @property
    def vx(self):
        """
        Get the x-component of the ball's velocity.
        """
        return self._physics['velocity'][0]

    @vx.setter
    def vx(self, vx):
        """
        Set the x-component of the ball's velocity.
        """
        self._physics['velocity'][0] = vx

    @property
    def vy(self):
        """
        Get the y-component of the ball's velocity.
        """
        return self._physics['velocity'][1]

    @vy.setter
    def vy(self, vy):
        """
        Set the y-component of the ball's velocity.
        """
        self._physics['velocity'][1] = vy

    @property
    def number(self):
        """
        Get the ball's number.
        """
        return self._properties['number']

    @property
    def color(self):
        """
        Get the ball's color.
        """
        return self._properties['color']

    @property
    def size(self):
        """
        Get the size or radius of the ball.
        """
        return BALL_RADIUS

    @property
    def mass(self):
        """
        Get the mass of the ball.
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
        
        Physics Explanation:
            The coefficient of restitution (COR or e) is like a "bounciness" factor for collisions.
            It tells us how much energy is kept after two objects hit each other. A COR of 1
            means the collision is very bouncy (no energy lost), while 0 means all energy is lost
            during the collisions.

            In this pool game, I use the COR for calculating the impulse during
            a collision. Impulse is the change in momentum resulting from the collision,
            and it is applied to both balls to adjust their loss in velocities.
            For pool balls, the COR is around 0.96.
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
        e = BALL_BALL_RESTITUTION # coefficient of restitution (COR or e)
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
        
        Physics Explanation:
            The ball's movement is affected by friction, which slows it down over time.
            Friction is a force that opposes the motion of the ball (F = µmg).

            In this simulation, I use frictional force to adjust the ball's velocity.
            If the speed drops below a certain level, the ball is considered to have stopped.
            This is because it would took a while to decelerate when it come to a certain point.
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
    Special ball class representing the cue ball.

    Attributes:
        Inherits from Ball:
            # _physics (dict)
            # _properties (dict)
            + turtle

    Explanation:
        The cue ball is a special ball that:
        - Is struck directly by the cue stick
        - Has a simpler visual appearance (no number)
        - Can be repositioned after being pocketed
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
    Special ball class representing striped balls (9-15).

    Attributes:
        Inherits from Ball:
            # _physics (dict)
            # _properties (dict)
            + turtle
        - _stripe_color: Color of the stripe pattern

    Explanation:
        Striped balls have:
        - A base color (cream)
        - A colored stripe in the middle
        - Numbers 9 through 15
        - More complex drawing routine
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
        self._stripe_color = info[2]  # Get stripe color from info tuple

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
        self.turtle.color(self._stripe_color, self._stripe_color)
        self.turtle.begin_fill()
        self.turtle.circle(stripe_radius)
        self.turtle.end_fill()
