import os
import subprocess

# Get the current directory
current_directory = os.getcwd()

# Iterate through all files in the current directory
for file_name in os.listdir(current_directory):
	if file_name.endswith('.txt') and os.path.isfile(file_name):
		# Run the main program in trace generation mode.
		print(f'Generating trace for {file_name}...')
		command = f'python main.py --trace="{file_name}"'
		subprocess.run(command, shell=True)