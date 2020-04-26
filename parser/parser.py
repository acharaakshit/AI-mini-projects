import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word" | "assignment"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat" | "copied"
V -> "smiled" | "tell" | "were" 
"""

NONTERMINALS = """
S -> NP VP 
AdjP -> Adj | Det Adj
AdvP -> Adv | Det Adv 
NP -> N | Det NP | AdjP NP | N PP | NP AdvP | N Conj NP| N VP 
PP -> P NP | Det PP | P
VP -> V | V NP | AdvP VP | V PP | VP AdvP | Conj VP
"""

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
    # draw the tree
    tree.draw()

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # to keep track of words that don't have any alphabets
    non_alphabets = set()
    words = nltk.word_tokenize(sentence)
    for word_index in range(0, len(words)):
        if words[word_index].isalpha():
            # convert to lowercase
            words[word_index] = words[word_index].lower()
        else:
            # remove non alphabets i.e digits/special characters
            non_alphabets.add(word_index)
    if len(non_alphabets) > 0:
        for elem in non_alphabets:
            del words[elem]

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list_nodes = list()
    # get all the NP nodes
    for noun_nodes in tree.subtrees():
        if noun_nodes.label() == 'NP':
            list_nodes.append(noun_nodes)

    return list_nodes


if __name__ == "__main__":
    main()
