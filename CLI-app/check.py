def install():
    import os
    os.system("pip install -r requirements.txt")

def check():

    """
        @author: Brandon Wright - Barnold8

        This function does a simple file check to see if the program has been ran for the first time or not. If it has, it will do nothing and exit cleanly.
        Otherwise, it will run the command to install the requirements given "requirements.txt", this is so the dependencies can be installed at the first run of the program.

        I did all of this so the filesize of the software in total wasnt something massive. 
    """

    try:
        with open("startup.txt","r+") as file:
            contents = file.readlines()
            if len(contents) == 0 or int(contents[0]) != 1:
                install()
                file.write("1")
    except FileNotFoundError as error:
        with open("startup.txt","w") as file:
            install()
            file.write("1")     

check()