class Window:
    def __init__(self, height, width, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.size = (width, height)
        self.position = (x, y)

    def json(self):
        return {
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y
        }
