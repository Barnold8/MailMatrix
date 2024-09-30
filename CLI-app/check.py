def install():
    import os
    os.system("pip install -r requirements.txt")

def check():
    try:
        with open("startup.txt","w+") as file:
            contents = file.readlines()
            if len(contents) == 0 or int(contents[0]) != 1:
                install()
                file.write("1")
    except FileNotFoundError as error:
        with open("start.bool","w") as file:
            install()
            file.write("1")     

check()