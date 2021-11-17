import tkinter as tk
from tkinter import messagebox


class LoginWindow(tk.Toplevel):
    """A login window which can be called upon to obtain the username and password entered by the
    user"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Login")
        self.geometry('400x250')

        self.password = tk.StringVar()
        self.username = tk.StringVar()

        tk.Label(self, text="Username * ").pack()
        user_entry1 = tk.Entry(self, textvariable=self.username)
        user_entry1.pack()

        tk.Label(self, text="Password * ").pack()
        pass_entry1 = tk.Entry(self, textvariable=self.password, show='*')
        pass_entry1.pack()

        tk.Label(self, text="").pack()
        self.flag = tk.IntVar(0)
        self.btLogin = tk.Button(self, text="Login", width=10, height=1, \
                                 command=lambda *args: self.flag.set(1)).pack()

    def get_username_and_password(self):
        """waits for the login button to be pressed and then returns the username and
        password entered by the user"""
        self.wait_variable(self.flag)
        self.destroy()
        return self.username.get(), self.password.get()


"""sample usage"""
if __name__ == "__main__":

    main = tk.Tk()
    print(LoginWindow(main).get_username_and_password())