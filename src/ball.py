import turtle
import math
from config import (
    CREAM,
    BALL_MASS,
    BALL_RADIUS,
    GRAVITY,
    FRICTION_COEIFFICIENT,
)
# from playsound import playsound


class Ball:
    """Ball class for simulating the pool game."""
    def __init__(self, pos, velocity, info):
        """Initialize a ball with size, position, velocity, color, and number."""
        self._pos = pos
        self._velocity = velocity
        self.__number = info[0]
        self.__color = info[1]

    @property
    def x(self):
        """pos x"""
        return self._pos[0]

    @x.setter
    def x(self, x):
        """pos x"""
        self._pos[0] = x

    @property
    def y(self):
        """pos y"""
        return self._pos[1]

    @y.setter
    def y(self, y):
        """pos y"""
        self._pos[1] = y

    @property
    def vx(self):
        """velocity x"""
        return self._velocity[0]

    @vx.setter
    def vx(self, vx):
        """velocity x"""
        self._velocity[0] = vx

    @property
    def vy(self):
        """velocity y"""
        return self._velocity[1]

    @vy.setter
    def vy(self, vy):
        """velocity y"""
        self._velocity[1] = vy

    @property
    def number(self):
        """number"""
        return self.__number

    @property
    def color(self):
        """pos y"""
        return self.__color

    @property
    def size(self):
        """size or radius of ball"""
        return BALL_RADIUS

    @property
    def mass(self):
        """mass of ball"""
        return BALL_MASS

    def draw(self):
        """Draw the ball on the table."""
        turtle.hideturtle()
        turtle.pensize(3)
        turtle.penup()
        turtle.goto(self._pos[0], self._pos[1] - BALL_RADIUS)
        turtle.color(self.__color)
        turtle.fillcolor(self.__color)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(BALL_RADIUS)
        turtle.end_fill()
        self._draw_inner_number()
        turtle.pensize(0)

    def _draw_inner_number(self):
        """Draw the number on the ball."""
        inner_white_radius = BALL_RADIUS * 0.5
        turtle.penup()
        turtle.goto(self._pos[0], self._pos[1] - inner_white_radius)
        turtle.pendown()
        turtle.color(CREAM)  # Cream color
        turtle.begin_fill()
        turtle.circle(inner_white_radius)
        turtle.end_fill()

        # Draw the number in the center
        turtle.penup()
        turtle.goto(self._pos[0], self._pos[1] - (BALL_RADIUS * 0.6))
        turtle.color("black")
        font_size = int(BALL_RADIUS / 1.25)
        turtle.write(
            str(self.__number), align="center", font=("Helvetica", font_size))

    def distance(self, other):
        """Calculate the distance to another ball"""
        return math.sqrt((other.y - self._pos[1]) ** 2 + (other.x - self._pos[0]) ** 2)

    def bounce_off_horizontal(self, canvas_width):
        """Handle collisions with the horizontal edges of the table"""
        if self._pos[0] - BALL_RADIUS < -canvas_width:
            self._pos[0] = -canvas_width + BALL_RADIUS
            self._velocity[0] = -self._velocity[0]
        elif self._pos[0] + BALL_RADIUS > canvas_width:
            self._pos[0] = canvas_width - BALL_RADIUS
            self._velocity[0] = -self._velocity[0]

    def bounce_off_vertical(self, canvas_height):
        """Handle collisions with the vertical edges of the table."""
        if self._pos[1] - BALL_RADIUS < -canvas_height:
            self._pos[1] = -canvas_height + BALL_RADIUS
            self._velocity[1] = -self._velocity[1]
        elif self._pos[1] + BALL_RADIUS > canvas_height:
            self._pos[1] = canvas_height - BALL_RADIUS
            self._velocity[1] = -self._velocity[1]

    def bounce_off(self, other):
        """Handle ball-to-ball collisions with energy preservation."""
        dx = other.x - self._pos[0]
        dy = other.y - self._pos[1]
        dist = self.distance(other)

        # Unit normal vector
        nx = dx / dist
        ny = dy / dist

        # Relative velocity
        dvx = other.vx - self._velocity[0]
        dvy = other.vy - self._velocity[1]
        vn = dvx * nx + dvy * ny  # Normal velocity
        if vn > 0:  # vn > 0 if balls are moving away
            return  # Thus, no collision

        # Compute impulse with coefficient of restitution
            # """The coefficient of restitution (COR) is a measure
            # of how much kinetic energy is preserved during a collision between objects.
            # basically "bounciness" of the collision.
            # Billiard balls: ~0.95"""

            # """For physically acceptable collisions 0 < e < 1.
            # The value of e = 1 corresponds to an elastic collision, whereas
            # the value of e = 0 corresponds to a totally inelastic collision
            # in which the restoration impulse is equal to zero.
            # We can consider each particle separately
            # and set the impulse on the particle equal to the change of linear momentum"""
        e = 0.95  # Coefficient of restitution for billiard balls
        # We can acutaully use BALL_MASS here since every ball has identical mass
        # I leave it like this to make it more understandable.
        m1 = self.mass
        m2 = other.mass
        impulse = -(1 + e) * vn / (1 / m1 + 1 /m2)

        # Apply impulse to both balls
        self._velocity[0] -= (impulse * nx) / m1
        self._velocity[1] -= (impulse * ny) / m2
        other.vx += (impulse * nx) / m1
        other.vy += (impulse * ny) / m2
        # playsound("collision.mp3")

    def move(self, dt):
        """Update the ball's position and velocity with friction."""
        # F(friction) = µmg
        friction_force = (1 + FRICTION_COEIFFICIENT) * BALL_MASS * GRAVITY
        # Calculate speed (Apply Newton's second law)
        # Acceleration due to friction in opposite direction
        # ∑F = ma
        # We will get Fsin(ø) = ma
        speed = math.sqrt(self._velocity[0]**2 + self._velocity[1]**2)
        if speed > 0:
            # Direction of motion
            dx = self._velocity[0] / speed
            dy = self._velocity[1] / speed
            # Calculate acceleration due to friction
            ax = (-friction_force / BALL_MASS) * dx
            ay = (-friction_force / BALL_MASS) * dy
        else:
            ax = 0
            ay = 0

        # Update velocities and positions
        self._velocity[0] += ax * dt
        self._velocity[1] += ay * dt
        self._pos[0] += self._velocity[0] * dt
        self._pos[1] += self._velocity[1] * dt

        # Stop the ball if its is slow enough
        min_velocity = 0.4
        if abs(self._velocity[0]) < min_velocity and abs(self._velocity[1]) < min_velocity:
            self._velocity[0] = 0
            self._velocity[1] = 0

    def is_moving(self):
        """Check if the ball is moving."""
        return self._velocity[0] != 0 or self._velocity[1] != 0

    def __str__(self):
        out = f"Ball {self.__number}: Pos=({self._pos[0]:.2f}, {self._pos[1]:.2f})"
        out += f", Spd=({self._velocity[0]:.2f}, {self._velocity[1]:.2f})"
        return out

class CueBall(Ball):
    """Inheritance class for cue ball"""
    def __init__(self, pos, velocity, info):
        """Initialize a cue ball with position, velocity, and color."""
        super().__init__(pos, velocity, info)
        # self.turtle = turtle.Turtle()

    def draw(self):
        """Draw the cue ball."""
        turtle.hideturtle()
        turtle.pensize(3)
        turtle.penup()
        turtle.goto(self.x, self.y - BALL_RADIUS)
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(BALL_RADIUS)
        turtle.end_fill()
        turtle.pensize(0)


class StripeBall(Ball):
    """Inheritance class for stripe ball"""
    def __init__(self, pos, velocity, info, stripe_color):
        """Initialize a stripe ball with position, velocity, color, and stripe color."""
        super().__init__(pos, velocity, info)
        # self.turtle = turtle.Turtle()
        self.__stripe_color = stripe_color

    def draw(self):
        """Draw the striped ball."""
        turtle.hideturtle()
        turtle.pensize(3)
        turtle.penup()
        turtle.goto(self.x, self.y - BALL_RADIUS)
        turtle.color(CREAM)  # Cream base
        turtle.fillcolor(CREAM)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(BALL_RADIUS)
        turtle.end_fill()

        self._draw_stripe()
        self._draw_inner_number()
        turtle.pensize(0)

    def _draw_stripe(self):
        """Draw the stripe on the ball."""
        stripe_radius = BALL_RADIUS * 0.8
        turtle.penup()
        turtle.goto(self.x, self.y - stripe_radius)
        turtle.pendown()
        turtle.color(self.__stripe_color, self.__stripe_color)
        turtle.begin_fill()
        turtle.circle(stripe_radius)
        turtle.end_fill()
