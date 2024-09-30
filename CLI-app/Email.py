class Email:

    m_sender    = None # Who sent the email
    m_subject   = None # What the subject is 
    m_platform  = None # Where this Email came from
    m_timeStamp = None # What time was this email sent

    def __init__(self, sender= None, subject = None, platform=None, timestamp= None) -> None:

        self.m_sender    = sender
        self.m_subject   = subject
        self.m_platform  = platform
        self.m_timeStamp = platform

    # SETTERS

    def setSender(self,sender):
        self.m_sender = sender

    def setSubject(self, subject):
        self.m_subject = subject

    def setPlatform(self, platform):
        self.m_platform = platform 

    def setTimeStamp(self, timeStamp):
        self.m_timeStamp = timeStamp

    # SETTERS

    # GETTERS

    def getSender(self) -> any:
        return self.m_sender

    def getSubject(self) -> any:
        return self.m_subject

    def getPlatform(self) -> any:
        return self.m_platform

    def getTimeStamp(self) -> any:
        return self.m_timeStamp

    # GETTERS
        
