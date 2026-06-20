import turtle


pen = turtle.Turtle()
pen.speed(3)
pen.color("red")

pen.begin_fill()

pen.left(140)
pen.forward(120)

for _ in range(200):
    pen.right(1)
    pen.forward(1)

pen.left(120)

for _ in range(200):
    pen.right(1)
    pen.forward(1)

pen.forward(120)

pen.end_fill()

turtle.done()
