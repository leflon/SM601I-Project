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
        self.matrix = [[None for _ in range(len(lines) + 2)] for _ in range(len(lines) + 2)]
        for line in lines:
            split = line.strip().split(' ') # strip() gets rid of the \n character
            vertex = int(split[0])
            constraints = [int(c) for c in split[2:]]
            if len(constraints) == 0:
                # There is no constraint so this is a starting task,
                # Hence, it is the tail of an edge going from the alpha vertex
                self.matrix[0][vertex] = 0
            # Else, we add to the matrix each constraint
            for c in constraints:
                self.matrix[c][vertex] = int(lines[c - 1].split(' ')[1])
        # We check dead-ends to link them forwards to the omega vertex
        for i in range(1, len(self.matrix) - 1):
            line = self.matrix[i]
            if (not any(line)):
                self.matrix[i][len(lines) + 1] = int(lines[i - 1].split(' ')[1])