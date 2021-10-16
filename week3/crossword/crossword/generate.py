import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain in self.domains:
            invalidVars = [x for x in self.domains[domain]
                           if len(x) != domain.length]
            for invalidVar in invalidVars:
                self.domains[domain].remove(invalidVar)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get overlap and return False if there is none
        overlap = self.getVariableOverlaps(x, y)
        if overlap is None:
            return False

        # Loop through and find the words that need removed
        removeWords = set()
        for xWord in self.domains[x]:
            remove = True
            for yWord in self.domains[y]:
                if xWord[overlap[0]] == yWord[overlap[1]]:
                    remove = False
                    break
            if remove:
                removeWords.add(xWord)

        # Remove words if needed and return True if changed
        if len(removeWords) > 0:
            for word in removeWords:
                self.domains[x].remove(word)
            return True

        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = self.getAllArcs()

        # Loop through queue of arcs and revise if necissary, adds new arcs to check after changing
        while len(arcs) > 0:
            x, y = arcs.pop()
            if len(self.domains[x]) == 0 or len(self.domains[y]) == 0:
                return False
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.add((neighbor, x))

        # return false if any domains are empty
        for x in self.crossword.variables:
            if len(self.domains[x]) == 0:
                return False

        return True

    def getAllArcs(self):
        """
        Returns a list of all possible arcs in the crossword variables
        """
        arcs = set()
        for x in self.crossword.variables:
            for y in self.crossword.neighbors(x):
                arcs.add((x, y))
        return arcs

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check word length matches variable length
        for word in assignment:
            if word.length != len(assignment[word]):
                return False

        # Check overlaps for each variable
        for x in assignment:
            neighbors = self.crossword.neighbors(x)
            for y in neighbors:
                if y in assignment:
                    overlapX, overlapY = self.getVariableOverlaps( x, y)
                    if assignment[x][overlapX] != assignment[y][overlapY]:
                        return False

        # Check that each assignment word is unique
        if len(assignment) != len(set(assignment.values())):
            return False

        return True

    def getWordCount(self, var, assignment):
        wordCounts = {}
        varDomains = self.domains[var]

        for word in varDomains:
            
            neighbors = self.getNeighborsNotInAssignment(var, assignment)
            
            wordCounts[word] = self.getNeighborEliminationCount(word, var, neighbors)

        return wordCounts

    def getNeighborsNotInAssignment(self, var, assignment):
        trimmedNeighboars = set()
        neighbors = self.crossword.neighbors(var)

        if len(assignment) > 0:
            for neighbor in neighbors:
                if neighbor not in assignment:
                    trimmedNeighboars.add(neighbor)
            return trimmedNeighboars
        return neighbors

    def getNeighborEliminationCount(self, word, var, neighbors):
        count = 0
        for neighbor in neighbors:
            wordOverlap, neighborOverlap = self.getVariableOverlaps(var, neighbor)

            for x in self.domains[neighbor]:
                if word == x:
                    count += 1
                    continue
                if word[wordOverlap] != x[neighborOverlap]:
                    count += 1
        return count

    def getVariableOverlaps(self, var1, var2):
        return self.crossword.overlaps.get((var1, var2))

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if len(self.domains[var]) <= 1:
            return self.domains[var]

        wordCount = self.getWordCount(var, assignment)

        return sorted(wordCount, key=wordCount.__getitem__)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Loops through finding the variables with the least remaining values
        lowestCount = sys.maxsize
        for x in self.crossword.variables:
            if x in assignment:
                continue
            length = len(self.domains[x])
            if length < lowestCount:
                lowestCount = length
                lowestVars = [x]
            elif length == lowestCount:
                lowestVars.append(x)

        # If there are more than one with the least remaining values, find the one with most neighbors. If tie return the first.
        if len(lowestVars) > 1:
            highestCount = -sys.maxsize
            for x in lowestVars:
                neighborCount = len(self.crossword.neighbors(x))
                if neighborCount > highestCount:
                    highestCount = neighborCount
                    highestVars = [x]
                elif neighborCount == highestCount:
                    highestVars.append(x)

            return highestVars[0]

        return lowestVars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Get new unassigned var
        var = self.select_unassigned_variable(assignment)

        # Recursively try each possible value for var. Returns final assignments or None
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
