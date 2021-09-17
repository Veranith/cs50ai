import os
import random
import re
import sys
import random
from typing import FrozenSet
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probabilityDistribution = {}
    probabilityAllPages = (1 - damping_factor) * (1 / len(corpus))
    numPageLinks = len(corpus[page])

    if numPageLinks > 0:
        for i in corpus:
            probabilityDistribution[i] = probabilityAllPages
    
        probabilityPageLinks = damping_factor * (1 / numPageLinks)
        for j in corpus[page]:
            probabilityDistribution[j] += probabilityPageLinks
    else:
        for i in corpus:
            probabilityDistribution[i] = 1 / len(corpus)

    for i in probabilityDistribution:
        probabilityDistribution[i] = round(probabilityDistribution[i], 4)

    return probabilityDistribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page = random.choice(list(corpus.keys()))

    data = []

    for i in range(0, n):
        sample = transition_model(corpus, page, damping_factor)
        page = random.choices(list(sample.keys()), list(sample.values()))[0]
        data.append(page)
     
    count = Counter(data)
    for i in count:
        count[i] /= n

    return count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = len(corpus)
    pageRank = dict()

    # Set inital pageRanks. All pages have equal possibility
    for item in corpus.keys():
        pageRank[item] = 1 / pages

    parents = getLinkParents(corpus)

    return iterate_pagerank_sub(corpus, damping_factor, pageRank, parents)
    

def iterate_pagerank_sub(corpus, damping_factor, pageRank, parents):
    
    newPageRank = dict()
    firstEqSection = round((1 - damping_factor) / len(corpus), 5)

    for page in pageRank:
        result = 0
        
        for parent in parents[page]:
            result += pageRank[parent] / (len(corpus[parent]) if len(corpus[parent]) > 0 else 1)

        newPageRank[page] = round(firstEqSection + (damping_factor * result),6)
    
    if iterateCheckDifference(newPageRank, pageRank):
        return newPageRank
    else:
        return iterate_pagerank_sub(corpus, damping_factor, newPageRank, parents)


def iterateCheckDifference(newPageRank, pageRank):
    for page in pageRank:
        if abs(pageRank[page] - newPageRank[page]) > .0001:
            return False
    return True


def getLinkParents(corpus):
    parents = {}
    
    for page in corpus.keys():
        parents[page] = set()
        for item in corpus.keys():
            if page in corpus[item]:
                parents[page].add(item)

    return parents


if __name__ == "__main__":
    main()
