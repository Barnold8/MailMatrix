import check # does all the dependency checking
from GMail.Gmail import *


if __name__ == "__main__":
    gclient = GMAIL_CLIENT()

    for email in gclient.get_recent_emails():
        print(email)




