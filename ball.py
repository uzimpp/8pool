import turtle
import math

class Ball:
    def __init__(self, size, x, y, vx, vy, color, id):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100*size**2
        self.count = 0
        self.id = id
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        

    def draw(self):
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y-self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def time_to_hit(self, that):
        """Calculate time until collision with another ball"""
        if self is that:
            return math.inf
            
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        
        if dvdr > 0:
            return math.inf
            
        dvdv = dvx * dvx + dvy * dvy
        drdr = dx * dx + dy * dy
        sigma = self.size + that.size
        
        if dvdv == 0:
            return math.inf
            
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        
        if d < 0:
            return math.inf
            
        t = -(dvdr + math.sqrt(d)) / dvdv
        
        if t <= 0:
            return math.inf
            
        return t
    
    def time_to_hit_vertical_wall(self):
        """Calculate time until collision with vertical walls"""
        if self.vx == 0:
            return math.inf
            
        # Time to hit right wall
        if self.vx > 0:
            dt = (self.canvas_width - self.size - self.x) / self.vx
        # Time to hit left wall
        else:
            dt = (-self.canvas_width + self.size - self.x) / self.vx
            
        return dt if dt > 0 else math.inf
    
    def time_to_hit_horizontal_wall(self):
        """Calculate time until collision with horizontal walls"""
        if self.vy == 0:
            return math.inf
            
        # Time to hit top wall
        if self.vy > 0:
            dt = (self.canvas_height - self.size - self.y) / self.vy
        # Time to hit bottom wall
        else:
            dt = (-self.canvas_height + self.size - self.y) / self.vy
            
        return dt if dt > 0 else math.inf

    def bounce_off(self, that):
        dx  = that.x - self.x
        dy  = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy; # dv dot dr
        dist = self.size + that.size   # distance between particle centers at collison

        # magnitude of normal force
        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass
        
        # update collision counts
        self.count += 1
        that.count += 1

    def bounce_off_vertical_wall(self):
        # Force ball back inside bounds if it somehow got outside
        if self.x + self.size > self.canvas_width:
            self.x = self.canvas_width - self.size
        elif self.x - self.size < -self.canvas_width:
            self.x = -self.canvas_width + self.size
        
        self.vx = -self.vx
        self.count += 1
    
    def bounce_off_horizontal_wall(self):
        # Force ball back inside bounds if it somehow got outside
        if self.y + self.size > self.canvas_height:
            self.y = self.canvas_height - self.size
        elif self.y - self.size < -self.canvas_height:
            self.y = -self.canvas_height + self.size
            
        self.vy = -self.vy
        self.count += 1
    
    def move(self, dt):
        # Prevent moving outside bounds
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt
        
        # Clamp positions to stay within bounds
        self.x = max(min(new_x, self.canvas_width - self.size), -self.canvas_width + self.size)
        self.y = max(min(new_y, self.canvas_height - self.size), -self.canvas_height + self.size)

    def time_to_hit_paddle(self, paddle):
        # Calculate distances to paddle edges
        dx_left = paddle.location[0] - paddle.width/2 - self.x
        dx_right = paddle.location[0] + paddle.width/2 - self.x
        dy_top = paddle.location[1] + paddle.height/2 - self.y
        dy_bottom = paddle.location[1] - paddle.height/2 - self.y
        
        # Time to hit vertical edges (left/right)
        dt_x = None
        if self.vx > 0:  # Moving right
            if dx_left > 0:
                dt_x = dx_left / self.vx
        elif self.vx < 0:  # Moving left
            if dx_right < 0:
                dt_x = dx_right / self.vx
                
        # Time to hit horizontal edges (top/bottom)
        dt_y = None
        if self.vy > 0:  # Moving up
            if dy_bottom > 0:
                dt_y = dy_bottom / self.vy
        elif self.vy < 0:  # Moving down
            if dy_top < 0:
                dt_y = dy_top / self.vy
        
        # If no collision possible
        if dt_x is None and dt_y is None:
            return math.inf
            
        # Find earliest collision time
        dt = min(dt for dt in [dt_x, dt_y] if dt is not None)
        if dt < 0:
            return math.inf
            
        # Check if collision point is within paddle bounds
        future_x = self.x + self.vx * dt
        future_y = self.y + self.vy * dt
        
        paddle_left = paddle.location[0] - paddle.width/2
        paddle_right = paddle.location[0] + paddle.width/2
        paddle_bottom = paddle.location[1] - paddle.height/2
        paddle_top = paddle.location[1] + paddle.height/2
        
        # Add ball size to collision bounds
        if (paddle_left - self.size <= future_x <= paddle_right + self.size and
            paddle_bottom - self.size <= future_y <= paddle_top + self.size):
            return dt
        return math.inf

    def bounce_off_paddle(self, paddle):
        """Bounce off paddle considering the collision point"""
        # Determine collision point
        paddle_center_x = paddle.location[0]
        paddle_center_y = paddle.location[1]
        
        # Check if collision is more horizontal or vertical
        dx = abs(self.x - paddle_center_x)
        dy = abs(self.y - paddle_center_y)
        
        if dx * paddle.height > dy * paddle.width:
            # Horizontal collision (sides)
            self.vx = -self.vx
        else:
            # Vertical collision (top/bottom)
            self.vy = -self.vy
            
        # Add a small velocity boost to prevent sticking
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed != 0:
            self.vx = (self.vx / speed) * (speed * 1.01)
            self.vy = (self.vy / speed) * (speed * 1.01)
        self.count += 1

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)
