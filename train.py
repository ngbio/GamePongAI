import turtle
import math
import random
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 4
PADDLE_LENGTH = 1
PADDLE_SPEED = 20
BALL_SPEED = 20

# Initialize screen
sc = turtle.Screen()
sc.title("Pong-AI Training")
sc.bgcolor("black")
sc.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 240)

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

            # Store ball vert position and angle to save into dataset
            store_ball_y = y
            store_ball_angle = angle

    if paddle == right_pad:
        if (370 < ball.xcor() < 390) and (paddle.ycor() + 40 > ball.ycor() > paddle.ycor() - 40):
            # Modify angle based on paddle impact position
            angle = 180 - angle - y + paddle.ycor()

    # Normalize angle
    while angle > 360:
        angle = angle - 360
    while angle < 0:
        angle = angle + 360


def record_data(store_ball_y, store_ball_angle, paddle_y):
    """Store ball and paddle data in dataset csv file"""
    string = str(store_ball_y) + ',' + str(store_ball_angle) + ',' + str(paddle_y) + '\n'
    print(string)
    f = open('dataset.csv', 'a+')
    if os.stat('dataset.csv').st_size == 0:
        f.write('ball_y,ball_angle,paddle_y\n')
    f.write(string)
    f.close()


def reset_game():
    """Reset ball and paddles to starting positions"""
    global x, y, angle, direction, speed, store_ball_y, store_ball_angle, paddle_y
    x = 0
    y = 0
    angle = random.randint(-30, 30)
    speed = BALL_SPEED
    direction = -1
    store_ball_y = 0
    store_ball_angle = 0
    paddle_y = 0

    ball.goto(x, y)
    move_paddle(right_pad, 0)
    move_paddle(left_pad, 0)


# Initialize game to start
x, y = 0, 0
store_ball_y, store_ball_angle, store_paddle_y = 0, 0, 0
reset_game()
while True:
   #  Main game loop
    move_ball()
    bounce_ball()

    #  Automatic move left paddle
    move_paddle(left_pad, y + random.randint(-40, 40))

    #  Automatic move right paddle
    move_paddle(right_pad, y + random.randint(-40, 40))

    #  Detect ball collision with left paddle
    if x < -370:
        detect_collision(left_pad)

    #  Detect ball collision with right paddle
    if x > 370:
        # Store right paddle vert pos
        detect_collision(right_pad)

        store_paddle_y = right_pad.ycor()

        # Save ball and paddle data in dataset csv file
        if 'store_ball_y' in vars() and 'store_ball_angle' in vars():
            record_data(store_ball_y, store_ball_angle, store_paddle_y)

    # Detect paddle missed ball
    if x < -500 or x > 500:
        reset_game()
