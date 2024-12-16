"""Module containing the main pool game simulator and controller."""

import turtle
import math
from ball import Ball, CueBall, StripeBall
from table import Table
from cuestick import CueStick
from handler import Handler
from physic import PhysicsEngine
from config import (
    BALL_COLORS,
    BALL_ROWS,
    BALL_DIAMETER,
    CUEBALL_POS,
    POOL_TABLE_COLOR,
    ANGLE_STEP,
    POWER_STEP,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    TABLE_LENGTH,
    TABLE_WIDTH,
    GUIDE_LINE_COLOR,
    PEN_SIZE,
)



class PoolGame:
    """
    Main class for simulating and controlling the pool game.

    Attributes:
        # _game_objects (dict): Contains game entities
            - 'table': Table instance [GET] [SET]
            - 'cuestick': CueStick instance [GET] [SET]
            - 'ball_list': List of Ball instances [GET] [SET]
        # _game_state (dict): Tracks game status
            - 'shot_made': Shot status flag [GET] [SET]
            - 'game_won': Game completion flag [GET] [SET]
        # _display (dict): Manages display elements
            - 'screen': Main turtle screen [GET] [SET]
            - 'turtles': Dictionary of turtle objects [GET] [SET]

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
        """Initialize the Pool Simulator."""
        self._state = {
            'game': {
                'objects': {
                    'table': None,
                    'cuestick': None,
                    'ball_list': []
                },
                'shot_made': False,
                'game_won': False,
                'display': {
                    'screen': turtle.Screen(),
                    'turtles': {}
                },
                'physics': None  # Will hold PhysicsEngine instance
            }
        }
        self._turtle_setup()
        self._setup_table()
        self._setup_balls()
        self._setup_cuestick()
        self._state['game']['physics'] = PhysicsEngine(
            self._state['game']['objects'],
            self._state['game']['display']
        )

    @property
    def screen(self):
        """Get the main turtle screen."""
        return self._state['game']['display']['screen']

    @screen.setter
    def screen(self, screen):
        """Set the screen object."""
        self._state['game']['display']['screen'] = screen

    @property
    def turtles(self):
        """Get the dictionary of turtle objects."""
        return self._state['game']['display']['turtles']

    @turtles.setter
    def turtles(self, turtles):
        """Set the dictionary of turtle objects."""
        if not isinstance(turtles, dict):
            raise ValueError("turtles must be a dictionary.")
        self._state['game']['display']['turtles'] = turtles

    @property
    def table(self):
        """Get the table object."""
        return self._state['game']['objects']['table']

    @table.setter
    def table(self, table):
        """Set the table object."""
        if not isinstance(table, Table):
            raise ValueError("table must be a Table instance.")
        self._state['game']['objects']['table'] = table

    @property
    def ball_list(self):
        """Get the list of ball objects."""
        return self._state['game']['objects']['ball_list']

    @ball_list.setter
    def ball_list(self, ball_list):
        """Set cue stick."""
        if not isinstance(ball_list, list):
            raise ValueError
        self._state['game']['objects']['ball_list'] = ball_list

    @property
    def cuestick(self):
        """Get the cuestick object."""
        return self._state['game']['objects']['cuestick']

    @cuestick.setter
    def cuestick(self, cuestick):
        """Set cue stick."""
        if not isinstance(cuestick, CueStick):
            raise ValueError
        self._state['game']['objects']['cuestick'] = cuestick

    @property
    def game_won(self):
        """Get the game won state."""
        return self._state['game']['game_won']

    @game_won.setter
    def game_won(self, value):
        """Set the game won state."""
        if not isinstance(value, bool):
            raise ValueError("game_won must be a boolean.")
        self._state['game']['game_won'] = value

    @property
    def shot_made(self):
        """Get the current shot made state."""
        return self._state['game']['shot_made']

    @shot_made.setter
    def shot_made(self, value):
        """Set the shot made state, ensuring it is a boolean."""
        if not isinstance(value, bool):
            raise ValueError("shot_made must be a boolean.")
        self._state['game']['shot_made'] = value

    def set_newgame(self):
        """
        Reset the game to its initial state.
    
        Modifies:
            - Reinitializes game objects and states
            - Resets display elements
        """
        self._state['game']['objects'] = {
            'table': None,
            'cuestick': None,
            'ball_list': []
        }
        self._state['game']['shot_made'] = False
        self._state['game']['game_won'] = False
        self._state['game']['display'] = {
            'screen': turtle.Screen(),
            'turtles': {}
        }

        self._turtle_setup()
        self._setup_table()
        self._setup_balls()
        self._setup_cuestick()
        self._state['game']['physics'] = PhysicsEngine(
            self._state['game']['objects'],
            self._state['game']['display']
        )

    def _turtle_setup(self):
        """
        Configure the turtle graphics environment.

        Modifies:
            self.screen: Sets up main display window
                - tracer: Disabled for manual screen updates
                - colormode: Set to RGB (255)
                - bgcolor: Set to table color
                - setup: Window dimensions adjusted
            self.turtles: Creates turtle objects
                - 'main': For general messages
                - 'table': For drawing table
                - 'ball': For drawing balls
                - 'cuestick': For drawing cue stick
        """
        self.screen.tracer(0)
        self.screen.colormode(255)
        self.screen.bgcolor(POOL_TABLE_COLOR)
        self.screen.setup(TABLE_LENGTH + 100, TABLE_WIDTH + 100)

        # Store turtles in dictionary
        self.turtles = {
            'main': turtle.Turtle(),
            'table': turtle.Turtle(),
            'ball': turtle.Turtle(),
            'cuestick': turtle.Turtle()
        }
        for t in self.turtles.values():
            t.hideturtle()
            t.speed(0)

    def _setup_table(self):
        """
        Set up the pool table.

        Modifies:
            self.table: Creates new Table instance
                with reference to table turtle
        """
        self.table = Table(self.turtles['table'])

    def _setup_balls(self):
        """
        Arrange the balls on the pool table in standard triangle formation.

        Modifies:
            self.ball_list: Adds all balls to the game
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
                self.ball_list.append(ball)
                row_y += BALL_DIAMETER
            row_x += x_spacing

        # Cue ball
        cue_x, cue_y = CUEBALL_POS
        cueball = CueBall([cue_x, cue_y], [0, 0], [
                          None, BALL_COLORS[None]], self.turtles['ball'])
        self.ball_list.append(cueball)

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
            return StripeBall([x, y], [0, 0], info, self.turtles['ball'])
        info = [num, BALL_COLORS[num]]
        return Ball([x, y], [0, 0], info, self.turtles['ball'])

    def _setup_cuestick(self):
        """
        Set up the cue stick in the simulation.

        Modifies:
            self.cuestick: Creates new CueStick instance
                with reference to cue ball and cuestick turtle
        """
        cueball = self.find_ball(
            None)  # use cue ball as a ref pos for cuestick
        self.cuestick = CueStick(
            cueball, self.turtles['cuestick'])

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
            self.cuestick: Updates cue stick properties
                - angle: Changed by rotation
                - power: Changed by power adjustments
        """
        # Allow user to adjust the aiming angle
        # Listen for keyboard input to control rotation and shooting
        if not self.shot_made:
            self.screen.listen()
            self.screen.onkey(lambda:
                                self.cuestick.rotate(-ANGLE_STEP), "a")
            self.screen.onkey(lambda:
                                self.cuestick.rotate(ANGLE_STEP), "d")
            self.screen.onkey(lambda:
                                self.cuestick.power(POWER_STEP), "w")
            self.screen.onkey(lambda:
                                self.cuestick.power(-POWER_STEP), "s")
            self.screen.onkey(
                self._attempt_shot, "space")  # Handle space key for shooting

    def _attempt_shot(self):
        """
        Attempt to make a shot. Ensure it can only be executed once per turn.
        Prevents rapid-fire shooting by checking shot_made flag.
        """
        # Prevent holding space to repeatedly shoot
        if not self.shot_made:
            self.make_a_shot()

    def make_a_shot(self):
        """
        Handle the cue stick shot. Executes shooting funnction
        and mark shot as made.
        """
        self.cuestick.shoot()
        self.shot_made = True

    def _unbind_keys(self):
        """
        Unbind all keyboard controls for the cue stick.

        Modifies:
            self.screen: Removes all key bindings
                - 'a': Left rotation
                - 'd': Right rotation
                - 'w': Increase power
                - 's': Decrease power
                - 'space': Shoot
        """
        self.screen.onkey(None, "a")
        self.screen.onkey(None, "d")
        self.screen.onkey(None, "w")
        self.screen.onkey(None, "s")
        self.screen.onkey(None, "space")

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
        # self.ball_list = [self.find_ball(None)]
        while True:
            # Stop game loop after the game is won
            while not self.game_won:
                self._update_game()
                if self._next_move():
                    if self._is_game_won():
                        self.game_won = True  # Mark game as won
                    else:
                        self.input()  # Allow input only when all balls have stopped
                else:
                    self._unbind_keys()  # Unbind keys if balls are still moving
            # Display the victory message and reset option
            self._display_win_message()
            text = self.screen.textinput(
                "You won!!!", "Press Enter to play again or Cancel to quit."
            )
            if text is None:  # User cancelled
                break
            self.set_newgame()  # Reset the game for a new round

    def _update_game(self):
        """
        Update the game state using physics engine.

        Modifies:
            self._game_objects: Updates all game object positions and states
        """
        self._state['game']['physics'].update()  # Use physics engine to handle all physics updates
        self._redraw()

    def _redraw(self):
        """
        Redraw the table, balls, and cue stick.

        Modifies:
            self.turtles: Clears and redraws
                - 'table': Redraws table and pockets
                - 'ball': Redraws all balls
                - 'cuestick': Updates cue stick position
            self.screen: Updates display
        """
        # Redraw table
        self.turtles['table'].clear()
        self.table.draw_table()

        # Redraw balls
        self.turtles['ball'].clear()
        for ball in self.ball_list:
            ball.draw()

        # Draw guideline
        if not self.shot_made:
            self.draw_guide_line()

        # Redraw cue stick
        self.cuestick.update_position()

        # Update screen
        self.screen.update()

    def _next_move(self):
        """
        Check if all balls have stopped moving.

        Returns:
            bool: True if all balls stopped, False if any still moving

        Modifies:
            When all balls stop:
            - self.shot_made: Reset to False
            - self.cuestick: Reset position
        """
        for ball in self.ball_list:
            if ball.is_moving():
                return False

        # If all balls stop, reset shot state and cue stick
        if self.shot_made:
            # Reset the cue stick to follow the cue ball
            self.cuestick.reset()
            self.shot_made = False  # Allow the next shot
        return True

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
        is_cueball = isinstance(self.ball_list[0], CueBall)
        return len(self.ball_list) == 1 and is_cueball

    def _display_win_message(self):
        """
        Display a victory message.
        """
        self.turtles['main'].goto(0,0)
        self.turtles['main'].color("black")
        self.turtles['main'].write(
            "You won!!!",
            align="center",
            font=("Helvetica", 36)
        )

    def find_ball(self, number):
        """
        Find a ball by its number.

        Parameters:
            number (int): Ball number to find (None for cue ball)

        Returns:
            Ball or None: The found ball instance or None if not found
        """
        for ball in self.ball_list:
            if ball.number == number:
                return ball
        return None

    def draw_guide_line(self):
        """
        Draw a guideline for the cue stick until it hits a ball or rail.

        Modifies:
            self.turtles['main']: Draws the guide line on the screen.
        """
        cueball = self.find_ball(None)
        if not cueball:
            return

        # Initialize intersection handler
        handler = Handler(CANVAS_WIDTH, CANVAS_HEIGHT)
        # Starting position and direction
        start_pos = (cueball.x, cueball.y)
        angle_rad = math.radians(self.cuestick.angle)
        end_pos = (
            start_pos[0] - 2000 * math.cos(angle_rad),
            start_pos[1] - 2000 * math.sin(angle_rad)
        )
        # Check for rail intersection
        end_pos = handler.calculate_rail_intersection(start_pos, end_pos)

        # Check for ball intersection
        for ball in self.ball_list:
            if ball.number is not None:
                ball_intersection = handler.calculate_ball_intersection(
                    start_pos, end_pos, ball)
                if ball_intersection:
                    end_pos = ball_intersection
                    break

        # Draw the guideline
        turtle_main = self.turtles['main']
        turtle_main.clear()
        turtle_main.color(GUIDE_LINE_COLOR)
        turtle_main.pensize(PEN_SIZE)
        turtle_main.penup()
        turtle_main.goto(*start_pos)
        turtle_main.pendown()
        turtle_main.goto(*end_pos)
        turtle_main.penup()


# Run the simulation
if __name__ == "__main__":
    sim = PoolGame()
    sim.run()
