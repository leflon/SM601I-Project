from utils import bold, dark_gray, yesno
class ScheduleGraph:
    def __init__(self, path: str):
        """
        Initializes a ScheduleGraph object by reading a constraint table from a file.
        Args:
            path: The file path to the schedule data.
        """     
        file = open(path, 'r')
        lines = file.readlines()
        file.close()
        # We add two vertices for the alpha and omega tasks
        # Absent edges are represented as None, to avoid confusion with 0-valued edges from alpha.
        self.matrix = [[None for _ in range(len(lines) + 2)] for _ in range(len(lines) + 2)]
        for line in lines:
            split = line.strip().split(' ') # strip() gets rid of the trailing \n character
            vertex = int(split[0])
            constraints = [int(c) for c in split[2:]]
            if len(constraints) == 0:
                # There is no constraint so this is a starting task,
                # Hence, it is the tail of an edge going from the alpha vertex
                self.matrix[0][vertex] = 0
            # Else, we add each constraint to the matrix
            for c in constraints:
                self.matrix[c][vertex] = int(lines[c - 1].split(' ')[1])
        # We check dead-ends to link them forwards to the omega vertex
        for i in range(1, len(self.matrix) - 1):
            line = self.matrix[i]
            if (not any(line)):
                self.matrix[i][len(lines) + 1] = int(lines[i - 1].split(' ')[1])

    def display_matrix(self):
        N = len(self.matrix)
        top = '╔' # Top border of the table
        sep = '╠' # Separator between each row
        bot = '╚' # Bottom border of the table
        col_lengths = [] # Represents the length of each column, based on the length of its longuest cell
        # This loops defines the upper 4 variables based the matrix' cells lengths
        for i in range(N + 1): # + 1 to account for the heading column
            if (i == 0): # This is the heading column, the cells will simply contain names of each vertex, which are merely the indexes of the array.
                max_cell_length = len(str(N - 1)) + 2 # +2 is added for padding, -1 is added in case the last index is 10. Since it's replaced by 
                                                      # omega, one character, this avoids unnecessary big cells, if that ever happens.
            else:
                # Iterating through the current column, we keep the l
                max_cell_length = max([len(str(self.matrix[j][i - 1])) if self.matrix[j][i - 1] != None else 1 for j in range(N)]) + 2 # + 2 for padding
            col_lengths.append(max_cell_length)
            line = '═' * max_cell_length
            top += line + '╦'
            sep += line + '╬'
            bot += line + '╩'
        top = top[:-1] + '╗'
        sep = sep[:-1] + '╣'
        bot = bot[:-1] + '╝'
        print(top)
        header_row = '║'
        # This loops prints the header row, displaying the name of each column
        for i in range(N + 1): # + 1 for the empty top-left corner 
            if i == 0: # Empty corner
                header_row+= '\\'.center(col_lengths[0], ' ') + '║'
            else: 
                if i == 1:
                    name = 'α'
                elif i == N:
                    name = 'ω'
                else: 
                    name = str(i - 1)
                header_row += bold(name.center(col_lengths[i], ' ')) + '║'
        print(header_row)
        print(sep)
        # This loop displays each row of the table
        for i in range(N):
            # First, it displays the name of each row
            line = self.matrix[i]
            if i == 0:
                name = 'α'
            elif i == N - 1:
                name = 'ω'
            else: 
                name = str(i)
            row = '║' + bold(name.center(col_lengths[0], ' ')) + '║'
            # This loop displays the rest of the row
            for j in range(N):
                cell = str(line[j]) if line[j] != None else '*'
                padded = cell.center(col_lengths[j + 1], ' ')
                row+= (dark_gray(padded) if cell == '*' else padded) + '║'
            print(row)
            if i + 1 < N:
                print(sep)
        print(bot)


ScheduleGraph('test.txt').display_matrix()#