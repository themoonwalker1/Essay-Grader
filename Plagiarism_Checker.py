from strsimpy import *

# Closer to 1 --> More Plagariazed
class color:
    LIGHTBLUE = "\033[94m"
    BOLD = '\033[1m'
    END = '\033[0m'

jaccard = Jaccard(2)
#
# Can think of corpus as a list of essays in a way
# corpus=[
# "In the CV model, there's a key difference between Gaussian quantum doors and non-Gaussian ones. . The Gaussian gates are the easy operations for a quantum computer with a CV in many ways. The easiest Gaussian single-mode doors are rotation, displacement, and squeezing",
# "There is a key distinction in the CV model between the quantum gates which are Gaussian and those which are not. In many ways, the Gaussian gates are the “easy” operations for a CV quantum computer. The simplest single-mode Gaussian gates are rotation "
# ]
# print(str(100 * jaccard.similarity(corpus[0], corpus[1])))

corpus=[
"The thick foliage and intertwined vines made the hike nearly impossible. It had been sixteen days since the zombies first attacked.",
"It had been sixteen days since the zombies first attacked.",
"The climb was very difficult because of the dense forest on top of the mountain. More than 2 weeks passed since the Undead rose up.",
"He was surprised that his immense laziness was inspirational to others.",
"Lightning Paradise was the local hangout joint where the group usually ended up spending the night.I may struggle with geography, but I'm sure I'm somewhere around here.",
]
#
# corpus=[
# "night",
# "day",
# ]


scores = []
for i in range(0, len(corpus)):
    for j in range(0, len(corpus)):
        if 1 > jaccard.similarity(corpus[i], corpus[j]) > 0.5:
            print("Student " + str(i+1) + " and Student " + str(j+1) + ": " + color.LIGHTBLUE + color.BOLD + str(jaccard.similarity(corpus[i], corpus[j]) + 0.11) + color.END)
        elif jaccard.similarity(corpus[i], corpus[j]) == 1:
            print("Student " + str(i+1) + " and Student " + str(j+1) + ": " + color.LIGHTBLUE + color.BOLD + str(jaccard.similarity(corpus[i], corpus[j])) + color.END)
        else:
            if jaccard.similarity(corpus[i], corpus[j]) - 0.1 <= 0:
                print("Student " + str(i+1) + " and Student " + str(j+1) + ": " + color.LIGHTBLUE + color.BOLD + str(0.0) + color.END)
            else:
                print("Student " + str(i+1) + " and Student " + str(j+1) + ": " + color.LIGHTBLUE + color.BOLD + str(jaccard.similarity(corpus[i], corpus[j]) - 0.11) + color.END)
        scores.append(jaccard.similarity(corpus[0], corpus[i]))




