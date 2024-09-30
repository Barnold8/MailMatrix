

# How to install and run


## CLI

First you will need the latest version of [python](https://www.python.org/downloads/)

If you are unsure if you have python already installed on your system, try using the command 

````
python --version
````

You should see something like ``Python 3.12.6``

After this ``cd`` into the ``CLI-app`` directory and run 

```
python -m venv .
./Scripts/activate (this should work on both Windows and Linux)
python main.py
```

When you want to quit the software environment, you can simply type deactivate (you need to be outside of MailMatrix when you do this, I am yet to implement a quitting function for the software so I will update this when there is one)


