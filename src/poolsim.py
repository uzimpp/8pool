import turtle
import random
import math
from ball import Ball, CueBall, StripeBall
from cuestick import CueStick
from table import Table

class PoolSimulator:
    def __init__(self, myturtle):
        """Basics"""
        self.turtle = myturtle
        self.pen_size = 3
        self.ball_list = []
        self.HZ = 60
        self.dt = 1.0 / self.HZ
        self.screen = turtle.Screen()

        """Object balls"""
        # Ball radius (approx. 2.25" diameter, 2.25"/12 = 0.1875 ft * 100 px/ft ≈ 18.75 px dia)
        # Radius ~9 px
        ball_radius = 11
        ball_colors = {
            1: (255, 223, 86),     # yellow
            2: (62, 88, 240),      # blue
            3: (242, 63, 51),      # red
            4: (136, 67, 190),     # purple
            5: (251, 129, 56),     # orange
            6: (151, 234, 160),    # green
            7: (139, 0, 0),        # maroon
            8: (21, 9, 30),        # black
            9: (248, 240, 211),
            10: (248, 240, 211),
            11: (248, 240, 211),
            12: (248, 240, 211),
            13: (248, 240, 211),
            14: (248, 240, 211),
            15: (248, 240, 211),
        }  # Ball colors and arrangement
        ball_rows = [
            [1],
            [2, 3],
            [4, 5, 6],
            [7, 8, 9, 10],
            [11, 12, 13, 14, 15]
        ]  # The standard 15-ball triangle:
        ball_diameter =  2 * ball_radius + 2 * self.pen_size

        """Table and screen"""
        # Table dimensions (in feet): 9ft x 4.5ft
        # Scale: 1 ft = 100 px
        # 1 meter = 30.48 px
        # Table in pixels: 900 px x 450 px
        self.table_length = 900
        self.table_width = 450
        self.screen.setup(width=self.table_length + 100, height=self.table_width + 100)

        # Canvas half-width and half-height for convenience
        self.canvas_width = self.table_length / 2
        self.canvas_height = self.table_width / 2

        self.table = Table(self.table_length, self.table_width, ball_diameter)

        """Cue ball"""
        # placing the cue ball on the left
        cue_x = -self.canvas_width / 3
        cue_y = 0
        cue_ball_color = (253, 249, 237)  # off-white
        cueball = CueBall(ball_radius, cue_x, cue_y, 0, 0, cue_ball_color, self.pen_size, number=None)
        self.ball_list.append(cueball)

        """Cue Stick"""
        # self.cuestick = CueStick("cuestick.gif", cueball, 90)

        start_x = self.canvas_width / 3
        start_y = 0
        # y_spacing = ball_radius   # y offset between rows in each column is ball_diameter already
        x_spacing = ball_diameter * math.sqrt(3)/2
        row_x = start_x
        for row in ball_rows:
            row_height = (len(row)-1) * ball_diameter
            row_y = start_y - row_height/2
            for num in row:
                color = ball_colors[num]
                if num >= 9:
                    stripe_color = color = ball_colors[num % 8]
                    b = StripeBall(ball_radius, row_x, row_y, 0,
                                   0, color, stripe_color, self.pen_size, number=num)
                else:
                    b = Ball(ball_radius, row_x, row_y,
                             0, 0, color, self.pen_size, number=num)
                self.ball_list.append(b)
                row_y += ball_diameter
            # Add spacing for the next
            row_x += x_spacing

    def find_ball(self, number):
        for ball in self.ball_list:
            if ball.number == number:
                return ball
        return None

    def input(self):
        """Aim and apply power."""
        
        # > Command line
        # spd = float(input("Type the power you want to put into the cue ball (0 - 100): "))
        # angle_deg = float(input("Type your angle to hit (in degrees, 0°=to the right, 90°=up): "))
        
        # > Pop-up UI
        while True:
            try:
                # Prompt the user for shot power (ensure it's a valid float within range)
                power = self.screen.textinput("Power", "Enter shot power (0-100): ")
                if power is None:  # User cancelled the input
                    continue
                power = float(power)
                if not (0 <= power <= 100):
                    raise ValueError("Shot power must be between 0 and 100.")
        
                # Prompt the user for aiming angle (ensure it's a valid float)
                angle = self.screen.textinput("Aiming", "Enter aiming angle (in degrees, 0-360): ")
                if angle is None:  # User cancelled the input
                    continue
                try:
                    angle = float(angle)
                    break
                except ValueError:
                    raise ValueError("Aiming angle must be integer or float")
            except ValueError as e:
                # Inform the user about invalid input and restart the loop
                self.screen.textinput("Invalid Input", f"{e}. Press Enter to try again.")
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

        # self.cue_stick.hide()
        angle_rad = math.radians(angle)

        max_speed_m_s = 11.623
        px_per_m = 30.48
        max_speed_px_s = max_speed_m_s * px_per_m
        v = (power / 100) * max_speed_px_s

        for i in self.ball_list:
            if i.number is None:
                i.vx = v * math.cos(angle_rad)
                i.vy = v * math.sin(angle_rad)
        print(power, angle)

    def run(self):
        game_over = False
        while not game_over:
            self.__update()
            if self.next_move():
                if self.is_game_won():
                    game_over = True
                else:
                    self.input()

        self.display_win_message()

    def __update(self):
        for b in self.ball_list:
            b.move(self.dt)
            self.check_pockets()
            self.check_table_edge_collisions(b)
        self.check_ball_collisions()
        self.__redraw()

    def __redraw(self):
        turtle.clear()
        self.table.draw_table()
        for b in self.ball_list:
            b.draw()
        turtle.update()

    def next_move(self):
        for ball in self.ball_list:
            if ball.is_moving():
                return False
        return True

    def check_pockets(self):
        to_rm = self.table.check_pockets(self.ball_list)
        for ball in to_rm:
            if ball.number is None:  # Cue ball pocketed
                self.handle_cue_ball_pocketed(ball)
            else:
                self.ball_list.remove(ball)  # Remove other balls as usual
            print(ball.number)

    def handle_cue_ball_pocketed(self, ball):    
        # Penalize the player (display a message or adjust scores, if applicable)
        self.screen.textinput("Scratch!", "The cue ball has been pocketed! Press Enter to continue.")
        # Place the cue ball back on the table
        # Behind the head string (1/3 of table length from the nearest rail)
        ball.x = -self.canvas_width / 3
        ball.y = 0
        ball.vx = 0
        ball.vy = 0

    def check_table_edge_collisions(self, ball):
        # For now, keep using the canvas_width/canvas_height as your boundaries
        # If you want balls to only bounce inside a smaller inner area, adjust here
        if ball.x - ball.size < -self.canvas_width:
            ball.x = -self.canvas_width + ball.size
            ball.vx = -ball.vx
        elif ball.x + ball.size > self.canvas_width:
            ball.x = self.canvas_width - ball.size
            ball.vx = -ball.vx

        if ball.y - ball.size < -self.canvas_height:
            ball.y = -self.canvas_height + ball.size
            ball.vy = -ball.vy
        elif ball.y + ball.size > self.canvas_height:
            ball.y = self.canvas_height - ball.size
            ball.vy = -ball.vy

    def check_ball_collisions(self):
        n = len(self.ball_list)
        for i in range(n):
            for j in range(i + 1, n):
                bi = self.ball_list[i]
                bj = self.ball_list[j]
                dx = bj.x - bi.x
                dy = bj.y - bi.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < (bi.size + bj.size):
                    bi.bounce_off(bj)
                    overlap = (bi.size + bj.size) - dist
                    nx = dx / dist
                    ny = dy / dist
                    bi.x -= nx * (overlap / 2)
                    bi.y -= ny * (overlap / 2)
                    bj.x += nx * (overlap / 2)
                    bj.y += ny * (overlap / 2)

    def is_game_won(self):
        return len(self.ball_list) == 1 and self.ball_list[0].number is None

    def display_win_message(self):
        self.turtle.color("black")
        self.turtle.write("Victory!!!!", align="center", font=("Helvetica", 36))


# Run the simulation
screen = turtle.Screen()

# Set up the screen
screen.tracer(0)
screen.colormode(255)
screen.bgcolor((173, 106, 62))

# Create a turtle instance
myturtle = turtle.Turtle()
myturtle.speed(0)
myturtle.hideturtle()
sim = PoolSimulator(myturtle)
sim.run()
