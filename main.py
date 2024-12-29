import tkinter as tk
import itertools as it
from typing import Tuple

WIDTH = 880
HEIGHT = 880
GRID_SPACING = 40

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
    def show_coordinated_inner(event, width=WIDTH, height=HEIGHT, spacing=GRID_SPACING):
        x, y = event.x, event.y
        x_coord, y_coord = get_coordinates(x, y, width, height, spacing)
        input_canvas.delete("cursor_text")
        input_canvas.create_text(x - 15, y - 15, text=f"({round(x_coord, 3)}, {round(y_coord, 3)})",
                                 fill="red", font=("Arial", 8), tag="cursor_text")
    return show_coordinated_inner

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grid Coordinate System")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    canvas.bind("<Motion>", show_coordinates(canvas))

    draw_grid(canvas, WIDTH, HEIGHT, GRID_SPACING)
    root.mainloop()
