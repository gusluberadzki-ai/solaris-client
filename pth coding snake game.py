# snake_turtle.py

import turtle
import time
import random

# --- Configurable settings ---
WIDTH, HEIGHT = 1445, 920      # screen size
DELAY = 0.12                 # delay (seconds) between frames; lower = faster
FOOD_DIST = 15               # distance threshold to count as "eating" food
SEGMENT_GAP = 20             # how far apart segments are placed

# --- Screen setup ---
screen = turtle.Screen()
screen.title("Snake - Turtle")
screen.bgcolor("gray")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)  # turn off automatic animation; we'll call screen.update()


# --- Scoreboard ---
score = 0
high_score = 0

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, HEIGHT//2 - 40)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal"))


def update_scoreboard():
    pen.clear()
    pen.goto(0, HEIGHT//2 - 40)
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal"))

# --- Snake head ---
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"  # can be "up", "down", "left", "right", or "stop"

# --- Food ---
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(0.8, 0.8)  # slightly smaller
food.goto(0, 100)

def random_food_position():
    # Choose coordinates inside the screen bounds, avoiding edges
    x = random.randint(-WIDTH//2 + 20, WIDTH//2 - 20)
    y = random.randint(-HEIGHT//2 + 20, HEIGHT//2 - 20)
    # Snap to grid of SEGMENT_GAP pixels to keep alignment
    x = (x // SEGMENT_GAP) * SEGMENT_GAP
    y = (y // SEGMENT_GAP) * SEGMENT_GAP
    return x, y

# --- Body segments list ---
segments = []

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
    elif head.direction == "down":
        head.sety(y - SEGMENT_GAP)
    elif head.direction == "left":
        head.setx(x - SEGMENT_GAP)
    elif head.direction == "right":
        head.setx(x + SEGMENT_GAP)
    # if "stop", don't move

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

# --- Main game loop ---
def reset_game():
    global score, DELAY
    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    # hide segments
    for seg in segments:
        seg.goto(1000, 1000)  # move offscreen
    segments.clear()

    score = 0
    DELAY = 0.12
    update_scoreboard()

# Put food initial position aligned to grid
food.goto(random_food_position())

while True:
    screen.update()  # redraw screen

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
        new_seg = turtle.Turtle()
        new_seg.shape("square")
        new_seg.color("lightgreen")
        new_seg.penup()
        segments.append(new_seg)

        # Increase the score and slightly speed up the game
        score += 10
        if score % 50 == 0 and DELAY > 0.03:
            DELAY -= 0.01
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
