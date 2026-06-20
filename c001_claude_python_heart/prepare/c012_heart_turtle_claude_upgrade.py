import turtle


screen = turtle.Screen()
screen.title("Claude Python Heart")
screen.bgcolor("#111827")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(5)
pen.color("#ff4f9a")
pen.fillcolor("#ff4f9a")

pen.begin_fill()

pen.left(140)
pen.forward(150)

for _ in range(200):
    pen.right(1)
    pen.forward(1.35)

pen.left(120)

for _ in range(200):
    pen.right(1)
    pen.forward(1.35)

pen.forward(150)

pen.end_fill()

pen.penup()
pen.goto(0, -90)
pen.color("white")
pen.write("Hello Claude", align="center", font=("Arial", 22, "bold"))

turtle.done()
