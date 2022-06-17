import itertools
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
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) == 0:
            return set(self.cells)
        return set()




    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return None


            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return None


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
        self.possible_mines = set()

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

        # making cell as safe and move made
        self.moves_made.add(cell)
        self.mark_safe(cell)

        #  adding sentece to knowledge base
        new_sentence = Sentence(cell, count)
        self.knowledge.append(new_sentence)

        self.check_neighbors(cell,count)
        
        

    def check_neighbors(self, cell, count):


        if count == 0: 
            a, b = cell

            for x in range(-1,2):
                for y in range(-1,2):
                    if ((a+x,b+y)) not in self.moves_made and ((a+x,b+y)) not in self.safes:
                        if (a+x) >= 0 and (a+x) <= 7 and (b+y) >= 0 and (b+y) <= 7:
                            self.mark_safe((a+x,b+y))
                            sent = Sentence((a+x,b+y),self.nearby_mines((a+x,b+y)))
                            self.knowledge.append(sent)
                        if self.nearby_mines((a+x,b+y)) == 1:
                            self.check_neighbors_when1((a+x,b+y, 1))
                        if self.nearby_mines((a+x,b+y)) == 2:
                            self.check_neighbors_when2((a+x,b+y, 2))


    def check_neighbors_when1(self, cell, count):
        if count == 1:
            a, b = cell
            mines = 0
            mine_place = set()

            for x in range(-1,2):
                for y in range(-1,2):
                    if ((a+x,b+y)) not in self.moves_made and ((a+x,b+y)) not in self.safes:
                        if (a+x) >= 0 and (a+x) <= 7 and (b+y) >= 0 and (b+y) <= 7:
                            mines += 1
                            mine_place.add((a+x,b+y))


            if mines == 1:
                self.mark_mine(mine_place.pop())

    def check_neighbors_when2(self, cell, count):
        if count == 1:
            a, b = cell
            mines = 0
            mine_place = set()

            for x in range(-1,2):
                for y in range(-1,2):
                    if ((a+x,b+y)) not in self.moves_made and ((a+x,b+y)) not in self.safes:
                        if (a+x) >= 0 and (a+x) <= 7 and (b+y) >= 0 and (b+y) <= 7:
                            mines += 1
                            mine_place.add((a+x,b+y))


            if mines == 2:
                self.mark_mine(mine_place.pop())
                self.mark_mine(mine_place.pop())

                            

                       

    def check_mines(self):
        """
        Checks to see if all mines have been marked.
        """
        return self.mines == self.moves_made



    def nearby_mines(self, cell):
        count = 0
        for a in range(-1,2):
            for b in range(-1,2):
                if a == 0 and b == 0:
                    continue
                if (a+cell[0],b+cell[1]) in self.mines:
                    count += 1
        return count


    def maybe_mine(self, cell):
        """
        Returns True if the cell is a possible mine, False otherwise.
        """
        if cell in self.mines:
            return True
        return False


                    


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
                print("New move made:", move)
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
        if move not in self.moves_made and move not in self.mines:
            print(move)
            return move
        return self.make_random_move()
