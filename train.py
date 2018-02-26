#This script trains the neural network using the dataset specified
#edit the capitalized veriables below if you want to customize the training process
#and neural network architecture 

import pickle
import network2


#file from which the dataset should be loaded
DATA_FILE = 'data2.pkl'	

#architecture of the neural network. 6 is the number of inputs and 3 is the number of outputs
#the 30s in the middle represent the number of neurons per hidden layer. So this configuration 
#has 2 hidden layers with 30 neurons each. Feel free to add more hidden layers and change the number
#of neurons per hidden layer, but do not change the inputs and outputs unless you modify pong.py 
#to account for that
ARCHITECTURE = [6, 30, 30, 3]	

#file to which the trained network will be written
NETWORK_FILE = 'net.pkl'

#hyperparameters for stochastic gradient descent
NUM_EPOCHS = 200
MINI_BATCH_SIZE = 75
LEARNING_RATE = 0.5

#load dataset
with open(DATA_FILE, 'rb') as f: 
	training_data = pickle.load(f)

#create network with described architecture and the cross entropy cost function
#you can choose to instead load an existing network from a file to further train it by 
#uncommenting the two lines below the following line
net = network2.Network(ARCHITECTURE, cost = network2.CrossEntropyCost)

#with open('net.pkl', 'rb') as n:
#	net = pickle.load(n)

print("created network...")

print("training started...")

#train the network using stochastic gradient descent
#For implementation, look at network2.py
net.SGD(training_data, NUM_EPOCHS, MINI_BATCH_SIZE, LEARNING_RATE)

print("training ended...")

print("storing network...")

#print(net.biases)

#store network with name described by NETWORK_FILE
with open(NETWORK_FILE, 'wb') as d: 
	pickle.dump(net, d, protocol=pickle.HIGHEST_PROTOCOL)

print('network dumped!')

