#IMPORTS
import numpy as np
import gym
import universe
import random
import copy
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# GLOBAL PARAMETERS

# Number of games to play
no_games = 100

# Max number of frames per game
max_frames = 5000

# Random move threshold
rm_thresh = .99

# Decay of random threshold as algorithm learns
rm_thresh_decay = 0.995

# Minimum randomness that we want int deciding the next move
rm_min_thresh = 0.01

class Model:
	def __init__(self, input_size, output_size):
		self.model = Sequential()
		self.model.add(Conv2D(32, 2, padding="same", activation="relu", input_shape=input_size))
		self.model.add(MaxPooling2D(pool_size=(3,3)))
		self.model.add(Dropout(0.5))
		self.model.add(Flatten())
		self.model.add(Dense(64, activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(64, activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(output_size, activation='softmax'))
		self.model.compile(loss='mse', optimizer='adam')


		# Storing last n runs
		self.memory = []

		self.discount = 0.95

		# Game no
		self.game = 0
		self.game_rewards = {}
		self.highest_reward = 0
		self.reward_threshold = 0

	def get_move(self, state):
		global rm_thresh
		if np.random.rand() <= rm_thresh:
			return random.randint(0,8)

		state = np.array([state])
		result = self.model.predict(state)[0]

	 	return np.argmax(result)

	def add_to_memory(self, current_state, action, reward, next_state):
		#if len(self.memory) == 4:
		#	self.memory.pop(0)
		#	self.memory.append([current_state, action, reward, next_state])
		#else:
		#	self.memory.append([current_state, action, reward, next_state])
		self.memory.append([current_state, action, reward, next_state, self.game])

		if len(self.memory) > 100000:
			self.memory = []

	def learn(self):
		global rm_thresh
		global rm_thresh_decay
		global rm_min_thresh
		shape = self.memory[0][0].shape
		l = len(self.memory)
		r = random.randint(0,len(self.memory)-5)
		for current_state, action, reward, next_state, game in self.memory[r:r+4]:
			current_state = current_state.reshape(1,shape[0],shape[1],shape[2])
			next_state = next_state.reshape(1,shape[0],shape[1],shape[2])

			target = reward + self.discount * np.amax(self.model.predict(next_state)[0])
			
			target_f = self.model.predict(current_state)
			target_f[0][action] = target

			if rm_thresh > rm_min_thresh:
				rm_thresh = rm_thresh*rm_thresh_decay

			self.model.fit(current_state, target_f, epochs=1, verbose=0)
		self.memory = []

	def update_game(self,game, reward):
		self.game_rewards[self.game] = reward
		self.game = game
		if reward > self.highest_reward:
			self.highest_reward = reward
			self.reward_threshold = 0.3*self.highest_reward

	def clean(self):
		games_to_keep = []
		for key in self.game_rewards.keys():
			if self.game_rewards[key] > self.reward_threshold:
				games_to_keep.append(key)

		new_memory = []
		for state in self.memory:
			if state[4] in games_to_keep:
				new_memory.append(state)

		self.memory = new_memory

def main():
	global no_games
	global max_frames
	# Initialize game
	pacman = gym.make('MsPacman-v0')

	# Get the shape of the frame
	input_size = pacman.reset().shape

	output_size = pacman.action_space.n

	# Initialize the NN that will help approximate the next best move
	NN = Model(input_size, output_size)

	all_rewards = []

	# Play number of games
	i = 1
	for game in range(no_games):	
		# Get initial state
		current_state = pacman.reset()

		total_reward = 0

		# Play for number of frames
		for frame in range(max_frames):
			#print frame,'/',max_frames
			# Display game
			#pacman.render()


			# Get next action to take
			action = NN.get_move(current_state)

			# Play the next sample
			next_state, reward, done, info = pacman.step(action)

			total_reward += reward

			NN.add_to_memory(current_state, action, reward, next_state)

			if len(NN.memory) > 5:
				NN.learn()

			if done:
				break

		NN.update_game(game + 1, total_reward)

		if i == 5:
			NN.clean()
			i = 1
		else:
			i += 1

		print 'Game: ',game,'/',no_games,' Reward: ', total_reward
		all_rewards.append(total_reward)
		#NN.learn()

	print 'Saving Model'
	NN.model.save('model.h5')

	f = open('rewards','w+')
	for reward in all_rewards:
		f.write(str(reward)+'\n')
	f.close()
 			

if __name__=='__main__':
	main()
