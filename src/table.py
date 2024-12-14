import turtle
import math

class Table:
    def __init__(self, length_px, width_px, pocket_radius=100):
        self.length = length_px
        self.width = width_px
        self.pocket_radius = pocket_radius

        # Canvas half-width and half-height for convenience
        self.canvas_width = self.length / 2
        self.canvas_height = self.width / 2

        # Define pockets (as before)
        self.pockets = [
            (-self.canvas_width, self.canvas_height),
            (self.canvas_width, self.canvas_height),
            (-self.canvas_width, -self.canvas_height),
            (self.canvas_width, -self.canvas_height),
            (0, self.canvas_height),
            (0, -self.canvas_height)
        ]
        self.pocketed = []

    def draw_table(self):
        # Draw the green cloth area
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(0)
        turtle.pendown()
        turtle.color((93, 125, 88)) # green cloth
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)
        turtle.end_fill()

        # Draw pockets
        self.draw_pockets()

    def draw_trapezoid(self,):
        # Draw the green cloth area
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(0)
        turtle.pendown()
        turtle.color((150, 205, 152)) # green cloth
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)
        turtle.end_fill()

        # Draw pockets
        self.draw_pockets()

    def draw_pockets(self):
        turtle.penup()
        turtle.color("black")
        turtle.fillcolor("black")
        for (px, py) in self.pockets:
            turtle.goto(px, py - self.pocket_radius)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(self.pocket_radius)
            turtle.end_fill()
            turtle.penup()

    def check_pockets(self, balls):
        adjust = 15
        to_remove = []
        for b in balls:
            for (px, py) in self.pockets:
                dist = math.sqrt(((b.x) - px)**2 + (b.y - py)**2)
                # If the ball center is within the pocket radius minus the ball radius,
                # we consider it pocketed.
                if dist + b.size - adjust < self.pocket_radius: # adjust to pocket easier
                    to_remove.append(b)
                    self.pocketed.append(b)
                    break
        return to_remove