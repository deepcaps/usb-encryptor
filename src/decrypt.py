from cryptography.fernet import Fernet
from hashlib import sha256
import tempfile
import shutil
import csv
import os


class Decrypt():
    def __init__(self, volume):        
        # set variables
        self.volume = volume
        self.id = None
        self.hash = None
        
        self.archive_path = None
        
        # set tagid path
        self.tagid_path = os.path.join(self.volume, "tagid")
    
    def init(self):
        '''
        Init Decrypt : load variables
        '''
        try:
            self.id, self.hash = self.readTAGID()   # read TAGID file
            self.archive_path = os.path.join(self.volume, self.id)
        except Exception as e:
            raise Exception("Error reading TAGID file : " + str(e))
                
        return True
    
    def decryptArchive(self, key):
        '''
        Decrypt archive with key
        '''
        # verify integrity of archive
        if self.getHash() != self.hash:   # if file hash doesn't match
            raise Exception("Invalid hash")
        
        # load key
        fernet = Fernet(key)
        
        # open archive in read mode
        with open(self.archive_path, "rb") as f:
            original = f.read()

        # decrypt archive
        try:
            decrypt = fernet.decrypt(original)
        except Exception as e:
            raise Exception("Invalid credentials " + str(e))
        
        # write changes
        with open(self.archive_path, "wb") as f:
            f.write(decrypt)
        
        return True
    
    def extractArchive(self):
        '''
        Extract files to volume
        '''
        try:
            with tempfile.TemporaryDirectory() as tempdir:   # create temporary directory
                # make working directory
                tempdir = os.path.join(tempdir, "working_dir")
                
                # extract archive
                shutil.unpack_archive(self.archive_path, tempdir, "tar")
                
                # copy to volume
                shutil.copytree(tempdir, self.volume, dirs_exist_ok=True)
        except Exception as e:
            raise Exception("Unable to read archive : " + str(e))
        
        try:
            # delete archive and tagid files
            os.remove(self.tagid_path)
            os.remove(self.archive_path)
        except Exception as e:
            raise Exception("Unable to remove old files : " + str(e))
            
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
    
    def readTAGID(self):
        '''
        Read informations of TAGID file
        '''
        with open(self.tagid_path, "r") as fb:
            f = csv.reader(fb, delimiter=";")   # open file

            # load variables
            for row in f:
                id = row[0]
                hash = row[1]
        
        return id, hash