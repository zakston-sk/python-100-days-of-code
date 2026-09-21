"""Hirst-style dot painting (Day 18).

Extracts a colour palette from an image with colorgram.py
and draws a grid of coloured dots using turtle graphics.
"""

import random
import turtle

import colorgram

IMAGE_PATH = "image.jpg"
NUM_COLORS = 30
ROWS = 10
DOTS_PER_ROW = 10
DOT_SIZE = 20
SPACING = 50
START_OFFSET = 300


def extract_palette(image_path, num_colors):
    """Return a list of RGB tuples extracted from the image."""
    colors = colorgram.extract(image_path, num_colors)
    return [(c.rgb.r, c.rgb.g, c.rgb.b) for c in colors]


def draw_dot_row(pen, dots_per_row, dot_size, spacing, palette):
    """Draw one horizontal row of coloured dots."""
    for _ in range(dots_per_row):
        pen.dot(dot_size, random.choice(palette))
        pen.forward(spacing)


def draw_hirst_painting(pen, palette, rows, dots_per_row, dot_size, spacing):
    """Draw a grid of coloured dots inspired by Damien Hirst."""
    for _ in range(rows):
        draw_dot_row(pen, dots_per_row, dot_size, spacing, palette)

        # Move to the start of the next row: left, then up.
        pen.setheading(180)
        pen.forward(spacing * dots_per_row)
        pen.setheading(90)
        pen.forward(spacing)
        pen.setheading(0)


def main():
    """Set up the canvas, extract the palette, and draw the painting."""
    palette = extract_palette(IMAGE_PATH, NUM_COLORS)

    turtle.colormode(255)

    screen = turtle.Screen()
    screen.title("Hirst Painting — Day 18")

    pen = turtle.Turtle()
    pen.speed("fastest")
    pen.penup()
    pen.hideturtle()

    # Move the pen to the bottom-left corner of the future grid.
    pen.setheading(225)
    pen.forward(START_OFFSET)
    pen.setheading(0)

    draw_hirst_painting(pen, palette, ROWS, DOTS_PER_ROW, DOT_SIZE, SPACING)

    screen.mainloop()


if __name__ == "__main__":
    main()
