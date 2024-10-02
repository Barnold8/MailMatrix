

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


## Known Issues

### FileNotFoundError: [Errno 2] No such file or directory: '../keys/client_secret.json'

Unfortunately right now, I am learning how all these APIs work, as in, how I can actually work with them. A problem I am facing right now is authorisation. Google's G-mail API requires a client secret so it knows the app is legitimate, this means I either have to have every user make their own Gmail API client secret (which is not user friendly and plain stupid, or I have to find a way of authing without a client secret OR I have to make the app server sided which is also annoying and stupid). 

So to put a long story short, for now, you will need to make your own Gmail Client secret 

Here -> https://console.cloud.google.com/projectcreate? to make the API

Here -> https://console.cloud.google.com/apis/credentials/consent to make the client secret (you will need to rename it to client_secret) and have it in the "keys" directory. 

Once done, you will be able to run the app and it should ask you to sign into your gmail account through Google's OAuth screen. 

