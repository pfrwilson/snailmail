import tkinter as tk
from tkinter import ttk
from PublicInfo import PublicInfo


class ChooseStatusWindow(tk.Toplevel):
    """A window which can be used to obtain a status selection from the user"""

    def __init__(self, parent, username):
        super().__init__(parent)

        self.configure(bd=3, relief=tk.RAISED)

        # left frame
        fr_left = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_left.grid(row=0, column=0)

        # right frame
        fr_right = tk.Frame(self, bd=1, relief=tk.SOLID)
        fr_right.grid(row=0, column=1)

        # header area
        ttk.Label(fr_left, text='Choose Status', font=('Calibri', 14, 'bold')).grid(row=0, column=0, sticky='ew')

        # username area
        fr_username = tk.Frame(fr_left)
        ttk.Label(fr_username, text='Username: ').grid(row=0, column=0)
        txt_username = tk.Text(fr_username, height=1, width=15, font=('Calibri', 14, 'bold'))
        txt_username.grid(row=0, column=1, stick='nsew')
        txt_username.insert('1.0', username)
        txt_username['state'] = tk.DISABLED
        fr_username.grid(row=1, column=0, sticky='ew')

        # status area
        fr_status = tk.Frame(fr_left)
        ttk.Label(fr_status, text='Status:      ').grid(row=0, column=0)
        self.flag = tk.IntVar(0)
        self.selected_status = tk.StringVar()
        status_box = ttk.Combobox(fr_status, height=1, width=15, font=('Calibri', 14, 'bold'),
                                  values=['ONLINE', 'BUSY', 'AWAY'],
                                  textvariable=self.selected_status)
        status_box.grid(row=0, column=1)
        status_box.bind('<<ComboboxSelected>>', lambda *args: self.flag.set(1))
        fr_status.grid(row=2, column=0, sticky='ew')

    def get_status(self):
        """waits for a status to be selected and returns the public info object
        created for the user"""
        self.wait_variable(self.flag)
        self.destroy()
        status = self.selected_status.get()
        tags = {'ONLINE': PublicInfo.ONLINE,
                'AWAY': PublicInfo.AWAY,
                'BUSY': PublicInfo.BUSY}
        return PublicInfo(status_tag=tags[status])


"""sample usage"""
if __name__ == "__main__":

    main = tk.Tk()
    print(ChooseStatusWindow(main, 'paul').get_status())
