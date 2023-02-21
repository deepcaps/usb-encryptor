from cryptography.fernet import Fernet
from hashlib import sha256
from random import randint
import tempfile
import shutil
import csv
import os


class Encrypt():
    def __init__(self, volume):
        # set variables
        self.volume = volume
        
        # generate id
        self.id = str(randint(10000, 99999))
        
        # set files paths
        self.archive_path = os.path.join(self.volume, self.id)
        self.tagid_path = os.path.join(self.volume, "tagid")
    
    def createArchive(self):
        '''
        Create archive with all file in volume except script file
        '''
        try:
            with tempfile.TemporaryDirectory() as tempdir:   # create temporary directory
                # make working directory
                tempdir = os.path.join(tempdir, "working_dir")
                
                # copy all files and folder to temporary directory
                file_name = os.path.basename(__file__)
                shutil.copytree(self.volume, tempdir, ignore=shutil.ignore_patterns(file_name, "System Volume Information", "key.key", "logs"))
                
                # create archive on volume with name = id
                shutil.make_archive(self.archive_path, "tar", tempdir)
                shutil.move(self.archive_path+".tar", self.archive_path)
        except Exception as e:
            raise Exception("Unable to create archive : " + str(e))
        
        try:
            # delete old files
            for e in os.listdir(self.volume):
                if e == self.id or e == file_name or e == "key.key" or e == "System Volume Information" or e == "logs":   # if file is archive or program
                    continue
                
                e = os.path.join(self.volume, e)   # get full path of file
                
                if os.path.isdir(e):   # if element is a directory
                    shutil.rmtree(e)
                else:
                    os.remove(e)
        except Exception as e:
            raise Exception("Error during files deleting : " + str(e))
        
        return True

    def encryptArchive(self, key):
        '''
        Encrypt archive with key
        '''
        # load key
        fernet = Fernet(key)
        
        # open archive in read mode
        with open(self.archive_path, "rb") as f:
            original = f.read()

        # encrypt archive
        encrypt = fernet.encrypt(original)
        
        # write changes
        with open(self.archive_path, "wb") as f:
            f.write(encrypt)
        
        return True

    def getHash(self):
        '''
        Get hash of archive
        '''
        # make a hash object
        hash = sha256()

        # open file
        with open(self.archive_path,'rb') as f:
            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                chunk = f.read(1024)   # to avoid ram limits
                hash.update(chunk)
        
        return hash.hexdigest()

    def writeTAGID(self, hash):
        '''
        Write informations into TAGID file
        '''
        with open(self.tagid_path, "w", newline='') as fb:
            f = csv.writer(fb, delimiter=';')   # create object
            
            f.writerow([self.id, hash])   # write row
        
        return True