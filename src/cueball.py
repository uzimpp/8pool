import turtle
import math


class Ball:
    def __init__(self, size, x, y, vx, vy, color, number=None):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.number = number
        self.mass = 0.17
        self.count = 0
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]

    def draw(self):
        # Draw the ball
        turtle.penup()
        turtle.goto(self.x, self.y - self.size)
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

        # Write the number on the ball, except that one is the
        if self.number is not None:
            self.draw_inner_number()

    def draw_inner_number(self):
        # Draw inner white circle to create a ring (stripe)
        inner_white_radius = self.size * 0.5
        turtle.penup()
        turtle.goto(self.x, self.y - inner_white_radius)
        turtle.pendown()
        turtle.color((248, 240, 211))
        turtle.begin_fill()
        turtle.circle(inner_white_radius)
        turtle.end_fill()
    
        # Write the number in the center
        turtle.penup()
        # Move to the center of the ball
        turtle.goto(self.x + (self.size * 0.2), self.y - (self.size * 0.6))
        turtle.color("black")
        turtle.write(str(self.number), align="center",
                     font=("Helvetica", int(self.size)))

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def bounce_off_vertical_table_edge(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_table_edge(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        """The coefficient of restitution (COR) is a measure of how much kinetic energy is preserved
        during a collision between objects.
        basically "bounciness" of the collision.
        Billiard balls: ~0.95"""

        """For physically acceptable collisions 0 < e < 1. The value of e = 1 corresponds to an elastic collision, whereas
        the value of e = 0 corresponds to a totally inelastic collision in which the restoration impulse is equal to
        zero.
        We can consider each particle separately and set the impulse on the particle equal to the change of linear
        momentum"""
        # e = 0.95 # coefficient_of_restitution or e
        # dx  = that.x - self.x # Direction of pos in x-axis
        # dy  = that.y - self.y # Direction of pos in y-axis
        # dist = math.sqrt(dx*dx + dy*dy)

        # dvx = that.vx - self.vx # Direction of velocity in x-axis
        # dvy = that.vy - self.vy # Direction of velocity in Y-axis
        # dvdr = (dx * dvx) + (dy * dvy) # A result vector
        # if dist == 0 or dvdr > 0: # Check if balls are actually moving towards each other
        #     return
        # # By the
        # j = -(1 + e) * (dvdr/dist) / ((1/self.mass) + (1/that.mass))
        # print(self.distance(that), math.sqrt(dx * dx + dy * dy))
        # fx = j * dx / dist
        # fy = j * dy / dist

        # # update velocities according to normal force
        # self.vx += fx / self.mass
        # self.vy += fy / self.mass
        # that.vx -= fx / that.mass
        # that.vy -= fy / that.mass

        # self.count += 1
        # that.count += 1
        e = 0.95
        dx = that.x - self.x
        dy = that.y - self.y
        dist = self.distance(that)
        # Unit normal vector
        nx = dx/dist
        ny = dy/dist
    
        # Relative velocity
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        vn = dvx*nx + dvy*ny # velocity along the normal direction
    
        if vn > 0:
            return
    
        # Compute impulse
        m1 = self.mass
        m2 = that.mass
        J = -(1+e)*vn/(1/m1 + 1/m2)
        # Apply impulse to each ball
        self.vx -= (J*nx)/m1
        self.vy -= (J*ny)/m1
        that.vx += (J*nx)/m2
        that.vy += (J*ny)/m2
    
        self.count += 1
        that.count += 1

    def move(self, dt):
        """ Apply friction"""
        # F(friction) = µmg
        gravity = 9.8
        friction_coefficient = 0.2 # ball-cloth coefficient of sliding friction
        friction_force = friction_coefficient * self.mass * gravity
        
        """ Apply Newton's second law"""
        speed = math.sqrt((self.vx ** 2) + (self.vy ** 2))
        if speed > 0:
            # Direction of the ball
            dx = self.vx / speed
            dy = self.vy / speed
            # Acceleration due to friction in opposite direction
            # ∑F = ma
            # We will get Fsin(ø) = ma
            ax = -friction_force / self.mass * dx
            ay = -friction_force / self.mass * dy
        else:
            ax = 0
            ay = 0
        
        # Update velocities and positions
        self.vx += ax * dt
        self.vy += ay * dt
        # friction_coefficient = 0.997
        # self.vx *= friction_coefficient
        # self.vy *= friction_coefficient
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Stop if slow enough
        min_velocity = 0.4
        if abs(self.vx) < min_velocity and abs(self.vy) < min_velocity:
            self.vx = 0
            self.vy = 0

    def is_moving(self):
        if self.vx == 0 and self.vy == 0:
            return False
        return True

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)

class StripeBall(Ball):
    def __init__(self, size, x, y, vx, vy, color, stripe_color, number=None):
        super().__init__(size, x, y, vx, vy, color, number)
        self.stripe_color = stripe_color

    def draw(self):
        # Draw the ball
        turtle.penup()
        turtle.goto(self.x, self.y - self.size)
        turtle.color((248, 240, 211))
        turtle.fillcolor((248, 240, 211))
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()
        
        self.draw_stripe()
        # Write the number on the ball, except that one is the
        if self.number is not None:
            self.draw_inner_number()
    
    def draw_stripe(self):
        stripe_radius = self.size * 0.8
        turtle.penup()
        turtle.goto(self.x, self.y - stripe_radius)
        turtle.pendown()
        turtle.color(self.stripe_color, self.stripe_color)
        turtle.begin_fill()
        turtle.circle(stripe_radius)
        turtle.end_fill()