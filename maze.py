# a simple maze game 
import turtle
import math
import random
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Game")
wn.setup(700, 700)
wn.tracer(0)

#register images

turtle.register_shape("/Users/gusluberadzki/Documents/hero_left.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/hero_right.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/mazewall.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/moneycoin.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/hero_down.gif")
turtle.register_shape("/Users/gusluberadzki/Documents/hero_up.gif")



##create pen
class Pen(turtle.Turtle):
   def __init__(self):
      turtle.Turtle.__init__(self)
      self.shape("square")
      self.color("white")
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
        self.shape("/Users/gusluberadzki/Documents/hero_up.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        self.shape("/Users/gusluberadzki/Documents/hero_down.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape("/Users/gusluberadzki/Documents/hero_left.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape("/Users/gusluberadzki/Documents/hero_right.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        


    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2) )
        if distance < 5:
            return True
        else:
            return False 
    def destroy(self):
            self.goto(500,500)
            self.hideturtle()


class Treasure(turtle.Turtle):
    def __init__(self,x, y):
        turtle.Turtle.__init__(self)
        self.shape("/Users/gusluberadzki/Documents/moneycoin.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.direction = random.choice(["up","down","left","right"])

    def is_close(self,other):
        a = self.xcor()- other.xcor()
        b = self.ycor()- other.ycor()
        distance = math.sqrt ((a ** 2)+(b ** 2) )

        if distance < 100:
            return True
        else:
            return False


    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx=0
            dy=-24
        elif self.direction == "left":
            dx=-24
            dy=0
        elif self.direction == "right":
            dx=24
            dy=0
        else:
            dx=0
            dy=0

        #calculate the spot to move on
        move_to_x=self.xcor() + dx
        move_to_y=self.ycor() + dy

        #check if the space has a wall
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        else:
            self.direction = random.choice(["up","down","left","right"])
        turtle.ontimer(self.move,t=random.randint(100,300))

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()



#levels list
levels = [""]

#Define first level
level_1=[
"xxxxxxxxxxxxxxxxxxxxxxxxx",
"x p   xxxxxe    xxxxxxxxx",
"xxxxx xxxxx xxx xxxxxxxxx",
"x     x     xxx xxxxxxxxx",
"x xxxxxxxxx xxxxxxxxxxxxx",
"x xxxxxe    xxxxx     xxx",
"x xxxxx xxx xxxxx xxx xxx",
"x       xxx       xxx xxx",
"xxxxxxx xxxxxxxxxexxx xxx",
"xxxxxxx  e    t        xx",
"xxxxxxxxxxxxxxxxx xxxxxxx",
"xxx     xxxxxe    xxxxxxx",
"xxx xxx xxxxx xxx xxxxxxx",
"xxx xxx       xxx     xxx",
"xxx xxxxxxxxxxxxxxxxx xxx",
"xxx     xxxxx       t xxx",
"xxxxx x xxxxx xxxxxxxxxxx",
"xxxxx x   t   xxxxxxxxxxx",
"xxxxxexxxxxxxxx xxx     x",
"xxxxx xxxxxxxxx xxx xxx x",
"x   t       xxx     xxx x",
"x xxxxxxxxx xxxexxxxxxxxx",
"x xxxxxxxxx xxx xxxxxxxxx",
"x      t               xx",
"xxxxxxxxxxxxxxxxxxxxxxxxx"
]

#add a treasure list
treasures = []

#add a enemy list
enemies =[]

#add a level list
levels.append(level_1)

#create pen and player instances
pen = Pen()
player = Player()

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
                pen.shape("/Users/gusluberadzki/Documents/mazewall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            #check is p is representing player
            if character == "p":
                player.goto(screen_x, screen_y)

            #check if it is a t representing treasure
            if character == "t":
                treasures.append(Treasure(screen_x, screen_y))



#set up the level


#add enemies to the level
for y in range(len(level_1)):
    for x in range(len(level_1[y])):
        character = level_1[y][x]
        screen_x = -288 + (x * 24)
        screen_y = 288 - (y * 24)
        if character == "e":
            enemies.append(Enemy(screen_x, screen_y))

#set up the level
setup_maze(levels[1])

def reset_game():
    global player, treasures, enemies, walls
    player.gold = 0
    player.goto(-288 + (1 * 24), 288 - (1 * 24))
    for treasure in treasures:
        treasure.destroy()
    for enemy in enemies:
        enemy.destroy()
    treasures.clear()
    enemies.clear()
    walls.clear()
    setup_maze(levels[1])
    start_enemies()

def start_enemies():
    for enemy in enemies:
        enemy.move()

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


#start enemy movement
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

#turn off screen updates
#wn.tracer(0)

#start enemy movement
#turn off screen updates
#wn.tracer(0)



#main game loop
while True:
     for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print("Player Gold: {}".format(player.gold))
            treasure.destroy()
            treasures.remove(treasure)


        for enemy in enemies:
            if player.is_collision(enemy):
                print("Player dies!")
                
        
        #move enemies each frame
        for enemy in enemies:
            enemy.move()

    #update screen
     wn.update()
