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
            x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
            y = 0.0
            # x = random.uniform(-1*self.canvas_width + self.ball_radius, self.canvas_width - self.ball_radius)
            # y = random.uniform(-1*self.canvas_height + self.ball_radius, self.canvas_height - self.ball_radius)
            vx = 4*random.uniform(-1.0, 1.0)
            vy = 4*random.uniform(-1.0, 1.0)
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
    
    def __check_ball_collision(self, i):
        collision_pairs = []
        for j in range(len(self.ball_list)):
            if i == j:
                continue
            if self.ball_list[i].distance(self.ball_list[j]) <= self.ball_list[i].size + self.ball_list[j].size:
                collision_pairs.append([i, j])
        return collision_pairs

    def run(self):
        dt = 0.5
        while (True):
            turtle.clear()
            self.__draw_border()                
            for i in range(self.num_balls):
                self.ball_list[i].draw()
                self.ball_list[i].move(dt)
                # the code below will update ball velocities based on colliding conditions
                if (self.ball_list[i].check_h_wall_collision()):
                    self.ball_list[i].hitting_h_wall()
                if (self.ball_list[i].check_v_wall_collision()):
                    self.ball_list[i].hitting_v_wall()
                if (len(self.__check_ball_collision(i)) != 0):
                    for each_collision_pair in self.__check_ball_collision(i):
                        self.ball_list[each_collision_pair[0]].bounce_off(self.ball_list[each_collision_pair[1]])

            turtle.update()
        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

num_balls = int(input("Number of balls to simulate: "))
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
