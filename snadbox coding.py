import turtle

turtle.setup (700,700)
sandbox=turtle.Screen()


sandbox.title("Gustaw´s Turtle Sandbox")
sandbox.bgcolor("midnightblue")

Jerry=turtle.Turtle()
Jerry.pencolor("darkmagenta")
Jerry.pensize(4)

#functions
def key1():
    Jerry.setheading(90)
    Jerry.forward(30)
#functions
def key2():
    Jerry.setheading(180)
    Jerry.forward(30)
#functions
def key3():
    Jerry.setheading(270)
    Jerry.forward(30)
#functions
def key4():
    Jerry.setheading(0)
    Jerry.forward(30)
#functions
def key5():
    Jerry.penup

#functions
def key6():
    Jerry.pendown()






#Keyboard Controls
sandbox.onkey(key1,"w")


#Keyboard Controls
sandbox.onkey(key2,"a")


#Keyboard Controls
sandbox.onkey(key3,"s")


#Keyboard Controls
sandbox.onkey(key4,"d")


#Keyboard Controls
sandbox.onkey(key5,"Up")


#Keyboard Controls
sandbox.onkey(key6,"Down")


sandbox.listen()
