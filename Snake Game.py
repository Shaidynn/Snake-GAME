import random
import turtle
import time

class Square:
    def __init__(self, x, y, color="black"):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, turtle):
        turtle.goto(self.x - 9, self.y - 9)
        turtle.begin_fill()
        turtle.fillcolor(self.color)
        for _ in range(4):
            turtle.forward(18)
            turtle.left(90)
        turtle.end_fill()

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "ON"

    def change_location(self):
        self.x = random.randint(0, 20) * 20 - 200
        self.y = random.randint(0, 20) * 20 - 200

    def draw(self, turtle):
        if self.state == "ON":
            turtle.goto(self.x - 9, self.y - 9)
            turtle.begin_fill()
            for _ in range(4):
                turtle.forward(18)
                turtle.left(90)
            turtle.end_fill()

    def change_state(self):
        self.state = "OFF" if self.state == "ON" else "ON"

class Snake:
    def __init__(self):
        self.head_position = [20, 0]
        self.body = [Square(-20, 0, "green"), Square(0, 0, "green"), Square(20, 0, "green")]
        self.next_x = 1
        self.next_y = 0
        self.crashed = False
        self.next_position = [self.head_position[0] + 20 * self.next_x,
                              self.head_position[1] + 20 * self.next_y]

    def move_one_step(self):
        if Square(self.next_position[0], self.next_position[1]) not in self.body:
            self.body.append(Square(self.next_position[0], self.next_position[1], "green"))
            del self.body[0]
            self.head_position[0], self.head_position[1] = self.body[-1].x, self.body[-1].y
            self.next_position = [self.head_position[0] + 20 * self.next_x,
                                  self.head_position[1] + 20 * self.next_y]
        else:
            self.crashed = True

    def move_up(self):
        if self.next_y != -1:  # Prevent the snake from reversing direction
            self.next_x = 0
            self.next_y = 1

    def move_left(self):
        if self.next_x != 1:
            self.next_x = -1
            self.next_y = 0

    def move_right(self):
        if self.next_x != -1:
            self.next_x = 1
            self.next_y = 0

    def move_down(self):
        if self.next_y != 1:
            self.next_x = 0
            self.next_y = -1

    def eat_food(self):
        self.body.append(Square(self.next_position[0], self.next_position[1], "green"))
        self.head_position[0], self.head_position[1] = self.body[-1].x, self.body[-1].y
        self.next_position = [self.head_position[0] + 20 * self.next_x,
                              self.head_position[1] + 20 * self.next_y]

    def draw(self, turtle):
        for segment in self.body:
            segment.draw(turtle)

class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.artist = turtle.Turtle()
        self.artist.up()
        self.artist.hideturtle()
        self.snake = Snake()
        self.food = Food(100, 0)
        self.counter = 0
        self.command_pending = False
        self.score = 0
        self.game_over = False

    def next_frame(self):
        while not self.game_over:
            self.screen.listen()
            self.screen.onkey(self.snake.move_down, "Down")
            self.screen.onkey(self.snake.move_up, "Up")
            self.screen.onkey(self.snake.move_left, "Left")
            self.screen.onkey(self.snake.move_right, "Right")
            turtle.tracer(0)
            self.artist.clear()

            if self.counter == 5:
                if (self.snake.next_position[0], self.snake.next_position[1]) == (self.food.x, self.food.y):
                    self.snake.eat_food()
                    self.food.change_location()
                    self.score += 1
                else:
                    self.snake.move_one_step()
                self.counter = 0
            else:
                self.counter += 1

            self.food.change_state()
            self.food.draw(self.artist)
            self.snake.draw(self.artist)
            turtle.update()

            self.command_pending = False
            time.sleep(0.05)

        self.show_game_over()

    def show_game_over(self):
        self.artist.goto(0, 0)
        self.artist.write("Game Over", align="center", font=("Arial", 24, "bold"))

    def quit_game(self):
        self.game_over = True

    def increase_speed(self):
        # Increase the speed of the game
        self.counter -= 1

game = Game()
game.next_frame()
turtle.done()
