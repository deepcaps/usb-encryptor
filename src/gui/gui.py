from tkinter import Tk, messagebox
from os import path

from gui.decrypt_menu.gui import DecryptMenu
from gui.encrypt_menu.gui import EncryptMenu


class Gui():
    def __init__(self, main):
        # set variables
        self.current_window = None
        self.pop = messagebox
        
        # create window
        self.window = Tk()
        
        # init menus
        self.decrypt_menu = DecryptMenu(self, main)
        self.encrypt_menu = EncryptMenu(self, main)
    
    def start(self):
        '''
        Display the GUI
        '''        
        # configure window
        self.window.geometry("350x552")   # window size
        self.window.title("usb-encryptor")   # window title
        self.window.configure(bg = "#232429")   # windows background
        self.window.resizable(False, False)   # disable window resizing
        # set icon
        current_path = path.dirname(__file__)
        self.window.iconbitmap(path.join(current_path, "icon.ico"))   # windows ico

        # display encrypt menu
        self.current_window = self.encrypt_menu
        self.current_window.display()

        # run window
        self.window.mainloop()
    
    def changeMenu(self, menu):
        '''
        Change menu of GUI
        '''
        if menu == "decrypt":
            self.current_window = self.decrypt_menu
            self.current_window.display()
        elif menu == "encrypt":
            self.current_window = self.encrypt_menu
            self.current_window.display()