import itertools as it
from typing import Tuple


def draw_grid(input_canvas, width, height, spacing):
    """
    Creates gridlines on the canvas
    """
    central_x = int(width/2)
    central_y = int(height/2)

    for x in it.chain(range(spacing, central_x, spacing), range(central_x + spacing, width, spacing)):
        input_canvas.create_line(x, 0, x, height, fill="lightgray")

    for y in it.chain(range(spacing, central_y, spacing), range(central_y + spacing, width, spacing)):
        input_canvas.create_line(0, y, width, y, fill="lightgray")

    input_canvas.create_line(central_x, 0, central_x, height, fill="black")
    input_canvas.create_line(0, central_y, width, central_y, fill="black")

def get_coordinates(x, y, width, height, spacing) -> Tuple[float, float]:
    """
    Returns coordinates based on X and Y location
    """
    return (x - (width/2)) / spacing, (y - (height/2)) / spacing

def show_coordinates(input_canvas):
    """
    Shows coordinates at the tip of the cursor
    """
    def show_coordinates_inner(event, width=880, height=880, spacing=40):
        x, y = event.x, event.y
        x_coord, y_coord = get_coordinates(x, y, width, height, spacing)
        input_canvas.delete("cursor_text")
        input_canvas.create_text(x - 15, y - 15, text=f"({round(x_coord, 3)}, {round(y_coord, 3)})", fill="red", font=("Arial", 8), tag="cursor_text")
    return show_coordinates_inner