# pong_ml
A simple pong game implemented in python along with a neural network based pong playing bot. .   

**Demo:**  

<img src='https://github.com/ApGa/pong_ml/blob/master/nn_bot_demo.gif' width='' alt='Demo' />  

**Requirements:**  
python3  
numpy  
pygame  

**Approach:**  
The general approach is to use an AI that is calculates the position of the ball relative to the paddle to generate data points per frame. 
This dataset is then used to train a neural network to play the game by trying to mimic this AI.  

**Purpose:**  
This project does not really have any practical purpose as finds a more computationally expensive approximation to a function we already know the form of. 
Rather, this project serves as an environment to implement and test out various machine learning algorithms for educational purposes.  

**Usage/Instructions:**  
The game can be run in 4 ways:  
 	1. If you want to play the game yourself (no AI) use: **py -3 run_pong.py user**  
 		-> Play using up and down arrow keys  
 	2. If you want a non-ml based perfect AI (generator_bot) to play the game by calculating analytically the position of the ball  
 		i)  If you want to generate a dataset use: **py -3 run_pong.py generator True**  
 		ii) If you do not want the generator_bot to generate a dataset but still want it to play: **py -3 run_pong.py generator False**    
 	3. After training a neural network using train.py, if you want to see it play, use: **py -3 run_pong.py nn** 

 To train a neural network on a dataset generated using the generator_bot, use: py -3 train.py  

 For implementation details and more detailed usage instructions (such as how to change the network architecture, dataset size 
 and hyperparameters) please read the comments and annotations within the source code. Two particularly interesting functions are 
 generator_bot and nn_bot in pong.py.   


**Todos:**   
Add more detailed usage instruction (for now refer to the detailed comments in the code)  
Try out genetic algorithms such as NEAT algorithm  
Try out reinforcement algorithm  
Create an incomplete jupyter notebook to serve as a tutorial    

**Sources and References:**  
	1. The neural network implementaion network2.py is taken from Michael Nielsen's excellent discussion on neural networks:  
		http://neuralnetworksanddeeplearning.com/  
	2. Also check out the curriculum created by CAIS++, a club I am part of at USC:  
		http://caisplusplus.usc.edu/