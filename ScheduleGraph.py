from utils import bold, dark_gray, print_matrix
class ScheduleGraph:
    def __init__(self, path: str):
        """
        Initializes a ScheduleGraph object by reading a constraint table from a file.
        Args:
            path: The file path to the schedule data.
        """

        """Rank of each vertex of the graph"""
        self.ranks = []
        """Earliest date of each task"""
        self.earliest_dates = []
        """Latest date of each task"""
        self.latest_dates = []
        """Total float of each task"""
        self.total_floats = []
        """Free float of each task"""
        self.free_floats = []

        file = open(path, 'r')
        lines = file.readlines()
        file.close()
        # We add two vertices for the alpha and omega tasks
        # Absent edges are represented as None, to avoid confusion with 0-valued edges from alpha.
        """Adjacency matrix of the graph"""
        self.matrix: list[list[int | None]] = [[None for _ in range(len(lines) + 2)] for _ in range(len(lines) + 2)]
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
        """
        Displays the adjacency matrix of the graph.
        """
        N = len(self.matrix)
        adapted_matrix = [] # Adds the names of rows and columns to the matrix, and replaces Nones with asterisks
        vertex_name = lambda index: 'α' if index == 0 else 'ω' if index == N - 1 else str(index)
        top_row = ['\\'] # This first cell is the top corner of the table.
        for i in range(N):
            top_row.append(vertex_name(i))
        adapted_matrix = [top_row]
        for i in range(N):
            row = self.matrix[i]
            row.insert(0, vertex_name(i))
            for j in range(N + 1):
                if row[j] == None: 
                    row[j] = '*'
            adapted_matrix.append(row)
        # We want to display all asterisks and the very first cell in dark gray for better readability.
        print_matrix(adapted_matrix, lambda render, val, i, j: dark_gray(render) if val == '*' or i == j == 0 else render)


    def check(self, display_result=False) -> bool:
        """
        Checks that the necessary properties of the graph such that it can serve as a scheduling graph are satisfied. That is:
         - No cycle
         - No negative edges
         Args:
            display_result: Whether the function should display the result of the check in addition to returning it.
        """ 
        #TODO: implement
        #Assigned to: @mattelothere
        pass
    
    def compute_ranks(self) -> None:
        """
        Computes are stores the ranks of each vertex of the graph
        """
        #TODO: implement
        #Assigned to: @matthelothere
        pass
    
    def compute_calendars(self) -> None:
        """
        Computes and stores the earliest/latest dates and the floats.
        """
        #TODO: implement
        #Assigned to: @hexadelusional @iri-rsl
        pass