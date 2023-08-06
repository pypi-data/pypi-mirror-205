"""A class to bring up a debugging window"""

from tkinter import Tk, Canvas, NW, PhotoImage, TclError

def rgb2hex(red,green,blue):
    """
    converts an rgb code to hex
    """
    return f'#{blue:02x}{green:02x}{red:02x}'

def bitmap_to_photo(bitmap, subsample = 1):
    """
    converts a 3 channel numpy array image into
    a tkinter photoImage suitable for putting into
    tk widget
    https://stackoverflow.com/questions/1581799/
    how-to-draw-a-bitmap-real-quick-in-python-using-tk-only

    :param bitmap: The bitmap image, taken from opencv as a
        3 channel numpy array
    :param subsample: You can optionally subsample the image
        which might be useful if you want it to run faster. A value of
        n will give an nxn speed up as we use 2 loops to convert the image.
    """
    ss_bitmap = bitmap[1::subsample, 1::subsample]
    image_width = ss_bitmap.shape[1]
    image_height = ss_bitmap.shape[0]

    photo_image = PhotoImage(width=image_width, height=image_height)

    imgstring = " ".join(("{"+" ".join(rgb2hex(*ss_bitmap[row,col,:])
        for col in range(image_width)) + "}")
            for row in range(image_height)) \

    photo_image.put(imgstring, (0,0,image_width -1, image_height - 1))
    photo_image = photo_image.zoom(subsample)

    return photo_image


class ImshowTk():
    """
    Creates a window using TkInter, into which we can
    place an opencv image. Conceived as a zero dependency alternative
    to opencv's imshow window, for when we want to use opencv-headless
    or avoid conflict with Qt.
    """
    def __init__(self, in_use = True, subsample = 1):
        """
        :param in_use: Boolean, if false we're not using the window, useful
            if your using this an optional debug window.
        :param subsample: we can subsample the image to speed things up
        """
        self.in_use = in_use
        self.initialised = False
        self.canvas = None
        self.tk_window = None
        self.image = None
        self.subsample = subsample

    def __del__(self):
        """
        Destroys the TK window
        """
        if self.tk_window is not None:
            self.tk_window.destroy()

    def setup_window(self, frame):
        """
        Do this after init as we need a frame of
        video to set the window size
        """
        if self.in_use:
            self.tk_window = Tk()
            self.tk_window.title('imshow with Tk')
            self.canvas = Canvas(self.tk_window,
                        width = frame.shape[1], height = frame.shape[0])
            self.canvas.pack()
        self.initialised = True

    def imshow(self, frame):
        """
        Shows the image
        """
        if not self.in_use:
            return

        if not self.initialised:
            self.setup_window(frame)

        self.image = bitmap_to_photo(frame, self.subsample)
        try:
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)
        except TclError as error_msg:
            #this seems to happen when we're not running inside
            #a persistent application (i.e. CI testing),
            #self.image is getting deleted before we can use it.
            #We haven't seen it in practice.
            print ("Ignoring Tk error: ", str(error_msg))
            return

        self.tk_window.update()
