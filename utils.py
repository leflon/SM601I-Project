def bold(text: str) -> str:
	"""
	Returns the given text wrapped in ANSI escape codes to display it in bold.
	Args:
		text (str): The text to be formatted in bold.
	Returns:
		str: The text formatted in bold using ANSI escape codes.
	"""
	if 'DISABLE_ANSI' in vars() and DISABLE_ANSI: # This global variable is defined in the project's entry file. If it is not defined, it will be ignored.
		return text
	return f'\033[1m{text}\033[0m'

def dark_gray(text: str) -> str:
	if 'DISABLE_ANSI' in vars() and DISABLE_ANSI: # This global variable is defined in the project's entry file. If it is not defined, it will be ignored.
		return text
	return f'\033[1;30m{text}\033[0m'


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