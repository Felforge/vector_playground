import tkinter as tk
from create_canvas import draw_grid, show_coordinates

WIDTH = 880
HEIGHT = 880
GRID_SPACING = 40

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Grid Coordinate System")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    draw_grid(canvas, WIDTH, HEIGHT, GRID_SPACING)
    
    canvas.bind("<Motion>", show_coordinates(canvas))
    
    root.mainloop()
