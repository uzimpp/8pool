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
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.colormode(255)
        self.screen.bgcolor(POOL_TABLE_COLOR)
        self.screen.setup(TABLE_LENGTH + 100, TABLE_WIDTH + 100)
        self.myturtle = turtle.Turtle()
        self.myturtle.hideturtle()
        self.myturtle.speed(0)

        # Initialize turtles for each layer
        self.table_turtle = turtle.Turtle()
        self.table_turtle.hideturtle()
        self.table_turtle.speed(0)

        self.ball_turtle = turtle.Turtle()
        self.ball_turtle.hideturtle()
        self.ball_turtle.speed(0)

        self.cuestick_turtle = turtle.Turtle()
        self.cuestick_turtle.hideturtle()
        self.cuestick_turtle.speed(0)

        # Set up the table, balls, and cue stick
        self._setup_table()
        self._setup_balls()
        self._setup_cuestick()
        self.shot_made = False

    def _setup_table(self):
        """Set up the pool table."""
        self.table = Table(self.table_turtle)

    def _setup_balls(self):
        """Arrange the balls on the pool table."""
        self.ball_list = []
        start_x, start_y = CUEBALL_POS
        x_spacing = BALL_DIAMETER * math.sqrt(3) / 2
        row_x = -start_x # Since reference from cue ball pos
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
        cueball = CueBall([cue_x, cue_y], [0, 0], [None, BALL_COLORS[None]], self.ball_turtle)
        self.ball_list.append(cueball)

    def _create_ball(self, x, y, num):
        """Create a Ball & stripe ball."""
        info = [num, BALL_COLORS[num]]
        if num >= 9:
            stripe_color = BALL_COLORS[num % 8]
            return StripeBall([x, y], [0, 0], info, self.ball_turtle, stripe_color)
        return Ball([x, y], [0, 0], info, self.ball_turtle)

    def find_ball(self, number):
        """Find a ball by its number."""
        for ball in self.ball_list:
            if ball.number == number:
                return ball
        return None

    def _setup_cuestick(self):
        """Set up the cue stick in the simulation."""
        cueball = self.find_ball(None)  # use cue ball as a ref pos for cuestick
        self.cuestick = CueStick(cueball, self.cuestick_turtle)

    def input(self):
        """Handle user input for aiming and hitting the cue ball."""
        # Allow user to adjust the aiming angle
        # Listen for keyboard input to control rotation and shooting
        self.screen.listen()
        # Bind keys for cue stick actions
        self.screen.onkey(lambda: self.cuestick._rotate(-ANGLE_STEP), "a")  # Rotate left
        self.screen.onkey(lambda: self.cuestick._rotate(ANGLE_STEP), "d")   # Rotate right
        self.screen.onkey(lambda: self.cuestick._power(POWER_STEP), "w")   # Increase power
        self.screen.onkey(lambda: self.cuestick._power(-POWER_STEP), "s")  # Decrease power

        # Mark the shot as made to exit the loop
        self.screen.onkey(lambda: self.make_a_shot(), "space")  # Shoot the cue ball
        # Main loop for listening
        while not self.shot_made: # Keep the screen updated
            self.screen.update()
        # Unbind all keys after the shot is made
        self._unbind_keys()

    def _unbind_keys(self):
        """Unbind all keyboard controls for the cue stick."""
        self.screen.onkey(None, "a")
        self.screen.onkey(None, "d")
        self.screen.onkey(None, "w")
        self.screen.onkey(None, "s")
        self.screen.onkey(None, "space")

    def make_a_shot(self):
        """Handle the cue stick shot."""
        self.cuestick.shoot()
        self.shot_made = True

    def run(self):
        """Main game loop."""
        while True:
            self._update_game()
            if self._next_move():
                if self._is_game_won():
                    break
                else:
                    self.input()
        self._display_win_message()

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
        self.table_turtle.clear()
        self.table.draw_table()
    
        # Redraw balls
        self.ball_turtle.clear()
        for ball in self.ball_list:
            ball.draw()
    
        # Redraw cue stick
        if not self.shot_made:
            self.cuestick._update_position()
        else:
            self.cuestick._update_position()
    
        # Update screen
        self.screen.update()


    def _next_move(self):
        """Check if all balls have stopped moving."""
        for ball in self.ball_list:
            if ball.is_moving():
                return False
    
        # If all balls stop, reset shot state and cue stick
        if self.shot_made:
            self.shot_made = False  # Allow the next shot
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
        ball.bounce_off_horizontal(CANVAS_WIDTH)
        ball.bounce_off_vertical(CANVAS_HEIGHT)

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
        self.myturtle.color("black")
        self.myturtle.write("Victory!!!!", align="center",
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
