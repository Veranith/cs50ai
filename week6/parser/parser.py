import nltk
import sys
from nltk.tokenize import wordpunct_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# 'We arrived the day before Thursday.\n'
# N   V       Det N   P      N

# 'Holmes sat in the red armchair and he chuckled.\n'
#  N      V   P  Det Adj N Conj N V

# 'She never said a word until we were at the door here.\n'
#  N   Adv   V    Det N  Conj  N  V    P  Det N    Adv

# I had a little moist red paint in the palm of my hand.
# N V   Det Adj  Adj   Adj N     P  Det N    P  Det N

NONTERMINALS = """
S -> S Conj S
S -> NP VP | NP VP NP | VP NP
NP -> N
NP -> Det NP
NP -> Adj NP
NP -> N PP
PP -> P NP
VP -> V
VP -> V PP
VP -> Adv VP
VP -> VP Adv
"""
# NP -> N P N
# NP -> N Adv
# VP -> Adv V
# VP -> V Adv


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    tokens = nltk.word_tokenize(sentence)
    result = list()
    for word in tokens:
        word = word.lower()
        if word.isalpha():
            result.append(word)
    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    return []


if __name__ == "__main__":
    main()
