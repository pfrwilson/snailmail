import tkinter as tk
from tkinter import ttk
from Message import Message


class MessageDisplayWindow(tk.Toplevel):
    """A simple message display window. Pass it a message object and it shows all the information.
    """

    def __init__(self, parent, message):
        """Constructs window by adding the correct data fields """

        super().__init__(parent)

        self.title(f"Message Display")

        # right frame
        fr_right = tk.Frame(self, relief=tk.RAISED, bd=2)
        fr_right.grid(row=0, column=1)

        # sender area
        fr_sender = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_sender, text='Sender: ').grid(row=0, column=0)
        txt_sender = tk.Text(fr_sender, height=1, font='Calibri')
        txt_sender.insert(tk.END, message.get_sender())
        txt_sender['state'] = tk.DISABLED
        txt_sender.grid(row=0, column=1)
        fr_sender.grid(row=0, column=0, sticky='ew')

        # recipients area
        fr_recipients = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_recipients, text='Recipients: ').grid(row=0, column=0)
        txt_recipients = tk.Text(fr_recipients, height=1, font='Calibri')
        for recipient in message.get_recipients():
            txt_recipients.insert(tk.END, f'{recipient}; ')
        txt_recipients['state'] = tk.DISABLED
        txt_recipients.grid(row=0, column=1)
        fr_recipients.grid(row=1, column=0, sticky='ew')

        # subject area
        fr_subject = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_subject, text='Subject: ').grid(row=0, column=0)
        txt_subject = tk.Text(fr_subject, height=1, font='Calibri')
        txt_subject.insert(tk.END, message.get_subject())
        txt_subject['state'] = tk.DISABLED
        txt_subject.grid(row=0, column=1)
        fr_subject.grid(row=2, column=0, sticky='ew')

        # date area
        fr_date = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_date, text='Date/Time: ').grid(row=0, column=0)
        txt_date = tk.Text(fr_date, height=1, font='Calibri')
        txt_date.insert(tk.END, message.get_datetime())
        txt_date['state'] = tk.DISABLED
        txt_date.grid(row=0, column=1)
        fr_date.grid(row=3, column=0, sticky='ew')

        # message area
        fr_message = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_message, text='Message: ').grid(row=0, column=0, sticky='nw')
        txt_message = tk.Text(fr_message, height=20, font='Calibri')
        txt_message.insert(tk.END, message.get_content())
        txt_message['state'] = tk.DISABLED
        txt_message.grid(row=0, column=1)
        fr_message.grid(row=4, column=0, sticky='ew')


"""Sample usage"""
if __name__ == "__main__":
    m = Message(sender='paul', recipients=['wilson'], subject='greeting', content='hello world!')
    MessageDisplayWindow(m).mainloop()
