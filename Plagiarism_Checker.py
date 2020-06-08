from strsimpy import *

# Closer to 1 --> More Plagariazed 
class color:
    LIGHTBLUE = "\033[94m"
    BOLD = '\033[1m'
    END = '\033[0m'

jaccard = Jaccard(1)

# Can think of corpus as a list of essays in a way
# corpus=[
# "In the CV model, there's a key difference between Gaussian quantum doors and non-Gaussian ones. . The Gaussian gates are the easy operations for a quantum computer with a CV in many ways. The easiest Gaussian single-mode doors are rotation, displacement, and squeezing",
# "There is a key distinction in the CV model between the quantum gates which are Gaussian and those which are not. In many ways, the Gaussian gates are the “easy” operations for a CV quantum computer. The simplest single-mode Gaussian gates are rotation "
# ]
# print(str(100 * jaccard.similarity(corpus[0], corpus[1])))

corpus=[
"The thick foliage and intertwined vines made the hike nearly impossible. It had been sixteen days since the zombies first attacked.",
"It had been sixteen days since the zombies first attacked.",
"Happiness can be found in the depths of chocolate pudding. She did a happy dance because all of the socks from the dryer matched. The Tsunami wave crashed against the raised houses and broke the pilings as if they were toothpicks.",
"He was surprised that his immense laziness was inspirational to others.",
"Lightning Paradise was the local hangout joint where the group usually ended up spending the night.I may struggle with geography, but I'm sure I'm somewhere around here.",
" ", 
]



scores = []
for i in range(0, len(corpus)):
	for j in range(0, len(corpus)):
		print("Student " + str(i+1) + " and Student " + str(j+1) + ": " + color.LIGHTBLUE + color.BOLD + str(jaccard.similarity(corpus[i], corpus[j])) + color.END)
		scores.append(jaccard.similarity(corpus[0], corpus[i]))

