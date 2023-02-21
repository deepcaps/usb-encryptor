from tkinter import Canvas, Entry, Button, PhotoImage, filedialog, END
from os import path


class EncryptMenu():
    '''
    Encrypt menu windows
    '''
    def __init__(self, gui, main):
        # set variables
        self.window = gui.window
        self.gui = gui
        self.main = main
        self.volume = main.volume
        
        # public elements
        self.password_entry = None
        self.salt_entry = None
    
    def display(self):
        '''
        Display the menu
        '''
        # create canvas
        canvas = Canvas(
            self.window,
            bg = "#232429",
            height = 552,
            width = 350,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # place elements
        canvas.place(x = 0, y = 0)
        canvas.create_text(
            136.1111297607422,
            533.5555419921875,
            anchor="nw",
            text="by @deepcaps",
            fill="#C3C3C4",
            font=("Inter Medium", 11 * -1)
        )

        canvas.create_rectangle(
            199.0,
            447.22222900390625,
            299.0,
            489.22222900390625,
            fill="#744722",
            outline="")

        canvas.create_text(
            241.0,
            459.22222900390625,
            anchor="nw",
            text=self.volume,
            fill="#C79651",
            font=("Inter Medium", 15 * -1)
        )

        canvas.create_text(
            232.0,
            422.22222900390625,
            anchor="nw",
            text="Disk",
            fill="#C3C3C4",
            font=("Inter Medium", 15 * -1)
        )

        global salt_entry_image
        salt_entry_image = PhotoImage(
            master=self.window,
            file=self.path("salt_entry_background.png"))
        canvas.create_image(
            101.0,
            468.22222900390625,
            image=salt_entry_image
        )
        self.salt_entry = Entry(
            bd=0,
            bg="#295E4D",
            fg="#3ED77C",
            justify="center",
            insertbackground="#295E4D",
            highlightthickness=0,
        )
        self.salt_entry.place(
            x=62.66666507720947,
            y=447.22222900390625,
            width=76.66666984558105,
            height=40.0
        )

        canvas.create_text(
            77.0,
            459.22222900390625,
            anchor="nw",
            text="111111",
            fill="#3ED67C",
            font=("Inter Medium", 15 * -1)
        )

        global circle_image
        circle_image = PhotoImage(
            file=self.path("circle.png"))
        Button(
            image=circle_image,
            borderwidth=0,
            highlightthickness=0,
            relief="sunken",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=115.0,
            y=422.22222900390625,
            width=6.0,
            height=6.0
        )

        canvas.create_text(
            85.0,
            422.22222900390625,
            anchor="nw",
            text="Salt",
            fill="#C3C3C4",
            font=("Inter Medium", 15 * -1)
        )

        global submit_button_image
        submit_button_image = PhotoImage(
            file=self.path("submit_button.png"))
        Button(
            image=submit_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda : self.main.s_encrypt(),
            relief="flat",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=96.22224426269531,
            y=331.44451904296875,
            width=155.55555725097656,
            height=54.4444465637207
        )

        global key_file_button_image
        key_file_button_image = PhotoImage(
            file=self.path("key_file_button.png"))
        Button(
            image=key_file_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.keyFileMethod(),
            relief="flat",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=118.22207641601562,
            y=288.7778015136719,
            width=113.5555648803711,
            height=15.686431884765625
        )

        global password_entry_image
        password_entry_image = PhotoImage(
            file=self.path("password_entry_background.png"))
        canvas.create_image(
            175.00000762939453,
            254.72222900390625,
            image=password_entry_image
        )
        self.password_entry = Entry(
            bd=0,
            bg="#2B2F3B",
            fg="#FFFFFF",
            insertbackground="white",
            highlightthickness=0
        )
        self.password_entry.place(
            x=63.00000858306885,
            y=233.33334350585938,
            width=223.99999809265137,
            height=40.77777099609375
        )

        canvas.create_text(
            51.333343505859375,
            211.55555725097656,
            anchor="nw",
            text="Password",
            fill="#C3C3C4",
            font=("Inter Medium", 15 * -1)
        )

        global slider_image
        slider_image = PhotoImage(
            file=self.path("slider.png"))
        Button(
            image=slider_image,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="sunken",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=88.66668701171875,
            y=124.4444580078125,
            width=172.66665649414062,
            height=44.333343505859375
        )

        global current_image
        current_image = PhotoImage(
            file=self.path("current.png"))
        Button(
            image=current_image,
            borderwidth=0,
            highlightthickness=0,
            command=None,
            relief="sunken",
            activebackground="#1C1D21",
            background="#1C1D21"
        ).place(
            x=172.0,
            y=129.22222900390625,
            width=81.66666412353516,
            height=35.0
        )

        global decrypt_button_image
        decrypt_button_image = PhotoImage(
            file=self.path("decrypt_button.png"))
        Button(
            image=decrypt_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.gui.changeMenu("decrypt"),
            relief="flat",
            activebackground="#1C1D21",
            background="#1C1D21"
        ).place(
            x=102.0,
            y=138,
            width=59.111114501953125,
            height=21.0
        )

        canvas.create_text(
            56.77777099609375,
            66.11114501953125,
            anchor="nw",
            text="USB-ENCRYPTOR",
            fill="#FFFFFF",
            font=("Inter Bold", 27 * -1)
        )

        global debug_button_image
        debug_button_image = PhotoImage(
            file=self.path("debug_button.png"))
        Button(
            image=debug_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.main.switchDebug(),
            relief="flat",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=300.22222900390625,
            y=24.888885498046875,
            width=35.000003814697266,
            height=35.0
        )
    
    def path(self, file):
        '''
        Get relative path to ressource
        '''
        current_path = path.dirname(__file__)
        return path.join(current_path, "assets", file)
    
    def setSalt(self, salt):
        '''
        Write salt value into salt entry
        '''
        self.salt_entry.delete(0, END)
        self.salt_entry.insert(0, salt)
    
    def keyFileMethod(self):
        '''
        Ask path to save key file
        '''
        # ask path
        save_path = filedialog.askdirectory(initialdir=self.volume, title="Key file save path")

        if save_path == "":   # if no file has been chosen
            return False
        
        # encrypt
        self.main.s_encrypt(save_path)
        
        return True