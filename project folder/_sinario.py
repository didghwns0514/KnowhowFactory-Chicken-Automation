# -*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
# ctrl + / => block comment hotkey
# shift + tab or tab => indent hotkey

########################import py field####################
import tensorflow as tf
import pandas
import random
import numpy as np
import time
import os
import pygame
import tkinter as tk
from tkinter import *
import threading
import sys
#import Queue

########################import field#######################
# import state
########################global value#######################
#import Global as G
#import TIME as T
#import FLAG as F  # flag으로 training이랑 loop 조작할 때 쓰기
#import simulator
#import screen_disp

###########################################################


def order_breaker(first_CN, second_CN):
	# 2개 쪼개서 넣어주는 함수,  input placeholder 용
	# T.times
	# order 자체 times
	# address 1개 받음
	# address 2
	# importance
	# stage
	def single_breaker(CN):
		lister = []
		lister.append(T.times)
		lister.append(G.list_chicken[CN].times)
		lister.append(G.list_chicken[CN].address[0])
		lister.append(G.list_chicken[CN].address[1])
		lister.append(G.list_chicken[CN].importance)
		lister.append(G.list_chicken[CN].workingstage_template)
		return lister

	lister_1 = None
	lister_2 = None

	lister_1 = single_breaker(first_CN)
	lister_2 = single_breaker(second_CN)

	if lister_1 == None or lister_2 == None:
		raise ValueError('wrong order_breaker in agent.py')

	lister_1.extend(lister_2)

	return lister_1


class Q_agent:
	# naive neural network with 3 hidden layers and relu as non-linear function
	def __init__(self, options):
		# option으로 뭔가를 해주는 듯, 일단 input 차원만큼 넣어준다, 매 layer 옵션 다 들어있는 듯
		self.w1 = self.weight_variable([options.OBSERVATION_DIM, options.H1_SIZE])
		self.b1 = self.bias_variable([options.H1_SIZE])
		self.w2 = self.weight_variable([options.H1_SIZE, options.H2_SIZE])
		self.b2 = self.bias_variable([options.H2_SIZE])
		self.w3 = self.weight_variable([options.H2_SIZE, options.H3_SIZE])
		self.b3 = self.bias_variable([options.H3_SIZE])
		self.w4 = self.weight_variable([options.H3_SIZE, options.ACTION_DIM])
		self.b4 = self.bias_variable([options.ACTION_DIM])

	def xavier_initializer(self, shape):
		# weight용 초기화 함수 - 자비어 방식
		dim_sum = np.sum(shape)
		if len(shape) == 1:
			# 1차원 짜리 행렬 이라면
			dim_sum = dim_sum + 1
		# 2 이상의 차원으로 생각???
		bound = np.sqrt(6.0 / dim_sum)
		return tf.random_uniform(shape, minval=-bound, maxval=bound, dtype=tf.float32)

	# -3 ~ 3 아마 검증 된 부분인 듯

	def weight_variable(self, Shape):
		# weight Variable 만들기 위함 - variable인 텐서는 값이 바뀔 수 있다
		return tf.Variable(self.xavier_initializer(Shape))

	def bias_variable(self, Shape):
		# bias Variable 만들기 위함
		return tf.Variable(self.xavier_initializer(Shape))

	def add_value_net(self, options):  # 그래프들 def 들을 연결한다
		# adding options to graph - 차후 사용성을 위해서 input 용인 듯
		observation = tf.compat.v1.placeholder(tf.float32, [None, options.OBSERVATION_DIM])
		# tf.compat.v1.disable_eager_execution()
		h1 = tf.compat.v1.nn.relu(tf.matmul(observation, self.w1) + self.b1)
		#h1 = tf.nn.dropout(h1, keep_prob=0.75)
		h2 = tf.nn.relu(tf.matmul(h1, self.w2) + self.b2)
		#h2 = tf.nn.dropout(h2, keep_prob=0.75)
		h3 = tf.nn.relu(tf.matmul(h2, self.w3) + self.b3)
		#h3 = tf.nn.dropout(h3, keep_prob=0.75)
		Q = tf.squeeze(tf.matmul(h3, self.w4) + self.b4)
		# 요소 갯수 재한 없도록 squeeze 사용, 마지막 output layer

		return observation, h1, h2, h3, Q

	def sample_action(self, Q, feed, eps, options):
		# Q는 전체 그래프, feed :?
		# eps : epsilon-greedy 위한 것
		# options : NN 개수 파라미터

		act_values = Q.eval(feed_dict=feed)
		# input으로 기억함, 이게 들어갔을 때 q의 output
		# action dimension 전체

		if random.random() <= eps:
			# random action / Q value는 어차피 max로 업데이트 됨
			action_index = random.randrange(options.ACTION_DIM)

		else:
			action_index = np.argmax(act_values)
		# max Q 따르는 action 고를 때

		action = np.zeros(options.ACTION_DIM)
		action[action_index] = 1
		# 고른 action을 1로 하자...

		return action


class Options:
	def __init__(self, env):
		# 인자들 전부 전달해주는 부분
		self.OBSERVATION_DIM = env[0]  # input 디멘션
		self.H1_SIZE = env[1]  # size of hidden layer 1
		self.H2_SIZE = env[2]  # size of hidden layer 2
		self.H3_SIZE = env[3]  # size of hidden layer 3
		self.ACTION_DIM = env[4]  # number of actions to take

		self.MAX_EPISODE = env[5]  # max number of episodes iteration
		self.GAMMA = env[6]  # discount factor of Q learning
		self.INIT_EPS = env[7]  # initial probability for randomly sampled action
		self.FINAL_EPS = env[8]  # final probability for randomly sampled action
		self.EPS_DECAY = env[9]  # epsilon decay rate
		self.EPS_ANNEAL_STEPS = env[10]  # steps of intervals to decay epsilon
		self.LR = env[11]  # learning rate
		self.MAX_EXPERIENCE = env[12]  # size of experience replay memory
		self.BATCH_SIZE = env[13]  # mini batch size


def clipped_error(error):
	# 후버 로스를 사용하여 error clip
	return tf.where(tf.abs(error) < 1.0, 0.5 * tf.square(error), tf.abs(error) - 0.5)


def getActivations(layer,stimuli):
	units = sess.run(layer,feed_dict={x:np.reshape(stimuli,[1,784],order='F'),keep_prob:1.0})
	plotNNFilter(units)

	
class InputBox:


	def __init__(self, return_val, text=''):
		x, y, w, h = return_val
		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('lightskyblue3')
		self.text = text
		self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(event.pos):
				# Toggle the active variable.
				self.active = not self.active
			else:
				self.active = False
			# Change the current color of the input box.
			self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					print(self.text)
					self.text = ''
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				# Re-render the text.
				self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

	def update(self):
		# Resize the box if the text is too long.
# 		width = max(200, self.txt_surface.get_width()+10)
# 		self.rect.w = width
		pass

	def draw(self, screen):
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		# Blit the rect.
		pygame.draw.rect(screen, self.color, self.rect, 2)
	
def run_sinario():
	# 분석을 위해서 시나리오를 대입하기 위한 부분
	# @ AGENT 부분
	############################################
	env = [12, 12,  10,   8,  2,  300,0.95,  1,  1e-5,  0.95, 300,  1e-4, 2000,  256]
	options = Options(env)
	agent = Q_agent(options)
	obs, h1, h2, h3, Q = agent.add_value_net(options)


	curr_dir1 = str(os.getcwd() + "\\checkpoints-order_sorter")
	curr_dir = os.path.join(curr_dir1, "model-order_sorter")
	saver = tf.train.Saver()
	checkpoint = tf.train.get_checkpoint_state(curr_dir1)
	
	able_to_debug = 0 # chekpoint 로드 되면은 1로 가게 한다
	sess = tf.compat.v1.InteractiveSession()
	sess.run(tf.global_variables_initializer())
	
	if checkpoint and checkpoint.model_checkpoint_path : 
	# 둘다 체크 들어가는데 폴더는 있어야 할듯
		saver.restore(sess, checkpoint.model_checkpoint_path)
		#restore 하기 전에 init 하지 마라는데 무슨 뜻??
		print("★"*50)
		print('Successfully loaded : ', checkpoint.model_checkpoint_path)
		print("★"*50)
		able_to_debug = 1
		time.sleep(3)
	else:
		print('failed to load the checkpoint...')

	if able_to_debug == 1:
	# 로드 해서 test하는 것이 가능하다면 전체 수행을 할 수 있으므로...
	###############################################################################

		#@TKINTER common variables
		##########################
		SCREEN_SIZE = (1000, 800)
		
		# @TKINTER
		##########################

# 		root = tk.Tk()
# 		embed = tk.Frame(root, width = SCREEN_SIZE[0], height = SCREEN_SIZE[1])
# 		# ^creates embed frame for pygame window
# 		embed.grid(columnspan = (SCREEN_SIZE[0]+100), rowspan = SCREEN_SIZE[1]) # Adds grid
# 		embed.pack(side = LEFT) #packs window to the left
# 		buttonwin = tk.Frame(root, width = 75, height = SCREEN_SIZE[1])
# 		buttonwin.pack(side = LEFT)
# 		os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# 		os.environ['SDL_VIDEODRIVER'] = 'windib'
		
		###############################################################################
		###############################################################################
		
		# @PYGAME
		#PYGAME initialization
		############################
		pygame.init()
		#Title and Icon
		pygame.display.set_caption("chicken-agent-NN")
		curr_dir = str(os.getcwd() + "\\logos_pygame"+"\\fried-chicken.png")
		icon = pygame.image.load(curr_dir)
			#icon = pygame.image.load('logo.png')
		pygame.display.set_icon(icon)
		done = False
		flag = True  
		clock = pygame.time.Clock()
		

		
		#@ PYGAME common variables
		############################
		BLACK= ( 0,  0,  0)
		WHITE= (255,255,255)
		BLUE = ( 0,  0,255)
		GREEN= ( 0,255,  0)
		RED  = (255,  0,  0)
		OFF =  (131, 131, 151)
		OFF_LINE = (83,83,83)
		CIRCLE_SIZE = 10
		
		SCREEN_COL = (0, 0, 30)
		SCREEN_SIZE = (800, 600)
		
		COLOR_INACTIVE = pygame.Color('lightskyblue3')
		COLOR_ACTIVE = pygame.Color('dodgerblue2')
		FONT = pygame.font.Font(None, 32)
		
		
		
		
		
		# @create screen
		##########################
		screen = pygame.display.set_mode(SCREEN_SIZE)
		
		


		
		
		
		
		###############################################################################
		###############################################################################
	
	
		# GAME loop + tkinter: 
		# infinite loop, opening the game

		h1_axis = []
		for i in range(int(options.H1_SIZE)):
			h1_axis.append([100 + 150, 68+ i*40])
		h2_axis = []
		for i in range(int(options.H2_SIZE)):
			h2_axis.append([200 + 150, 108 + i*40])
		h3_axis = []
		for i in range(int(options.H3_SIZE)):
			h3_axis.append([300 + 150, 148 + i*40])
		q_axis = []
		for i in range(int(options.ACTION_DIM)):
			q_axis.append([400 + 150, 268 + i*40])
		
		
		def rect_pos(center):
			quarter_len = 6
			
			x = int(center[0] - (quarter_len*2))
			y = int(center[1] - quarter_len)
			w = int(4*quarter_len)
			h = int(2*quarter_len)
			if x < 0 or y < 0:
				raise ValueError('??? _1')
			
			
			#x, y, w, h
			return x-60, y-10, w+30, h+20
		
		
		input_box1 = InputBox(rect_pos(h1_axis[0]))
		input_box2 = InputBox(rect_pos(h1_axis[1]))
		input_box3 = InputBox(rect_pos(h1_axis[2]))
		input_box4 = InputBox(rect_pos(h1_axis[3]))
		input_box5 = InputBox(rect_pos(h1_axis[4]))
		input_box6 = InputBox(rect_pos(h1_axis[5]))
		input_box7 = InputBox(rect_pos(h1_axis[6]))
		input_box8 = InputBox(rect_pos(h1_axis[7]))
		input_box9 = InputBox(rect_pos(h1_axis[8]))
		input_box10 = InputBox(rect_pos(h1_axis[9]))
		input_box11 = InputBox(rect_pos(h1_axis[10]))
		input_box12 = InputBox(rect_pos(h1_axis[11]))
		
		input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5,
					  input_box6, input_box7, input_box8, input_box9, input_box10, 
					  input_box11, input_box12]
		##########################
		while not done :
			# screen update for # per seconds(frames per seconds)
			clock.tick(10)
			
			for event in pygame.event.get() : # EVENT window 프로그램 돌리기 위해 반드시 필요
			# for any event parameter happening while game is running, we loop
				if event.type == pygame.QUIT :
				# ex) if ESC is pressed
					done = True
					pygame.quit()
					sys.exit()
					quit()
				elif event.type == pygame.ACTIVEEVENT: # mouse position? in the screen or not
					flag ^= True
				for box in input_boxes:
					box.handle_event(event)
			
			for box in input_boxes:
				box.update()

			
			# anything that has to continuously happen in the screen
			#______________________________________________________________
			# add value of RGB 0~255
			screen.fill(SCREEN_COL)
			

			#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			#@ ACTUAL WORK
			##################
			
			
			# -1) tesnsor feed 해줄 value들 설정해주어야됨
			
			
			# 0) tensor feed 해주어야 됨
			
			for box in input_boxes:
				box.draw(screen)
			
			# 좌측 상단이 0,0  /  우측 하단이 800, 600
			# 1) H1 : 12

			for i in range(len(h1_axis)):
				for j in range(len(h2_axis)):
					pygame.draw.aaline(screen, OFF_LINE, h1_axis[i], h2_axis[j], True)
			for i in range(len(h2_axis)):
				for j in range(len(h3_axis)):
					pygame.draw.aaline(screen, OFF_LINE, h2_axis[i], h3_axis[j], True)
			for i in range(len(h3_axis)):
				for j in range(len(q_axis)):
					pygame.draw.aaline(screen, OFF_LINE, h3_axis[i], q_axis[j], True)
					
			for i in range(len(h1_axis)): #h1 size
				# if tensorvalue == XXX :
				pygame.draw.circle(screen, OFF, h1_axis[i], CIRCLE_SIZE)
				# else: XXXX
				
			for i in range(len(h2_axis)):
				pygame.draw.circle(screen, OFF, h2_axis[i], CIRCLE_SIZE)

					
			for i in range(len(h3_axis)):
				pygame.draw.circle(screen, OFF, h3_axis[i], CIRCLE_SIZE)

					
			for i in range(len(q_axis)):
				pygame.draw.circle(screen, OFF, q_axis[i], CIRCLE_SIZE)

			
			
			#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			

			# always needed
			pygame.display.update() #portion update
			#pygame.display.flip() #entire screen w/o arguments passed
			#______________________________________________________________
	else:
		print('since unable to load the check-point, exit program!')
		time.sleep(3)

if __name__ == '__main__':
	run_sinario() # stand alone

'''
https://github.com/AdnanZahid/SnakeGame/blob/master/SnakeGame.py
https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html
pygame -> https://kkamikoon.tistory.com/129

tkinter + pygame - > http://grapevine.com.au/~wisteria/tkfront/pygame_tkinter.html

'''


