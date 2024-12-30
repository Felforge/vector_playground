import math
import tkinter as tk
from create_canvas import get_coordinates

class Vector:
    """
    Create vectors in tkinter
    """
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.vectors = []
        self.selected_vector = None
        self.resultant_line = None
        self.resultant_arrow = None
        self.resultant_label = None
        self.delete_button = tk.Button(root, text="X", command=self.delete_vector)
        self.delete_button.place_forget()
        
        canvas.bind("<Button-1>", self.on_click())
        canvas.bind("<B1-Motion>", self.on_drag())
        canvas.bind("<ButtonRelease-1>", self.on_release())

    def on_click(self, node_color="RoyalBlue2"):
        """
        Handle mouse clicks for creating vector or selecting a node
        """
        def on_click_inner(event):
            for vector in self.vectors:
                if self.is_inside_node(event.x, event.y, vector["start_node"]):
                    self.selected_vector = vector
                    self.show_delete_button(vector["start_node"])
                    return
                elif self.is_inside_node(event.x, event.y, vector["end_node"]):
                    self.selected_vector = vector
                    self.show_delete_button(vector["end_node"])
                    return

            self.selected_vector = None
            self.hide_delete_button()

            start_node = self.create_node(event.x, event.y, color=node_color)
            vector = {
                "start_node": start_node,
                "end_node": None,
                "line": None,
                "arrow": None,
                "start_label": None,
                "end_label": None
            }
            self.vectors.append(vector)
        return on_click_inner

    def on_drag(self, line_color="SteelBlue3"):
        """
        Handle mouse drag
        """
        def on_drag_inner(event):
            if self.selected_vector is None:
                vector = self.vectors[-1]
                if vector["end_node"] is None:
                    x, y = self.get_node_center(vector["start_node"])
                    if vector["line"]:
                        self.canvas.delete(vector["line"])
                    vector["line"] = self.canvas.create_line(x, y, event.x, event.y, fill=line_color, dash=(4, 2))
            else:
                if self.is_inside_node(event.x, event.y, self.selected_vector["start_node"]):
                    self.update_node(self.selected_vector["start_node"], event.x, event.y)
                elif self.is_inside_node(event.x, event.y, self.selected_vector["end_node"]):
                    self.update_node(self.selected_vector["end_node"], event.x, event.y)
                self.update_vector_display(self.selected_vector)
        return on_drag_inner

    def on_release(self, line_color="SteelBlue3", node_color="RoyalBlue2"):
        """
        Finalize vector/release node
        """
        def on_release_inner(event):
            if self.selected_vector is None:
                vector = self.vectors[-1]
                if vector["end_node"] is None:
                    vector["end_node"] = self.create_node(event.x, event.y, color=node_color)

                    x, y = self.get_node_center(vector["start_node"])

                    if vector["line"]:
                        self.canvas.delete(vector["line"])

                    vector["line"] = self.canvas.create_line(x, y, event.x, event.y, fill=line_color, width=2)
                    vector["arrow"] = self.create_arrowhead(x, y, event.x, event.y)
                    vector["start_label"] = self.create_node_label(vector["start_node"])
                    vector["end_label"] = self.create_node_label(vector["end_node"])
            self.update_resultant()
        return on_release_inner

    def update_vector_display(self, vector):
        """
        Update vector display in real time
        """
        x1, y1 = self.get_node_center(vector["start_node"])
        x2, y2 = self.get_node_center(vector["end_node"])
        self.canvas.coords(vector["line"], x1, y1, x2, y2)

        self.canvas.delete(vector["arrow"])
        vector["arrow"] = self.create_arrowhead(x1, y1, x2, y2)

        self.canvas.coords(vector["start_label"], x1 + 10, y1 - 10)
        self.canvas.coords(vector["end_label"], x2 + 10, y2 - 10)

        conv_x1, conv_y1 = get_coordinates(x1, y1)
        self.canvas.itemconfig(vector["start_label"], text=f"({round(conv_x1, 3)}, {round(conv_y1, 3)})")

        conv_x2, conv_y2 = get_coordinates(x2, y2)
        self.canvas.itemconfig(vector["end_label"], text=f"({round(conv_x2, 3)}, {round(conv_y2, 3)})")

    def delete_vector(self):
        """
        Delete selected vector
        """
        if self.selected_vector:
            for obj in self.selected_vector.values():
                self.canvas.delete(obj)
            self.vectors.remove(self.selected_vector)
            self.selected_vector = None
            self.hide_delete_button()
            self.update_resultant()

    def create_node(self, x, y, color):
        """
        Create a draggable node
        """
        return self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)

    def update_node(self, node, x, y):
        """
        Update a node's position
        """
        self.canvas.coords(node, x - 5, y - 5, x + 5, y + 5)

    def is_inside_node(self, x, y, node):
        """
        Check if input is inside node
        """
        coords = self.canvas.coords(node)
        return coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]

    def get_node_center(self, node):
        """
        Get center coordinates of node
        """
        coords = self.canvas.coords(node)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def show_delete_button(self, node):
        """
        Display delete button for vector
        """
        x, y = self.get_node_center(node)
        self.delete_button.place(x=x+15, y=y+15)

    def hide_delete_button(self):
        """
        Hide delete button
        """
        self.delete_button.place_forget()

    def create_arrowhead(self, vx1, vy1, vx2, vy2, length=10, arrow_angle=math.pi/6, color="SteelBlue3"):
        """
        Create arrowhead at the end of vector
        """
        angle = math.atan2(vy2 - vy1, vx2 - vx1)
        x1 = vx2 - length * math.cos(angle - arrow_angle)
        y1 = vy2 - length * math.sin(angle - arrow_angle)
        x2 = vx2 - length * math.cos(angle + arrow_angle)
        y2 = vy2 - length * math.sin(angle + arrow_angle)
        return self.canvas.create_line(vx2, vy2, x1, y1, vx2, vy2, x2, y2, fill=color, width=2)

    def create_node_label(self, node):
        """
        Display coordinates of node
        """
        x, y = self.get_node_center(node)
        conv_x, conv_y = get_coordinates(x, y)
        return self.canvas.create_text(x+10, y-10, text=f"({round(conv_x, 3)}, {round(conv_y, 3)})", font=("Arial", 8), fill="RoyalBlue2")

    def update_resultant(self, origin_x=440, origin_y = 440, color="DarkOrchid3"):
        """
        Calculate and draw the resultant vector from the origin
        """
        sum_x = origin_x
        sum_y = origin_y

        for vector in self.vectors:
            if vector["start_node"] and vector["end_node"]:
                x1, y1 = self.get_node_center(vector["start_node"])
                x2, y2 = self.get_node_center(vector["end_node"])
                sum_x += x2 - x1
                sum_y += y2 - y1

        if self.resultant_line:
            self.canvas.delete(self.resultant_line)
        if self.resultant_arrow:
            self.canvas.delete(self.resultant_arrow)
        if self.resultant_label:
            self.canvas.delete(self.resultant_label)

        if len(self.vectors) != 0:
            self.resultant_line = self.canvas.create_line(origin_x, origin_y, sum_x, sum_y, fill=color)
            self.resultant_arrow = self.create_arrowhead(origin_x, origin_y, sum_x, sum_y, color=color)
            conv_x, conv_y = get_coordinates(sum_x, sum_y)
            self.resultant_label = self.canvas.create_text(sum_x + 10, sum_y - 10, text=f"({round(conv_x, 3)}, {round(conv_y, 3)})", fill=color, font=("Arial", 10))
