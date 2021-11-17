import tkinter as tk
from tkinter import messagebox


class RegisterWindow(tk.Toplevel):
    """A login window which can be called upon to obtain the username and password entered by the
    user"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Register")
        self.geometry('400x250')

        self.password = tk.StringVar()
        self.username = tk.StringVar()
        self.password_confirmation = tk.StringVar()

        tk.Label(self, text="Username * ").pack()
        user_entry1 = tk.Entry(self, textvariable=self.username)
        user_entry1.pack()

        tk.Label(self, text="Password * ").pack()
        pass_entry1 = tk.Entry(self, textvariable=self.password, show='*')
        pass_entry1.pack()

        tk.Label(self, text="Confirm Password * ").pack()
        pass_entry2 = tk.Entry(self, textvariable=self.password_confirmation, show='*')
        pass_entry2.pack()

        tk.Label(self, text="").pack()
        self.flag = tk.IntVar(0)
        self.bt_register = tk.Button(self, text="Register", width=10, height=1, \
                                 command=lambda *args: self.flag.set(1)).pack()

    def get_username_and_password(self):
        """waits for the login button to be pressed and then returns the username and
        password entered by the user. If the password does not match the password confirmation,
        the fields are erased and an error is displayed"""
        while True:
            self.wait_variable(self.flag)
            username = self.username.get()
            password = self.password.get()
            password_confirmation = self.password_confirmation.get()
            if password == password_confirmation:
                self.destroy()
                return username, password
            else:
                self.username.set('')
                self.password.set('')
                self.password_confirmation.set('')
                messagebox.showerror("Error", "Passwords do not match")


"""sample usage"""
if __name__ == "__main__":

    main = tk.Tk()
    print(RegisterWindow(main).get_username_and_password())