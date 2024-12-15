import math
from config import (
    CREAM,
    BALL_MASS,
    BALL_RADIUS,
    GRAVITY,
    SLIDING_FRICTION_COEF,
    BALL_BALL_RESTITUTION,
)
# from playsound import playsound
class Ball:
    """Ball class for simulating the pool game."""
    def __init__(self, pos, velocity, info, turtle):
        """Initialize a ball with size, position, velocity, color, and number."""
        self.turtle = turtle
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
        self.turtle.hideturtle()
        self.turtle.pensize(3)
        self.turtle.penup()
        self.turtle.goto(self._pos[0], self._pos[1] - BALL_RADIUS)
        self.turtle.color(self.__color)
        self.turtle.fillcolor(self.__color)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(BALL_RADIUS)
        self.turtle.end_fill()
        self._draw_inner_number()
        self.turtle.pensize(0)

    def _draw_inner_number(self):
        """Draw the number on the ball."""
        inner_white_radius = BALL_RADIUS * 0.5
        self.turtle.penup()
        self.turtle.goto(self._pos[0], self._pos[1] - inner_white_radius)
        self.turtle.pendown()
        self.turtle.color(CREAM)  # Cream color
        self.turtle.begin_fill()
        self.turtle.circle(inner_white_radius)
        self.turtle.end_fill()

        # Draw the number in the center
        self.turtle.penup()
        self.turtle.goto(self._pos[0] + (BALL_RADIUS * 0.1245), self._pos[1] - (BALL_RADIUS * 0.575))
        self.turtle.color("black")
        font_size = int(BALL_RADIUS / 1.4)  # Slightly smaller font size
        self.turtle.write(
            str(self.__number), align="center", font=("Helvetica", font_size, "bold")
)

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
        """Update the ball's position and velocity with friction."""
        # F(friction) = µmg
        friction_force = (1 + SLIDING_FRICTION_COEF) * self.mass * GRAVITY
        speed = self._speed() 
        # Calculate speed (Apply Newton's second law)
        # Acceleration due to friction in opposite direction
        # ∑F = ma
        # We will get Fsin(ø) = ma
        if speed > 0:
            dx = self.vx / speed
            dy = self.vy / speed
            
            # Friction forces
            ax = -friction_force / self.mass * dx
            ay = -friction_force / self.mass * dy
            
            # Update velocities
            self.vx += ax * dt
            self.vy += ay * dt
        else:
            ax, ay = 0, 0
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Stop ball if slow enough
        min_speed = 0.3
        speed = self._speed()
        if speed < min_speed:
            self.vx = 0
            self.vy = 0
    
    def _speed(self):
        return math.sqrt(self.vx**2 + self.vy**2)

    def is_moving(self):
        """Check if the ball is moving."""
        return self._velocity[0] != 0 or self._velocity[1] != 0

    def __str__(self):
        out = f"Ball {self.__number}: Pos=({self._pos[0]:.2f}, {self._pos[1]:.2f})"
        out += f", Spd=({self._velocity[0]:.2f}, {self._velocity[1]:.2f})"
        return out

class CueBall(Ball):
    """Inheritance class for cue ball"""
    def __init__(self, pos, velocity, info, turtle):
        """Initialize a cue ball with position, velocity, and color."""
        super().__init__(pos, velocity, info, turtle)
        # self.turtle = self.turtle.Turtle()

    def draw(self):
        """Draw the cue ball."""
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
    """Inheritance class for stripe ball"""
    def __init__(self, pos, velocity, info, turtle, stripe_color):
        """Initialize a stripe ball with position, velocity, color, and stripe color."""
        super().__init__(pos, velocity, info, turtle)
        # self.turtle = self.turtle.Turtle()
        self.__stripe_color = stripe_color

    def draw(self):
        """Draw the striped ball."""
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
        """Draw the stripe on the ball."""
        stripe_radius = BALL_RADIUS * 0.8
        self.turtle.penup()
        self.turtle.goto(self.x, self.y - stripe_radius)
        self.turtle.pendown()
        self.turtle.color(self.__stripe_color, self.__stripe_color)
        self.turtle.begin_fill()
        self.turtle.circle(stripe_radius)
        self.turtle.end_fill()
