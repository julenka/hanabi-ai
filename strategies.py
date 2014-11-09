import re

from hanabi import HANABI_COLORS as HANABI_COLORS

class InteractiveStrategy:
	def doTurn(self, player_num, player_guesses, other_players, table, logger):
		''' Perform a single turn  

		Params:
		player_num -- number of player for current turn
		player_guesses -- guesses for the current player
		other_players -- state of other players

		Returns:
		(method, params) tuple
		method - one of ["sayColor", "sayNumber","discard","play","say"]
		params - if method is "play" or "discard", then a single int representing the card to players
		otherwise, (player_index, color or number tuple)

		Possible Actions:
		sayColor(player_num, color)
		sayNumber(play_num, num)
		discard(index)
		play(index)
		'''
		print
		print "*" * 80
		print
		print "player_guesses:"
		for i,g in enumerate(player_guesses):
			print i, g
		print "other_players:"
		for p in other_players:
			print str(p)
		print "table: ", table
		print "your move, player {}:".format(player_num)
		commands = ["sayColor", "sayNumber","discard","play","say"]
		validPlay = False
		errorMessage = None
		while not validPlay:
			validPlay = True
			if errorMessage:
				print errorMessage 
			action = raw_input()	
			match = re.match(r"(.+)\((.+)\)",action)
			if not match:
				validPlay = False
				errorMessage = "Invalid command format. Should be command(args)"
				continue
			method, params = match.groups()
			if method not in commands:
				validPlay = False
				errorMessage = "Invalid command {}, try one of {}".format(method, commands)
			if method in ["play", "discard"]:
				try:
					n = int(params)
					if n < 0 or n >= len(player_guesses):
						errorMessage = "Argument to {} must be >=0 and < {}".format(method, len(player_guesses))
						validPlay = False
					else:
						return method, n
				except ValueError:
					validPlay = False
					errorMessage = "Argument to {} must be int, was {}".format(method, params)
			else:
				# this is a "say" command
				idx, param = params.split(',')
				try:
					idx = int(idx)
				except ValueError:
					validPlay = False
					errorMessage = "Argument to {} must of form (player_index, info)".format(method)
				return method, (idx, param)

class PlayZerothStrategy:
	''' A strategy which always plays the zeroth card in its hand '''
	def doTurn(self, player_num, player_guesses, other_players, table, logger):
		return "play", 0


class Strategy1:
	''' A strategy which always plays the zeroth card in its hand '''
	def doTurn(self, player_num, player_guesses, other_players, table, logger):
		# check if you can play a card
		playableCards = table.getPlayableCards()
		logger.debug("playableCards are {}".format(playableCards))

		return "say", (1, "red")
