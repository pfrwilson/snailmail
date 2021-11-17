import tkinter as tk
from PublicInfo import PublicInfo
from Message import Message
from tkinter import ttk
from datetime import datetime


class UserThumbnail(tk.Frame):

    def __init__(self, parent, username, public_info):
        super().__init__(parent)
        self.configure(bd=3, relief=tk.RAISED)

        colors = {PublicInfo.ONLINE : 'lightgreen',
                  PublicInfo.AWAY: 'yellow',
                  PublicInfo.BUSY: 'indian red',
                  PublicInfo.OFFLINE: 'lightgrey'}

        statuses = {PublicInfo.ONLINE : 'ONLINE',
                  PublicInfo.AWAY: 'AWAY',
                  PublicInfo.BUSY: 'BUSY',
                  PublicInfo.OFFLINE: 'OFFLINE'}

        # left frame
        fr_left = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_left.grid(row=0, column=0)

        # right frame
        fr_right = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_right.grid(row=0, column=0)

        # header area
        ttk.Label(fr_left, text='User Info', font=('Calibri', 14, 'bold')).grid(row=0, column=0, sticky='ew')

        # username area
        fr_username = tk.Frame(fr_left)
        ttk.Label(fr_username, text='Username: ').grid(row=0, column=0)
        txt_username = tk.Text(fr_username, height=1, width=15, font=('Calibri', 14, 'bold'))
        txt_username.grid(row=0, column=1)
        txt_username.insert('1.0', username)
        txt_username['state'] = tk.DISABLED
        fr_username.grid(row=1, column=0, sticky='ew')

        #status area
        fr_status = tk.Frame(fr_left)
        ttk.Label(fr_status, text='Status:      ').grid(row=0, column=0)
        txt_status = tk.Text(fr_status, height=1, width=15, font=('Calibri', 14, 'bold'),
                             bg=colors[public_info.get_status_tag()])
        txt_status.grid(row=0, column=1)
        txt_status.insert('1.0', statuses[public_info.get_status_tag()])
        txt_status['state'] = tk.DISABLED
        fr_status.grid(row=2, column=0, sticky='ew')

    # status area



if __name__ == "__main__":
    window = tk.Tk()
    UserThumbnail(window, 'paul', PublicInfo(status_tag=PublicInfo.BUSY)).pack()
    window.mainloop()
