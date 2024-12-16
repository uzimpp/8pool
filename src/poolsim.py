"""Main module for the pool game simulation, handling game logic and visualization."""

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
# import simpleaudio as sa


class PoolSimulator:
    """Main class for simulating the pool game."""

    def __init__(self):
        """Initialize the Pool Simulator."""
        self.turtles = {}  # Consolidate turtle instances into a dictionary
        self._turtle_setup()
        self._setup_table()
        self._setup_balls()
        self._setup_cuestick()
        self.game_state = {  # Consolidate game state variables
            'shot_made': False,
            'game_won': False
        }

    def _turtle_setup(self):
        self.screen = turtle.Screen()
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
        """Set up the pool table."""
        self.table = Table(self.turtles['table'])

    def _setup_balls(self):
        """Arrange the balls on the pool table."""
        self.ball_list = []
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
        """Create a Ball & stripe ball."""
        if num >= 9:
            stripe_color = BALL_COLORS[num % 8]
            info = [num, BALL_COLORS[num], stripe_color]  # Include stripe color in info
            return StripeBall([x, y], [0, 0], info, self.turtles['ball'])
        info = [num, BALL_COLORS[num]]
        return Ball([x, y], [0, 0], info, self.turtles['ball'])

    def find_ball(self, number):
        """Find a ball by its number."""
        for ball in self.ball_list:
            if ball.number == number:
                return ball
        return None

    def _setup_cuestick(self):
        """Set up the cue stick in the simulation."""
        cueball = self.find_ball(
            None)  # use cue ball as a ref pos for cuestick
        self.cuestick = CueStick(cueball, self.turtles['cuestick'])

    def input(self):
        """Handle user input for aiming and hitting the cue ball."""
        # Allow user to adjust the aiming angle
        # Listen for keyboard input to control rotation and shooting
        self.screen.listen()
        self.screen.listen()
        self.screen.onkey(lambda: self.cuestick.rotate(-ANGLE_STEP), "a")
        self.screen.onkey(lambda: self.cuestick.rotate(ANGLE_STEP), "d")
        self.screen.onkey(lambda: self.cuestick.power(POWER_STEP), "w")
        self.screen.onkey(lambda: self.cuestick.power(-POWER_STEP), "s")
        self.screen.onkey(self._attempt_shot, "space")  # Handle space key for shooting

    def _attempt_shot(self):
        """Attempt to make a shot. Ensure it can only be executed once per turn."""
        if not self.game_state['shot_made']:  # Prevent holding space to repeatedly shoot
            self.make_a_shot()

    def make_a_shot(self):
        """Handle the cue stick shot."""
        self.cuestick.shoot()
        self.game_state['shot_made'] = True

    def _unbind_keys(self):
        """Unbind all keyboard controls for the cue stick."""
        self.screen.onkey(None, "a")
        self.screen.onkey(None, "d")
        self.screen.onkey(None, "w")
        self.screen.onkey(None, "s")
        self.screen.onkey(None, "space")

    def run(self):
        """Main game loop."""
        while True:
            while not self.game_state['game_won']:  # Stop game loop after the game is won
                self._update_game()
                if self._next_move():
                    if self._is_game_won():
                        self.game_state['game_won'] = True  # Mark game as won
                    else:
                        self.input()  # Allow input only when all balls have stopped
                else:
                    self._unbind_keys()  # Unbind keys if balls are still moving
            self._display_win_message()
            text = self.screen.textinput("Game Over", "Press enter to continue the game")
            if text is None:  # User cancelled
                break


    def _update_game(self):
        """Update the game state."""
        for ball in self.ball_list:
            ball.move(DT)
            self.check_pockets()
            self.check_table_edge_collisions(ball)
        self.check_ball_collisions()
        self._redraw()

    def _redraw(self):
        """Redraw the table, balls, and cue stick."""
        # Redraw table
        self.turtles['table'].clear()
        self.table.draw_table()
        # Redraw balls
        self.turtles['ball'].clear()
        for ball in self.ball_list:
            ball.draw()
        # Redraw cue stick
        self.cuestick.update_position()
        # Update screen
        self.screen.update()

    def _next_move(self):
        """Check if all balls have stopped moving."""
        for ball in self.ball_list:
            if ball.is_moving():
                return False

        # If all balls stop, reset shot state and cue stick
        if self.game_state['shot_made']:
            self.game_state['shot_made'] = False  # Allow the next shot
            self.cuestick.reset()   # Reset the cue stick to follow the cue ball
        return True

    def check_pockets(self):
        """Check for balls pocketed."""
        pocketed_balls = self.table.check_pockets(self.ball_list)
        for ball in pocketed_balls:
            if isinstance(ball, CueBall):  # Cue ball pocketed
                self._handle_cue_ball_pocketed(ball)
                print("Scratch!", "The cue ball has been pocketed!")
            else:
                self.ball_list.remove(ball)  # Remove other balls
                print(f"Ball {ball.number} is pocketed")

    def _handle_cue_ball_pocketed(self, cueball):
        """Handle the event when the cue ball is pocketed."""
        self.screen.textinput(
            "Scratch!", "The cue ball has been pocketed! Press Enter to continue."
        )
        cueball.x = -CANVAS_WIDTH / 3
        cueball.y = 0
        cueball.vx = 0
        cueball.vy = 0

    def check_table_edge_collisions(self, ball):
        """Check and handle collisions with table edges."""
        ball.bounce_off_horizontal_rail(CANVAS_WIDTH)
        ball.bounce_off_vertical_rail(CANVAS_HEIGHT)

    def check_ball_collisions(self):
        """Check and handle collisions between balls."""
        n = len(self.ball_list)
        for i in range(n):
            for j in range(i + 1, n):
                ball1 = self.ball_list[i]
                ball2 = self.ball_list[j]
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
        """Check if the game is won."""
        return len(self.ball_list) == 1 and isinstance(self.ball_list[0], CueBall)

    def _display_win_message(self):
        """Display a victory message."""
        self.turtles['main'].color("black")
        self.turtles['main'].write("Victory!!!!", align="center",
                            font=("Helvetica", 36))

    # def play_sound(file_path):
    #     wave_obj = sa.WaveObject.from_wave_file(file_path)
    #     play_obj = wave_obj.play()
    #     play_obj.wait_done()

    # def shoot_sound():
    #     play_sound('8-Bit.wav')


# Run the simulation
if __name__ == "__main__":
    sim = PoolSimulator()
    sim.run()

    # > Command line
    # spd = float(input("Type the power you want to put into the cue ball (0 - 100): "))
    # angle_deg = float(input("Type your angle to hit (in degrees, 0°=to the right, 90°=up): "))

    # > Pop-up UI
    # while True:
    #     try:
    #         # Prompt for shot power
    #         power = self.screen.textinput(
    #             "Power", "Enter shot power (0-100): ")
    #         if power is None:  # User cancelled
    #             continue
    #         power = float(power)
    #         if not (0 <= power <= 100):
    #             raise ValueError("Shot power must be between 0 and 100.")

    #         # Prompt for aiming angle
    #         angle = self.screen.textinput(
    #             "Aiming", "Enter aiming angle (in degrees, 0-360): "
    #         )
    #         if angle is None:  # User cancelled
    #             continue
    #         try:
    #             angle = float(angle)
    #             break
    #         except ValueError:
    #             raise ValueError("Aiming angle must be integer or float.")
    #     except ValueError as e:
    #         out = f"Invalid Input", f"{e}. Press Enter to try again."
    #         self.screen.textinput(out)
    # Convert angle to radians and calculate velocity
    # angle_rad = math.radians(angle)
    # velocity = (power / 100) * MAX_SPEED_PX_S
    # # Set velocity for the cue ball
    # for ball in self.ball_list:
    #     if isinstance(ball, CueBall):  # Cue ball
    #         ball.vx = velocity * math.cos(angle_rad)
    #         ball.vy = velocity * math.sin(angle_rad)
    # print(power, angle)
