import turtle
import tkinter as tk

ttl = turtle.Turtle()


def draw_logo():
    ttl.reset()
    ttl.speed(8)
    ttl.pensize(6)
    ttl.color("cyan")

    # Setup screen
    displaay = turtle.Screen()
    displaay.screensize(canvwidth=900, canvheight=800)
    displaay.bgcolor("black")
    displaay.title("MB Logo - MixBhia")

    # Draw M
    ttl.penup()
    ttl.goto(-200, 100)
    ttl.pendown()
    ttl.setheading(-90)  # face down
    ttl.forward(150)
    ttl.backward(150)
    ttl.setheading(-45)
    ttl.forward(100)
    ttl.setheading(45)
    ttl.forward(100)
    ttl.setheading(-90)
    ttl.forward(150)

    # Draw B
    ttl.penup()
    ttl.goto(50, 100)
    ttl.pendown()
    ttl.setheading(-90)
    ttl.forward(150)
    ttl.backward(150)
    ttl.setheading(0)
    ttl.circle(-40, 180)  # top loop
    ttl.setheading(0)
    ttl.circle(-40, 180)  # bottom loop

    # Write "MixBhia" under MB
    ttl.penup()
    ttl.goto(-120, -100)
    ttl.color("gold")
    ttl.pendown()
    ttl.write("MixBhia", font=("consolas", 32, "bold"))

    button1.config(state=tk.DISABLED)


def draw_virus():
    n = 200
    ttl.speed(7)
    ttl.color("maroon")
    while n > 0:
        ttl.forward(n)
        ttl.left(n)
        n -= 1
    button2.config(state=tk.DISABLED)


if __name__ == "__main__":
    screen = turtle.Screen()
    screen.title("GUI+Turtle")
    screen.bgcolor("black")
    canvas = screen.getcanvas()

    button1 = tk.Button(
        canvas.master,
        text="Click to draw my LOGO :)".upper(),
        font=("consolas", 10, "bold"),
        bg="yellow",
        fg="blue",
        command=draw_logo,
    )
    button1.pack(side=tk.LEFT)

    button2 = tk.Button(
        canvas.master,
        text="Click to draw a virus :)".upper(),
        font=("consolas", 10, "bold"),
        bg="yellow",
        fg="blue",
        command=draw_virus,
    )
    button2.pack(side=tk.RIGHT)

    headline = tk.Label(
        text="What Do You want to Draw ?".upper(),
        font=("consolas", 12, "bold"),
        fg="cyan",
        bg="black",
    )
    headline.pack(side=tk.BOTTOM)

    turtle.done()

