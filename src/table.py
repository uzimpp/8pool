import turtle
import math
from config import (
    POOL_TABLE_CLOTH_COLOR,
    POOL_TABLE_POCKET_COLOR,
)


class Table:
    """Represents a pool table with pockets and dimensions."""

    def __init__(self, length_px, width_px, pocket_radius):
        """Initialize the table dimensions and pockets."""
        self.length = length_px
        self.width = width_px
        self.pocket_radius = pocket_radius

        # Canvas half-width and half-height for convenience
        self.canvas_width = self.length / 2
        self.canvas_height = self.width / 2

        # Define pocket positions
        self.pockets = [
            (-self.canvas_width, self.canvas_height),  # Top-left corner
            (self.canvas_width, self.canvas_height),   # Top-right corner
            (-self.canvas_width, -self.canvas_height),  # Bottom-left corner
            (self.canvas_width, -self.canvas_height),  # Bottom-right corner
            (0, self.canvas_height),                  # Center-top pocket
            # Center-bottom pocket
            (0, -self.canvas_height)
        ]
        self.pocketed = []  # List to keep track of pocketed balls

    def draw_table(self):
        """Draw the table's cloth surface and pockets."""
        # Draw green cloth area
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(0)
        turtle.pendown()
        turtle.color(POOL_TABLE_CLOTH_COLOR)  # Green cloth color
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)
        turtle.end_fill()
        # Draw table pockets
        self.draw_pockets()

    def draw_pockets(self):
        """Draw circular pockets at the predefined locations."""
        turtle.penup()
        turtle.color(POOL_TABLE_POCKET_COLOR)
        turtle.fillcolor(POOL_TABLE_POCKET_COLOR)
        for px, py in self.pockets:
            turtle.goto(px, py - self.pocket_radius)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(self.pocket_radius)
            turtle.end_fill()
            turtle.penup()

    def check_pockets(self, balls):
        """Check if any balls are pocketed."""
        adjust = 15  # Adjust pocket radius for easier detection
        to_remove = []
        for ball in balls:
            for px, py in self.pockets:
                dist = math.sqrt((ball.x - px) ** 2 + (ball.y - py) ** 2)
                if dist + ball.size - adjust < self.pocket_radius:  # Check pocket
                    to_remove.append(ball)
                    self.pocketed.append(ball)
                    break
        return to_remove

   # def draw_trapezoid(self):
    # 	# Draw the green cloth area
    # 	turtle.penup()
    # 	turtle.goto(-self.canvas_width, -self.canvas_height)
    # 	turtle.pensize(0)
    # 	turtle.pendown()
    # 	turtle.color((150, 205, 152))  # green cloth
    # 	turtle.begin_fill()
    # 	for i in range(2):
    # 		turtle.forward(2 * self.canvas_width)
    # 		turtle.left(90)
    # 		turtle.forward(2 * self.canvas_height)
    # 		turtle.left(90)
    # 	turtle.end_fill()
