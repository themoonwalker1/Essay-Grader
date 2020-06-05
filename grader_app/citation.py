import re

class APACitation():
    def __init__(self):
        self.authors = []
        self.year = ""
        self.title = ""
        self.journal = ""
        self.volume = None
        self.issue = None
        self.pageStart = None
        self.pageEnd = None
        self.url = ""
    
    def checkAPAcitation(self, citation):
        cursor = 0

        while True:
            ascii_value = ord(citation[cursor])

            #check if the current character is not " &-'." or any alphanumeric in English or Latin-1

            if ascii_value == 32 or 38 <= ascii_value <= 39 or 45 <= ascii_value <= 46 or 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122 or 192 <= ascii_value <= 255:
                cursor += 1
            else:
                break
                    #RIGHT NOW CURSOR SHOULD EQUAL TO "(", IF IT DOESNT MARK ERROR 

        author_section = ""
        if citation[cursor - 1] == " ":
            author_section = citation[:cursor - 1]
        else:
            #TODO: mark error
            pass
        
        #TODO: check to see if author section has formatting when it shouldn't (italics, bold, etc)
        
        #single author case
        #get rid of any non-English alphabetic characters (vowels w/ accents, etc.)
        filtered_authors = ""
        
        for i in author_section:
            if(192 <= ord(i) <= 255):
                filtered_authors += 'X'
            else:
                filtered_authors += i

        #check for single author
        if not re.match("^[A-Z][a-z]+[,][ ][A-Z][.]$", filtered_authors) \
        or not re.match("^[A-Z][A-Za-z-']+[.]$", filtered_authors) \
        or not re.match("^[a-z]['][A-Z][a-z]+[,][ ][A-Z][.][ ][A-Z][.]$", filtered_authors) \
        or not re.match("^[a-z]['][A-Z][a-z]+[,][ ][A-Z][.]$", filtered_authors) \
        or not re.match("^[A-Z][a-z]+[,][ ][A-Z][.][ ][A-Z][.]$", filtered_authors) \
        or not re.match("^[A-Z][a-z]+[,][ ][A-Z][.][-][A-Z][.]$", filtered_authors):
            if " " in filtered_authors:
                tokens = filtered_authors.split(" ")
                for token in tokens:
                    if not re.match("^[A-Z][A-Za-z-']+[.]$", token):
                        break
                else:
                    #TODO: add filtered_authors to author field
                    pass

        #one author with multiple parts in name
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
                        #add name[0] to authorLastName field
                        pass
        except:
            pass

        
        #check for multiple authors
        author_section = author_section[:-1]
        delimiters = [' & ', ' ... ', ' . . . ']
        delim = ""

        for i in delimiters:
            if i in author_section:
                delim = i
                break
        else:
            #mark error: wrong formatting before last author (last author should be preceded by a '&' or ellipsis)
            pass

        author_section = author_section.replace(delim, " ", 1)

        if ", " not in author_section:
            #mark error, exit out cuz you cant salvage anymore
            pass

        authors = author_section.split(", ")

        for i in range(len(authors)):
            author = authors[i]

            #last name case
            if i % 2 == 0:
                for ch in author:
                    if not (ord(ch) == 32 or ord(ch) == 39 or ord(ch) == 45 or 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122 or 192 <= ord(ch) <= 255):
                        #mark error: bad formatting in author last name
                        break
                else:
                    #add author to the authorLastNames field
                    pass
            else:
                #get rid of all Latin-1 characters in author first name
                filtered_author = ""

                for ch in author:
                    if(192 <= ord(ch) <= 255):
                        filtered_author += 'X'
                    elif not (45 <= ord(ch) <= 46 or 65 <= ord(ch) <= 90):
                        #mark error, exit out cuz you cant salvage
                        pass
                    else:
                        filtered_author += ch

                if not re.match("^[A-Z][.]$", filtered_author) \
                or not re.match("^[A-Z][.][ ][A-Z][.]$", filtered_author) \
                or not re.match("^[A-Z][.][-][A-Z][.]$", filtered_author):
                    #mark error: bad formatting in author initials
                    pass

        #if len(authorLastNames) > 20:
            #mark error

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



'''
algorithm for APA citation: 

get match length: https://stackoverflow.com/questions/28304320/find-length-of-string-matched-by-regex


WRAP ENTIRE METHOD IN TRY CATCH AND MARK THE THING WITH AN ERROR IF THERE'S AN EXCEPTION


have a cursor variable to store current position in string

let x = index of first character outside ascii values 32, 38, 45-46, 65-90, 97-122, 192-255

//check authors:

Extract text from first character to x:

    if any of the characters here have formatting other than normal text (like italics, bold, etc.):
        mark error

    if single author:
        def single author:
            (create a temp string) replace all characters from 192-255 with 'X'
            if not matches ^[A-Z][a-z]+[,][ ][A-Z][.] or ^[A-Z][A-Za-z-]+[.]$ or ^[A-Z][a-z]+[,][ ][A-Z][.][ ][A-Z][.] or ^[A-Z][a-z]+[,][ ][A-Z][.][-][A-Z][.]
                if contains " ":
                    split on " "
                    for each thing in split:
                        everything here must match ^[A-Z][A-Za-z-']+[.]$

                elif contains " ":
                    split on " "
                    everything here must match ^[A-Z][a-z]+

    if no error in the above, store the name in self.authors

    FOR THE & OR ...: STORE THE ACCEPTABLE CHARACTERS IN A LIST AND FOR LOOP THROUGH THEM AND SEE IF CONTAINS
    if contains ' & ' xor contains (" . . . " or (" " + character 8230 + " ") or " ... ":
        remove that character from the string, leaving one space in its place
    elif it contains those characters.trim():
        mark error: there should be a space before and after the delimiter that precedes the last author (either ampersand or ellipsis)
    else:
        mark error: wrong formatting before last author (last author should be preceded by a '&' or ellipsis)

    split on ', ':
        even indices marked as last names, odd indices marked as initials:
            if even index contains a character outside ascii values 45, 65-90, 97-122, 192-255
                mark error: bad formatting in author last name
            else: 
                store last name in authors list

            if odd index:
                replace all characters from 192-255 with 'X'

                if contains a character outside ascii values 45-46, 65-90, 97-122:
                    mark error: bad formatting in author initials
                elif not matches ^[A-Z][.]$ or ^[A-Z][.][ ][A-Z][.]$ or ^[A-Z][.][-][A-Z][.]$ :
                    mark error: bad formatting in author initials

    if len(authors) > 20:
        mark error

    if '. (' not in string:
        mark error

questions to ask dr. boswell: is ellipsis a single character or three spaced periods


//check year:

if x != '(':
    mark error in year
else:
    year = characters from x up until (not including) you reach ')'
    if theres any special formatting in year, mark error

//check title:

if ". " + [start of italics] not in string:
    mark error, exit out (pretty hard to salvage from here)

go from current position until ". " + [start of italics]:

    if anythings italicized, the italicized portion must be <= 2 words, the first word must be capitalized and the second word (if applicable) must be lowercase

    store the string in a temp string
    remove all italicized things from that temp string
    split that string on " ":
        truecase and check to see if each word in split should be capitalized (remember the case after the colon):
            if bad capitalization: throw error
        
go from current position until ", " + [number]:
    if ", " + [number] isn't there, mark error
    string should be italicized
    add string to journal field

go from current position to "("
    if no "(", mark error
    number should be italicized
    add it as a string to the volume number field

go from current position to "),":
    if no "),", mark error
    if theres any italics past the volume number, mark error
    add number to the issue number field

go from current position to ".":
    if no ".", mark error
    the string should match [0-9]+[-][0-9]+ or [0-9]+, no formatting

if not end of text:
    if 'https://' in text or 'http://' in text:
        start at beginning of url and go to end, add this to url


'''