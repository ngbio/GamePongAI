import turtle
import math
import random
import time
from joblib import load

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 4
PADDLE_LENGTH = 1
PADDLE_SPEED = 20
PADDLE_STEP = 25
BALL_SPEED = 20

# Initialize screen
sc = turtle.Screen()
sc.title("Pong-AI")
sc.bgcolor("black")
sc.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

sketch = turtle.Turtle() #hiển thị tỉ số
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 240)

#======>  đây vẽ ra thanh và bóng
# Draw left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_LENGTH)
left_pad.penup()
left_pad.goto(-400, 0)

# Draw right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_LENGTH)
right_pad.penup()
right_pad.goto(400, 0)

# Draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)


def move_ball():
    """Calculate and update ball position based on angle and speed"""
    global x, y
    dx = speed * math.cos(math.radians(angle)) * direction
    dy = speed * math.sin(math.radians(angle)) * direction
    x = int(x + dx)
    y = int(y + dy)
    ball.setx(x)
    ball.sety(y)

def paddle_up():
    left_pad.sety(left_pad.ycor() + PADDLE_STEP)


def paddle_down():
    left_pad.sety(left_pad.ycor() - PADDLE_STEP)


def move_paddle(paddle, target_y):
    """Move paddle to specified y-coordinate"""
    paddle.sety(target_y)


def bounce_ball():
    """Bounce ball on top and bottom edges and update angle"""
    global angle, x, y
    if y > 280:
        y = 275
        angle = -angle
    if y < -280:
        y = -275
        angle = -angle


def detect_collision(paddle):
    # Detect collision between ball and paddle and update angle
    global angle, x, y, angle, store_ball_y, store_ball_angle
    if paddle == left_pad:
        if (-370 > ball.xcor() > -390) and (paddle.ycor() + 40 > ball.ycor() > paddle.ycor() - 40):
            # Modify angle based on paddle impact position
            angle = 180 - angle + y - paddle.ycor()

    if paddle == right_pad:
        if (370 < ball.xcor() < 390) and (paddle.ycor() + 40 > ball.ycor() > paddle.ycor() - 40):
            # Modify angle based on paddle impact position
            angle = 180 - angle - y + paddle.ycor()

    # Normalize angle
    while angle > 360:
        angle = angle - 360
    while angle < 0:
        angle = angle + 360


def reset_game():
    """Reset ball and paddles to starting positions"""
    global x, y, angle, direction, speed, store_ball_y, store_ball_angle, paddle_y, spacer
    x = 0
    y = 0
    angle = random.randint(-10, 10)
    speed = BALL_SPEED
    direction = -1
    paddle_y = 0

    spacer = ""
    for n in range(80):
        spacer += " "

    ball.goto(x, y)
    move_paddle(right_pad, 0)
    move_paddle(left_pad, 0)


# Initialize game to start
x, y, = 0, 0
store_ball_y, store_ball_angle, store_paddle_y = 0, 0, 0
score_human, score_ai = 0, 0

reset_game()

# get key press
sc.listen()
sc.onkeypress(paddle_up, "e")
sc.onkeypress(paddle_down, "x")

# show score
sketch.clear()
sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai),
             align="center", font=("helvetica", 24, "normal"))

# import the machine learning model
spline_model = load('spline_model.joblib')

while True:
   #  Main game loop
    sc.update()
    move_ball()
    bounce_ball()

# Phát hiện va chạm bóng với vợt trái
    if x < -370:
        detect_collision(left_pad)

        # move right paddle to predicted position
        prediction_paddle_y = spline_model.predict([[y, angle]])
        right_pad.sety(int(prediction_paddle_y) + random.randint(-5, 5))

    #  Detect ball collision with right paddle
    if x > 370:
        # Store right paddle vert pos
        detect_collision(right_pad)

    # Detect paddle missed ball
    if x < -500 or x > 500:

        if x > 500:
            score_human += 1
        else:
            score_ai += 1

        sketch.clear()
        sketch.write("HUMAN: " + str(score_human) + spacer + "AI: " + str(score_ai),
                     align="center", font=("helvetica", 24, "normal"))

        time.sleep(1)
        reset_game()
