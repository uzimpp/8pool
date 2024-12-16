"""Module containing utility classes for intersection calculations."""

import math
from config import BALL_RADIUS


class Handler:
    """Handles intersection calculations for the pool game."""

    def __init__(self, width, height):
        """
        Initialize the Handler with table dimensions.

        Parameters:
            width (float): The width of the pool table.
            height (float): The height of the pool table.
        """
        self.width = width
        self.height = height

    def calculate_rail_intersection(self, start_pos, end_pos):
        """
        Calculate the intersection point of a line with the table rails.

        Parameters:
            start_pos (tuple): The starting position of the line (x, y).
            end_pos (tuple): The ending position of the line (x, y).

        Returns:
            tuple: The intersection point (x, y) with the nearest rail.
        """
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        t_min = 1.0

        for rail_pos, is_vertical in [
            (-self.width, True),   # Left
            (self.width, True),    # Right
            (self.height, False),  # Top
            (-self.height, False)  # Bottom
        ]:
            if t := self._check_rail(rail_pos, (start_x, start_y), (end_x, end_y), is_vertical):
                t_min = min(t_min, t)

        return (start_x + t_min * (end_x - start_x),
                start_y + t_min * (end_y - start_y))

    def _check_rail(self, rail_pos, start, end, is_vertical):
        """
        Check for intersection with a single rail.

        Parameters:
            rail_pos (float): The position of the rail.
            start (tuple): The starting position of the line (x, y).
            end (tuple): The ending position of the line (x, y).
            is_vertical (bool): True if the rail is vertical, False if horizontal.

        Returns:
            float or None: The parameter t of the intersection point, or None if no intersection.
        """
        start_x, start_y = start
        end_x, end_y = end

        if is_vertical:
            if end_x != start_x:
                t = (rail_pos - start_x) / (end_x - start_x)
                y_at_t = start_y + t * (end_y - start_y)
                if 0 < t < 1 and -self.height <= y_at_t <= self.height:
                    return t
        else:
            if end_y != start_y:
                t = (rail_pos - start_y) / (end_y - start_y)
                x_at_t = start_x + t * (end_x - start_x)
                if 0 < t < 1 and -self.width <= x_at_t <= self.width:
                    return t
        return None

    def calculate_ball_intersection(self, start_pos, end_pos, ball):
        """
        Calculate the intersection point of a line with a ball.

        Parameters:
            start_pos (tuple): The starting position of the line (x, y).
            end_pos (tuple): The ending position of the line (x, y).
            ball (Ball): The ball to check for intersection.

        Returns:
            tuple or None: The intersection point (x, y) with the ball, or None if no intersection.
        """
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        dx = end_x - start_x
        dy = end_y - start_y

        a = dx**2 + dy**2
        b = 2 * (dx * (start_x - ball.x) + dy * (start_y - ball.y))
        c = (start_x - ball.x)**2 + (start_y - ball.y)**2 - BALL_RADIUS**2

        if discriminant := b**2 - 4*a*c >= 0:
            t = (-b - math.sqrt(discriminant)) / (2*a)
            if 0 < t < 1:
                return (start_x + t*dx, start_y + t*dy)
        return None
