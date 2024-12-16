"""Configuration constants and settings for the pool game simulation."""

# Simulation Constants
HZ = 60  # Frames per second
DT = 1 / HZ  # Time step per frame
PEN_SIZE = 3  # Pen size for drawing


# Table Configurations
# Table dimensions in feet: 9ft x 4.5ft
# Scale: 1 ft = 100 px, 1 meter = 30.48 px
TABLE_LENGTH = 900  # Table length in pixels
TABLE_WIDTH = 450  # Table width in pixels
PX_PER_M = 30.48  # Pixels per meter

# Table Colors
POOL_TABLE_CLOTH_COLOR = (121, 163, 103)  # Muted moss green
POOL_TABLE_COLOR = (65, 50, 40)  # Warm dark brown for table boundary
POOL_TABLE_POCKET_COLOR = (45, 35, 25)  # Deep walnut brown for pockets

# Canvas Dimensions (Half of the Table Dimensions)
CANVAS_WIDTH = TABLE_LENGTH / 2  # Half the table length in pixels
CANVAS_HEIGHT = TABLE_WIDTH / 2  # Half the table width in pixels


# Ball Configurations
CREAM = (220, 210, 190)  # Warm, soft cream color
BALL_COLORS = {
    1: (200, 160, 50),  # Muted golden yellow
    2: (70, 110, 150),  # Slate blue
    3: (180, 60, 50),  # Coral red
    4: (120, 90, 140),  # Lavender purple
    5: (200, 120, 70),  # Peach orange
    6: (80, 140, 110),  # Sage green
    7: (90, 45, 35),  # Brick red
    8: (20, 20, 20),  # Charcoal black (8-ball)
    9: CREAM,  # Stripe - golden cream
    10: CREAM,  # Stripe - slate cream
    11: CREAM,  # Stripe - coral cream
    12: CREAM,  # Stripe - lavender cream
    13: CREAM,  # Stripe - apricot cream
    14: CREAM,  # Stripe - teal cream
    15: CREAM,  # Stripe - mahogany cream
    None: (230, 220, 200)  # Cue ball - soft ivory
}

# Ball Rows (Standard Triangle Setup)
BALL_ROWS = [
    [1],
    [2, 3],
    [4, 5, 6],
    [7, 8, 9, 10],
    [11, 12, 13, 14, 15],
]
BALL_RADIUS = 12  # Radius of each ball
BALL_DIAMETER = 2 * BALL_RADIUS + 1.25 * PEN_SIZE  # Diameter of each ball
CUEBALL_POS = (-CANVAS_WIDTH / 2, 0)  # Initial position of the cue ball


# Cue Stick Configurations
CUESTICK_HANDLE_COLOR = (120, 85, 60)  # Rich mahogany for the handle
CUESTICK_SHAFT_COLOR = (200, 170, 140)  # Light warm beige for the shaft
CUESTICK_TIP_COLOR = (100, 90, 85)  # Soft charcoal gray for the tip
CUESTICK_THICKNESS = 3.25  # Thickness of the cue stick
CUESTICK_LENGTH = 320  # Length of the cue stick
OFFSET = 30  # Initial distance between cue stick tip and cue ball
POWER_STEP = 10  # Power adjustment step
ANGLE_STEP = 4  # Angle rotation step (degrees)


# Physics Configurations
GRAVITY = 9.8  # Acceleration due to gravity
SLIDING_FRICTION_COEF = 0.2  # Ball-cloth sliding friction coefficient
BALL_BALL_RESTITUTION = 0.96  # Coefficient of restitution for ball collisions
BALL_RAIL_RESTITUTION = 0.75  # Coefficient of restitution for rail collisions
BALL_MASS = 0.17  # Mass of a billiard ball in kilograms
MAX_SPEED_M_S = 11.623  # Maximum cue ball speed in meters per second

# Maximum cue ball speed in pixels per second
MAX_SPEED_PX_S = MAX_SPEED_M_S * PX_PER_M
MIN_SPEED_PX_S = 0.1  # Minimum speed threshold in pixels per second
