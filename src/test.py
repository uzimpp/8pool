import turtle
import random
import math
from cueball import Ball, StripeBall


class SnookerSimulator:
    def __init__(self):
        """Basics"""
        self.ball_list = []
        self.t = 0.0
        self.HZ = 60
        self.dt = 1.0 / self.HZ

        """Table and screen"""
        # Table dimensions (in feet): 9ft x 4.5ft
        # Scale: 1 ft = 100 px
        # 1 meter = 30.48 px
        # Table in pixels: 900 px x 450 px
        self.table_length = 900
        self.table_width = 450
        turtle.setup(width=self.table_length+100, height=self.table_width+100)

        # Canvas half-width and half-height for convenience
        self.canvas_width = self.table_length / 2
        self.canvas_height = self.table_width / 2
        
        """Balls"""
        # Ball radius (approx. 2.25" diameter, 2.25"/12 = 0.1875 ft * 100 px/ft ≈ 18.75 px dia)
        # Radius ~9 px
        ball_radius = 9
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
        } # Ball colors and arrangement
        ball_rows = [
            [1],
            [2, 3],
            [4, 5, 6],
            [7, 8, 9, 10],
            [11, 12, 13, 14, 15]
        ] # The standard 15-ball triangle:

        start_x = self.canvas_width / 3
        start_y = 0 
        ball_diameter = ball_radius * 2 * 1.25
        # y_spacing = ball_radius   # y offset between rows in each column is ball_diameter already
        x_spacing = ball_diameter * math.sqrt(3)/2
        row_x = start_x
        for idx, row in enumerate(ball_rows):
            # total height of this column
            row_height = (len(row)-1) * ball_diameter
            # center them around start_y
            row_y = start_y - row_height/2
            for num in row:
                color = ball_colors[num]
                if num >= 9:
                    stripe_color = color = ball_colors[num % 8]
                    b = StripeBall(ball_radius, row_x, row_y, 0, 0, color, stripe_color, number=num)
                else:
                    b = Ball(ball_radius, row_x, row_y, 0, 0, color, number=num)
                self.ball_list.append(b)
                row_y += ball_diameter
            # Add spacing for the next
            row_x += x_spacing

        """Cue ball"""
        # placing the cue ball on the left
        cue_x = -self.canvas_width / 3
        cue_y = 0
        cue_ball_color = (253, 249, 237)  # off-white
        self.ball_list.append(Ball(ball_radius, cue_x, cue_y, 0, 0, cue_ball_color, number=None))

        self.screen = turtle.Screen()

    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(5)
        turtle.pendown()
        turtle.color((93, 125, 88))
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)
        turtle.end_fill()

    def __redraw(self):
        turtle.clear()
        self.__draw_border()
        for b in self.ball_list:
            b.draw()
        turtle.update()

    def check_table_edge_collisions(self, ball):
        # Top & Bottom edge
        if ball.x - ball.size < -self.canvas_width:
            ball.x = -self.canvas_width + ball.size
            ball.vx = -ball.vx
        elif ball.x + ball.size > self.canvas_width:
            ball.x = self.canvas_width - ball.size
            ball.vx = -ball.vx
        # Left & Right edge
        if ball.y - ball.size < -self.canvas_height:
            ball.y = -self.canvas_height + ball.size
            ball.vy = -ball.vy
        elif ball.y + ball.size > self.canvas_height:
            ball.y = self.canvas_height - ball.size
            ball.vy = -ball.vy

    def check_ball_collisions(self):
        n = len(self.ball_list)
        for i in range(n):
            for j in range(i+1, n):
                bi = self.ball_list[i]
                bj = self.ball_list[j]
                dx = bj.x - bi.x
                dy = bj.y - bi.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < (bi.size + bj.size):
                    bi.bounce_off(bj)
                    # Preventing overlap
                    overlap = (bi.size + bj.size) - dist
                    nx = dx/dist
                    ny = dy/dist
                    bi.x -= nx*(overlap/2.0)
                    bi.y -= ny*(overlap/2.0)
                    bj.x += nx*(overlap/2.0)
                    bj.y += ny*(overlap/2.0)

    def next_move(self):
        for ball in self.ball_list:
            if ball.is_moving():
                return False
        return True

    def input(self):
        spd = float(input("Type the power you want to put into the cue ball (0 - 100): "))
        angle_deg = float(input("Type your angle to hit (in degrees, 0°=to the right, 90°=up): "))
        angle = math.radians(angle_deg)
        
        # More realistic speed scaling
        # Max speed ever record
        max_speed_m_s = 11.623
        px_per_m = 30.48  # from scaling
        max_speed_px_s = max_speed_m_s * px_per_m  # ~656 px/s
        v = (spd / 100) * max_speed_px_s

        for i in self.ball_list:
            if i.number is None:  # cue ball
                i.vx = v * math.cos(angle)
                i.vy = v * math.sin(angle)

    def run(self):
        while True:
            while True:
                for b in self.ball_list:
                    b.move(self.dt)
                    self.check_table_edge_collisions(b)
                self.check_ball_collisions()
                self.__redraw()
                if self.next_move():
                    self.input()
                    break

        turtle.done()

# Run the simulation
turtle.speed(0)
turtle.tracer(0)
turtle.hideturtle()
turtle.colormode(255)
sim = SnookerSimulator()
sim.run()
