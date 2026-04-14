# a simple maze game 
import turtle
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Game")
wn.setup(700, 700)

#register images
turtle.register_shape("/Users/gusluberadzki/Documents/hero_left.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/hero_right.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/mazewall.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/moneycoin.gif")



#CReate turtle Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")# reminder to change to a wall graphic (gif)
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("/Users/gusluberadzki/Documents/hero_right.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0


    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        self.shape("/Users/gusluberadzki/Documents/hero_left.gif")
        

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        self.shape("/Users/gusluberadzki/Documents/hero_right.gif")
        


    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2) )

        if distance < 5:
            return True
        else:
            return False 


class Treasure(turtle.Turtle):
    def __init__(self,x, y):
        turtle.Turtle.__init__(self)
class Treasure(turtle.Turtle):
    def __init__(self,x, y):
        turtle.Turtle.__init__(self)
        self.shape("/Users/gusluberadzki/Documents/moneycoin.gif")
        self.color("gold")
        self.goto(x, y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()


#levels list
levels = [""]

#Define first level
level_1=[
"xxxxxxxxxxxxxxxxxxxxxxxxx",
"x p   xxxxx     xxxxxxxxx",
"xxxxx xxxxx xxx xxxxxxxxx",
"x     x     xxx xxxxxxxxx",
"x xxxxxxxxx xxxxxxxxxxxxx",
"x xxxxx     xxxxx     xxx",
"x xxxxx xxx xxxxx xxx xxx",
"x       xxx       xxx xxx",
"xxxxxxx xxxxxxxxx xxx xxx",
"xxxxxxx       t        xx",
"xxxxxxxxxxxxxxxxx xxxxxxx",
"xxx     xxxxx     xxxxxxx",
"xxx xxx xxxxx xxx xxxxxxx",
"xxx xxx       xxx     xxx",
"xxx xxxxxxxxxxxxxxxxx xxx",
"xxx     xxxxx       t xxx",
"xxxxx x xxxxx xxxxxxxxxxx",
"xxxxx x   t   xxxxxxxxxxx",
"xxxxx xxxxxxxxx xxx     x",
"xxxxx xxxxxxxxx xxx xxx x",
"x   t       xxx     xxx x",
"x xxxxxxxxx xxx xxxxxxxxx",
"x xxxxxxxxx xxx xxxxxxxxx",
"x      t              xx",
"xxxxxxxxxxxxxxxxxxxxxxxxx"
]

#add a treasure list
treasures = []

levels.append(level_1)




#create level setup list
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            #check if x is representing a wall
            if character == "x":
                pen.goto(screen_x, screen_y)
            #check if x is representing a wall
            if character == "x":
                pen.goto(screen_x, screen_y)
                pen.shape("/Users/gusluberadzki/Documents/mazewall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))
                player.goto(screen_x, screen_y)

            #check if it is a t representing treasure
            if character == "t":
                treasures.append(Treasure(screen_x, screen_y))
                
           

#create class instances
pen = Pen()
player = Player()

#create wall coords list
walls = []


#set up the level
setup_maze(levels[1])


#Keyboard bindings
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

turtle.onkey(player.go_left,"a")
turtle.onkey(player.go_right,"d")
turtle.onkey(player.go_up,"w")
turtle.onkey(player.go_down,"s")

#turn off screen updates
wn.tracer(0)

#main game loop
while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print("Player Gold: {}".format(player.gold))
            treasure.destroy()
            treasures.remove(treasure)

    #update screen
    wn.update()
    
