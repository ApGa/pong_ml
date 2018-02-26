#Pong clone with bots to play the game or generate a dataset 

import pygame
import numpy as np
import network2
import pickle


class Pong: 

	#constants related to gameplay
	WIDTH = 20
	PADDLE_HEIGHT = 100
	PADDLE_WIDTH = 10
	BALL_DIM = 10
	PADDLE_SPEED = 400
	WIN_WIDTH = 1024
	WIN_HEIGHT = 768
	#negate the velocity's below if you want to change the direction of ball's initial velocity
	BALL_VELOCITY_X = -400
	BALL_VELOCITY_Y = 200

	#constants related to generating the data set
	NUM_DATA = 20000 #number data points to be collected for this dataset
	FRAME_SKIP = 1 #number of frames to skip between collection of data points

	def __init__(self, player = 'user', generate = 'False'): 

		#initialize pygame		
		pygame.init()

		#data members related to gameplay
		self.window = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
		self.quit = False
		self.direction = 0 #direction of the paddle movement; 0 means no movement, 1 is up and -1 is down
		self.ballVelocity = [self.BALL_VELOCITY_X, self.BALL_VELOCITY_Y]
		self.ballPosition = [(self.WIN_WIDTH - self.BALL_DIM)/2, (self.WIN_WIDTH - self.BALL_DIM)/2]
		self.paddlePosition = [self.PADDLE_WIDTH, (self.WIN_HEIGHT - self.PADDLE_HEIGHT)//2]
		self.currentTime = pygame.time.get_ticks()/1000.

		#data members related to generating the dataset
		self.numFrames = 0
		self.training_inputs = []
		self.training_results = []
		self.training_data = []
		self.generate = generate

		self.player = player

		if(player == 'nn'):
			#load neural network
			with open('net.pkl', 'rb') as f: 
				self.net = pickle.load(f)

	#runs the game -- contains the loop that controls the game flow
	def runLoop(self):
		quit = False
		while not self.quit: 
			self.processInput()
			self.updateGame()
			self.generateOutput()


	#processes input from user during the game
	def processInput(self): 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit = True 
				if(self.generate == 'True'): #if self.generate == 'True', dump dataset to file when quitting
					with open("data.pkl", "wb") as f:
						pickle.dump(list(zip(self.training_inputs, self.training_results)), f, protocol=pickle.HIGHEST_PROTOCOL)
		
		pressed = pygame.key.get_pressed()

		#quit game if the escape key is pressed. Also, dump data to the file if generating a dataset
		if pressed[pygame.K_ESCAPE]: 
			self.quit = True
			if(self.generate == 'True'):
				with open("data.pkl", "wb") as f:
					pickle.dump(list(zip(self.training_inputs, self.training_results)), f, protocol=pickle.HIGHEST_PROTOCOL)

		if pressed[pygame.K_UP]: self.direction = -1 #paddle up
		if pressed[pygame.K_DOWN]: self.direction = 1 #paddle down
		self.numFrames+= 1

		if(self.player == 'generator'):
			self.generator_bot()

		if(self.player == 'nn'):
			self.nn_bot()

	#updates position and velocities of game objects for the new frame, and checks if the game has been
	def updateGame(self):
		deltaTime = pygame.time.get_ticks()/1000. - self.currentTime

		#lock fps at 60
		while (deltaTime * 1000 < 16):
			deltaTime = pygame.time.get_ticks()/1000. - self.currentTime

		self.currentTime += deltaTime
		

		#update paddle position
		self.paddlePosition[1] += self.direction*self.PADDLE_SPEED*deltaTime
		self.direction = 0
		
		#prevent paddle from going off screen
		if (self.paddlePosition[1] > self.WIN_HEIGHT - self.PADDLE_HEIGHT - self.WIDTH):
			self.paddlePosition[1] = self.WIN_HEIGHT - self.PADDLE_HEIGHT - self.WIDTH
		elif (self.paddlePosition[1] < self.WIDTH):
			self.paddlePosition[1] = self.WIDTH

		#update balls position
		self.ballPosition[1] += self.ballVelocity[1]*deltaTime
		self.ballPosition[0] += self.ballVelocity[0]*deltaTime


		#check if the ball collided; if so handle it
		self.handleCollision()

		#check if the game has been lost
		self.hasLost()


	#draws the new frame to the screen
	def generateOutput(self): 
		color = (100, 255, 255)
		self.window.fill((0, 0, 0))
		#top wall
		pygame.draw.rect(self.window, color, pygame.Rect(0, 0, self.WIN_WIDTH, self.WIDTH))

		#bottom wall
		pygame.draw.rect(self.window, color, pygame.Rect(0, self.WIN_HEIGHT - self.WIDTH, self.WIN_WIDTH, self.WIDTH))

		#right wall 
		pygame.draw.rect(self.window, color, pygame.Rect(self.WIN_WIDTH - self.WIDTH, 0, self.WIDTH, self.WIN_HEIGHT))

		#paddle 
		pygame.draw.rect(self.window, color, pygame.Rect(self.paddlePosition[0], self.paddlePosition[1], self.WIDTH/2, self.PADDLE_HEIGHT))

		#ball
		pygame.draw.rect(self.window, color, pygame.Rect(self.ballPosition[0], self.ballPosition[1], self.BALL_DIM, self.BALL_DIM))

		#this game is double buffered. This function essentially switches buffers to display the new frame
		pygame.display.flip()

	
	#Handles changes in ball velocity when the ball collides with a surface. Uncomment the commented lines, and comment the lines 
	#immediately above for speed up when the ball collides. Note: Neural network should be retrained to handle speedups if desired.
	def handleCollision(self): 
		#top wall
		if (self.ballPosition[1] <= self.WIDTH): 
			self.ballPosition[1] = self.WIDTH
			self.ballVelocity[1] *= -1
			#self.ballVelocity[1] *= -1.1
		
		#right wall
		if (self.ballPosition[0] >= self.WIN_WIDTH - self.BALL_DIM): 
			self.ballPosition[0] = self.WIN_WIDTH - self.BALL_DIM
			self.ballVelocity[0] *= -1
			#self.ballVelocity[0] *= -1.1
		
		#bottom wall
		if (self.ballPosition[1] >= self.WIN_HEIGHT - self.WIDTH - self.BALL_DIM):
			self.ballPosition[1] = self.WIN_HEIGHT - self.WIDTH - self.BALL_DIM 
			self.ballVelocity[1] *= -1 
			#self.ballVelocity[1] *= -1.1
		

		#paddle
		if (self.ballPosition[0] <= self.PADDLE_WIDTH + self.WIDTH / 2 and self.ballPosition[0] >= self.PADDLE_WIDTH):
			if (self.ballPosition[1] >= self.paddlePosition[1] and self.ballPosition[1] <= self.paddlePosition[1] + self.PADDLE_HEIGHT):
				self.ballPosition[0] = self.PADDLE_WIDTH + self.WIDTH / 2 
				self.ballVelocity[0] *= -1
				#self.ballVelocity[0] *= -1.1

		
	#sets quit flag to true when the ball goes off-screen -- Game Over
	def hasLost(self):
		if (self.ballPosition[0] < 0): 
			self.quit = True
			


	#fitness function to train the neural network using the NEAT algorithm. Essentially the square of the gameplay time. 
	#The square is taken to differentiate higher times from lower times more significantly
	#Not currently used
	def fitness(self): 
		return (pygame.time.get_ticks()/1000)**2


	#plays the game perfectly by calculating what the position of the ball will be when the ball is at the same x coordinate as the paddle
	#and accordingly choosing whether to move the paddle and in which direction. 
	#If self.generate = True, the decisions of this bot and the corresponding inputs will be used to create a dataset
	def generator_bot(self):
		
		#the direc_vec represents the direction the paddle should move [1, 0, 0] => down, [0, 1, 0] => idle, [0, 0, 1] => up
		direc_vec = [0, 1, 0] #by default the paddle should not move

		#if the ball is moving to the left, calculate the y-position (collisionPosition) of the ball when it crosses the paddle's x-position
		#if at this time, the paddle is below the ball => the paddle should decide to move up in the current frame
		#else if at this time, the paddle is above the ball => the paddle should decide to move down
		if (self.ballVelocity[0] < 0 ):
			collisionTime = (self.ballPosition[0] - self.WIDTH - self.PADDLE_WIDTH)/(-1 * self.ballVelocity[0])
			collisionPosition = self.ballVelocity[1] * collisionTime + self.ballPosition[1]
			if (self.paddlePosition[1] + self.PADDLE_HEIGHT/2 + 5 < collisionPosition): 	#paddle above the ball
				self.direction = 1 
				direc_vec = [1, 0, 0]
			elif (self.paddlePosition[1] + self.PADDLE_HEIGHT/2 - 5 > collisionPosition):   #paddle is below the ball
				self.direction = -1
				direc_vec = [0, 0, 1]

		if(self.generate == 'True'):
			#log will contain a list of the inputs for this frame to be added to the dataset as a single data point
			log = []

			#In particular, log contains the following six inputs (scaled down to prevent overflow in calculations while training the neural network):
			#(ball's x position, ball's y position, ball's x velocity, ball's y velocity, paddle's x position, paddle's y position)
			log.extend((round(self.ballPosition[0])/self.WIN_WIDTH, round(self.ballPosition[1])/self.WIN_HEIGHT, round(self.ballVelocity[0])/100, 
				round(self.ballVelocity[1])/100, round(self.paddlePosition[0])/self.WIN_WIDTH, round(self.paddlePosition[1])/self.WIN_HEIGHT))


			#if generating a dataset, generate a datapoint every FRAME_SKIP number of frames
			if(self.numFrames % self.FRAME_SKIP == 0):
				print("DataPoint: " + str(self.numFrames/self.FRAME_SKIP))

				#create a numpy array from the logged inputs from this frame
				np_log = np.reshape(log, (6, 1))

				#create a numpy array for the paddle direction (output) associated with the inputs logged 
				np_direc = np.reshape(direc_vec, (3, 1)) 

				#append the above numpy arrays for input and output to the training_inputs and training_results
				self.training_inputs.append(np_log) 
				self.training_results.append(np_direc)

				#if reached NUM_DATA number of datapoints, save the dataset and quit the game 
				if(self.numFrames == self.NUM_DATA):
					with open("data.pkl", "wb") as f:
						self.quit = 1
						pickle.dump(list(zip(self.training_inputs, self.training_results)), f, protocol=pickle.HIGHEST_PROTOCOL)


	#plays the game by feeding information about the current frame into the neural network and using the output of the network to 
	#decide which way to move the paddle
	def nn_bot(self): 

		#feeds the scaled inputs for the current frame asn a numpy array into the neural network and stores the returned direction vector (direc_vec)
		direc_vec = self.net.feedforward(np.reshape([(round(self.ballPosition[0])/self.WIN_WIDTH, round(self.ballPosition[1])/self.WIN_HEIGHT, 
			round(self.ballVelocity[0])/100, round(self.ballVelocity[1])/100, round(self.paddlePosition[0])/self.WIN_WIDTH, round(self.paddlePosition[1])/self.WIN_HEIGHT)], (6, 1)))
		
		#This returns the index of the direc_vec with the highest value. Consistent with our notation for direc_vec in analytic_bot:
		#if the 0th index is the highest the paddle should move down, if the 1st index is the highest the paddle should stay idle
		#and if the the 2nd index is the highest the paddle should move up
		direc_vec = np.argmax(direc_vec)
		if direc_vec == 0 :
			self.direction = 1 #down
		elif direc_vec == 1 :
			self.direction = 0 #idle
		else :
			self.direction = -1 #up

	#rounds the number to the closest whole number. If exactly in the middle, rounds up. 
	def round(num):
		return floor(num + 0.5) 
