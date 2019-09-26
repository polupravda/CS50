from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    aList = a.splitlines()
    bList = b.splitlines()
    linesList = [al for al in aList for bl in bList if al == bl]
    linesList = set(linesList)

    return linesList


def sentences(a, b):
    """Return sentences in both a and b"""

    aList = sent_tokenize(a)
    bList = sent_tokenize(b)
    linesList = [al for al in aList for bl in bList if al == bl]
    linesList = set(linesList)
    return linesList


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    linesList = [s for s in (a[i:i+n] for i in range(len(a)-n+1)) if s in b]
    linesList = set(linesList)

    return linesList