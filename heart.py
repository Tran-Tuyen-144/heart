import random
import math
import tkinter as tk
from tkinter import Canvas, Label

# ===================== CẤU HÌNH =====================
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#E599F7"   # Màu tím hồng nhẹ

# ===================== HÀM CƠ BẢN =====================
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    x = 16 * math.sin(t) ** 3
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    ratio_x = -beta * math.log(random.random())
    ratio_y = -beta * math.log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    return 2 * (2 * math.sin(4 * p)) / (2 * math.pi)

# ===================== CLASS TRÁI TIM =====================
class Heart:
    def __init__(self, generate_frame=40):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * math.pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        # Viền tim
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        # Trung tâm tim
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.52)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.uniform(-0.8, 0.8)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.uniform(-0.8, 0.8)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * math.pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * math.pi)))
        halo_number = int(2500 + 3500 * abs(curve(generate_frame / 10 * math.pi) ** 2))
        all_points = []

        # Vòng sáng
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * math.pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-12, 12)
                y += random.randint(-12, 12)
                size = random.choice((1, 2))
                all_points.append((x, y, size))

        # Viền tim
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # Vùng lan tỏa
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # Trung tâm
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)

# ===================== VẼ =====================
def draw(main, render_canvas, render_heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(120, draw, main, render_canvas, render_heart, render_frame + 1)  # chậm hơn cho mượt

# ===================== CHẠY =====================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("💗💞💗")
    center_window(root, CANVAS_WIDTH, CANVAS_HEIGHT)

    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()  

    heart = Heart()
    draw(root, canvas, heart)

    Label(root,
          text="💞",
          bg="black",
          fg="#E599F7",
          font=("Arial", 20, "bold")).place(relx=0.5, rely=0.9, anchor='center')

    root.mainloop()
