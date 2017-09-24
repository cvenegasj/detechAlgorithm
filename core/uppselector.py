def launchUIForSelection(imgPath):
    import tkinter
    from PIL import ImageTk, Image

    FACTOR = 3

    class Paint:
        def __init__(self, canvas):
            self.canvas = canvas
            self._obj = None
            self.lastx, self.lasty = None, None
            self.canvas.bind('<Button-1>', self.update_xy)
            self.canvas.bind('<B1-Motion>', self.draw)
            self.points = {}
            self.f = FACTOR

        def draw(self, event):
            x, y = self.lastx, self.lasty
            self.canvas.coords(self._obj, (x, y, event.x, event.y))
            self.points['p1'] = event.x / self.f, event.y / self.f

        def update_xy(self, event):
            x, y = event.x, event.y
            self.points['p0'] = x / self.f, y / self.f
            self._obj = self.canvas.create_rectangle((x, y, x, y), outline='red', width=2)
            self.lastx, self.lasty = x, y

        def getPoints(self):
            return self.points

    root = tkinter.Tk()

    root.title = "UPP Selector"

    pilimage = Image.open(imgPath)
    (x, y) = pilimage.size

    pilimage = pilimage.resize((FACTOR * x, FACTOR * y))

    img = ImageTk.PhotoImage(pilimage)

    canvas = tkinter.Canvas()
    canvas.create_image(0, 0, image=img, anchor='nw')
    whiteboard = Paint(canvas)
    canvas.pack(padx=6, pady=6)

    root.mainloop()

    return whiteboard.getPoints()