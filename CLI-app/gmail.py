import google.auth
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
KEYS = "keys/"


class GMAIL_CLIENT:
   
    m_creds = None

    def __init__(self, grab= False) -> None:
        
        self.creds = self.grab_credentials() if self.m_creds == None and grab else self.m_creds # on init of object, grab credentials


    def grab_credentials(self) -> any:
        """
            @author : Brandon Wright - Barnold88

            This function checks for a user token to be stored locally on the host machine. Later down the line, support for multiple user accounts
            could be implemented looking for a user token for a specific account on a SQLite database. 

            If no token is found, the user will be redirected to the google login auth webpage, this will then send the token to the program which
            is stored in the keys directory. This is not secure and should not be trusted as so for now

            :return: credentials (not sure of type, type hint of "any")
        """
    
        if os.path.exists(f"{KEYS}token.json"):
            creds = Credentials.from_authorized_user_file(f"{KEYS}token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{KEYS}client_secret.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(f"{KEYS}token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def show_all_threads(self, number_min = 1) -> None:
        """
            @author Brandon Wright - Barnold88

            :param number_min: This parameter dictates how many emails should be in a thread for it to be displayed, this allows for basic filtering. The parameter is defaulted
            to 1 to allow defaults.

            This function will grab ALL of the emails found on a user account with no respect to specific thread - i.e junk,trash,important etc
            
            It will then display how many nested emails are within that thread. Unfortunately you cannot expand into these threads. 

            :return: None
        """

        self.creds = self.grab_credentials() if self.m_creds == None else self.m_creds
        
        try:
            # create gmail api client
            service = build("gmail", "v1", credentials=self.creds)

            threads = (
                service.users().threads().list(userId="me").execute().get("threads", [])
            )
            for thread in threads:
            #   print(f"Thread: {thread}")
                tdata = (
                    service.users().threads().get(userId="me", id=thread["id"]).execute()
                )
                nmsgs = len(tdata["messages"])

             
                if nmsgs >= number_min :
                    msg = tdata["messages"][0]["payload"]
                    subject = ""
                    for header in msg["headers"]:
                        if header["name"] == "Subject":
                            subject = header["value"]
                            break
                    if subject:  # skip if no Subject line
                        print(f"- {subject}, {nmsgs}")
                        pass
            return threads

        except HttpError as error:
            print(f"An error occurred: {error}")


    def get_recent_emails(self, max_results=5) -> None:
        """
            Fetches and displays the most recent emails along with their metadata (like date and timestamp).

            :param max_results: Number of recent emails to retrieve (default: 5)
            :return: None
        """
        self.creds = self.grab_credentials() if self.m_creds == None else self.m_creds

        try:
            # create gmail api client
            service = build("gmail", "v1", credentials=self.creds)

            # Fetch the most recent emails using 'messages.list'
            results = service.users().messages().list(userId="me", maxResults=max_results).execute()
            messages = results.get('messages', [])

            if not messages:
                print("No new emails found.")
                return

            print(f"Recent {max_results} Emails:\n")
            for message in messages:
                # Get the individual message details
                msg = service.users().messages().get(userId="me", id=message["id"]).execute()
                payload = msg.get("payload", {})
                headers = payload.get("headers", [])

                subject = ""
                from_email = ""
                date = ""

                # Extract subject, from address, and date from headers
                for header in headers:
                    if header["name"] == "Subject":
                        subject = header["value"]
                    if header["name"] == "From":
                        from_email = header["value"]
                    if header["name"] == "Date":
                        date = header["value"]

                print(f"From: {from_email}\nSubject: {subject}\nDate: {date}\n")

        except HttpError as error:
            print(f"An error occurred: {error}")