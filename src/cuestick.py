import turtle

class CueStick:
    def __init__(self, image, cueball, angle_deg=90):
        # Create a turtle for the cue stick
        self.turtle = turtle.Turtle()
        self.turtle.screen.register_shape(image)
        self.turtle.shape(image)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.cueball = cueball
        self.angle = angle_deg
        self.offset = 100
        self.location = [cueball.x, cueball.y]

    def set_location(self, location):
        self.location = location
        self.turtle.goto(self.location[0], self.location[1])

    def draw(self):
        self.turtle.goto(self.cueball.x, self.cueball.y)
        # self.turtle.pendown()
        # self.turtle.begin_fill()
        # for _ in range(2):
        #     self.turtle.left(90)
        #     self.turtle.forward(self.height)
        #     self.turtle.left(90)
        #     self.turtle.forward(self.width)
        # self.turtle.end_fill()
        # self.turtle.penup()
        # self.turtle.goto(self.location[0], self.location[1])

    def clear(self):
        self.turtle.clear()

    def __str__(self):
        return "Cue stick"
