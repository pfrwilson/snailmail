import tkinter as tk
from tkinter import ttk
from Message import Message
from tkinter import messagebox


class MessageEditorWindow(tk.Toplevel):
    """A simple message editing window class.
    The window allows editing the subject, recipients and content of a message.
    The send button collects the information from the text fields and sends the message
    object using the passed on_send_message_event function
    sample usage:
    MessageEditorWindow('paul', ['paul', 'francis', 'raymond', 'wilson'],
                        on_send_message_event = lambda message: print(message)).mainloop()
    """

    def __init__(self, parent, username, user_list, on_send_message_event=lambda message: print(message)):
        """Constructs window by adding the correct widgets. Requires passing the username
        of the message editor and a list of users on the server"""

        super().__init__(parent)

        self.username = username
        self.user_list = user_list
        self.on_send_message_event = on_send_message_event

        self.title(f"Message Editor : {username}")

        # left frame
        fr_left = tk.Frame(self,  relief=tk.RAISED, bd=2, padx=3, pady=3)
        fr_left.grid(row=0, column=0, sticky='ns')

        # recipients selector
        tk.Button(fr_left, text="Choose recipients:", command=self.select_recipients \
                  ).grid(column=0, row=0, padx=3, pady=3)
        self.user_selector = tk.Listbox(fr_left, width=15, selectmode=tk.MULTIPLE)
        for i, user in enumerate(user_list):
            self.user_selector.insert(i, user)
        self.user_selector.grid(row=1, column=0, padx=5, pady=5)

        # send button
        btn_send = tk.Button(fr_left, text='Send', command=self.send_message)
        btn_send.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # right frame
        fr_right = tk.Frame(self, relief=tk.RAISED, bd=2)
        fr_right.grid(row=0, column=1)

        # recipients area
        fr_recipients = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_recipients, text='Recipients:').grid(row=0, column=0)
        self.txt_recipients = tk.Text(fr_recipients, height=1, state=tk.DISABLED)
        self.txt_recipients.grid(row=0, column=1)
        fr_recipients.grid(row=0, column=0, sticky='ew')

        # subject area
        fr_subject = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_subject, text='Subject:').grid(row=0, column=0)
        self.txt_subject = tk.Text(fr_subject, height=1)
        self.txt_subject.grid(row=0, column=1)
        fr_subject.grid(row=2, column=0, sticky='ew')

        # message area
        fr_message = tk.Frame(fr_right, relief=tk.RAISED, bd=2)
        ttk.Label(fr_message, text='Message:').grid(row=0, column=0, sticky='nw')
        self.txt_message = tk.Text(fr_message, height=20)
        self.txt_message.grid(row=0, column=1)
        fr_message.grid(row=3, column=0, sticky='ew')

    def get_recipient_selection(self):
        """Obtains the recipient selection currently highlighted in the recipient selector"""

        users = self.user_list
        return [users[i] for i in self.user_selector.curselection()]

    def select_recipients(self):
        """Takes the list of selected recipients and displays them in the recipients field.
        called by the select recipients button."""

        self.txt_recipients['state'] = tk.NORMAL
        self.txt_recipients.delete('1.0', tk.END)
        for recipient in self.get_recipient_selection():
            self.txt_recipients.insert(tk.END, f'{recipient}; ')
        self.txt_recipients['state'] = tk.DISABLED

    def send_message(self):
        """Collects the data fields and sends the message. Using the on_message_send_event method provided
        in the constructor"""

        subject = self.txt_subject.get('1.0', 'end')
        recipients = self.get_recipient_selection()
        content = self.txt_message.get('1.0', 'end')
        message = Message(sender=self.username, subject=subject, recipients=recipients, content=content)
        self.on_send_message_event(message)
        self.destroy()