from os import listdir
from os.path import isfile
from ScheduleGraph import ScheduleGraph
from utils import bold, dark_gray, get_predecessors, get_successors, menu, print_matrix, vertex_name, yesno, disable_ansi
import argparse
import sys
import os

# Using the --trace command line argument and setting it to a given constraint file will run the whole program automatically, while sending the output to a trace file.
parser = argparse.ArgumentParser(description="Test constraint tables.")
parser.add_argument('--trace', type=str, help="The name of the constraint file to test. The program will run automatically and output the results to a trace file.")
args = parser.parse_args()
trace_value = args.trace

if trace_value:
	if not os.path.isfile(trace_value):
		print(f"Error: The file '{trace_value}' does not exist.")
		sys.exit(1)
	os.makedirs('traces', exist_ok=True)
	sys.stdout = open(f'traces/{trace_value}', 'w')

# This program uses ANSI control sequences to style text (add colors, bold, etc.)
# To make sure the experience is great for everybody, we first make sure it functions properly.
# If not, it will be disabled.
if trace_value is None:
	print(bold('BOLD'), dark_gray('Dark gray'))
	if not yesno('Does the text above display properly on your device?'):
		disable_ansi()
else: disable_ansi() # ANSI control sequences are pointless in a trace file
# Assigned to: @paulleflon
menu_title = 'What would you like to do?'
actions = [
	'Test a constraint table',
	'Help',
	'Credits',
	'Exit'
]

running = True
trace_generated = False
while running:
	print('\n' + '=' * len(menu_title))
	print(menu_title)
	if trace_value is None: # User interaction
		choice = menu(actions)
	elif trace_generated: # The trace was generated, we can exit the program
		choice = 3
	else: # The trace was not generated yet, we can run the program automatically
		choice = 0
		trace_generated = True 
	print('=' * len(menu_title) + '\n')

	if choice == 3: # Exit
		running = False
	elif choice == 2: # Credits
		print('This delightful program was brought to you by')
		print_matrix([['Ingé1 INT-1 • Group 5'], ['Adèle Chamoux'], ['Mattéo Launay'], ['Paul Leflon'], ['Iriantsoa Rasoloarivalona']], header_column=False)
	elif choice == 1: # Help
		print('To make a constraint accessible to this program, please save it in a .txt file and place it in the same directory as this file.')
		print('Then, you will find it in the constraint tables list when using the', bold(actions[0]), 'feature.')
	elif choice == 0: # Constraint table test
		# First, we let the user choose the table they want to test.
		if trace_value: # The trace_value is the file we want to test
			working_file = trace_value
		else:
			files = [f for f in listdir() if isfile(f) and f.endswith('.txt')] # We ignore directories and non .txt files.
			if len(files) == 0:
				print('No constraint tables found. Please make sure your current working directory contains .txt files.')
				continue
			print('Please select a constraint table to import:')
			selected_index = menu([f.split('.txt')[0] for f in files]) # For readability, we don't display the file extension in the list
			working_file = files[selected_index]
		# Then, we can instantiate our ScheduleGraph and run the different algorithms on it
		print(f'Importing constraints from {bold(working_file)}...')
		try:
			graph = ScheduleGraph(working_file)
			graph.display_matrix()

			if graph.has_cycle():
				print(bold('This graph contains cycles, and therefore cannot be scheduled.'))
				continue

			N = len(graph.matrix)
			# Earliest dates
			earliest_dates = [
				['Rank'],
				['Task'],
				['Duration'],
				['Predecessors'],
				['Dates per predecessor'],
				['Earliest dates'],
			]
			# We can now compute the calendars
			graph.compute_calendars()
			ranks = graph.compute_ranks()
			# The dates are stored in the order of the ranks, this is used to find the indexes of said dates based on task names.
			ranks_flat = [j for i in ranks for j in i]
			if ranks is None:
				print(bold('This graph contains cycles, and therefore cannot be scheduled.'))
				continue
			k = 0 # The earliest dates are in the same order as the ranks, this counter keeps track of the current earliest date index.

			for i in range(len(ranks)):
				for j in ranks[i]:
					earliest_dates[0].append(i)	
					earliest_dates[1].append(vertex_name(j, N))
					earliest_dates[2].append(graph.durations[j] if j != 0 and j != len(graph.matrix) - 1 else 0)
					predecessors = ', '.join([vertex_name(k, N) for k in get_predecessors(j, graph.matrix)])
					predecessors = predecessors if predecessors else '-'
					earliest_dates[3].append(predecessors)
					if (j == 0): pred_dates = '0'
					else: pred_dates = ', '.join([f'{graph.earliest_dates[ranks_flat.index(l)]}({vertex_name(l, N)})' for l in get_predecessors(j, graph.matrix)])
					earliest_dates[4].append(pred_dates)
					earliest_dates[5].append(graph.earliest_dates[k])
					k+=1
			print_matrix([['Earliest dates calendar']])
			print_matrix(earliest_dates, header_row=False)
			# Latest dates
			latest_dates = [
				earliest_dates[0],
				earliest_dates[1],
				earliest_dates[2],
				['Successors'],
				['Dates per successor'],
				['Latest dates'],
			]
			k = 0
			for i in range(len(ranks)):
				for j in ranks[i]:
					sucessors = ', '.join([vertex_name(k, N) for k in get_successors(j, graph.matrix)])
					sucessors = sucessors if sucessors else '-'
					latest_dates[3].append(sucessors)
					if (j == len(graph.matrix) - 1): succ_dates = graph.earliest_dates[-1]
					else: succ_dates = ', '.join([f'{graph.latest_dates[ranks_flat.index(l)]}({vertex_name(l, N)})' for l in get_successors(j, graph.matrix)])
					latest_dates[4].append(succ_dates)
					latest_dates[5].append(graph.latest_dates[k])
					k+=1

			print_matrix([['Latest dates calendar']])
			print_matrix(latest_dates, header_row=False)

			# Floats
			floats = [
				latest_dates[0],
				latest_dates[1],
				earliest_dates[-1],
				latest_dates[-1],
				['Free float'] + graph.free_floats,
				['Total float'] + graph.total_floats,
			]
			print_matrix([['Total & Free floats calendar']])
			print_matrix(floats, header_row=False, transformer=lambda f,v,y,x: dark_gray(f) if y != 0 and v == 0 else f)
			# Critical path
			print_matrix([['Critical Path']])
			if graph.critical_paths :
				for path in graph.critical_paths :
					print_matrix([[' -> '.join([vertex_name(i, N) for i in path])]], header_row=False)
			else :
				print_matrix([['No Critical Path']])
				
		except:
			print('Something went wrong while treating this file.')
			print('Please check the file and try again.')
			continue

print('Goodbye!')