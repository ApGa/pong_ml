#Run this script using to run the pong game
#Refer to the commandLineError and generatorError below for more information 
#about the command line arguments for the options with which to run pong

import pong
import sys

commandLineError = "Please enter a command line argument as follows:\n" \
	+ "'user' if you want to play\n" \
	+ "'nn' if you want a neural network to play\n" \
	+ "'generator' if you want a perfect non-ml based bot to play\n"

generatorError = "Note: If you choose generator, enter a second argument specifying:\n" \
	+ "'True' if you want it to generate a dataset and 'False' otherwise\n"

if(len(sys.argv) < 2): 
	print(commandLineError + generatorError)
else:
	if(sys.argv[1] == 'user'):
		game = pong.Pong('user')
		game.runLoop()

	elif(sys.argv[1] == 'nn'):
		game = pong.Pong('nn')
		game.runLoop()

	elif(sys.argv[1] == 'generator'):
		if(len(sys.argv) < 3):
			print(generatorError)
		elif(sys.argv[2] == 'True' or sys.argv[2] == 'False'):
			game = pong.Pong('generator', sys.argv[2])
			game.runLoop()
		else:
			print(generatorError)
