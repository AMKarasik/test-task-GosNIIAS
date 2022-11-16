from PIL import Image, ImageDraw
import random
import numpy as np          


class Rectangle:
    """
        Rectangle generation class:
        create_rec: gives coordinates of rectangle,
                    height, width and coordinates of top-left angle of surrounding rectangle
        image_gen: generates, saves and show our rectangle
    """
    def __init__(self, gen, bound):
        self.coords_gen = gen
        self.coords_bound = bound
        self.save = None
        self.background = None
        self.create_rect()
        self.image_gen()

    def create_rect(self):
        w = np.random.randint(150, 250)  # rectangle width
        h = np.random.randint(150, 250)  # rectangle height
        angle = random.randint(0, 89) * 3.14159 / 180  # rotation angle

        h1 = (h * np.cos(angle))
        h2 = (w * np.sin(angle))
        hhh = h1 + h2  # surrounding rectangle height
        w1 = (h * np.sin(angle))
        w2 = (w * np.cos(angle))
        www = w1 + w2  # surrounding rectangle width

        x0, y0 = (np.random.randint(www/2, 640-www/2), np.random.randint(hhh/2, 480-hhh/2))  # center

        # surrounding angle coordinates
        xb1yb1, xb2yb2, xb3yb3, xb4yb4 = ((x0 - www/2, y0 - hhh/2),
                                          (x0 - www/2, y0 + hhh/2),
                                          (x0 + www/2, y0 + hhh/2),
                                          (x0 + www/2, y0 - hhh/2))

        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        # angle coordinates
        x01y01 = (x0 + (x0 - w / 2 - x0) * rotation_matrix[0][0] + (y0 - h / 2 - y0) * rotation_matrix[0][1],
                  y0 + (x0 - w / 2 - x0) * rotation_matrix[1][0] + (y0 - h / 2 - y0) * rotation_matrix[1][1])
        x02y02 = (x0 + (x0 + w / 2 - x0) * rotation_matrix[0][0] + (y0 - h / 2 - y0) * rotation_matrix[0][1],
                  y0 + (x0 + w / 2 - x0) * rotation_matrix[1][0] + (y0 - h / 2 - y0) * rotation_matrix[1][1])
        x03y03 = (x0 + (x0 + w / 2 - x0) * rotation_matrix[0][0] + (y0 + h / 2 - y0) * rotation_matrix[0][1],
                  y0 + (x0 + w / 2 - x0) * rotation_matrix[1][0] + (y0 + h / 2 - y0) * rotation_matrix[1][1])
        x04y04 = (x0 + (x0 - w / 2 - x0) * rotation_matrix[0][0] + (y0 + h / 2 - y0) * rotation_matrix[0][1],
                  y0 + (x0 - w / 2 - x0) * rotation_matrix[1][0] + (y0 + h / 2 - y0) * rotation_matrix[1][1])

        self.coords_gen = (x01y01, x02y02, x03y03, x04y04)
        self.coords_bound = xb2yb2, www, hhh

    def image_gen(self):
        # background with random color
        background = Image.new('RGB', (640, 480), (random.randint(0, 255),
                                                   random.randint(0, 255),
                                                   random.randint(0, 255)))
        rectangle = ImageDraw.Draw(background)
        # rectangle with random color
        rectangle.polygon(self.coords_gen, (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255)))
        background.show()
        name = 'rect_pics_gen/15.png'
        background.save(name, 'png')


if __name__ == "__main__":
    data = open('data.txt', 'w')  # shape data file
    for i in range(0, 1):
        rect = Rectangle(None, None)
        print(f"Bounding rectangle:\n"
              f"x = {rect.coords_bound[0][0]}\n"
              f"y = {rect.coords_bound[0][1]}\n"
              f"w = {rect.coords_bound[1]}\n"
              f"h = {rect.coords_bound[2]}\n\n"
              f"Angles coordinates:\n"
              f"x1 = {rect.coords_gen[0][0]}, y1 = {rect.coords_gen[0][1]}\n"
              f"x2 = {rect.coords_gen[1][0]}, y2 = {rect.coords_gen[1][1]}\n"
              f"x3 = {rect.coords_gen[2][0]}, y3 = {rect.coords_gen[2][1]}\n"
              f"x4 = {rect.coords_gen[3][0]}, y4 = {rect.coords_gen[3][1]}\n"
              f"****************\n", file=data)
    data.close()
