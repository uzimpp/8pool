"""Configuration constants and settings for the pool game simulation."""
# Simulation Constants
HZ = 60
DT = 1 / HZ
PEN_SIZE = 3

# Table Configurations
# Table dimensions (in feet): 9ft x 4.5ft
# Scale: 1 ft = 100 px
# 1 meter = 30.48 px
# Table in pixels: 900 px x 450 px
PX_PER_M = 30.48

# Table Dimensions
TABLE_LENGTH = 900  # in pixels
TABLE_WIDTH = 450  # in pixels

# Table Colors
POOL_TABLE_CLOTH_COLOR = (121, 163, 103)     # Muted moss green for a cozy feel
# Warm dark brown for table boundary
POOL_TABLE_COLOR = (65, 50, 40)
POOL_TABLE_POCKET_COLOR = (45, 35, 25)       # Deep walnut brown for pockets


# Canvas Dimensions (Half of the Table Dimensions)
CANVAS_WIDTH = TABLE_LENGTH / 2  # Half the length of the table in pixels
CANVAS_HEIGHT = TABLE_WIDTH / 2  # Half the width of the table in pixels


# Ball Configurations
CREAM = (220, 210, 190)        # Warm, soft cream
BALL_COLORS = {
    1: (200, 160, 50),         # Muted golden yellow
    2: (70, 110, 150),         # Slate blue
    3: (180, 60, 50),          # Coral red
    4: (120, 90, 140),         # Lavender purple
    5: (200, 120, 70),         # Peach orange
    6: (80, 140, 110),         # Sage green
    7: (90, 45, 35),           # Brick red
    8: (20, 20, 20),           # Charcoal black (8-ball)
    9: CREAM,                  # Stripe - golden cream
    10: CREAM,                 # Stripe - slate cream
    11: CREAM,                 # Stripe - coral cream
    12: CREAM,                 # Stripe - lavender cream
    13: CREAM,                 # Stripe - apricot cream
    14: CREAM,                 # Stripe - teal cream
    15: CREAM,                 # Stripe - mahogany cream
    None: (230, 220, 200)      # Cue ball - soft ivory
}

# Ball Rows (Standard Triangle Setup)
BALL_ROWS = [
    [1],
    [2, 3],
    [4, 5, 6],
    [7, 8, 9, 10],
    [11, 12, 13, 14, 15],
]
BALL_RADIUS = 12
BALL_DIAMETER = 2 * BALL_RADIUS + 1.25 * PEN_SIZE
CUEBALL_POS = (-CANVAS_WIDTH / 2, 0)


# Cue Stick Configurations
CUESTICK_HANDLE_COLOR = (120, 85, 60)      # Rich mahogany for the handle
CUESTICK_SHAFT_COLOR = (200, 170, 140)     # Light warm beige for the shaft
CUESTICK_TIP_COLOR = (100, 90, 85)         # Soft charcoal gray for the tip
CUESTICK_THICKNESS = 3.25                # Thickness of the cue stick
CUESTICK_LENGTH = 320                    # Length of the cue stick
# Initial distance between cue stick tip and cue ball
OFFSET = 30
POWER_STEP = 10                          # Power adjustment step
ANGLE_STEP = 6                           # Angle rotation step (degrees)


# Physics Configurations
GRAVITY = 9.8
SLIDING_FRICTION_COEF = 0.2  # Ball-cloth sliding friction
BALL_BALL_RESTITUTION = 0.96  # Typical for billiard balls
BALL_RAIL_RESTITUTION = 0.75
BALL_MASS = 0.17  # Standard mass for billiard balls in kilograms
MAX_SPEED_M_S = 11.623  # Maximum cue ball speed
MAX_SPEED_PX_S = MAX_SPEED_M_S * PX_PER_M
MIN_SPEED_PX_S = 0.1
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
