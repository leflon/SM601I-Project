from typing import Any, Callable

DISABLE_ANSI = False

def disable_ansi():
	"""
	Disables ANSI control sequences for older devices
	""" 
	global DISABLE_ANSI
	DISABLE_ANSI = True

def bold(text: str) -> str:
	"""
	Returns the given text wrapped in ANSI escape codes to display it in bold.
	Args:
		text (str): The text to be formatted in bold.
	Returns:
		str: The text formatted in bold using ANSI escape codes.
	"""
	if DISABLE_ANSI:
		return text
	return f'\033[1m{text}\033[0m'

def dark_gray(text: str) -> str:
	if 'DISABLE_ANSI' in vars() and DISABLE_ANSI:
		return text
	return f'\033[1;30m{text}\033[0m'

def print_matrix(matrix: list[list[Any]], transformer: Callable[[str, Any, int, int], str] = None, cell_padding = 2, header_row = True, header_column = True) -> None:
	"""
	Displays a matrix.
	Args:
		- table : The matrix to display
		- transformer : Allows to transform the rendering of a cell based on its value and its position in the matrix.

			This is useful for empty cells of adjacency matrix, which we want to render as dark gray asterisks. 
			We have to apply the dark_gray *after* applying the python `center` method (the other way around does not function properly).\\
			This lambda function allows us to perform this transformation.
		- cell_padding : The spacing to apply on the left and right of each cell
		- header_row : Whether to display the first row in bold.
		- header_column : Whether to display the first column in bold.
	"""
	N = len(matrix)
	M = len(matrix[0])
	border_top = '╔' # Top border of the table
	row_sep = '╠' # Separator between each row
	border_bot = '╚' # Bottom border of the table
	col_lengths = [] # Represents the length of each column, based on the length of its longuest cell
	# This generates the top, bottom, and separator lines to correctly align with the size of each cell.
	for i in range(M):
		max_cell_length = max([len(str(matrix[j][i])) for j in range(N)]) + cell_padding * 2
		col_lengths.append(max_cell_length)
		line = '═' * max_cell_length
		border_top += line + '╦'
		row_sep += line + '╬'
		border_bot += line + '╩'
	# We replace the last character with a closing character instead of the previous connecting ones
	border_top = border_top[:-1] + '╗'
	row_sep = row_sep[:-1] + '╣'
	border_bot = border_bot[:-1] + '╝'
	print(border_top)
	# This loop displays each row of the table
	for i in range(N):
		line = matrix[i]
		row = '║'
		for j in range(M):
			cell = line[j]
			padded = str(line[j]).center(col_lengths[j], ' ')
			if i == 0 and header_row or j == 0 and header_column:
				padded = bold(padded)
			if transformer:
				padded = transformer(padded, cell, i, j)
			row+= padded + '║'
		print(row)
		if i + 1 < N: # We print a separator after each row, except the last one since the bottom border comes afterwards
			print(row_sep)
	print(border_bot)

def get_predecessor(vertex_index: int, target_matrix: list[list[int]], verbose_mode:bool = False) -> list[int]:
	"""
	returns a list of the predecessors of a vertex in a particular target matrix
	if target_matrix is not provided, then we'll look for the predecessors of that vertex in the self.matrix
	Args:
		vertex_index: an int to tell which vertex we are talking about
		verbose_mode: an int defaulting to False that enables verbose prints if set to True.
		target_matrix: a list of lists of ints representing the adjacency matrix, defaulting to self.matrix
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
	vertices = ["α"]+[str(i) for i in range(1, len(target_matrix)-1)]+["ω"]
	answer = []
	for i in range(len(target_matrix)): # for every line of the adjacency mat, 
		if target_matrix[i][vertex_index] != None: # looking at the column of the vertex, if theres a non-null value,  
			answer.append(i)   # then the vertex behind vertex_index has at least 1 predecessor
			if verbose_mode: print("The vertex {} has a predecessor : at indices [{}][{}], \
			{} is accessible from {}".format(vertices[vertex_index], i, vertex_index, vertices[vertex_index], vertices[i]))
		else:
			if verbose_mode: print("The vertex {} has no predecessor at index [{}][{}], \
			{} is not accessible from {}".format(vertices[vertex_index], i, vertex_index, vertices[vertex_index], vertices[i]))
	return answer        

def has_negative_edge(target_matrix: list[list[int]]) -> bool:
	"""
	checks if there is at least one negative edge in the target_matrix
	if target_matrix is not provided, then we'll look in self.matrix
	Args:
		target_matrix: a list of lists of ints representing the adjacency matrix, defaulting to self.matrix
	Returns:
		bool: True if there is a negative edge, False otherwise
	"""

	answer = False
	for line in target_matrix:
		col = 0
		while col < len(line) and answer == False:  # go out of the loop as soon as theres a negative
			if line[col] != None:
				answer = line[col] < 0
			col += 1
	return answer

def remove_col(col_index: int, target_matrix: list[list[int]]) -> None:
	"""
	pops a column out of a matrix (in place)

	Args : 
		col_index: int indexing which column we should remove
		matrix: list of lists of ints 
	"""
	for i in range(len(target_matrix)):
		target_matrix[i].pop(col_index)
		
def remove_line(row_index: int, target_matrix: list[list[int]]) -> None:
	"""
	pops a row out of a matrix (in place)
	
		Args : 
		col_index: int indexing which row we should remove
		matrix: list of lists of ints 
	"""
	target_matrix.pop(row_index)

def yesno(question: str) -> bool:
	"""
	Prompt the user with a yes/no question and return the response as a boolean.
	Args:
		question (str): The yes/no question to present to the user.
	Returns:
		bool: True if the user responds positively, False otherwise.
	"""
	answer = None
	while answer not in ['y', 'n']:
		answer = input(question + ' [y/n]: ')[:1].lower()		
	return answer == 'y'

def menu(options: list[str]) -> int:
	"""
	Displays a menu of options and prompts the user to select one.
	Args:
		options: A list of strings representing the menu options.
	Returns:
		int: The index of the selected option (0-based).
	The function prints each option with a corresponding number starting from 1.
	It then prompts the user to input a number corresponding to one of the options.
	If the input is not a valid number or not within the range of options, it will
	continue to prompt the user until a valid selection is made.
	"""
	N = len(options)
	for i in range(N):
		print(f'{i + 1}. {options[i]}')
	answer = -1
	while not (answer >= 1 and answer <= N):
		inp = input(f'Please select an option [1-{N}]: ')
		try:
			answer = int(inp)
		except:
			pass
	return answer - 1