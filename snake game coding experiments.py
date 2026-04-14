import turtle
import time
import random
from pathlib import Path
 
# --- Configurable settings ---
WIDTH, HEIGHT = 1475, 890
# Timing: starting delay and minimum delay (seconds)
INITIAL_DELAY = 0.1
MIN_DELAY = 0.001
DELAY = INITIAL_DELAY
FOOD_DIST = 15
SEGMENT_GAP = 20
 
# --- Assets ---
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path.cwd()

def asset_path(name: str) -> str:
    path = SCRIPT_DIR / name
    return str(path) if path.exists() else name

BACKGROUND_IMG = asset_path("forest.gif")
HEAD_UP = asset_path("snakehead.gif")
HEAD_RIGHT = asset_path("snakeheadright.gif")
HEAD_DOWN = asset_path("snakeheaddown.gif")
HEAD_LEFT = asset_path("snakeheadleft.gif")
BODY_PATH = asset_path("snakebody1.gif")

# --- Screen setup ---
screen = turtle.Screen()
screen.title("Snake - Turtle")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)
# register custom shapes if available (no-op if missing)
for shp in (BACKGROUND_IMG, HEAD_UP, HEAD_RIGHT, HEAD_DOWN, HEAD_LEFT, BODY_PATH):
    try:
        screen.register_shape(shp)
    except Exception:
        pass

try:
    screen.bgpic(BACKGROUND_IMG)
except Exception:
    pass
# --- Scoreboard ---
score = 0
high_score = 0
is_paused = False
 
def make_turtle(shape=None, color=None, hide=True):
    """Create and return a configured Turtle instance."""
    t = turtle.Turtle()
    if hide:
        t.hideturtle()
    t.penup()
    t.speed(0)
    if shape:
        try:
            t.shape(shape)
        except Exception:
            # fallback to default shape
            pass
    if color:
        try:
            t.color(color)
        except Exception:
            pass
    return t

pen = make_turtle(hide=False, color="white")
pen.hideturtle()
pen.penup()
pen.goto(0, HEIGHT//2 - 40)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal"))

def update_scoreboard():
    pen.clear()
    pen.goto(0, HEIGHT//2 - 40)
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal"))

# --- Snake head ---
head = make_turtle(shape=HEAD_UP, color="green", hide=False)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# --- Food ---
food = make_turtle(shape="circle", color="red", hide=False)
try:
    food.shapesize(0.8, 0.8)
except Exception:
    pass
food.goto(0, 100)

def random_food_position():
    
    x = random.randint(-WIDTH//2 + 20, WIDTH//2 - 20)
    y = random.randint(-HEIGHT//2 + 20, HEIGHT//2 - 20)
    # Snap to grid of SEGMENT_GAP pixels to keep alignment
    x = (x // SEGMENT_GAP) * SEGMENT_GAP
    y = (y // SEGMENT_GAP) * SEGMENT_GAP
    return x, y

# --- Body segments list ---
segments = []

# (obstacles removed)

# --- Movement functions (controls) ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move_head():
    x = head.xcor()
    y = head.ycor()
    if head.direction == "up":
        head.sety(y + SEGMENT_GAP)
        head.shape(HEAD_UP)
    elif head.direction == "down":
        head.sety(y - SEGMENT_GAP)
        head.shape(HEAD_DOWN)
    elif head.direction == "left":
        head.setx(x - SEGMENT_GAP)
        head.shape(HEAD_LEFT)
    elif head.direction == "right":
        head.setx(x + SEGMENT_GAP)
        head.shape(HEAD_RIGHT)
    # if "stop", don't move

# --- Cheat functions ---
def create_segment():
    seg = make_turtle(shape=BODY_PATH, hide=False)
    seg.penup()
    # start off-screen until placed
    try:
        seg.goto(1000, 1000)
    except Exception:
        pass
    return seg

def add_tail():
    segments.append(create_segment())
    global score
    score += 10
    update_scoreboard()

# --- Main game loop setup ---
def reset_game():
    global score, DELAY, is_paused
    is_paused = False
    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    # hide segments
    for seg in segments:
        seg.goto(1000, 1000)  
    segments.clear()


    score = 0
    DELAY = INITIAL_DELAY
    update_scoreboard()
    
    # (no obstacles)

# --- Pause state ---
pause_text = turtle.Turtle()
pause_text.hideturtle()
pause_text.penup()
pause_text.color("yellow")

def show_pause_menu():
    """Display pause text"""
    global is_paused
    pause_text.goto(0, 0)
    pause_text.write("PAUSED - Press SPACE to Resume", align="center", font=("Courier", 24, "bold"))

def hide_pause_menu():
    """Hide pause text"""
    global is_paused
    pause_text.clear()
    is_paused = False

def toggle_pause():
    """Toggle pause"""
    global is_paused
    if not is_paused:
        is_paused = True
        show_pause_menu()
    else:
        hide_pause_menu()

# --- Keyboard bindings ---
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")
# Also WASD for convenience
screen.onkey(go_up, "w")
screen.onkey(go_down, "s")
screen.onkey(go_left, "a")
screen.onkey(go_right, "d")
# Cheat key
screen.onkey(add_tail, "p")
# Pause/Resume
screen.onkey(toggle_pause, "space")

# Put food initial position aligned to grid
food.goto(random_food_position())

while True:
    screen.update()  # redraw screen
    
    # Skip game logic if paused
    if is_paused:
        time.sleep(0.1)
        continue

    # 1) Check collision with walls
    x, y = head.xcor(), head.ycor()
    half_w, half_h = WIDTH//2, HEIGHT//2
    # If head hits a wall (we use strict bounds)
    if x > half_w - 10 or x < -half_w + 10 or y > half_h - 10 or y < -half_h + 10:
        # Game over - reset
        # Update high score
        if score > high_score:
            high_score = score
        reset_game()

    # 2) Check collision with food
    if head.distance(food) < FOOD_DIST:
        # Move food to a new random location
        new_x, new_y = random_food_position()
        # Make sure it doesn't spawn on top of the snake
        collision = True
        while collision:
            collision = False
            for seg in segments + [head]:
                if seg.distance(new_x, new_y) < SEGMENT_GAP:
                    collision = True
                    new_x, new_y = random_food_position()
                    break
        food.goto(new_x, new_y)

        # Add a new segment to the snake
        segments.append(create_segment())

        # Increase the score and slightly speed up the game
        score += 10
        if score % 50 == 0 and DELAY > MIN_DELAY:
            DELAY = max(DELAY - 0.01, MIN_DELAY)
        update_scoreboard()

    # 3) Move the segments in reverse order so each follows the one in front
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    # Move first segment to where head was
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # 4) Move the head
    move_head()

    # 5) Check collision with body segments
    for seg in segments:
        if seg.distance(head) < SEGMENT_GAP/2:
            # Game over - reset
            if score > high_score:
                high_score = score
            reset_game()
            break

    time.sleep(DELAY)
        
