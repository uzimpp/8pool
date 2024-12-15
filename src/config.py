# Simulation Constants
HZ = 60
DT = 1 / HZ
PEN_SIZE = 3

# Ball Configurations
CREAM = (248, 240, 211)
# Ball Colors
BALL_COLORS = {
    1: (255, 223, 86),     # yellow
    2: (62, 88, 240),      # blue
    3: (242, 63, 51),      # red
    4: (136, 67, 190),     # purple
    5: (251, 129, 56),     # orange
    6: (151, 234, 160),    # green
    7: (139, 0, 0),        # maroon
    8: (21, 9, 30),        # black
    9: CREAM,              # stripe (yellow but background white)
    10: CREAM,             # stripe (blue)
    11: CREAM,             # stripe (red)
    12: CREAM,             # stripe (purple)
    13: CREAM,             # stripe (orange)
    14: CREAM,             # stripe (green)
    15: CREAM,             # stripe (maroon)
    None: (253, 249, 237)  # cue ball Configuration
}

# Ball Rows (Standard Triangle Setup)
BALL_ROWS = [
    [1],
    [2, 3],
    [4, 5, 6],
    [7, 8, 9, 10],
    [11, 12, 13, 14, 15],
]

BALL_RADIUS = 11
BALL_DIAMETER = 2 * BALL_RADIUS + 2 * PEN_SIZE

# Table Configurations
# Table dimensions (in feet): 9ft x 4.5ft
# Scale: 1 ft = 100 px
# 1 meter = 30.48 px
# Table in pixels: 900 px x 450 px
px_per_m = 30.48

# Table Dimensions
TABLE_LENGTH = 900  # in pixels
TABLE_WIDTH = 450  # in pixels

POOL_TABLE_CLOTH_COLOR = (150, 205, 152)
POOL_TABLE_COLOR = (15, 15, 15)
POOL_TABLE_POCKET_COLOR = (28, 55, 41)


# Physics
GRAVITY = 9.8
FRICTION_COEIFFICIENT = 0.3  # Sliding friction coefficient for pool cloth
BALL_MASS = 0.17  # Standard mass for billiard balls in kilograms
max_speed_m_s = 11.623  # Maximum cue ball speed ever recorded
MAX_SPEED_PX_S = max_speed_m_s * px_per_m
