from os import listdir
from os.path import isfile
from ScheduleGraph import ScheduleGraph
from utils import bold, dark_gray, menu, print_matrix, yesno, disable_ansi

# This program uses ANSI control sequences to style text (add colors, bold, etc.)
# To make sure the experience is great for everybody, we first make sure it functions properly.
# If not, it will be disabled.
print(bold('BOLD'), dark_gray('Dark gray'))
#f not yesno('Does the text above display properly on your device?'):
#	disable_ansi()

# Assigned to: @paulleflon
menu_title = 'What would you like to do?'
actions = [
	'Test a constraint table',
	'Help',
	'Credits',
	'Exit'
]

running = True
while running:
	print('\n' + '=' * len(menu_title))
	print(menu_title)
	choice = menu(actions)
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
		print('Please select a constraint table to import:')
		files = [f for f in listdir() if isfile(f) and f.endswith('.txt')] # We ignore directories and non .txt files.
		selected_index = menu([f.split('.txt')[0] for f in files]) # For readability, we don't display the file extension in the list
		working_file = files[selected_index]
		# Then, we can instantiate our ScheduleGraph and run the different algorithms on it
		print(f'Importing constraints from {bold(working_file)}...')
		try:
			graph = ScheduleGraph(working_file)
			graph.display_matrix()
			print("ranks : ", graph.compute_ranks())
			graph.compute_calendars()
		except:
			# TODO: Give more informations about the error.
			print('Something went wrong. Please make sure the constraint table is in the right format.')
		# TODO: implement the rest of the features when individual algorithms are implemented
		# Assigned to: @paulleflon