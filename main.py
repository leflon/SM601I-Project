from utils import bold, dark_gray, yesno, disable_ansi

# This program uses ANSI control sequences to style text (add colors, bold, etc.)
# To make sure the experience is great for everybody, we first make sure it functions properly.
# If not, it will be disabled.
print(bold('BOLD'), dark_gray('Dark gray'))
if not yesno('Does the text above display properly on your device?'):
	disable_ansi()

# Assigned to: @paulleflon
print('='*10)
print(bold('TODO: Implement the main loop ^^'))