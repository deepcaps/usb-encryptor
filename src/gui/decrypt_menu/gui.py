from tkinter import Canvas, Entry, Button, PhotoImage, filedialog
from os import path


class DecryptMenu():
    '''
    Decrypt menu windows
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
            136.11114501953125,
            533.5555419921875,
            anchor="nw",
            text="by @deepcaps",
            fill="#C3C3C4",
            font=("Inter Medium", 11 * -1)
        )

        global submit_button_image
        submit_button_image = PhotoImage(
            file=self.path("submit_button.png"))
        Button(
            image=submit_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.main.s_decrypt(),
            relief="flat",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=97.22222900390625,
            y=432.44451904296875,
            width=155.5555419921875,
            height=54.44444274902344
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
            x=118.22210693359375,
            y=385.7778015136719,
            width=109,
            height=14
        )

        global salt_entry_image
        salt_entry_image = PhotoImage(
            file=self.path("salt_entry_background.png"))
        canvas.create_image(
            175.00003051757812,
            351.166690826416,
            image=salt_entry_image
        )
        self.salt_entry = Entry(
            bd=0,
            bg="#2B2F3B",
            fg="#FFFFFF",
            insertbackground="white",
            highlightthickness=0
        )
        self.salt_entry.place(
            x=63.00003910064697,
            y=329.7778015136719,
            width=223.9999828338623,
            height=40.77777862548828
        )

        canvas.create_text(
            51.3333740234375,
            308.0000305175781,
            anchor="nw",
            text="Salt",
            fill="#C3C3C4",
            font=("Inter Medium", 15 * -1)
        )

        global password_entry_image
        password_entry_image = PhotoImage(
            file=self.path("password_entry_background.png"))
        canvas.create_image(
            175.00003051757812,
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
            x=63.00003910064697,
            y=233.33334350585938,
            width=223.9999828338623,
            height=40.77777099609375
        )

        canvas.create_text(
            51.3333740234375,
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
            bd=0,
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
            x=94.11114501953125,
            y=129.11114501953125,
            width=81.66668701171875,
            height=35.0
        )

        global encrypt_button_image
        encrypt_button_image = PhotoImage(
            file=self.path("encrypt_button.png"))
        Button(
            image=encrypt_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.gui.changeMenu("encrypt"),
            relief="flat",
            activebackground="#232429",
            background="#232429"
        ).place(
            x=189.77777099609375,
            y=141,
            width=58,
            height=14
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
            width=35.0,
            height=35.0
        )
    
    def path(self, file):
        '''
        Get relative path to ressource
        '''
        current_path = path.dirname(__file__)
        return path.join(current_path, "assets", file)
    
    def keyFileMethod(self):
        '''
        Ask path to key file and decrypt volume
        '''
        # ask file
        key_file = filedialog.askopenfilename(initialdir=self.volume, title="Select key file", filetypes=(("Key files", "*.key"), ("All files", "*.*")))
        
        if key_file == "":   # if no file has been chosen
            return False
        
        # decrypt
        self.main.s_decrypt(key_file)
        
        return True