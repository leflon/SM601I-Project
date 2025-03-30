from utils import bold, dark_gray, print_matrix, vertex_name
from utils import remove_line, remove_col, get_predecessor, has_negative_edge, get_successor
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

        """Earliest date of each task"""
        self.earliest_dates = []
        """Latest date of each task"""
        self.latest_dates = []
        """Total float of each task"""
        self.total_floats = []
        """Free float of each task"""
        self.free_floats = []
        """Critical path of the graph"""
        self.critical_path = []

        file = open(path, 'r')
        lines = [line.strip() for line in file.readlines() if line.strip() != '']
        file.close()
        # We add two vertices for the alpha and omega tasks
        # Absent edges are represented as None, to avoid confusion with 0-valued edges from alpha.
        """Adjacency matrix of the graph"""
        self.matrix: list[list[int | None]] = [[None for _ in range(len(lines) + 2)] for _ in range(len(lines) + 2)]
        """Duration of each task"""
        self.durations = [None] * (len(lines) + 2)
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
            # We also store the duration of the task separately
            self.durations[vertex] = int(split[1])
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
        top_row = ['\\'] # This first cell is the top corner of the table.
        for i in range(N):
            top_row.append(vertex_name(i, N))
        adapted_matrix = [top_row.copy()]
        for i in range(N):
            row = self.matrix[i].copy()
            row.insert(0, vertex_name(i, N))
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
        Computes and stores the ranks of each vertex of the graph

        Returns: 
            The vertices of the graph ordered by rank or None if it includes a cycle.
            
        Example:
            [[0], [1, 4], [2], [3], [5]]
            - The rank of vertex `0` is **0**.
            - The rank of vertices `1` and `4` is **1**.
            - The rank of vertex `2` is **2**. 
            - The rank of vertex `3` is **3**. 
            - The rank of vertex `5` is **4**. 
        """

        if self.has_cycle(): # The notion of rank does not exist for graphs containing cycles
            return None

        ranks = []  # The array returned at the end
        to_eleminate = None # Vertices with no predecessors at the current iteration
        work_matrix = copy.deepcopy(self.matrix)
        
        # Add one column and one row acting as labels (remove row and remove col have the side effect of 'shuffling' the indices)
        work_matrix.insert(0, [i for i in range(len(self.matrix))]) # Column labels
        for i in range(len(work_matrix)): # Row labels
            work_matrix[i].insert(0, work_matrix[0][i])

        k = 0 # Corresponds to the rank currenly reached in the loop
        while to_eleminate != []: # Until we have eliminated all vertices
            to_eleminate = []

            for i in range(1, len(work_matrix)): # Starting at 1 to avoid the 1st label row   
                predecessors = get_predecessor(i, work_matrix[1:])
                
                if predecessors == []:
                    to_eleminate.append(i)
                    if (k == len(ranks)): # First vertex of rank k
                        ranks.append([work_matrix[i][0]])
                    else: # Additional vertices of rank k.
                        ranks[k].append(work_matrix[i][0])
                
            for vertex in to_eleminate:
                vertex = vertex - to_eleminate.index(vertex) # Adjust vertex indexes on the fly
                remove_col(vertex, work_matrix)
                remove_line(vertex, work_matrix)
            
            k += 1

        return ranks
    

    def compute_calendars(self) -> None:
        """
        Computes and stores the earliest/latest dates and the floats.
        """

        actual_matrix = copy.deepcopy(self.matrix)
        ranks = self.compute_ranks()

        if ranks is None:
            return None

        ranked_vertices = [v for sublists in ranks for v in sublists] # Get the 2-dimension list in 1-dimension form
        durations = []
        for i in range(len(ranked_vertices)-1):
            vertex_duration = [elt for elt in actual_matrix[ranked_vertices[i]] if elt is not None][0]
            durations.append(vertex_duration)
        durations.append(0) # Last task doesn't have a duration but this will be access when computing latest dates. 

        # Computing the earlieast dates
        earliest_dates = [0] * len(ranked_vertices) 
        predecessors = [get_predecessor(vertex, actual_matrix) for vertex in ranked_vertices]
        for i in range(1, len(ranked_vertices)): # Starting from 1 because alpha's earliest date is always 0
            for j in range(len(predecessors[i])):
                pred_index = ranked_vertices.index(predecessors[i][j])
                potential_early_date = earliest_dates[pred_index]+durations[pred_index]
                if potential_early_date > earliest_dates[i] :
                    earliest_dates[i] = potential_early_date
        self.earliest_dates = earliest_dates

        # Computing the latest dates
        latest_dates = [earliest_dates[len(earliest_dates)-1] for i in range(len(ranked_vertices))] # Create an initial list for the latest dates
        successors = [get_successor(vertex, actual_matrix) for vertex in ranked_vertices]
        for i in range(len(ranked_vertices)-2, -1, -1):
            for j in range(len(successors[i])):
                succ_index = ranked_vertices.index(successors[i][j])
                potential_late_date = latest_dates[succ_index]-durations[i]
                if potential_late_date < latest_dates[i]:
                    latest_dates[i] = potential_late_date
        self.latest_dates = latest_dates

        # Computing total float
        self.total_floats = [latest_dates[i]-earliest_dates[i] for i in range(len(ranked_vertices))]

        # Computing free float
        free_float =[]
        for i in range(len(ranked_vertices)-1):
            succ_earliest_date = min([earliest_dates[ranked_vertices.index(vertex)] for vertex in successors[i]])
            free_float.append(succ_earliest_date-earliest_dates[i]-durations[i])
        self.free_floats = free_float
        
        # Computing critical path
        critical_path = []
        for i in range(len(ranked_vertices)-1):
            if free_float[i]==0:
                critical_path.append(ranked_vertices[i])
        self.critical_path = critical_path