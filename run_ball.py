import ball
import my_event
import turtle
import random
import heapq
import paddle
import math

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)
        self.move_speed = 50
        ball_radius = 0.025 * self.canvas_width
        for i in range(self.num_balls):
            x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
            y = 0.0
            vx = 10 * random.uniform(-1.0, 1.0)
            vy = 10 * random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))

        tom = turtle.Turtle()
        self.p1 = paddle.Paddle(20, 120, "black", tom)  # Left paddle
        self.p2 = paddle.Paddle(20, 120, "red", tom)   # Right paddle
        
        # Set initial positions for paddles
        self.p1.set_location([-self.canvas_width + 50, 0])  # Left side
        self.p2.set_location([self.canvas_width - 50, 0])   # Right side
        self.screen = turtle.Screen()
    
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

    def __redraw(self):
        turtle.clear()
        self.p1.clear()
        self.p2.clear()
        self.__draw_border()
        self.p1.draw()
        self.p2.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0/self.HZ, None, None, None))

    def __predict(self, ball):
        if ball is None:
            return
            
        # Predict wall collisions first
        dtv = ball.time_to_hit_vertical_wall()
        dth = ball.time_to_hit_horizontal_wall()
        
        # Add wall collision events if they're going to happen
        if dtv != math.inf:
            heapq.heappush(self.pq, my_event.Event(self.t + dtv, ball, None, None))
        if dth != math.inf:
            heapq.heappush(self.pq, my_event.Event(self.t + dth, None, ball, None))
        
        # Then predict ball collisions
        for other_ball in self.ball_list:
            if ball is not other_ball:
                dt = ball.time_to_hit(other_ball)
                if dt != math.inf:
                    heapq.heappush(self.pq, my_event.Event(self.t + dt, ball, other_ball, None))
    
    def __paddle_predict(self):
        for ball in self.ball_list:
            # Skip if ball is too close to walls
            if (abs(ball.x) >= self.canvas_width - ball.size or 
                abs(ball.y) >= self.canvas_height - ball.size):
                continue
                
            dtP1 = ball.time_to_hit_paddle(self.p1)
            dtP2 = ball.time_to_hit_paddle(self.p2)
            
            if dtP1 != math.inf:
                heapq.heappush(self.pq, my_event.Event(self.t + dtP1, ball, None, self.p1))
            if dtP2 != math.inf:
                heapq.heappush(self.pq, my_event.Event(self.t + dtP2, ball, None, self.p2))

    def move_paddle_up(self, paddle):
        if (paddle.location[1] + paddle.height/2 + self.move_speed) <= self.canvas_height:
            paddle.set_location([paddle.location[0], paddle.location[1] + self.move_speed])
    
    def move_paddle_down(self, paddle):
        if (paddle.location[1] - paddle.height/2 - self.move_speed) >= -self.canvas_height:
            paddle.set_location([paddle.location[0], paddle.location[1] - self.move_speed])
    
    def move_paddle_left(self, paddle):
        if paddle == self.p1:  # Left paddle
            if (paddle.location[0] - paddle.width/2 - self.move_speed) >= -self.canvas_width:
                paddle.set_location([paddle.location[0] - self.move_speed, paddle.location[1]])
        else:  # Right paddle
            if (paddle.location[0] - paddle.width/2 - self.move_speed) >= 0:
                paddle.set_location([paddle.location[0] - self.move_speed, paddle.location[1]])
    
    def move_paddle_right(self, paddle):
        if paddle == self.p1:  # Left paddle
            if (paddle.location[0] + paddle.width/2 + self.move_speed) <= 0:
                paddle.set_location([paddle.location[0] + self.move_speed, paddle.location[1]])
        else:  # Right paddle
            if (paddle.location[0] + paddle.width/2 + self.move_speed) <= self.canvas_width:
                paddle.set_location([paddle.location[0] + self.move_speed, paddle.location[1]])
    def run(self):
        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, my_event.Event(0, None, None, None))

        # listen to keyboard events and activate move_left and move_right handlers accordingly
        self.screen.listen()
        self.screen.onkey(lambda: self.move_paddle_up(self.p1), "w")
        self.screen.onkey(lambda: self.move_paddle_down(self.p1), "s")
        self.screen.onkey(lambda: self.move_paddle_left(self.p1), "a")
        self.screen.onkey(lambda: self.move_paddle_right(self.p1), "d")
        
        # Right paddle controls (Arrow keys)
        self.screen.onkey(lambda: self.move_paddle_up(self.p2), "Up")
        self.screen.onkey(lambda: self.move_paddle_down(self.p2), "Down")
        self.screen.onkey(lambda: self.move_paddle_left(self.p2), "Left")
        self.screen.onkey(lambda: self.move_paddle_right(self.p2), "Right")

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue
    
            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle
    
            # Update positions
            for ball in self.ball_list:
                ball.move(e.time - self.t)
            self.t = e.time
    
            # Handle collisions
            if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
                ball_a.bounce_off_paddle(paddle_a)
    
            # Predict next collisions
            self.__predict(ball_a)
            self.__predict(ball_b)
            self.__paddle_predict()
        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))
num_balls = 3
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
