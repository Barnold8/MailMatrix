class Email:

    m_sender    = None # Who sent the email
    m_subject   = None # What the subject is 
    m_platform  = None # Where this Email came from
    m_timeStamp = None # What time was this email sent


    def __init__(self, sender, subject, platform, timestamp) -> None:

        self.m_sender    = sender
        self.m_subject   = subject
        self.m_platform  = platform
        self.m_timeStamp = platform
        
