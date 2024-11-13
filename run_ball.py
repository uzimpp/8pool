import turtle
import ball
import random

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)
        self.ball_radius = 0.05 * self.canvas_width
        for i in range(self.num_balls):
            x = random.randint(-1*self.canvas_width + self.ball_radius, self.canvas_width - self.ball_radius)
            y = random.randint(-1*self.canvas_height + self.ball_radius, self.canvas_height - self.ball_radius)
            vx = 2*random.uniform(-1.0, 1.0)
            vy = 2*random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(ball.Ball(self.ball_radius, x, y, vx, vy, ball_color))
    
    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))   
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def run(self):
        dt = 1
        while (True):
            turtle.clear()
            self.__draw_border()                
            for i in range(self.num_balls):
                self.ball_list[i].draw()
                self.ball_list[i].move(dt)
                self.ball_list[i].update_velocity()
            turtle.update()
        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

num_balls = int(input("Number of balls to simulate: "))
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
