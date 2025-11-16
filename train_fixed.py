import turtle
import math
import random
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 4
PADDLE_LENGTH = 1
BALL_SPEED = 20
PADDLE_RANDOM_OFFSET = 20  # +/- y offset cho đa dạng

# Initialize screen
sc = turtle.Screen()
sc.title("Pong-AI Training")
sc.bgcolor("black")
sc.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Draw left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=1)
left_pad.penup()
left_pad.goto(-400, 0)

# Draw right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=1)
right_pad.penup()
right_pad.goto(400, 0)

# Draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)

# Global variables
x, y = 0, 0
angle = 0
direction = -1
speed = BALL_SPEED
store_ball_y, store_ball_angle, store_paddle_y = 0, 0, 0
has_record = False

#hàm chuẩn hóa góc để trả về góc chuẩn
def normalize_angle(a):
    while a > 360:
        a -= 360
    while a < 0:
        a += 360
    return a

def move_ball(): #tính duy chuyển bong qua mỗi fram
    global x, y
    dx = speed * math.cos(math.radians(angle)) * direction
    dy = speed * math.sin(math.radians(angle)) * direction
    x = int(x + dx)
    y = int(y + dy)
    ball.setx(x)
    ball.sety(y)

def move_paddle(paddle, target_y):
    # Thêm random nhỏ để dữ liệu đa dạng
    offset = random.randint(-PADDLE_RANDOM_OFFSET, PADDLE_RANDOM_OFFSET)
    paddle.sety(max(min(target_y + offset, SCREEN_HEIGHT//2 - 40), -SCREEN_HEIGHT//2 + 40))

def bounce_ball(): #va cham rìa trên dưới thì bật ngươc
    global angle, y
    if y > 280:
        y = 275
        angle = -angle
    if y < -280:
        y = -275
        angle = -angle

def detect_collision(paddle):
    global angle, store_ball_y, store_ball_angle
    collided = False#mặc định chưa có va chạm
    if paddle == left_pad:#khi va chạm trái
        if (-390 < ball.xcor() < -370) and (paddle.ycor() + 40 > ball.ycor() > paddle.ycor() - 40):
            angle = 180 - angle + y - paddle.ycor() #công thức phản xa
            angle = normalize_angle(angle)
            store_ball_y = y
            store_ball_angle = angle
            collided = True
    if paddle == right_pad:#khi va chạm phải
        if (370 < ball.xcor() < 390) and (paddle.ycor() + 40 > ball.ycor() > paddle.ycor() - 40):
            angle = 180 - angle - y + paddle.ycor()
            angle = normalize_angle(angle)
            collided = True
    return collided

# Ghi dữ liệu
def record_data(ball_y, ball_angle, paddle_y):
    string = f"{ball_y},{ball_angle},{paddle_y}\n"
    with open('dataset1.csv', 'a') as f:
        if os.stat('dataset1.csv').st_size == 0:
            f.write("ball_y,ball_angle,paddle_y\n")
        f.write(string)
    print(string)


def reset_game():
    global x, y, angle, direction, speed, has_record
    x, y = 0, 0
    angle = random.randint(-30, 30)
    speed = BALL_SPEED
    direction = -1
    has_record = False # cho phép ghi lại 1 luot mới để them vô data
    ball.goto(x, y)
    #di chuyen về trung tâm
    left_pad.sety(0)
    right_pad.sety(0)


# game loop
def game_loop():
    global store_paddle_y, has_record

    move_ball()
    bounce_ball()

    # Paddle di chuyển theo bóng
    move_paddle(left_pad, y)
    move_paddle(right_pad, y)

    # Va chạm paddle trái
    if x < -370:
        if detect_collision(left_pad):
            has_record = False

    # Va chạm paddle phải
    if x > 370:
        if detect_collision(right_pad) and not has_record:
            store_paddle_y = right_pad.ycor()
            record_data(store_ball_y, store_ball_angle, store_paddle_y)
            has_record = True

    # Một bên đã thua
    if x < -500 or x > 500:
        reset_game()

    sc.update()
    sc.ontimer(game_loop, 20)

# Main
reset_game()
game_loop()
turtle.done()
