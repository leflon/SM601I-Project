def bold(text: str) -> str:
	"""
	Returns the given text wrapped in ANSI escape codes to display it in bold.
	Args:
		text (str): The text to be formatted in bold.
	Returns:
		str: The text formatted in bold using ANSI escape codes.
	"""
	if 'DISABLE_ANSI' in vars() and DISABLE_ANSI: # this global variable is defined in the project's entry file
		return text
	return f'\033[1m{text}\033[0m'

def dark_gray(text: str) -> str:
	if 'DISABLE_ANSI' in vars() and DISABLE_ANSI: # this global variable is defined in the project's entry file
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