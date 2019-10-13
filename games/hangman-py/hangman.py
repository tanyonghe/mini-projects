import sys
import random

##############################
### I'm bored, send help ;-;
### WIP: Score System
##############################

# 49 words in a string for guessing
string_of_words = 'Awkward Bagpipes Banjo Bungler Croquet Crypt Dwarves Fervid Fishhook Fjord Gazebo Gypsy Haiku Haphazard Hyphen Ivory Jazzy Jiffy Jinx Jukebox Kayak Kiosk Klutz Memento Mystify Numbskull Ostracize Oxygen Pajama Phlegm Pixel Polka Quad Quip Rhythmic Rogue Sphinx Squawk Swivel Toady Twelfth Unzip Waxy Wildebeest Yacht Zealous Zigzag Zippy Zombie'

# Hangman graphics
hangman_zero = ['O-----', '|     ', '|     ', '|     ', '|      ', '|      ']
hangman_one = ['O-----', '|  |  ', '|     ', '|     ', '|      ', '|      ']
hangman_two = ['O-----', '|  |  ', '|  O  ', '|     ', '|      ', '|      ']
hangman_three = ['O-----', '|  |  ', '|  O  ', '|  |  ', '|      ', '|      ']
hangman_four = ['O-----', '|  |  ', '|  O  ', '|--|  ', '|      ', '|      ']
hangman_five = ['O-----', '|  |  ', '|  O  ', '|--|--', '|      ', '|      ']
hangman_six = ['O-----', '|  |  ', '|  O  ', '|--|--', '| /    ', '|      ']
hangman_seven = ['O-----', '|  |  ', '|  O  ', '|--|--', '| / \  ', '|      ']
hangman_lst = [hangman_seven, hangman_six, hangman_five, hangman_four, hangman_three, hangman_two, hangman_one, hangman_zero]

# Retrieves a random word from a string of words.
def getRandomWord(string_of_words):
	return random.choice(string_of_words.split())
	
# Displays the hangman graphics so far.
def displayHangman(lives_left):
	for hangman_layer in hangman_lst[lives_left]:
		print(hangman_layer)
	
# Displays the correctly guessed letters so far.
def displayHiddenWord(display):
	print(' '.join(display))
	
# Displays the guessed letters so far.
def displayGuessedLetters(guessed_lst):
	print('Guesses Made: ' + ' '.join(guessed_lst))
	
# Reveals a secret message when a secret passphrase is entered.
def secretMessage():
	print('Thank you for taking your time to try this game out!')
	print('I made this game out of boredom while trying to learn Python during work.')
	print('It\'s not much, but I enjoyed the process a lot building the game up bit by bit.')
	print('I first made the game functional using a fixed hidden word with no visuals at all.')
	print('Then I added in a random word generator to provide a lil\' bit of challenge to the player.')
	print('Eventually, I added in simple visuals to provide the player with some form of guidance during the game.')
	print('If you feel like challenging yourself, try making a game on your own too!')
	print('It doesn\'t have to be a new idea or concept - a simple game like hangman or tic-tac-toe works as well.')
	print('Most importantly, I hope you have fun playing/making games just as much as I do! (:')
	print('Well then, all the best! - YH')
	
# Displays a help page containing game instructions.
def help():
	print('Each turn, you can either guess a letter or the word directly.')
	print('You lose a life if you get it wrong, so be careful!')
	print('Lose all 7 lives (when the hangman is fully drawn) and it\'s game over for you.')
	print('Good luck!')

# Generates a new word for the player to start guessing until the game is over or the player quits.
def newGame():
	lives_left = 7
	hidden_word = getRandomWord(string_of_words)
	display = ['_'] * len(hidden_word)
	
	char_arr = list(hidden_word)
	guessed_chars = []
	chars_left = len(display)
	char_arr_lower = [char.lower() for char in char_arr]
	
	while True:
		displayHiddenWord(display)
		displayGuessedLetters(guessed_chars)
		if chars_left == 0:
			print('Congratulations! You won!')
			print('The hidden word is %s!' % hidden_word)
			break
		char_guess = input()
		incorrect_guess = True
		
		if char_guess.lower() == hidden_word.lower():
			chars_left = 0
			continue

		if char_guess.isalpha() and char_guess.lower() == 'help':
			help()
			continue
			
		if char_guess.isalpha() and char_guess.lower() == 'quit':
			print('Ending game now...')
			break
		
		if char_guess.isalpha():
			char_guess = char_guess.lower()
			if char_guess in guessed_chars:
				print('You already guessed that letter!')
				continue
			else:
				guessed_chars.append(char_guess)
		else:
			print('Only alphabetical characters are allowed!')
			continue
			
		while char_guess in char_arr_lower: 
			incorrect_guess = False
			char_idx = char_arr_lower.index(char_guess)
			display[char_idx] = char_arr[char_idx]
			char_arr_lower[char_idx] = '*'
			chars_left -= 1

		if incorrect_guess:
			lives_left -= 1
			displayHangman(lives_left)
			print('Incorrect! Lives left: ', lives_left)
			if lives_left == 0:
				print('Game Over!')
				break
			else:
				continue
				
		continue
		
# Generates a new session for the player.		
def generateNewSession():
	nextGame = 'y'
	while nextGame.lower() == 'y':
		newGame()
		print('Would you like to play again? [y/n]')
		nextGame = input()
	print('Hope you had fun! ^_^')
	
def main(args):
	print('Welcome to a game of hangman! What is your name?')
	player_name = input()
	if player_name == 'i am your owner':
		secretMessage()
		print('So what\'s your name?')
		player_name = input()	
	print('I hope you enjoy the game, %s!' %player_name)
	print('Enter "help" if you wish to know the game instructions. OvO')
	print('If you wish to quit the game, just type "quit"!')
	print('You may start by guessing a letter.')
	try:
		generateNewSession()
	except EOFError:
		print('N-nani?! The game ended abruptly.. OwO')
	except Exception:
		print('S-something went wrong! Go inform your master about it. OuO')
	
if __name__ == '__main__':
	main(sys.argv[1:])
	