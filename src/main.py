from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode, urlsafe_b64encode
from slogs import slogs, parents
from random import randint
import os

from encrypt import Encrypt
from decrypt import Decrypt
from gui.gui import Gui


class Main():
    def __init__(self):        
        # init slogs
        self.log = slogs(autoprint=True, log_saving=False)

        # get volume
        try:
            self.volume = self.getVolume()
        except Exception as e:   # if script is not at the root of the key or on the system drive
            self.log.error(str(e), parents.SYSTEM)
            raise e

        # init decrypt/encrypt modules
        self.decrypt = Decrypt(self.volume)
        self.encrypt = Encrypt(self.volume)

        # init GUI
        self.gui = Gui(self)

        # start GUI
        self.gui.start()
    
    def s_encrypt(self, save_path=None):
        '''
        Encrypt function: Encrypt disk with GUI inputs
        '''
        # verify if volume exist
        if not os.path.exists(self.volume):
            self.log.error("Volume is not disconnected", parents.SYSTEM)
            self.gui.pop.showerror("Error", "Volume is disconnected")
            return False
        
        # verify if volume is not already encrypted
        if os.path.exists(os.path.join(self.volume, "tagid")):
            self.log.error("Volume already encrypted", parents.SYSTEM)
            self.gui.pop.showerror("Error", "Volume already encrypted")
            return False
        
        if save_path == None:   # if save path is not specified (password mode)
            # get password entry content from GUI
            password = self.gui.current_window.password_entry.get()
            if password == "":   # if password is empty
                self.gui.pop.showwarning("Warning", "Password is empty")
            
            # generate key and salt
            key, salt = self.generateKey(password)
            
            # update GUI salt entry
            self.gui.current_window.setSalt(salt)
        else:   # if key file is specified
            # generate key
            key = self.generateKey()
            
            try:
                # create key file
                with open(os.path.join(save_path, "key.key"), "w") as f:
                    b_key = b64encode(key)   # encode key 
                    f.write(str(b_key.decode("utf-8")))
            except Exception as e:
                self.log.error(str(e), parents.SYSTEM)
                self.gui.pop.showerror("File error", str(e))
                return False
        
        # encrypt volume
        try:
            self.encrypt.createArchive()
        except Exception as e:
            self.log.error(str(e), "encrypt")
            self.gui.pop.showerror("Encrypt error", str(e))
            return False
        
        try:
            self.encrypt.encryptArchive(key)
            hash = self.encrypt.getHash()
            self.encrypt.writeTAGID(hash)
        except Exception as e:
            self.log.error("Error during archive encryption : " + str(e), parents.SYSTEM)
            self.gui.pop.showerror("Encrypt error", "Error during archive encryption")
            return False
        
        # log
        self.log.success("Succes to encrypt volume !", parents.SYSTEM)
        self.gui.pop.showinfo("Success", "Succes to encrypt volume !")
        if save_path == None:   # if method is password
            self.gui.pop.showwarning("Warning", "Please note and save the salt number")
        else:
            self.gui.pop.showwarning("Advice", "Don't save key file on encrypted volume")
        
        return True
    
    def s_decrypt(self, key_file=None):
        '''
        Decrypt function: Decrypt disk with GUI inputs
        '''
        if key_file == None:   # if key file is not specified (password mode)
            # get password and salt entry content from GUI
            password = self.gui.current_window.password_entry.get()
            salt = self.gui.current_window.salt_entry.get()
            
            # generate key
            key, salt = self.generateKey(password, salt)
        else:   # if key file is specified
            # open key file
            with open(key_file, "r") as f:
                key = f.read()
                key = b64decode(bytes(key.encode("utf-8")))   # convert key to bytes and decode it
        
        # decrypt volume
        try:
            self.decrypt.init()
        except Exception as e:
            self.log.error(str(e), "decrypt")
            self.gui.pop.showerror("Decrypt error", str(e))
            return False

        try:
            self.decrypt.decryptArchive(key)
        except Exception as e:
            self.log.error(str(e), "decrypt")
            self.gui.pop.showerror("Decrypt error", str(e))
            return False
        
        try:
            self.decrypt.extractArchive()
        except Exception as e:
            self.log.error(str(e), "decrypt")
            self.gui.pop.showerror("Decrypt error", str(e))
            return False
        
        # log
        self.log.success("Succes to decrypt volume !", parents.SYSTEM)
        self.gui.pop.showinfo("Success", "Succes to decrypt volume !")
        
        return True
    
    def getVolume(self):
        '''
        Get current used volume
        '''
        drive = os.getcwd()
        
        if len(drive) >= 4:   # if the program is not at the root of the key
            raise Exception("script isn't at the root of the key")
        
        try:   # remove / or \ if exist
            drive.replace("/", "")
            drive.replace("\\", "")
        except:
            None
        
        # check if isn't the system drive
        if drive == os.getenv("SystemDrive"):
            raise Exception("script is on the system drive")
        
        return drive
    
    def generateKey(self, password=None, salt=None):
        '''
        Generate key with a specific password/salt or nothing
        '''        
        if password == None:
            key = Fernet.generate_key()   # generate random key
            
            return key
        else:
            # generate salt
            if salt == None:   # if salt isn't specified
                salt = str(randint(10000000, 99999999))
            
            # create kdf
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=bytes(salt.encode("utf-8")),
                iterations=480000,
            )
            
            # generate key
            key = urlsafe_b64encode(kdf.derive(bytes(password.encode("utf-8"))))
        
        return key, salt

    def switchDebug(self):
        '''
        Switch log_saving status
        '''
        if self.log.log_saving:   # if enabled
            self.log.log_saving = False   # disable
            self.log.success("Debug file disabled !", parents.DEBUG)
            self.gui.pop.showinfo("Debug", "Debug file disabled !")
        else:
            self.log.log_saving = True   # enable
            self.log.success("Debug file enabled !", parents.DEBUG)
            self.gui.pop.showinfo("Debug", "Debug file enabled !")
    
        return True


if __name__ == "__main__":
    # run program
    main = Main()