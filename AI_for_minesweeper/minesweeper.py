import itertools
import math
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.count

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return len(self) - self.count + 1

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.cells.discard(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)

        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                sentence.count = sentence.count - 1

        cells = {}
        # add the neighbouring cells
        if 7 > cell[0] > 0 and 7 > cell[1] < 0:
            cells = {(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1]),
                     (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] + 1), (cell[0] - 1, cell[1] - 1),
                     (cell[0] + 1, cell[1] - 1), (cell[0] - 1, cell[1] + 1)}

        elif cell not in {(0, 0), (0, 7), (7, 0), (7, 7)}:
            if cell[0] == 0:
                cells = {(cell[0], cell[1] + 1), (cell[0] + 1, cell[1]), (cell[0], cell[1] - 1),
                         (cell[0] + 1, cell[1] - 1), (cell[0] + 1, cell[1] + 1)}
            elif cell[0] == 7:
                cells = {(cell[0] - 1, cell[1]), (cell[0], cell[1] + 1), (cell[0], cell[1] - 1),
                         (cell[0] - 1, cell[1] + 1), (cell[0] - 1, cell[1] - 1)}
            elif cell[1] == 0:
                cells = {(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1), (cell[0] - 1, cell[1]),
                         (cell[0] - 1, cell[1] + 1), (cell[0] + 1, cell[1] + 1)}
            elif cell[1] == 7:
                cells = {(cell[0] + 1, cell[1]), (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1),
                         (cell[0] - 1, cell[1] - 1), (cell[0] + 1, cell[1] - 1)}
        elif cell == (0, 0):
            cells = {(cell[0], cell[1] + 1), (cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] + 1)}
        elif cell == (0, 7):
            cells = {(cell[0], cell[1] - 1), (cell[0] + 1, cell[1]), (cell[0] + 1, cell[1] - 1)}
        elif cell == (7, 0):
            cells = {(cell[0], cell[1] + 1), (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] + 1)}
        else:
            cells = {(cell[0], cell[1] - 1), (cell[0] - 1, cell[1]), (cell[0] - 1, cell[1] - 1)}

        # append sentence to knowledge base
        self.knowledge.append(Sentence(cells, count))

        # infer knowledge
        self.infer_knowledge()
        
        count = 0
        flag = 1
        
        # keep filtering information till none of the sentences can be removed         
        while flag:
            senlen = len(self.knowledge)
            for sentence in self.knowledge:
                if sentence.count == 0 or len(sentence.cells) == sentence.count:
                    self.infer_knowledge()
                else:
                    count = count + 1
            if count == senlen:
                flag = 0

    def infer_knowledge(self):

        # contains the safe cells that can be removed
        removable_safe_cells = {}

        # find safe cells and mines using logic
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                self.mines.update(sentence.cells)
                self.knowledge.remove(sentence)
            elif sentence.count == 0:
                self.safes.update(sentence.cells)
                removable_safe_cells = sentence.cells
                self.knowledge.remove(sentence)

        # if the safe cells are found in any of the sentences, they can be removed.
        for cell1 in removable_safe_cells:
            for sentence1 in self.knowledge:
                if cell1 in sentence1.cells:
                    sentence1.cells.remove(cell1)

        # create new sentences using existing knowledge
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2:
                    if sentence1.cells in sentence2.cells:
                        sentence2.count = sentence2.count - sentence1.count
                        sentence2.remove(sentence1)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # choose random i and j
        i = random.randrange(self.height)
        j = random.randrange(self.width)
        count = 0
        while 1:
            # if it is not a mine and not an existing move, then return tuple
            if (i, j) not in self.mines and (i, j) not in self.moves_made:
                # add to the moves that are already made
                self.moves_made.add((i, j))
                return (i, j)
            count = count + 1
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            # if there is no random move return None
            if count > 10000:
                return None

