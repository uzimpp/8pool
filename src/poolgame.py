"""Module containing the main pool game simulator and controller."""

import turtle
import math
from ball import Ball, CueBall, StripeBall
from table import Table
from cuestick import CueStick
from config import (
    BALL_COLORS,
    BALL_ROWS,
    BALL_DIAMETER,
    CUEBALL_POS,
    POOL_TABLE_COLOR,
    DT,
    ANGLE_STEP,
    POWER_STEP,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    TABLE_LENGTH,
    TABLE_WIDTH
)


class PoolGame:
    """
    Main class for simulating and controlling the pool game.

    Attributes:
        # _game_objects (dict): Contains game entities
            - 'table': Table instance
            - 'cuestick': CueStick instance
            - 'ball_list': List of Ball instances
        # _game_state (dict): Tracks game status
            - 'shot_made': Shot status flag [GET] [SET]
            - 'game_won': Game completion flag [GET] [SET]
        # _display (dict): Manages display elements
            - 'screen': Main turtle screen
            - 'turtles': Dictionary of turtle objects

    Modifies:
        - Game state and object positions
        - Display elements and animations
        - User input handling and game flow

    Explanation:
        The simulator orchestrates:
        - Game initialization and setup
        - Physics updates and collision detection
        - User input processing
        - Game state management
        - Visual rendering
    """

    def __init__(self):
        """
        Initialize the Pool Simulator with all necessary components.

        Modifies:
            self._game_objects: Creates dictionary for game entities
                - 'table': Table instance
                - 'cuestick': CueStick instance
                - 'ball_list': List of Ball instances
            self._game_state: Sets up game state tracking
                - 'shot_made': Shot status flag
                - 'game_won': Game completion flag
            self._display: Initializes display components
                - 'screen': Main turtle screen
                - 'turtles': Dictionary of turtle objects
        """
        # Group all game objects and states into dictionaries
        self.set_newgame()

    @property
    def shot_made(self):
        """Get the current shot made state."""
        return self._game_state['shot_made']

    @shot_made.setter
    def shot_made(self, value):
        """Set the shot made state, ensuring it is a boolean."""
        if isinstance(value, bool):
            self._game_state['shot_made'] = value
        else:
            raise ValueError("shot_made must be a boolean.")

    def _turtle_setup(self):
        """
        Configure the turtle graphics environment.

        Modifies:
            self._display['screen']: Sets up main display window
                - tracer: Disabled for manual screen updates
                - colormode: Set to RGB (255)
                - bgcolor: Set to table color
                - setup: Window dimensions adjusted
            self._display['turtles']: Creates turtle objects
                - 'main': For general messages
                - 'table': For drawing table
                - 'ball': For drawing balls
                - 'cuestick': For drawing cue stick
        """
        self._display['screen'].tracer(0)
        self._display['screen'].colormode(255)
        self._display['screen'].bgcolor(POOL_TABLE_COLOR)
        self._display['screen'].setup(TABLE_LENGTH + 100, TABLE_WIDTH + 100)

        # Store turtles in dictionary
        self._display['turtles'] = {
            'main': turtle.Turtle(),
            'table': turtle.Turtle(),
            'ball': turtle.Turtle(),
            'cuestick': turtle.Turtle()
        }
        for t in self._display['turtles'].values():
            t.hideturtle()
            t.speed(0)

    def _setup_table(self):
        """
        Set up the pool table.

        Modifies:
            self._game_objects['table']: Creates new Table instance
                with reference to table turtle
        """
        self._game_objects['table'] = Table(self._display['turtles']['table'])

    def _setup_balls(self):
        """
        Arrange the balls on the pool table in standard triangle formation.

        Modifies:
            self._game_objects['ball_list']: Adds all balls to the game
                - Regular balls (1-8) in triangle formation
                - Striped balls (9-15) in triangle formation
                - Cue ball at starting position

        Explanation:
            Balls are arranged in a triangle with:
            - First row: 1 ball
            - Second row: 2 balls
            - Third row: 3 balls
            - Fourth row: 4 balls
            - Fifth row: 5 balls
            The cue ball is placed at its starting position
        """
        start_x, start_y = CUEBALL_POS
        x_spacing = BALL_DIAMETER * math.sqrt(3) / 2
        row_x = -start_x  # Since reference from cue ball pos
        for row in BALL_ROWS:
            row_height = (len(row) - 1) * BALL_DIAMETER
            row_y = start_y - row_height / 2
            for num in row:
                ball = self._create_ball(row_x, row_y, num)
                self._game_objects['ball_list'].append(ball)
                row_y += BALL_DIAMETER
            row_x += x_spacing

        # Cue ball
        cue_x, cue_y = CUEBALL_POS
        cueball = CueBall([cue_x, cue_y], [0, 0], [
                          None, BALL_COLORS[None]], self._display['turtles']['ball'])
        self._game_objects['ball_list'].append(cueball)

    def _create_ball(self, x, y, num):
        """
        Create a Ball or StripeBall based on the number.

        Parameters:
            x (float): X-coordinate for ball position
            y (float): Y-coordinate for ball position
            num (int): Ball number (1-15, None for cue ball)

        Returns:
            Ball or StripeBall: New ball instance with appropriate properties

        Explanation:
            - Numbers 1-8: Solid colored balls
            - Numbers 9-15: Striped balls with cream base
            - Each ball gets its color from BALL_COLORS
        """
        if num >= 9:
            stripe_color = BALL_COLORS[num % 8]
            # Include stripe color in info
            info = [num, BALL_COLORS[num], stripe_color]
            return StripeBall([x, y], [0, 0], info, self._display['turtles']['ball'])
        info = [num, BALL_COLORS[num]]
        return Ball([x, y], [0, 0], info, self._display['turtles']['ball'])

    def find_ball(self, number):
        """
        Find a ball by its number.

        Parameters:
            number (int): Ball number to find (None for cue ball)

        Returns:
            Ball or None: The found ball instance or None if not found
        """
        for ball in self._game_objects['ball_list']:
            if ball.number == number:
                return ball
        return None

    def _setup_cuestick(self):
        """
        Set up the cue stick in the simulation.

        Modifies:
            self._game_objects['cuestick']: Creates new CueStick instance
                with reference to cue ball and cuestick turtle
        """
        cueball = self.find_ball(
            None)  # use cue ball as a ref pos for cuestick
        self._game_objects['cuestick'] = CueStick(
            cueball, self._display['turtles']['cuestick'])

    def input(self):
        """
        Handle user input for aiming and hitting the cue ball.

        Controls:
            'a': Rotate cue stick counterclockwise
            'd': Rotate cue stick clockwise
            'w': Increase shot power
            's': Decrease shot power
            'space': Execute shot

        Modifies:
            self._game_objects['cuestick']: Updates cue stick properties
                - angle: Changed by rotation
                - power: Changed by power adjustments
        """
        # Allow user to adjust the aiming angle
        # Listen for keyboard input to control rotation and shooting
        self._display['screen'].listen()
        self._display['screen'].onkey(lambda:
                                      self._game_objects['cuestick'].rotate(-ANGLE_STEP), "a")
        self._display['screen'].onkey(lambda:
                                      self._game_objects['cuestick'].rotate(ANGLE_STEP), "d")
        self._display['screen'].onkey(lambda:
                                      self._game_objects['cuestick'].power(POWER_STEP), "w")
        self._display['screen'].onkey(lambda:
                                      self._game_objects['cuestick'].power(-POWER_STEP), "s")
        self._display['screen'].onkey(
            self._attempt_shot, "space")  # Handle space key for shooting

    def _attempt_shot(self):
        """
        Attempt to make a shot. Ensure it can only be executed once per turn.
        Prevents rapid-fire shooting by checking shot_made flag.
        """
        # Prevent holding space to repeatedly shoot
        if not self._game_state['shot_made']:
            self.make_a_shot()

    def make_a_shot(self):
        """
        Handle the cue stick shot. Executes shooting funnction
        and mark shot as made.
        """
        self._game_objects['cuestick'].shoot()
        self._game_state['shot_made'] = True

    def _unbind_keys(self):
        """
        Unbind all keyboard controls for the cue stick.

        Modifies:
            self._display['screen']: Removes all key bindings
                - 'a': Left rotation
                - 'd': Right rotation
                - 'w': Increase power
                - 's': Decrease power
                - 'space': Shoot
        """
        self._display['screen'].onkey(None, "a")
        self._display['screen'].onkey(None, "d")
        self._display['screen'].onkey(None, "w")
        self._display['screen'].onkey(None, "s")
        self._display['screen'].onkey(None, "space")

    def run(self):
        """
        Main game loop controlling the flow of the game.

        Game Flow:
            1. Update game state (physics, collisions)
            2. Check for completed shots
            3. Handle user input when appropriate
            4. Check for game completion
            5. Display victory message when won

        Runs until game is won or user quits.
        """
        # Temporary code to simulate game ending for testing
        # self._game_objects['ball_list'] = [self.find_ball(None)]
        while True:
            while not self._game_state['game_won']:  # Stop game loop after the game is won
                self._update_game()
                if self._next_move():
                    if self._is_game_won():
                        self._game_state['game_won'] = True  # Mark game as won
                    else:
                        self.input()  # Allow input only when all balls have stopped

            # Display the victory message and reset option
            self._display_win_message()
            text = self._display['screen'].textinput(
                "You won!!!", "Press Enter to play again or Cancel to quit."
            )
            if text is None:  # User cancelled
                break
            self.set_newgame() # Reset the game for a new round

    def _update_game(self):
        """
        Update the game state.

        Modifies:
            self._game_objects['ball_list']: Updates all ball positions
                - Applies physics (movement, friction)
                - Checks pocket collisions
                - Checks rail collisions
                - Checks ball-to-ball collisions

        Explanation:
            Main physics update loop that:
            1. Moves all balls according to their velocities
            2. Checks for and handles all types of collisions
            3. Updates visual representation
        """
        for ball in self._game_objects['ball_list']:
            ball.move(DT)
            self.check_pockets()
            self.check_table_edge_collisions(ball)
        self.check_ball_collisions()
        self._redraw()

    def _redraw(self):
        """
        Redraw the table, balls, and cue stick.

        Modifies:
            self._display['turtles']: Clears and redraws
                - 'table': Redraws table and pockets
                - 'ball': Redraws all balls
                - 'cuestick': Updates cue stick position
            self._display['screen']: Updates display
        """
        # Redraw table
        self._display['turtles']['table'].clear()
        self._game_objects['table'].draw_table()

        # Redraw balls
        self._display['turtles']['ball'].clear()
        for ball in self._game_objects['ball_list']:
            ball.draw()

        # Redraw cue stick
        self._game_objects['cuestick'].update_position()
        # Update screen
        self._display['screen'].update()

    def _next_move(self):
        """
        Check if all balls have stopped moving.

        Returns:
            bool: True if all balls stopped, False if any still moving

        Modifies:
            When all balls stop:
            - self._game_state['shot_made']: Reset to False
            - self._game_objects['cuestick']: Reset position
        """
        for ball in self._game_objects['ball_list']:
            if ball.is_moving():
                return False

        # If all balls stop, reset shot state and cue stick
        if self._game_state['shot_made']:
            # Reset the cue stick to follow the cue ball
            self._game_objects['cuestick'].reset()
            self._game_state['shot_made'] = False  # Allow the next shot
        return True

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

    def _is_game_won(self):
        """
        Check if the game is won.

        Returns:
            bool: True if only cue ball remains, False otherwise

        Explanation:
            Game is won when:
            - Only one ball remains
            - That ball is the cue ball
        """
        is_cueball = isinstance(self._game_objects['ball_list'][0], CueBall)
        return len(self._game_objects['ball_list']) == 1 and is_cueball

    def _display_win_message(self):
        """
        Display a victory message.
        """
        self._display['turtles']['main'].color("black")
        self._display['turtles']['main'].write(
            "You won!!!",
            align="center",
            font=("Helvetica", 36)
        )

    def set_newgame(self):
        """
        Reset the game to its initial state.

        Modifies:
            - Reinitializes game objects and states
            - Resets display elements
        """
        self._game_objects = {
            'table': None,
            'cuestick': None,
            'ball_list': []
        }
        self._game_state = {
            'shot_made': False,
            'game_won': False
        }
        self._display = {
            'screen': turtle.Screen(),
            'turtles': {}
        }

        self._turtle_setup()
        self._setup_table()
        self._setup_balls()
        self._setup_cuestick()


# Run the simulation
if __name__ == "__main__":
    sim = PoolGame()
    sim.run()
