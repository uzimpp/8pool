"""Module for handling the pool table, including its rendering and pocket detection."""

import math
from config import (
    POOL_TABLE_CLOTH_COLOR,
    POOL_TABLE_POCKET_COLOR,
    BALL_DIAMETER,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


class Table:
    """
    Represents a pool table with pockets and dimensions.

    Attributes:
        + turtle: Turtle object for drawing
        + pockets: List of pocket positions [(x, y), ...]
        + pocketed: List of balls that have entered pockets

    Modifies:
        - Visual representation of table and pockets
        - List of pocketed balls
        - Ball positions when checking pocket collisions

    Returns:
        None directly, but check_pockets returns list of pocketed balls

    Explanation:
        The table manages:
        - Drawing the playing surface
        - Pocket positions and collision detection
        - Tracking which balls have been pocketed
    """

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
        """
        Draw the table's cloth surface and pockets.

        Modifies:
            self.turtle: Clears and redraws the entire table surface.
        """
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
        """
        Draw circular pockets.
        """
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

    def check_pockets(self, balls):
        """
        Check if any balls are pocketed.

        Parameters:
            balls (list): List of Ball objects to check for pocketing

        Modifies:
            self.pocketed: Adds any newly pocketed balls to the list

        Returns:
            list: Balls that should be removed from play

        Explanation:
            For each ball, checks its distance to each pocket.
            If a ball is close enough to a pocket (within adjusted radius),
            it is considered pocketed and will be removed from play.
            The adjustment factor makes pocketing slightly easier than
            the exact pocket diameter.
        """
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
