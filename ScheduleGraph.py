from utils import bold, dark_gray, print_matrix
import copy     # copy lists by value, and not by reference
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
        adapted_matrix = [top_row.copy()]
        for i in range(N):
            row = self.matrix[i].copy()
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

        
        def get_predecessor(vertex_index:int, verbose_mode:bool = False) -> list[int]:
            """
            returns a list of the predecessors of a vertex
            Args:
                vertex_index: an int to tell which vertex we are talking about
                verbose_mode: an int defaulting to False that enables verbose prints if set to True.
            Returns:
                list: list containing the predecessors of that vertex
            Examples:
            Consider the following : 1-->2--->3 
                                    /          \
                                   A------>4--->O
            with :
            vertices = ["A", "1", ..., "4", "O"]

            >get_predecessor(5), i.e. predecessors of "O" will return the indices of "3" and "4" : [3, 4]
            >get_predecessor(0), i.e. predecessors of "A" will return an empty list : []
            """
            vertices = ["α"]+[str(i) for i in range(1, len(self.matrix)-1)]+["ω"]
            j = vertex_index  # for conciseness 
            answer = []
            for i in range(len(self.matrix)): # for every line of the adjacency mat, 
                if self.matrix[i][j] != None: # looking at the column of the vertex, if theres a non-null value,  
                    answer.append(i)   # then j has at least 1 predecessor
                    if verbose_mode: print("The vertex {} has a predecessor : at indices [{}][{}], \
                    {} is accessible from {}".format(vertices[j], i, j, vertices[j], vertices[i]))
                else:
                    if verbose_mode: print("The vertex {} has no predecessor at index [{}][{}], \
                    {} is not accessible from {}".format(vertices[j], i, j, vertices[j], vertices[j]))
            return answer        

        def check_negative_edge() -> bool:
            """
            checks if there is at least one negative edge in the graph
            
            Example : 
            if there is a negative edge, this returns True
            if there is no negative edge, this returns False
            """

            answer = False  # until proven contrary, there are no negative weighted edgeds in the graph
            for line in self.matrix:
                col = 0
                while col < len(line) and answer == False:  # go out of the loop as soon as theres a negative
                    if line[col] != None:
                        answer = line[col] < 0  # this will be True if theres a negative
                    col += 1
            return answer

        def remove_col(col_index:int, matrix:list[list[int]]) -> None:
            """
            pops a column out of a matrix (in place)

            Args : 
                col_index: int indexing which column we should remove
                matrix: list of lists of ints 
            """
            for i in range(len(matrix)):
                matrix[i].pop(col_index)
                
        def remove_line(row_index:int, matrix:list[list[int]]) -> None:
            """
            pops a row out of a matrix (in place)
            
             Args : 
                col_index: int indexing which row we should remove
                matrix: list of lists of ints 
            """
            matrix.pop(row_index)

        def check_cycle() -> bool:
            """
            Checks if there is a cycle in the graph.
            Returns:
                bool: True if there is a cycle, False otherwise.
            """
            # initialization
            eliminated_vertices = []
            current_matrix = copy.deepcopy(self.matrix)


            k = 0
            running = True
            while running:
                # for every vertex in the graph, look if they have a predecessor.
                for i in range(len(current_matrix)):
                    predecessors = get_predecessor(i)
                    if predecessors == []:
                        eliminated_vertices.append(i)
                
                # eliminate those who don't have predecessors
                for vertex in eliminated_vertices:
                    remove_col(vertex, current_matrix)
                    remove_line(vertex, current_matrix)

                running = eliminated_vertices != []
                k += 1
                eliminated_vertices = []     # remove all values from eliminated_vertices

            if current_matrix == []:
                return False
            else: 
                return True
            # Repeat until 1/ matrix is empty 2/ eliminated set = []
            
        print(check_cycle())


    
    def compute_ranks(self) -> None:
        """
        Computes are stores the ranks of each vertex of the graph
        """
        #TODO: implement
        #Assigned to: @mattelothere
        pass
    
    def compute_calendars(self) -> None:
        """
        Computes and stores the earliest/latest dates and the floats.
        """
        #TODO: implement
        #Assigned to: @hexadelusional @iri-rsl
        pass


if __name__ == "__main__":
    C = ScheduleGraph("constraints cycle.txt")
    D = ScheduleGraph("constraints.txt")

    print("for a non cyclic : ", D.check())
    print("For a cyclic : ", C.check())
    
    