import turtle
import math
from ball import Ball, CueBall, StripeBall
from table import Table
from config import (
    BALL_COLORS,
    BALL_ROWS,
    BALL_RADIUS,
    BALL_DIAMETER,
    PEN_SIZE,
    TABLE_LENGTH,
    TABLE_WIDTH,
    POOL_TABLE_COLOR,
    HZ,
    DT,
    MAX_SPEED_PX_S,
)


class PoolSimulator:
    """Main class for simulating the pool game."""
    def __init__(self, myturtle):
        """Initialize the Pool Simulator with turtle instance."""
        self.turtle = myturtle # main
        self.ball_list = []
        self.HZ = HZ
        self.dt = DT
        self.screen = turtle.Screen()

        # Initialize table and balls
        self._setup_table()
        self._setup_balls()

    def _setup_table(self):
        """Set up the pool table dimensions and visuals."""
        self.table_length = TABLE_LENGTH
        self.table_width = TABLE_WIDTH
        self.screen.setup(TABLE_LENGTH + 100,
                          TABLE_WIDTH + 100)

        self.canvas_width = self.table_length / 2
        self.canvas_height = self.table_width / 2

        # Table pockets and boundaries
        self.table = Table(self.table_length, self.table_width, BALL_DIAMETER)

    def _setup_balls(self):
        """Arrange the balls on the pool table."""
        # Object balls
        start_x = self.canvas_width / 3
        start_y = 0
        x_spacing = BALL_DIAMETER * math.sqrt(3) / 2
        row_x = start_x
        for row in BALL_ROWS:
            row_height = (len(row) - 1) * BALL_DIAMETER
            row_y = start_y - row_height / 2
            for num in row:
                ball = self._create_ball(row_x, row_y, num)
                self.ball_list.append(ball)
                row_y += BALL_DIAMETER
            row_x += x_spacing

        # Cue ball
        cue_x = -self.canvas_width / 3
        cue_y = 0
        cueball = CueBall([cue_x, cue_y], [0, 0], [None, BALL_COLORS[15]])
        self.ball_list.append(cueball)

    def _create_ball(self, x, y, num):
        """Create a Ball or StripeBall."""
        info = [num, BALL_COLORS[num]]
        if num >= 9:
            stripe_color = BALL_COLORS[num % 8]
            return StripeBall([x, y], [0, 0], info, stripe_color)
        return Ball([x, y], [0, 0], info)

    def find_ball(self, number):
        """Find a ball by its number."""
        for ball in self.ball_list:
            if ball.number == number:
                return ball
        return None

    def input(self):
        """Handle user input for aiming and hitting the cue ball."""
        # > Command line
        # spd = float(input("Type the power you want to put into the cue ball (0 - 100): "))
        # angle_deg = float(input("Type your angle to hit (in degrees, 0°=to the right, 90°=up): "))

        # > Pop-up UI
        while True:
            try:
                # Prompt for shot power
                power = self.screen.textinput(
                    "Power", "Enter shot power (0-100): ")
                if power is None:  # User cancelled
                    continue
                power = float(power)
                if not (0 <= power <= 100):
                    raise ValueError("Shot power must be between 0 and 100.")

                # Prompt for aiming angle
                angle = self.screen.textinput(
                    "Aiming", "Enter aiming angle (in degrees, 0-360): "
                )
                if angle is None:  # User cancelled
                    continue
                try:
                    angle = float(angle)
                    break
                except ValueError:
                    raise ValueError("Aiming angle must be integer or float.")
            except ValueError as e:
                out = f"Invalid Input", f"{e}. Press Enter to try again."
                self.screen.textinput(out)

        # >
        # angle = 90  # Default aiming angle
        # while True:
        #     key = self.screen.textinput("Aiming", "Press 'a' to rotate left, 'd' to rotate right, 'enter' to shoot:")
        #     if key == "a":
        #         angle -= 10
        #     elif key == "d":
        #         angle += 10
        #     elif key == " ":
        #         break
        #     self.cue_stick.set_angle(angle)
        #     self.cue_stick.show()

        # Convert angle to radians and calculate velocity
        angle_rad = math.radians(angle)
        velocity = (power / 100) * MAX_SPEED_PX_S

        # Set velocity for the cue ball
        for ball in self.ball_list:
            if isinstance(ball, CueBall):  # Cue ball
                ball.vx = velocity * math.cos(angle_rad)
                ball.vy = velocity * math.sin(angle_rad)
        print(power, angle)

    def run(self):
        """Main game loop."""
        game_over = False
        while not game_over:
            self._update_game()
            if self._next_move():
                if self._is_game_won():
                    game_over = True
                else:
                    self.input()

        self._display_win_message()

    def _update_game(self):
        """Update the game state."""
        for ball in self.ball_list:
            ball.move(self.dt)
            self.check_pockets()
            self.check_table_edge_collisions(ball)
        self.check_ball_collisions()
        self._redraw()

    def _redraw(self):
        """Clear and redraw the table and balls."""
        turtle.clear()
        self.table.draw_table()
        for ball in self.ball_list:
            ball.draw()
        turtle.update()

    def _next_move(self):
        """Check if all balls have stopped moving."""
        return all(not ball.is_moving() for ball in self.ball_list)

    def check_pockets(self):
        """Check for balls pocketed."""
        pocketed_balls = self.table.check_pockets(self.ball_list)
        for ball in pocketed_balls:
            if ball.number is None:  # Cue ball pocketed
                self._handle_cue_ball_pocketed(ball)
            else:
                self.ball_list.remove(ball)  # Remove other balls
            print(f"Ball {ball.number} is pocketed")


    def _handle_cue_ball_pocketed(self, ball):
        """Handle the event when the cue ball is pocketed."""
        self.screen.textinput(
            "Scratch!", "The cue ball has been pocketed! Press Enter to continue."
        )
        ball.x = -self.canvas_width / 3  # Reset position
        ball.y = 0
        ball.vx = 0
        ball.vy = 0

    def check_table_edge_collisions(self, ball):
        """Check and handle collisions with table edges."""
        ball.bounce_off_horizontal(self.canvas_width)
        ball.bounce_off_vertical(self.canvas_height)

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
        return len(self.ball_list) == 1 and self.ball_list[0].number is None

    def _display_win_message(self):
        """Display a victory message."""
        self.turtle.color("black")
        self.turtle.write("Victory!!!!", align="center",
                          font=("Helvetica", 36))


# Run the simulation
if __name__ == "__main__":
    screen = turtle.Screen()
    screen.tracer(0)
    screen.colormode(255)
    screen.bgcolor(POOL_TABLE_COLOR)

    myturtle = turtle.Turtle()
    myturtle.speed(0)
    myturtle.hideturtle()
    sim = PoolSimulator(myturtle)
    sim.run()
