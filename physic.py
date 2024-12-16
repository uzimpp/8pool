"""Module containing physics engine for the pool game."""

import math
from config import (
    DT,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    CUEBALL_POS
)
from ball import CueBall


class PhysicsEngine:
    """
    Class to manage the physics of the game.
    """

    def __init__(self, game_objects, display):
        self._game_objects = game_objects
        self._display = display

    def update(self):
        """Update the game state."""
        for ball in self._game_objects['ball_list']:
            ball.move(DT)
            self.check_pockets()
            self.check_table_edge_collisions(ball)
        self.check_ball_collisions()

    def check_pockets(self):
        """
        Check for balls pocketed.

        Modifies:
            self._game_objects['ball_list']: Removes pocketed balls
                - Repositions cue ball if pocketed
                - Removes other balls permanently

        Returns:
            None, but prints messages about pocketed balls
        """
        pocketed_balls = self._game_objects['table'].check_pockets(
            self._game_objects['ball_list'])

        for ball in pocketed_balls:
            if isinstance(ball, CueBall):  # Cue ball pocketed
                self._handle_cue_ball_pocketed(ball)
                print("Scratch!", "The cue ball has been pocketed!")
            else:
                self._game_objects['ball_list'].remove(
                    ball)  # Remove other balls
                print(f"Ball {ball.number} is pocketed")

    def _handle_cue_ball_pocketed(self, cueball):
        """
        Handle the event when the cue ball is pocketed.

        Parameters:
            cueball (CueBall): The pocketed cue ball

        Modifies:
            cueball: Resets cue ball position and velocity
                - Position: Back to starting position
                - Velocity: Set to zero

        Explanation:
            Shows scratch message and resets cue ball for next shot
        """
        self._display['screen'].textinput(
            "Scratch!", "The cue ball has been pocketed! Press Enter to continue."
        )
        cueball.x, cueball.y = CUEBALL_POS
        cueball.vx = 0
        cueball.vy = 0

    def check_table_edge_collisions(self, ball):
        """
        Check and handle collisions with table edges.

        Parameters:
            ball (Ball): Ball to check for rail collisions

        Modifies:
            ball: Updates position and velocity on collision
                - Bounces off horizontal rails
                - Bounces off vertical rails
        """
        ball.bounce_off_horizontal_rail(CANVAS_WIDTH)
        ball.bounce_off_vertical_rail(CANVAS_HEIGHT)

    def check_ball_collisions(self):
        """
        Check and handle collisions between balls.

        Modifies:
            self._game_objects['ball_list']: For each colliding pair
                - Updates velocities based on collision physics
                - Adjusts positions to prevent overlap
                - Applies coefficient of restitution

        Explanation:
            Uses elastic collision formulas with:
            - Conservation of momentum
            - Conservation of energy
            - Separation of overlapping balls
        """
        n = len(self._game_objects['ball_list'])
        for i in range(n):
            for j in range(i + 1, n):
                ball1 = self._game_objects['ball_list'][i]
                ball2 = self._game_objects['ball_list'][j]
                dx = ball2.x - ball1.x
                dy = ball2.y - ball1.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < (ball1.size + ball2.size):
                    ball1.bounce_off(ball2)
                    overlap = (ball1.size + ball2.size) - dist
                    nx = dx / dist
                    ny = dy / dist
                    ball1.x -= nx * (overlap / 2)
                    ball1.y -= ny * (overlap / 2)
                    ball2.x += nx * (overlap / 2)
                    ball2.y += ny * (overlap / 2)
