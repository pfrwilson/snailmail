from StorageUtility import StorageUtility
from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk
from LoginWindow import LoginWindow
from ClientNode import ClientNode
from VerticalScrolledPane import VerticalScrolledPane
from MessageThumbnail import MessageThumbnail
from RegisterWindow import RegisterWindow
from LoginWindow import LoginWindow
from tkinter import messagebox
from MessageEditorWindow import MessageEditorWindow
from MessageDisplayWindow import MessageDisplayWindow
from UserThumbnail import UserThumbnail
from ChooseStatusWindow import ChooseStatusWindow


class ClientMain(tk.Tk):

    def __init__(self):
        super().__init__()

        # disable resizing
        self.resizable(False, False)

        # set close protocol
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # set up widgets
        fr_left = tk.Frame(self, bd=2, relief=tk.RAISED)
        fr_left.grid(row=0, column=0, sticky='ns')

        tk.Label(fr_left, text="StaffChat", font=('Calibri', 20, 'bold')).grid(row=0, column=0, pady=10, sticky='w')

        tk.Button(fr_left, text="Inbox", command=self.show_inbox).grid(row=1, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Outbox", command=self.show_outbox).grid(row=2, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Set Status", command=self.set_status).grid(row=3, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="New Message", command=self.compose_message).grid(row=4, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Login", command=self.login).grid(row=5, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Logout", command=self.logout).grid(row=6, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Register", command=self.register).grid(row=7, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Restore", command=self.restore_server).grid(row=8, column=0, pady=10, sticky='ew')
        tk.Button(fr_left, text="Sync server", command=self.sync_server).grid(row=9, column=0, pady=10, sticky='ew')

        fr_middle = tk.Frame(self, bd=2, relief=tk.RAISED)
        fr_middle.grid(row=0, column=1, sticky='ns')

        tk.Label(fr_middle, text='Mailbox', font=('Calibri', 20, 'bold')).grid(row=0, column=0, pady=10)
        fr_message_thumbnails = VerticalScrolledPane(fr_middle, canvas_height=500, canvas_width=400)
        fr_message_thumbnails.grid(row=1, column=0)
        self.message_thumbnail_pane = fr_message_thumbnails.scrollable_frame
        self.message_thumbnails = []

        fr_right = tk.Frame(self, bd=2, relief=tk.RAISED)
        fr_right.grid(row=0, column=2, sticky='ns')
        tk.Label(fr_right, text='Users', font=('Calibri', 20, 'bold')).grid(row=0, column=0, pady=10)
        fr_user_thumbnails = VerticalScrolledPane(fr_right, canvas_height=500, canvas_width=250)
        fr_user_thumbnails.grid(row=1, column=0)
        self.user_thumbnail_pane = fr_user_thumbnails.scrollable_frame
        self.user_thumbnails = []

        self.username = None
        self.password = None
        self.host_address = None
        self.logged_in = False
        self.client_node: ClientNode = None
        self.setup_host_address()
        self.title(f'StaffChat Messaging at Host Address {self.host_address}')

    def show_inbox(self):
        if self.logged_in:

            # clear the message thumbnails
            for thumbnail in self.message_thumbnails:
                thumbnail.destroy()
            self.message_thumbnails = []

            inbox = self.client_node.get_inbox()
            for i, message in enumerate(inbox):
                thumbnail = MessageThumbnail(self.message_thumbnail_pane, message)
                thumbnail.set_on_delete_button_pressed(lambda message: self.client_node.delete_message(message))
                thumbnail.set_on_open_button_pressed(lambda message: MessageDisplayWindow(self, message).mainloop())
                thumbnail.grid(row=i, column=0)
                self.message_thumbnails.append(thumbnail)

    def show_outbox(self):
        if self.logged_in:
            # clear the message thumbnails
            for thumbnail in self.message_thumbnails:
                thumbnail.destroy()
            self.message_thumbnails = []

            outbox = self.client_node.get_outbox()
            for i, message in enumerate(outbox):
                thumbnail = MessageThumbnail(self.message_thumbnail_pane, message)
                thumbnail.set_on_delete_button_pressed(lambda message: self.client_node.delete_message(message))
                thumbnail.set_on_open_button_pressed(lambda message: MessageDisplayWindow(self, message).mainloop())
                thumbnail.grid(row=i, column=0)
                self.message_thumbnails.append(thumbnail)

    def show_user_thumbnails(self):
        if self.logged_in:
            # clear the user thumbnails
            for thumbnail in self.user_thumbnails:
                thumbnail.destroy()
            self.user_thumbnails = []

            server_public_info = self.client_node.get_server_public_info()
            for i, (username, public_info) in enumerate(server_public_info.items()):
                thumbnail = UserThumbnail(self.user_thumbnail_pane, username, public_info)
                thumbnail.grid(row=i, column=0)
                self.user_thumbnails.append(thumbnail)

    def register(self):
        if self.client_node is None:
            username, password = RegisterWindow(self).get_username_and_password()
            self.username = username
            self.password = password
            self.client_node = ClientNode(self.host_address, self.username, self.password)
            self.activate_window()
            if self.client_node.register_user():
                messagebox.showinfo("Success", "Registration Successful")
            else:
                messagebox.showerror("Failure", "Could not register account. Account may already exist")

    def login(self):
        if not self.logged_in:
            username, password = LoginWindow(self).get_username_and_password()
            self.username = username
            self.password = password
            self.client_node = ClientNode(self.host_address, self.username, self.password)
            self.activate_window()
            if self.client_node.login():
                self.logged_in = True
                self.sync_server()
                self.show_inbox()
                messagebox.showinfo("Success", "Login successful")
            else:
                self.client_node = None
                messagebox.showerror("Error", "Login unsuccessful")
        else:
            messagebox.showerror("Error", "You are already logged in")

    def restore_server(self):
        if self.logged_in:
            if self.client_node.restore_user_info():
                messagebox.showinfo("Success", "Sync successful")
            else:
                messagebox.showerror("Error", "Sync unsuccessful")
        else:
            messagebox.showerror("Error", "You are not logged in")

    def activate_window(self):
        self.client_node.set_on_new_messages_received(lambda messages:
                                                      messagebox.showinfo('New Messages!',
                                                                          f'You have {len(messages)} new message(s).'))
        self.client_node.set_on_new_server_public_info(lambda public_info: self.show_user_thumbnails())

    def close_window(self):
        try:
            self.logout()
            self.destroy()
        except:
            pass
        finally:
            exit(0)

    def logout(self):
        if self.logged_in:
            self.client_node.logout()
            self.client_node = None
            self.empty_page()
            self.logged_in = False

    def empty_page(self):
        # clear the user thumbnails
        for thumbnail in self.user_thumbnails:
            thumbnail.destroy()
        self.user_thumbnails = []

        # clear the message thumbnails
        for thumbnail in self.message_thumbnails:
            thumbnail.destroy()
        self.message_thumbnails = []

    def compose_message(self):
        if self.logged_in:
            MessageEditorWindow(self, self.username, self.client_node.get_user_list(),
                                on_send_message_event=self.send_message)

    def send_message(self, message):
        if self.logged_in:
            flag = self.client_node.send_message(message)
            if not flag:
                messagebox.showerror('Error', 'Message send failed')

    def set_status(self):
        if self.logged_in:
            public_info = ChooseStatusWindow(self, self.username).get_status()
            self.client_node.set_user_public_info(public_info)
            self.sync_server()

    def setup_host_address(self):
        host_address = StorageUtility('host_address.txt').load()
        if host_address is None:
            host_address = simpledialog.askstring("Connect to server", "Enter server address:",\
                                            parent=self)
            StorageUtility('host_address.txt').save(host_address)
        self.host_address = host_address

    def sync_server(self):
        self.client_node.refresh()
        self.show_user_thumbnails()


if __name__ == "__main__":
    ClientMain().mainloop()


