class APACitation():
    def __init__(self):
        self.authors = []
        self.year = None
        self.title = ""
        self.journal = ""
        self.volume = None
        self.issue = None
        self.pageStart = None
        self.pageEnd = None
        self.url = ""

class MLACitation():
    def __init__(self):
        self.authors = []
        self.title = ""
        self.container = []
        self.otherContributors = ""
        self.version = None
        self.volume = None
        self.issue = None
        self.publisher = ""
        self.year = None
        self.pageStart = None
        self.pageEnd = None
        self.url = ""
        self.publisherLocation = None
        self.dateOfAccess = None