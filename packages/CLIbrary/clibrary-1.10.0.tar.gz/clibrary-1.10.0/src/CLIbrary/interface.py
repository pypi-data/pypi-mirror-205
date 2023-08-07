from colorama import Fore, Back, Style
from getkey import getkey, keys # cmdInput.
import string
import sys
import json

from .outputs import *

# COMMANDS HANDLING

def cmdIn(cHandler: dict = {}) -> dict: # Command input.
	from .settings import style, commands

	handler = {}

	# Strings.
	handler["request"] = "Command" # The input request.
	handler["added"] = ": " # The set of added characters to the input request.
	handler["style"] = "" # Prompt style.
	handler["helpPath"] = "" # Path to the help JSON. Toggles "help" as an allowed command.

	# Lists.
	handler["allowedCommands"] = ["exit"] # The allowed commands. "exit" must be here.
	handler["history"]= [] # Command history.

	# Bools.
	handler["verbose"] = False # Verbosity.

	# Updates the handler.
	handler.update(cHandler)

	# Checks types and values.
	if not type(handler["request"]) == str:
		handler["request"] = "Command"
	if not type(handler["added"]) == str:
		handler["added"] = ": "
	if not type(handler["style"]) == str:
		handler["style"] = ""
	if not type(handler["helpPath"]) == str:
		handler["helpPath"] = ""

	if not type(handler["allowedCommands"]) == list:
		handler["allowedCommands"] = ["exit"]
	if "exit" not in handler["allowedCommands"]:
		handler["allowedCommands"].append("exit")
	if "help" not in handler["allowedCommands"] and handler["helpPath"]:
		handler["allowedCommands"].append("help")
	if not type(handler["history"]) == list:
		handler["history"] = []
	if "history" not in handler["allowedCommands"] and len(handler["history"]):
		handler["allowedCommands"].append("history")
	if "history" in handler["allowedCommands"] and not commands.setting_enableHistory:
		handler["allowedCommands"].remove("history")

	if not type(handler["verbose"]) == bool:
		handler["verbose"] = False

	if "help" in handler["allowedCommands"] and not handler["helpPath"]: # "help" as an embedded command.
		handler["allowedCommands"].remove("help")

	# Plain style.
	if style.setting_plainMode:
		handler["style"] = ""

	while True:
		try:
			command = cmdInput(handler)

			if not style.setting_caseSensitive: # Case-sensitiveness.
				command = command.lower()
			
			if handler["verbose"]:
				output({"type": "verbose", "string": "VERBOSE, INPUT: " + command})

			instructions = command.split(" ")

			if "-" not in instructions[0]: # Checks the first word.
				handler["command"] = instructions[0]

			else:
				output({"type": "error", "string": "SYNTAX ERROR"})
				continue

			if handler["command"] not in handler["allowedCommands"] and command != "": # Checks the commands list.
				output({"type": "error", "string": "UNKNOWN OR UNAVAILABLE COMMAND"})
				continue

			if handler["command"] == "help": # Prints the help.
				# Fixes history not showing when issuing help as first command.
				if "history" not in handler["allowedCommands"] and commands.setting_enableHistory:
					handler["allowedCommands"].append("history")

				handler["history"].append("help")
				helpPrint(handler)
				continue

			if handler["command"] == "history": # Prints the history of commands.
				handler["history"].append("history")

				# zsh-like format.
				spaces = len(str(len(handler["history"]))) # Ugly but it works.
				print("\n".join("{}{}. {}".format(" " * (spaces - len(str(index + 1))), index + 1, handler["history"][index]) for index in range(len(handler["history"]))))
				continue

			handler["sdOpts"], handler["ddOpts"] = optionsParser(instructions)
		
		except(IndexError):
			output({"type": "error", "string": "SYNTAX ERROR"})
			continue

		except(EOFError, KeyboardInterrupt): # Handles keyboard interruptions.
			output({"type": "error", "string": "KEYBOARD ERROR"})
			continue
		
		handler["history"].append(command)
		return handler # Returns the updated handler.

# UTILITIES

def cmdInput(handler: dict = {}) -> str:
	from .settings import commands

	buffer = ""

	# History handling.
	index = 0

	# Completion.
	completion = ""

	request = handler["style"] + handler["request"] + Style.RESET_ALL + handler["added"]
	style = lambda string: Style.DIM + string.replace(" ".join(buffer.split()), "") + Style.RESET_ALL

	sys.stdout.write(request)
	sys.stdout.flush()

	while True:
		key = getkey()

		# KEYS HANDLING.

		if key == keys.ENTER:
			print() # New line.
			return " ".join(buffer.split())
		
		elif key in [keys.LEFT, keys.RIGHT]: # Ignores arrows.
			continue

		elif key == keys.UP and len(handler["history"]):
			index -= 1

			try:
				buffer = handler["history"][index]

			except(IndexError):
				index = -1
				buffer = handler["history"][index]

		elif key == keys.DOWN and len(handler["history"]):
			index += 1

			try:
				buffer = handler["history"][index]

			except(IndexError):
				index = 0
				buffer = handler["history"][index]
		
		elif key == keys.BACKSPACE: # handles deletion.
			buffer = buffer[:-1]

		elif key == keys.TAB and completion and commands.setting_enableCompletion: # Tab completion.
			buffer = completion + " "

		elif key in string.printable: # Adds the newly inserted character.
			buffer += key

		# COMPLETION HANDLING.

		completion = ""
		# Search for a possibile completion.
		if " ".join(buffer.split()) != "" and len(" ".join(buffer.split()).split(" ")) == 1 and buffer[-1] != " " and commands.setting_enableCompletion:
			# This works if the buffer is made of a single word and does not end with a space.
			# This also checks for commands.setting_enableCompletion.
			for command in handler["allowedCommands"]:
				if command[0:len(" ".join(buffer.split()))] == " ".join(buffer.split()):
					completion = command
					break

		sys.stdout.write("\x1b[2K\r" + request + buffer + style(completion))
		sys.stdout.flush()

def helpPrint(handler: dict) -> None: # Prints the help.
	from .settings import style

	try:
		helpFile = open(handler["helpPath"], "r")
		helpJson = json.load(helpFile)
		helpFile.close()

		helpElements = []

		if style.setting_darkMode:
			font = Fore.BLACK
			back = Back.BLACK

		else:
			font = Fore.WHITE
			back = Back.WHITE

		if not style.setting_plainMode:
			for key in helpJson:
				helpString = ""

				if key not in handler["allowedCommands"]:
					helpString += Back.YELLOW + font + " UNAVAILABLE " + Style.RESET_ALL

				helpString += Back.GREEN + font + " " + key + " " + back + Fore.GREEN + " " + helpJson[key]["description"] + " " + Style.RESET_ALL
				
				if "options" in helpJson[key]:
					helpString += Back.GREEN + font + " " + str(len(helpJson[key]["options"])) + " option(s) " + Style.RESET_ALL

					for optionKey in helpJson[key]["options"]:
						if "#" in optionKey:
							helpString += "\n\t" + Back.RED + font + " " + optionKey.replace("#", "") + " "

							if "--" not in optionKey:
								helpString += back + Fore.RED + " " + helpJson[key]["options"][optionKey] + " "
						
						else:
							helpString += "\n\t" + Back.CYAN + font + " " + optionKey + " "

							if "--" not in optionKey:
								helpString += back + Fore.CYAN + " " + helpJson[key]["options"][optionKey] + " "
						
						helpString += Style.RESET_ALL
				
				helpElements.append(helpString)
			
		else:
			for key in helpJson:
				helpString = ""

				if key not in handler["allowedCommands"]:
					helpString += "[UNAVAILABLE] "

				helpString += key + ": " + helpJson[key]["description"]
				
				if "options" in helpJson[key]:
					helpString += " [" + str(len(helpJson[key]["options"])) + " option(s)]"

					for optionKey in helpJson[key]["options"]:
						if "#" in optionKey:
							helpString += "\n\t[MANDATORY] " + optionKey.replace("#", "")
						
						else:
							helpString += "\n\t" + optionKey

						if "--" not in optionKey:
							helpString += ": " + helpJson[key]["options"][optionKey]
						
						helpString += Style.RESET_ALL
				
				helpElements.append(helpString)
		
		print("\n\n".join(helpElements)) if len(helpElements) else output({"type": "warning", "string": "NO HELP FOR CURRENTLY AVAILABLE COMMANDS", "before": "\n"})
		
	except(FileNotFoundError):
		output({"type": "error", "string": "HELP FILE ERROR"})
	
	except:
		output({"type": "error", "string": "HELP ERROR"})

def optionsParser(instructions: list) -> dict: # Parses the options contained in a list of strings.
	# OPTIONS: SINGLE DASH [{(-)key1: value1}, ...] AND DOUBLE DASH [(--)key1, ...]

	sdOpts = dict()
	ddOpts = list()

	for inst in instructions:
		if "--" in inst:
			ddOpts.append(inst.replace("--", ""))
		
		elif inst[0] == "-":
			try: # Avoids parsing negative numbers as options.
				if type(float(inst)) == float:
					pass

			except(ValueError):
				sdOpts[inst.replace("-", "")] = instructions[instructions.index(inst) + 1]

	return sdOpts, ddOpts