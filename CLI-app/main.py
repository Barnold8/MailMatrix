from Gmail import *


gclient = GMAIL_CLIENT()

for email in gclient.get_recent_emails():
    print(email)