import re
import requests
from enum import Enum


class APACitationStatus(str, Enum):
    AUTHOR = "author"
    YEAR = "year"
    TITLE = "title"
    JOURNAL = "journal"
    VOLUME = "volume number"
    ISSUE = "issue number"
    PAGES = "page number"
    URL = "url"


class APACitation():
    def __init__(self):
        self.authors = []
        self.year = ""
        self.title = ""
        self.journal = ""
        self.volume = ""
        self.issue = ""
        self.pages = []
        self.url = ""
        self.citation_status = APACitationStatus.AUTHOR

    def checkAPAcitation(self,
                         citation):  # NOTE: when implementing, wrap the method in a try catch and print out any error + the citation status
        cursor = 0

        while True:
            ascii_value = ord(citation[cursor])

            # check if the current character is not " &-'." or any alphanumeric in English or Latin-1

            if ascii_value == 32 or 38 <= ascii_value <= 39 or 45 <= ascii_value <= 46 or 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122 or 192 <= ascii_value <= 255:
                cursor += 1
            else:
                break
                # RIGHT NOW CURSOR SHOULD EQUAL TO "(", IF IT DOESNT MARK ERROR

        if citation[cursor] != "(":
            raise Exception("Bad formatting in the author section: unable to find open parenthesis.")

        author_section = ""
        if citation[cursor - 1] == " ":
            author_section = citation[:cursor - 1]
        else:
            raise Exception("Bad formatting in the author section: '" + author_section + "'")

        # TODO: check to see if author section has formatting when it shouldn't (italics, bold, etc)

        # single author case
        # get rid of any non-English alphabetic characters (vowels w/ accents, etc.)
        filtered_authors = ""

        for i in author_section:
            if (192 <= ord(i) <= 255):
                filtered_authors += 'X'
            else:
                filtered_authors += i

        # check for single author
        if not re.match("^[A-Z][a-z]+[,][ ][A-Z][.]$", filtered_authors) \
                or not re.match("^[A-Z][A-Za-z-']+[.]$", filtered_authors) \
                or not re.match("^[a-z]['][A-Z][a-z]+[,][ ][A-Z][.][ ][A-Z][.]$", filtered_authors) \
                or not re.match("^[a-z]['][A-Z][a-z]+[,][ ][A-Z][.]$", filtered_authors) \
                or not re.match("^[A-Z][a-z]+[,][ ][A-Z][.][ ][A-Z][.]$", filtered_authors) \
                or not re.match("^[A-Z][a-z]+[,][ ][A-Z][.][-][A-Z][.]$", filtered_authors):
            if " " in filtered_authors and filtered_authors[-1] == ".":
                tokens = filtered_authors[:-1].split(" ")
                for token in tokens:
                    if not re.match("^[A-Z][A-Za-z-']+$", token):
                        break
                else:
                    self.authors.append(filtered_authors)

        # one author with multiple parts in name
        try:
            name = filtered_authors.split(", ")
            if len(name) == 2:
                lastName = name[0].split(" ")
                for i in lastName:
                    if not re.match('^[a-z]+$') and not re.match('^[A-Z][a-z]+$'):
                        break
                else:
                    firstName = name[1]
                    if re.match("^[A-Z][.][ ][A-Z][.]$", firstName) is not None \
                            or re.match("^[A-Z][.][-][A-Z][.]$", firstName) is not None \
                            or re.match("^[A-Z][.]$", firstName) is not None:
                        self.authors.append(name[0])
        except:
            pass

        # check for multiple authors
        if self.authors == []:
            author_section = author_section[:-1]
            delimiters = [' & ', ' ... ', ' . . . ']
            delim = ""

            for i in delimiters:
                if i in author_section:
                    delim = i
                    break
            else:
                raise Exception(
                    "Wrong formatting before last author (last author should be preceded by a '&' or ellipsis).")

            author_section = author_section.replace(delim, " ", 1)

            if ", " not in author_section:
                raise Exception("Bad formatting in the author section: '" + author_section + "'")

            authors = author_section.split(", ")

            for i in range(len(authors)):
                author = authors[i]

                # last name case
                if i % 2 == 0:
                    for ch in author:
                        if not (ord(ch) == 32 or ord(ch) == 39 or ord(ch) == 45 or 65 <= ord(ch) <= 90 or 97 <= ord(
                                ch) <= 122 or 192 <= ord(ch) <= 255):
                            raise Exception("Bad formatting in the author section: '" + author + "'")
                    else:
                        self.authors.append(author)
                else:
                    # get rid of all Latin-1 characters in author first name
                    filtered_author = ""

                    for ch in author:
                        if (192 <= ord(ch) <= 255):
                            filtered_author += 'X'
                        elif not (45 <= ord(ch) <= 46 or 65 <= ord(ch) <= 90):
                            raise Exception("Bad formatting in the author section: '" + filtered_author + "'")
                        else:
                            filtered_author += ch

                    if not re.match("^[A-Z][.]$", filtered_author) \
                            or not re.match("^[A-Z][.][ ][A-Z][.]$", filtered_author) \
                            or not re.match("^[A-Z][.][-][A-Z][.]$", filtered_author):
                        raise Exception("Bad formatting in an author's initials: '" + filtered_author + "'")

        if len(self.authors) > 20:
            raise Exception("Too many authors listed (there should be a maximum of 20 authors).")

            # check the year section
        self.citation_status = APACitationStatus.YEAR

        if '. (' not in citation:
            raise Exception(
                "Error in citation formatting: the year number must be directly preceded by a period, a space, and an open parenthesis, but this was not found.")

        # move cursor to the first number in the year
        cursor += 1
        year = ""

        while citation[cursor].isalnum():
            year += citation[cursor]
            cursor += 1

        if not re.match("^[0-9]{4}$", year) or not re.match("^[0-9]{4}[a-z]$", year):
            raise Exception("Bad formatting in the year section: '" + year + "'")

        self.year = year

        if ". <i>" not in citation[cursor + 4:]:
            raise Exception("The journal title should be italicized.")

        # check title
        self.citation_status = APACitationStatus.TITLE

        cursor += 1

        if citation[cursor + 1: cursor + 4] == "<i>":
            cursor += 4
        elif citation[cursor + 2: cursor + 5] == "<i>":
            cursor += 5

        if not citation[cursor].isupper():
            raise Exception("The first word in the title should be capitalized.")

        title = ""

        while citation[cursor + 1: cursor + 6] != ". <i>" or citation[cursor + 1: cursor + 5] != ".<i>":
            title += citation[cursor]
            cursor += 1

        title = title.replace("<i>", "")
        title = title.replace("</i>", "")

        words = title.split(" ")

        # TODO: implement truecasing
        for word in words[1:]:
            if word[0].isalpha() and word[0].isupper():
                # mark warning: capitalized word
                pass

        cursor += 1

        self.title = " ".join(words)

        # check journal name
        self.citation_status = APACitationStatus.JOURNAL

        journal = ""
        while citation[cursor + 1: cursor + 3] != ", ":
            journal += citation[cursor]
            cursor += 1

        if "<i>" not in journal or "</i>" in journal:
            raise Exception(
                "The journal title should be italicized, and the italics should not stop until the end of the volume number.")

        journal = journal.replace("<i>", "")

        self.journal = journal

        if citation[cursor: cursor + 2] != ", ":
            raise Exception(
                "There should be a comma and a space after the journal title, and both of these should be in italics.")

        cursor += 2

        # check for volume number
        self.citation_status = APACitationStatus.VOLUME

        volume = ""
        while citation[cursor] != "(":
            volume += citation[cursor]
            cursor += 1

        if "</i>" not in volume:
            raise Exception("The volume number should be italicized.")

        volume = volume.replace("</i>", "")
        if not volume.isdigit():
            raise Exception("Bad formatting in the volume number: '" + volume + "'")

        self.volume = volume

        cursor += 1

        # check for issue number
        self.citation_status = APACitationStatus.ISSUE

        issue = ""
        while citation[cursor] != ")":
            issue += citation[cursor]
            cursor += 1

        if not issue.isdigit():
            raise Exception("Bad formatting in the issue number: '" + issue + "'")

        self.issue = issue

        if citation[cursor + 1: cursor + 3] != ", ":
            raise Exception("The issue number should have a comma and a space after the ending parenthesis.")

        cursor += 3

        # check for page number
        self.citation_status = APACitationStatus.PAGES

        pages = ""
        pageNumbers = []

        while citation[cursor] != ".":
            pages += citation[cursor]
            cursor += 1

        if not re.match("^[0-9]+[-][0-9]+$", pages) or not re.match("^[0-9]+$", pages):
            raise Exception("Bad formatting in the page number section: '" + pages + "'")

        if "-" in pages:
            pageNumbers = pages.split("-")
        else:
            pageNumbers = [pages]

        self.pages = pageNumbers

        # check url
        self.citation_status = APACitationStatus.URL

        if "http://" in citation or "https://" in citation:
            cursor += 1
            url = citation[cursor:]
            response = requests.get(url)
            if response.status_code >= 400:
                raise Exception("Invalid URL: '" + url + "'")

            self.url = url


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
        self.dateOfAccess = None
