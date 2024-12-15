import math
from config import (
    POOL_TABLE_CLOTH_COLOR,
    POOL_TABLE_POCKET_COLOR,
    BALL_DIAMETER,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


class Table:
    """Represents a pool table with pockets and dimensions."""
    def __init__(self, turtle):
        """Initialize the table with dimensions and a dedicated turtle."""
        self.turtle = turtle
        self.turtle.hideturtle()
        self.turtle.speed(0)
        # Define pocket positions
        self.pockets = [
            (-CANVAS_WIDTH, CANVAS_HEIGHT),  # Top-left corner
            (CANVAS_WIDTH, CANVAS_HEIGHT),   # Top-right corner
            (-CANVAS_WIDTH, -CANVAS_HEIGHT),  # Bottom-left corner
            (CANVAS_WIDTH, -CANVAS_HEIGHT),  # Bottom-right corner
            (0, CANVAS_HEIGHT),                  # Center-top pocket
            (0, -CANVAS_HEIGHT)                  # Center-bottom pocket
        ]
        self.pocketed = []

    def draw_table(self):
        """Draw the table's cloth surface and pockets."""
        self.turtle.clear()

        # Draw the table surface
        self.turtle.penup()
        self.turtle.goto(-CANVAS_WIDTH, -CANVAS_HEIGHT)
        self.turtle.pendown()
        self.turtle.color(POOL_TABLE_CLOTH_COLOR)
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(2 * (CANVAS_WIDTH))
            self.turtle.left(90)
            self.turtle.forward(2 * (CANVAS_HEIGHT))
            self.turtle.left(90)
        self.turtle.end_fill()

        # Draw the pockets
        self.draw_pockets()

    def draw_pockets(self):
        """Draw circular pockets."""
        self.turtle.penup()
        self.turtle.color(POOL_TABLE_POCKET_COLOR)
        self.turtle.fillcolor(POOL_TABLE_POCKET_COLOR)
        for px, py in self.pockets:
            self.turtle.goto(px, py - BALL_DIAMETER)
            self.turtle.pendown()
            self.turtle.begin_fill()
            self.turtle.circle(BALL_DIAMETER)
            self.turtle.end_fill()
            self.turtle.penup()

    def draw_trapezoid(self, x, y):
        # Draw the green cloth area
        turtle.penup()
        turtle.goto(x, y)
        turtle.pensize(0)
        turtle.pendown()
        turtle.color((150, 205, 152))  # green cloth
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(2 * CANVAS_WIDTH)
            turtle.left(90)
            turtle.forward(2 * CANVAS_HEIGHT)
            turtle.left(90)
        turtle.end_fill()

    def check_pockets(self, balls):
        """Check if any balls are pocketed."""
        adjust = 15  # Adjust pocket radius for easier detection
        to_remove = []
        for ball in balls:
            for px, py in self.pockets:
                dist = math.sqrt((ball.x - px) ** 2 + (ball.y - py) ** 2)
                if dist + ball.size - adjust < BALL_DIAMETER:  # Check pocket
                    to_remove.append(ball)
                    self.pocketed.append(ball)
                    break
        return to_remove

