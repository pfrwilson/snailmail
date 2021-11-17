import tkinter as tk
from Message import Message
from tkinter import ttk
from datetime import datetime


class MessageThumbnail(tk.Frame):

    def __init__(self, parent, message, thumbnail_width=30):
        """Constructs the message thumbnail. Pass the parent object, the message
        object to display, and the thumbnail width in (measured by character width not pixels)"""

        super().__init__(parent, relief=tk.RAISED, bd=3)
        self.message = message
        self.on_open_button_pressed = lambda message: None
        self.on_delete_button_pressed = lambda message: None
        WIDTH = thumbnail_width

        fr_left = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_left.grid(row=0, column=0)

        # header area
        ttk.Label(fr_left, text='Message', font=('Calibri', 14, 'bold')).grid(row=0, column=0, sticky='ew')

        # sender area
        fr_recipients = tk.Frame(fr_left)
        ttk.Label(fr_recipients, text='From:     ').grid(row=0, column=0)
        txt_sender = tk.Text(fr_recipients, height=1, width=WIDTH, font=('Calibri'))
        txt_sender.grid(row=0, column=1)
        txt_sender.insert('1.0', self.message.get_sender())
        txt_sender['state'] = tk.DISABLED
        fr_recipients.grid(row=1, column=0, sticky='ew')

        # recipients area
        fr_recipients = tk.Frame(fr_left)
        ttk.Label(fr_recipients, text='To:         ').grid(row=0, column=0)
        txt_recipients = tk.Text(fr_recipients, height=1, width=WIDTH, font=('Calibri'))
        txt_recipients.grid(row=0, column=1)
        for recipient in message.get_recipients():
            txt_recipients.insert(tk.END, f'{recipient}; ')
        txt_recipients['state'] = tk.DISABLED
        fr_recipients.grid(row=2, column=0, sticky='ew')

        # subject area
        fr_subject = tk.Frame(fr_left)
        ttk.Label(fr_subject, text='Subject: ').grid(row=0, column=0)
        txt_subject = tk.Text(fr_subject, height=1, width=WIDTH, font=('Calibri'))
        txt_subject.grid(row=0, column=1)
        txt_subject.insert('1.0', self.message.get_subject())
        txt_subject['state'] = tk.DISABLED
        fr_subject.grid(row=3, column=0, sticky='ew')

        # time area
        fr_time = tk.Frame(fr_left)
        ttk.Label(fr_time, text='Time:      ').grid(row=0, column=0)
        txt_time = tk.Text(fr_time, height=1, width=WIDTH, font=('Calibri'))
        txt_time.grid(row=0, column=1)
        txt_time.insert('1.0', message.get_datetime())
        txt_time['state'] = tk.DISABLED
        fr_time.grid(row=4, column=0, sticky='ew')

        # buttons
        fr_right = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_right.grid(row=0, column=1, sticky='ns')
        bt_open = tk.Button(fr_right, text='open', command=self.open_message)
        bt_open.grid(row=0, column=0, padx=2)
        bt_delete = tk.Button(fr_right, text='delete', command=self.delete_message)
        bt_delete.grid(row=1, column=0, padx=2)

    def open_message(self):
        self.on_open_button_pressed(self.message)

    def delete_message(self):
        self.on_delete_button_pressed(self.message)
        self.destroy()

    def set_on_open_button_pressed(self, on_open_button_pressed):
        """Specified what function to perform on the message when the
        delete open button is pressed"""
        self.on_open_button_pressed = on_open_button_pressed

    def set_on_delete_button_pressed(self, on_delete_button_pressed):
        """Specifies what function to perform on the message when the delete
        button is pressed"""
        self.on_delete_button_pressed = on_delete_button_pressed


if __name__ == "__main__":
    window = tk.Tk()
    message = Message(sender='me', recipients=['you'], content='hello world')
    thumbnail = MessageThumbnail(window, message)
    thumbnail.grid(row=0, column=0)
    window.mainloop()