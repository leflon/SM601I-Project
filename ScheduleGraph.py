from utils import bold, dark_gray, print_matrix
from utils import remove_line, remove_col, get_predecessor, has_negative_edge
import copy

# TODO : add a output parameter, and redirect all the prints to that parameter.
# this will be useful for creating the asked-for logs

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
        lines = [line.strip() for line in file.readlines() if line.strip() != '']
        file.close()
        # We add two vertices for the alpha and omega tasks
        # Absent edges are represented as None, to avoid confusion with 0-valued edges from alpha.
        """Adjacency matrix of the graph"""
        self.matrix: list[list[int | None]] = [[None for _ in range(len(lines) + 2)] for _ in range(len(lines) + 2)]
        for line in lines:
            split = line.split(' ')
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


    def has_cycle(self) -> bool:
        """
        Checks if there is a cycle in the graph.
        Returns:
            bool: True if there is a cycle, False otherwise.
        """
        # Initialization
        eliminated_vertices = []
        current_matrix = copy.deepcopy(self.matrix)
        running = True
        k = 0
        while running:
            # For every vertex in the graph, look if they have a predecessor
            for i in range(len(current_matrix)):
                predecessors = get_predecessor(i, current_matrix)
                if predecessors == []:
                    eliminated_vertices.append(i)
                    
            # Eliminate the vertices who don't have predecessors
            for vertex in eliminated_vertices:
                vertex = vertex - eliminated_vertices.index(vertex)  # Adjust vertex indexes on the fly
                remove_col(vertex, current_matrix)
                remove_line(vertex, current_matrix)

            running = eliminated_vertices != []
            eliminated_vertices = []     # Reset the list of elminated vertices
            k += 1

        if current_matrix == []:    
            return False    # Empty matrix means no cycle
        else: 
            return True     # Non-empty matrix means a cycle 


    def check(self, display_result=False) -> bool:
        """
        Checks that the necessary properties of the graph such that it can serve as a scheduling graph are satisfied. That is:
         - No cycle
         - No negative edges
         Args:
            display_result: Whether the function should display the result of the check in addition to returning it.
        """ 
        #Assigned to: @mattelothere
        if not has_negative_edge(self.matrix):
            if not self.has_cycle():
                if display_result:  print("The graph verifies the absence of cycles and negative edges => is a valid scheduling graph.")
                return True
            else:
                if display_result: print("there is a cycle => not a scheduling graph")
                return False
        else:
            if display_result:  print("there is a negative edge => not a scheduling graph")
            return False 
   

    def compute_ranks(self) -> list[list[int]] | None:
        """
        Computes are stores the ranks of each vertex of the graph
        If the graph contains a cycle, the function returns None.

        Returns :
            -a list of list of ints. the first index is the rank, the second the vertex
            -None if the graph contains a cycle
            
        Example : 
            running it on some particular scheduling graph (having 4 constraints) will return the following
            > G.compute_ranks()
            > [[0], [1, 4], [2], [3], [5]]
            0 is of rank 0, 1 and 4 are of rank 1, ... 
        """
        #Assigned to: @mattelothere

        if self.has_cycle():    # the notion of rank does not exist for graphs containing cycles
            return None

        # Some initialization
        ranks = []  # the array we are going to return at the end
        to_eleminate = None #vertices with no predecessors at the current iteration
        work_matrix = copy.deepcopy(self.matrix)    # copy recursively the matrix to then pop rows and columns without affecting the base matrix
        
        # add one column and one row acting as labels (remove row and remove col have the side effect of 'shuffling' the indices)
        work_matrix.insert(0, [i for i in range(len(self.matrix))]) # col labels
        for i in range(len(work_matrix)):   # row labels
            work_matrix[i].insert(0, work_matrix[0][i])

        k = 0   # this k is our iteration number, used to know which rank to assingn to the eliminated vertices
        while to_eleminate != []:   # until we have eliminated all vertices

            to_eleminate = []  # clear everything
            
            for i in range(1, len(work_matrix)):    # range(1, ...) to not take the 1st label row   
                predecessors = get_predecessor(i, work_matrix[1:])  # the [1:] allows to remove the 1st label row
                
                if predecessors == []:
                    to_eleminate.append(i)
                    try :                     
                        ranks[k] += [work_matrix[i][0]]     # if no vertex of rank k was found yet, this will raise and IndexError
                    except IndexError:
                        ranks.append([work_matrix[i][0]])   # then we append instead of concatenating the vertex 
                
            for vertex in to_eleminate:
                vertex = vertex - to_eleminate.index(vertex)  # Adjust vertex indexes on the fly
                remove_col(vertex, work_matrix)
                remove_line(vertex, work_matrix)
            
            k += 1  # increment rank by 1 before going to next iteration
            

        return ranks
    

    def compute_calendars(self) -> None:
        """
        Computes and stores the earliest/latest dates and the floats.
        """
        #TODO: implement
        #Assigned to: @hexadelusional @iri-rsl
        pass
