import platform
import thread
import aes
import getpass
import os
import string
import random
import hashlib
import sys
import time
import os

class Vault:
    global lastcommand
    lastcommand = time.time()

    def __init__(self):
        self.password = None
        self.data = ""
        self.file_ = "file.db"
        self.commands = {

            "add":self.add,
            "read":self.read_passwords,
            "help":self.help_,
            "remove":self.remove,
            "search":self.search,
        }

    def help_(self):
        print """

        add - Adds a new password
        remove - remove a password
        read - Shows all saved passwords
        search - Search for specific Password based on description
        help - Displays this prompt                                                                                                                                                                    

        """
    
    def main(self):
        if not os.path.exists(self.file_):
            self.create()
        if not self.password:
            self.decryptData()
        thread.start_new_thread(self.inactivity, ())
        global lastcommand
        while True:
            command = raw_input("Vault Shell> ")
            lastcommand = time.time()
            if command in self.commands:
                self.commands[command]()
            elif command == "exit":
                sys.exit("Bye!")
    
    def inactivity(self):
        global lastcommand
        while True:
            if time.time() - lastcommand > 30:
                if platform.system() == "Linux":
                    os.system("clear")
                elif platform.system() == "Windows":
                    os.system("cls")
                os._exit(1)

    def search(self):
        searchTerm = raw_input("Input keywords to search for: ").lower()
        for x in self.data.split("\n"):
            z = x.lower()
            if z.find(searchTerm) != -1:
                print x
            else:
                for y in searchTerm.split():
                    if z.find(searchTerm) != -1:
                        print x
                        break
    def create(self):
        print "No passwords found stored, let's set it up."
        password = getpass.getpass("Create Password: ")
        confirm = getpass.getpass("Confirm Password: ")
        if password != confirm:
            print "Passwords did not match, restarting."
            self.create()
            return

        self.password = password
        self.add()

    def read_passwords(self):
        print self.data

    def remove(self):
        data = raw_input("Paste complete password data: ")
        self.data = self.data.replace(data+"\n", '')
        self.write()
        print "Password Removed!"

    def add(self):
        title = raw_input("Title given to password: ")
        password = getpass.getpass("Enter password (leave blank to generate random): ")
        confirm = getpass.getpass("Confirm Password: ")
        if password != confirm:
            print "Passwords did not match, restarting."
            self.add()
            return

        if not password:
            length = raw_input("Short or long password? ").lower()
            if length == "short":
                password = self.generate()[:8]
            elif length != "short" and length != "long":
                print "Okay, I don't know what that means so I'll just make it long."
            if not password:
                password = self.generate()
            print "Password is: {}".format(password)
        
        self.data += "{0} - {1}\n".format(title, password)
        self.write()

    def write(self):
        if not self.password:
            return

        data = aes.encryptData(hashlib.md5(self.password).hexdigest(), self.data)
        with open(self.file_, "wb") as file:
            file.write(data)
        print "Data saved!"

    def decryptData(self):
        self.password = getpass.getpass("Password: ")
        with open(self.file_, "rb") as file:
            try:
                self.data = aes.decryptData(hashlib.md5(self.password).hexdigest(), file.read())
            except:
                print "Password incorrect"
                self.decryptData()

    def generate(self):
        return ''.join([random.choice(string.uppercase+string.lowercase+string.digits) for x in range(20)])



if __name__ == "__main__":
    Vault().main()
