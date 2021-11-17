import tkinter as tk
from tkinter import ttk
from MessageThumbnail import MessageThumbnail
from Message import Message


class VerticalScrolledPane(ttk.Frame):
    """A frame with a scrollable region. Add items to scrollable region by setting
    their parent as '<ScrollableFrame_instance>.scrollable_frame', and packing them."""

    def __init__(self, container, canvas_height=400, canvas_width=400, *args, **kwargs):
        """Specify canvas_height and canvas_width in constructor to adjust the
        size of the object"""
        super().__init__(container, **kwargs)
        canvas = tk.Canvas(self, height=canvas_height, width=canvas_width)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


"""Sample usage for ScrollableFrame class"""
if __name__ == "__main__":
    root = tk.Tk()
    scrollframe = VerticalScrolledPane(root, canvas_height=600, canvas_width=400)

    for i in range(10):
        message = Message(sender='me', recipients=['you'], content='hello world')
        thumbnail = MessageThumbnail(scrollframe.scrollable_frame, message)
        thumbnail.grid(row=i, column=0)

    scrollframe.grid(row=0, column=0)
    root.mainloop()