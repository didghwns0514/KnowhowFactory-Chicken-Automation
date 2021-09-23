#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
import tensorflow as tf
#import pandas
import random
import numpy as np
import time
import os


########################import field#######################
#import state
########################global value#######################
import Global as G
import TIME as T
import FLAG as F # flag으로 training이랑 loop 조작할 때 쓰기
import simulator


###########################################################
 
########
# input으로 배달원 전체
# 6명 자리면 6칸 + 18개
#### 근데 치킨 소팅 먼저 하기로 함
#### dummy value
#### input은 얼만큼 받을 것인지
#### reward 함수 작성해야 한다
#### 배달부 차이는 그렇게 크지 않은 것으로 판별
#######################################################
#######################################################
# 1) 2개 이상의 치킨이 있을 때의 소팅 프로그램 먼저 처리될 것을 앞으로 올리는 식의... 배달 list 있을 때
# 2) 배달부 pick system
# 3) 두개 agent 함께 관리하는 agent
#######################################################
#######################################################
########
########
#version : tensorflow 1.15
########


MAX_SCORE_QUEUE_SIZE = 300

# def score_to_learning():
# # score 기록 대로 저장할지 안할지 판단하는 곳
# 	def average(lister):
# 	# 리스트 평균 구하는 함수
# 		if len(list) != 0 :
# 			return(sum(lister)/len(list))
# 		else:
# 			return False
# 	if average(G.score_queue) == False:
# 	# 기록을 할 score 자체가 없음
# 		return False
# 	# G.score
# 	else:
# 		if G.score_board_value < G.score_now_max :
			


def score_board():
# 점수를 파일로 저장해서, 지금까지 돌린거 중에 가장 좋은 score 남도록 한다
# 그리고 가장 높았던 점수를 리턴해준다

	G.content = None
	# 점수 마커
	G.curr_dir = str(os.getcwd() + "\\score_boarder")
	# 지금 작업중인 경로
	G.curr_dir_f = str(G.curr_dir) + "\\score_board.txt"
	# 파일까지의 경로
	file_exist = os.path.isfile(G.curr_dir_f)
	# 논리값 return, 파일이 있는가 없는가

	def write():
		if file_exist : # 파일 존재하면
			f = open(G.curr_dir_f, 'r')
			f.seek(0)
			content = f.read()
			f.close()

			if not(content == ""): # null이 아니면
				if F.lv_score_board_fix == 0 :
					G.score_board_value = float(content) # 에피 끝날 떄 까지 고정값
					F.score_board_fix(1)
				if float(content) >= G.score_now_max: #저장 값이 크다
					pass
				else:
					with open(G.curr_dir_f, 'w+') as out_file :
					# data is over-written with w+ parameter so use r+
						out_file.seek(0) # goint to top of the file just in case
						out_file.write(str(G.score_now_max)) # 값을 쓴다
							#G.score_board_value = G.score
			else: # 파일있는데 null인 경우
				out_file.write(str(G.score))
				G.score_board_value = G.score
		else: # 파일 생성만 하고 끝난다
			with open(G.curr_dir_f, 'w+') as out_file :
				out_file.write(str(G.score))
				G.score_board_value = G.score
				

	
	if not os.path.isdir(G.curr_dir):
	# 존재하지 않는다면
		os.mkdir(G.curr_dir)
		write()
		# 경로를 만들어준다
	else:
	# 폴더가 존재하면
	# 바로 파일 작업으로 넘어감
		write()

		

def tf_environment_check():
	
	print('tensorflow version : ', tf.VERSION)
	time.sleep(2)
	
	from tensorflow.python.client import device_lib
	print(device_lib.list_local_devices())
	### tensorflow에서 사용가능한 device list 출력
	time.sleep(5)
	
	if tf.test.is_gpu_available() == False :
	#사용가능한 gpu있으면 True
		print('._No Available GPU_.' * 5)
		time.sleep(5)
	else :
	#참일 떄
		print('GPU is available' * 3)
		
	#proceed = input('hit anything to proceed')
	print('\n'*5)

def bubble_sort():
#앞쪽 item인 경우에 chicken importance가 높은 애들을 배치
	list_buffer = None
	order_length = len(G.list_chicken)

	for i in range(order_length - 1):
		for j in range(order_length - i - 1):
			if G.list_chicken[j].importance < G.list_chicken[j+1].importance :
				list_buffer = G.list_chicken[j]
				G.list_chicken[j] = G.list_chicken[j+1]
				G.list_chicken[j+1] = list_buffer

def order_breaker(first_CN, second_CN):
#2개 쪼개서 넣어주는 함수,  input placeholder 용
	# T.times
	# order 자체 times
	# address 1개 받음
	# address 2
	# importance
	# score ? -> 딱히...
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
	
	if lister_1 == None or lister_2 == None :
		raise ValueError('wrong order_breaker in agent.py')
	
	lister_1.extend(lister_2)
	
	return lister_1
		

	
class Q_agent :
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
		if len(shape) == 1 : 
		# 1차원 짜리 행렬 이라면
			dim_sum = dim_sum + 1
			# 2 이상의 차원으로 생각???
		bound = np.sqrt(6.0/ dim_sum) 
		return tf.random_uniform(shape, minval = -bound, maxval=bound, dtype=tf.float32)
		# -3 ~ 3 아마 검증 된 부분인 듯
	
	
	def weight_variable(self, Shape):
	# weight Variable 만들기 위함 - variable인 텐서는 값이 바뀔 수 있다
		return tf.Variable(self.xavier_initializer(Shape))

	
	def bias_variable(self, Shape):
	# bias Variable 만들기 위함
		return tf.Variable(self.xavier_initializer(Shape))
	
	
	def add_value_net(self, options): #그래프들 def 들을 연결한다
	# adding options to graph - 차후 사용성을 위해서 input 용인 듯
		observation = tf.compat.v1.placeholder(tf.float32, [None, options.OBSERVATION_DIM])
		#tf.compat.v1.disable_eager_execution()
		h1 = tf.compat.v1.nn.relu(tf.matmul(observation, self.w1) + self.b1)
		h1 = tf.nn.dropout(h1, keep_prob = 0.75)
		h2 = tf.nn.relu(tf.matmul(h1, self.w2) + self.b2)
		h2 = tf.nn.dropout(h2, keep_prob = 0.75)
		h3 = tf.nn.relu(tf.matmul(h2, self.w3) + self.b3)
		h3 = tf.nn.dropout(h3, keep_prob = 0.75)
		Q = tf.squeeze(tf.matmul(h3, self.w4) + self.b4)
		#요소 갯수 재한 없도록 squeeze 사용, 마지막 output layer

		return observation, Q
	
	
	def sample_action(self, Q, feed, eps, options):
	# Q는 전체 그래프, feed :?
	# eps : epsilon-greedy 위한 것
	# options : NN 개수 파라미터
		
		act_values = Q.eval(feed_dict=feed)
		# input으로 기억함, 이게 들어갔을 때 q의 output
		# action dimension 전체 
		
		if random.random() <= eps :
		# random action / Q value는 어차피 max로 업데이트 됨
			action_index = random.randrange(options.ACTION_DIM)
			
		else: 
			action_index = np.argmax(act_values)
			#max Q 따르는 action 고를 때
		
		action = np.zeros(options.ACTION_DIM)
		action[action_index] = 1
		# 고른 action을 1로 하자...
		
		return action

class Options :
	def __init__(self, env):
		# 인자들 전부 전달해주는 부분
		self.OBSERVATION_DIM = env[0] # input 디멘션
		self.H1_SIZE = env[1] # size of hidden layer 1
		self.H2_SIZE = env[2] # size of hidden layer 2
		self.H3_SIZE = env[3] # size of hidden layer 3
		self.ACTION_DIM = env[4] # number of actions to take
		
		self.MAX_EPISODE = env[5] # max number of episodes iteration
		self.GAMMA = env[6] # discount factor of Q learning
		self.INIT_EPS = env[7] # initial probability for randomly sampled action
		self.FINAL_EPS = env[8] # final probability for randomly sampled action
		self.EPS_DECAY = env[9] # epsilon decay rate
		self.EPS_ANNEAL_STEPS = env[10] #steps of intervals to decay epsilon
		self.LR = env[11] # learning rate
		self.MAX_EXPERIENCE = env[12] # size of experience replay memory
		self.BATCH_SIZE = env[13] # mini batch size

def clipped_error(error):
# 후버 로스를 사용하여 error clip
	return tf.where(tf.abs(error) < 1.0, 0.5*tf.square(error), tf.abs(error) - 0.5)

def running_order_sorter():
# Agent trainer, simulator는 T.time 마다 돌도록 되어있음
	# T.times
	# order 자체 times
	# adress 2개 받음
	# importance
	# score ? -> 안 넣음
	# stage
	################################################################################
	# 이거 2개를 가지고 넣어야 하니깐... state의 시작 단계에서 부터 적용하는 것으로!
	################################################################################
	# T.times, times, address1, address2, importance, stage : 5개
	
	tf_environment_check()
	# 파라미터 체킹
	
	#      0,   1,   2,   3,  4,    5,   6,  7,     8,     9,  10,    11,   12,   13
	env = [12, 12,  10,   8,  2,  300,0.95,  1,  1e-5,  0.95, 300,  1e-4, 2000,  256]
	# 각종 파라미터들 전달
	#https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw?fbclid=IwAR3cWv4ULiZAQpAIyvRDY_KbgUT2G4g9BirZFUxI9Jho6uUHarqpqLgTQYk
	
	options = Options(env)
	# class로 graph parameter 생성
	
	agent = Q_agent(options) 
	# 그래프를 요소들을 전달
	
	sess = tf.compat.v1.InteractiveSession()
	# 텐서 용 session 생성, sess.run()하기 위한 것
	
	obs, Q1 = agent.add_value_net(options)
	# Max experience 이전 사용하는 Q 
	
	act = tf.compat.v1.placeholder(tf.float32, [None, options.ACTION_DIM])
	#구조체 hold하는 부분 input용 
	rwd = tf.compat.v1.placeholder(tf.float32, [None, ])
	#reward용인건 알겠음..?
	
	next_obs, Q2 = agent.add_value_net(options)
	# 그래프 생성,  (observation + 전체 그래프), target
	
	values1 = tf.reduce_sum(tf.multiply(Q1, act), reduction_indices = 1)
	#행 합계(reduction_indices)
	values2 = rwd + ( options.GAMMA * tf.reduce_max(Q2, reduction_indices = 1) )
	# reduction_indices = 1 행합계
	# reduce_max 최대값 1개만 고르는 형식 Q max 값
	
	loss = tf.reduce_mean(clipped_error( tf.square(values1 - values2) ))
	# loss graph/function 정의, square -> 제곱
	
	train_step = tf.train.AdamOptimizer(options.LR).minimize(loss)
	sess.run(tf.global_variables_initializer())
	# jupyter lab등에서 사용할 때 수행되어야 되는 것
	
	#####################################################################################
	
	
	#saving and loading networks
	############################
	# https://goodtogreate.tistory.com/entry/Saving-and-Restoring
	# https://www.google.com/search?q=tensorflow+saver.save(&rlz=1C1GCEA_enKR869KR869&oq=tensorflow+saver.save(&aqs=chrome..69i57j0l5.5249j0j4&sourceid=chrome&ie=UTF-8
	# https://www.easy-tensorflow.com/tf-tutorials/basics/save-and-restore
	# http://solarisailab.com/archives/2524
	
	test_query = 0
	# 0이면 load 해도 학습 진행, 1이면 학습 진행
	
	#curr_dir = str(os.getcwd() + "/checkpoints-order_sorter").replace('/','\\')
	curr_dir1 = str(os.getcwd() + "\\checkpoints-order_sorter")
	curr_dir = os.path.join(curr_dir1, "model-order_sorter")
	print(curr_dir)
	#question = input('directory check')
	# tensor save되는 폴더
	saver = tf.train.Saver()
	checkpoint = tf.train.get_checkpoint_state(curr_dir1)
	if not os.path.isdir(curr_dir1):
	# 존재하지 않는 폴더라면
		os.mkdir(curr_dir1)
		#만들어줌
		print("▼"*50)
		print('Could not find old network weights and added a new folder')
		print("▼"*50)
		time.sleep(3)
	else:
	# 존재한다면
		if checkpoint and checkpoint.model_checkpoint_path : 
		# 둘다 체크 들어가는데 폴더는 있어야 할듯
			saver.restore(sess, checkpoint.model_checkpoint_path)
			#restore 하기 전에 init 하지 마라는데 무슨 뜻??
			print("★"*50)
			print('Successfully loaded : ', checkpoint.model_checkpoint_path)
			print("★"*50)
			time.sleep(3)
			asked = input('if u want to just run test : 1, not type 0')
			# to run test or not when it is loaded
			
			try :
				if int(asked) == 1:
					test_query = 1
				else:
				# keep learning
					pass
			except ValueError :
				print(' worng number input, proceeding w/o TEST')
				test_query = 0
			else:
				test_query = 0
			
		else:
			print("※"*50)
			print('Just proceeding with no loading but existing directory')
			print("※"*50)
			time.sleep(3)
			
		time.sleep(1)
			
			
	#####################################################################################

	#some initial local variables
	#############################
	feed = {} 
	# tf placeholder 문법 용 -> Q2 용
	eps = options.INIT_EPS
	# initial probability for epsilon
	G.global_step = 0
	# epsilon decay 조정하기 위한 counter
	G.loop_counter = 0
	exp_pointer = 0
	# experience load 하기 위한, list pointer 동작 용
	learning_finished = False
	# 원하는 score에 도달 시 True로 변하는 flag
	i_episode = 0
	# 전체 epoch counter하는 용도
	observation = None
	# input 받아오는 용도
	G.score = 0
	#밑에서 쓰일 episode당 점수 
	sum_loss_value = 0
	# 밑에서 쓰일 episode당 전체 loss 합
	while_counter = 0
	agent_counter = 0
	order_length = 0
	reward = 0
	step_loss_value = 0
	# 밑에서 쓰이는거 선언
	print("Global variables in Agent.py initialized")
	time.sleep(3)
	
	# Epoch를 넘어서 사용하는 변수들
	##############################
	if (
		   (G.obs_queue == None)
		or (G.act_queue == None)
		or (G.rwd_queue == None)
		or (G.next_obs_queue == None)
		or (G.score_queue == None)
	):
	# 다음번 사용 시에는 state_wrapper 에서 global clear로 관장하도록 한다
	#replay memory - 선언하는 곳, 선택적으로 분산을 넓히기 위해서 사용
	#https://docs.scipy.org/doc/numpy/reference/generated/numpy.empty.html
	# 열 갯수 MAX_EXPERIENCE 만큼, -> 방향 행정보에 각각 parameter 전부 저장
		# empty 선언 -> 0은 아니고 아주 작은 값으로 행렬만 만들어주는 것
		G.obs_queue = np.empty([options.MAX_EXPERIENCE, options.OBSERVATION_DIM])
		G.act_queue = np.empty([options.MAX_EXPERIENCE, options.ACTION_DIM])
		G.rwd_queue = np.empty([options.MAX_EXPERIENCE])
		G.next_obs_queue = np.empty([options.MAX_EXPERIENCE, options.OBSERVATION_DIM])
		G.score_queue = []
		G.sum_loss_value_tmp = []
		print('replay memory is initialized for the first time')
		time.sleep(3)
	else:
		print('replay memory is available')
		time.sleep(3)
		
		
	G.epoch_counters(1) #100
	# 총 epoch 갯수
	G.epoch_counter_tmps(0) #0.25
	# bubble sorting으로 돌릴 epoch 갯수
	G.increase_times(15)
	# 시뮬레이터 증가 시간 정해줌
	G.time_step_orders_2()
	# 시간 별 주문 갯수 로그 남기기 위함
	
	# start of the episode loop
	#############################
	while((G.loop_counter) < (G.epoch_counter)): 
	# G.epoch_counter 번 episode epoch를 수행
	#for i_episode in xrange(options.MAX_EPISODE): #-> 가 원래 식임
		print( "===== Total LOOP : {}  has began =====".format( i_episode + 1) )
		print("")
		time.sleep(3)
		
		# 매 episode마다 initialize 시킬 부분들
		######################################
		while_counter = 0
		agent_counter = 0
		# 밑의 수행중인 while문 카운터
		observation = None
		# http://solarisailab.com/archives/2038
		done = False
		G.score = 0
		sum_loss_value = 0
		order_length = 0
		reward = 0
		step_loss_value  = 0
		
# 		if T.times>=G.times_max :
# 			done = True
# 		else:
# 			pass
		# epoch마다 끝나면 표기하는 부분

		simulator.main()
		print('simulator for one Episode is activated')
		# 시뮬레이터 환경 제공, simulator 필수 부분들 제공
		
		
		while (done == False and T.times<=G.times_max):
		# 하나의 epoch 당 수행 될 while 문
			time.sleep(0.0005) # while문 과열 방지
			print( "  &== In LOOP : {}  in {} sub loop =====".format( i_episode + 1, while_counter + 1 ) )
			
			
			
			simulator.sim_main()
			# 시뮬레이터 논리 도는 부분, G.list_chicken 생성(update)
			
			if (    (len(G.list_chicken) >= 2) 
				and (G.loop_counter <= G.epoch_counter_tmp)
			   ) :
			# 시뮬레이터 돌아가는 중에 agent 개입 조건을 충족하였는가?
			# 시뮬레이터 끝나기 전인가? 판단하는 부분, else로 가면 pass고 while loop 다시 돌림
				bubble_sort()
				print("  &== In sub lOOP : {}  BUBBLE =====".format( while_counter + 1))


			elif len(G.list_chicken) >= 2 and (G.loop_counter > G.epoch_counter_tmp):
			# AGENT 돌아갈 조건 추가 만족
				F.agent_active(1)
				print('HI ','★'*25)
				# 시뮬레이터 진입 하였음을 표기 -> 맨 처음만 표기
				order_length = int(len(G.list_chicken))
				
				count_innerloop = 0
				for i in range(order_length - 1):
					for j in range(order_length - i -1):
						count_innerloop = count_innerloop + 1
					
				
				print("  &== In sub lOOP : {}  AGENT  =====".format( (while_counter + 1)*( count_innerloop )))
				# 예상 학습량
				count_innerloop = 0
				
				for i in range(order_length - 1):
					#print('HI 2 ','★'*25)
					for j in range(order_length - i - 1):
						
						observation = order_breaker(j,j+1)
			
						G.global_step = G.global_step + 1 # epsilon decay 조정하기 위한 counter
						if G.global_step % options.EPS_ANNEAL_STEPS == 0 and eps > options.FINAL_EPS :
							# epsilon dcay 시키는 구문
							if test_query == 1:
							#테스트인 경우
								eps = options.FINAL_EPS
							
							else:
								eps = eps * options.EPS_DECAY
						else:
							pass

						#### G.list_chicken 전체를 돌리는 것은 state_wrapper 에서 feed 해주는 것으로
						#########################################################################
						#########################################################################
						G.obs_queue[exp_pointer] = observation # 1 epoch 안의 step 마다 input layer 저장

						# actions print 해봐야 할듯. 둘중 하나 골라야 됨...?
						action = agent.sample_action(Q1, {obs : np.reshape(observation, (1,-1))} , eps, options)
						G.act_queue[exp_pointer] = action # 1 epoch 안의 step 마다 action 저장

						########## 
						# ACTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
						#여기서 action에 따른 environmet 수정 
						# action 넘어오면 random 혹은 max 선택으로 [0, 1] [1, 0]
						list_buffer = None
						if action[0] == 1: # 바꾸지 않는다
							pass
						else: #action[0] == 0, action[1] == 1
							################ GIL 적용 시켜야됨, 아마도 state_wrapper에다가
								list_buffer = G.list_chicken[j]
								G.list_chicken[j] = G.list_chicken[j+1]
								G.list_chicken[j+1] = list_buffer
								list_buffer = None

						# DONE@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
						# while 도는 중에 Done이 될 수도 있는데..(시뮬레이션이 끝남)
# 						if T.times>=G.times_max :
# 							done = True 

						# REWARD@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
						# 아마도 기준 시간 안에 도달을 했는지... 를 기준으로 하면 될 듯
						# state k에서 p시간이 평균이면, 그거보다 넘었는지 아닌지를..?
						# delayed reward는 이것으로 일단 가능..
						if len(G.list_chicken_finished) >= 1:
							for i in range(len(G.list_chicken_finished)):
								if G.list_chicken_finished[i].lv_rwd_finished == 0:
									reward = G.list_chicken_finished[i].time_to_reward()
									G.score = G.score + reward #
									print('score, reward : ', G.score,' / ' ,reward )

									G.list_chicken_finished[i].lv_rwd_finished = 1 # reward 가져온 것 마크해줌
								else:
									pass
						else:
							pass

						#observation @@@@@@@@@@@@@@@@@@@@@@@
						# state_wrapper 에서 자동으로 feed -> 바로 위 REWARD랑 같이 묶여서 작동

						if done and G.score < 100 : # 100 평균주문량, 5점 = 500점 인데 300 정도면 안됨
							reward = -150 # failure, punish hard
							#observation = np.zeros_like(observation)

						# Target용 queue 저장
						G.rwd_queue[exp_pointer] = reward
						G.next_obs_queue[exp_pointer] = observation

						exp_pointer = exp_pointer + 1


						############# 이거 전체가 MAX_EXPERIENCE에 관계없이 Done 상태 도달 안할 수 있어서임,
						# 목표 달성 안되도 environmnet 기준하여 무조건 Done으로 만든다는 상태인 듯
						if exp_pointer == options.MAX_EXPERIENCE:
							exp_pointer = 0 #refill the experience from the begining, at the next while state
						else:
							pass
						if G.global_step >= options.MAX_EXPERIENCE : # MAX_EXPERIENCE 도달 했을 때, Q2(target update)
							rand_indexs = np.random.choice(options.MAX_EXPERIENCE, options.BATCH_SIZE)
							# Batch size 만큼, Max experience의 index를 돌려준다.

							#Q2 target update, feed / placeholder 사용
							# dictionary 에 key와 value 추가하는 .update 속성 사용
							feed.update({obs : G.obs_queue[rand_indexs]})
							feed.update({act : G.act_queue[rand_indexs]})
							feed.update({rwd : G.rwd_queue[rand_indexs]})
							feed.update({next_obs : G.next_obs_queue[rand_indexs]})

							# 여기서 학습 그래프 수행
							# feed에 먹여준 것 한번에 학습
							# https://stackoverflow.com/questions/45874620/tensorflow-sess-run-returns-list-instead-of-float32-causing-typeerror-unsupport
							if test_query == 0: 
							# test 진행 안한다면
								#if not learning_finished :
								step_loss_value, _ = sess.run([loss, train_step], feed_dict = feed)
								# else: # if solved -> solved의 기준은 밑에서 정의
								# 	step_loss_value, = sess.run([loss], feed_dict = feed)

							#sum_loss_value = sum_loss_value + step_loss_value
							G.sum_loss_value_tmp.append(step_loss_value)
							#MAX_EXPERIENCE 도달하고 step에 대해서 구해진 loss를 기록 -> 모든 epoch 끝날 때 까지 더함(기록용인 듯)

							agent_counter = agent_counter + 1 
							# loss 계산용
							
							G.score_queue.append(G.score)
							if test_query == 0 :
							# 테스트 진행시에는 loss를 줄이지 않으므로 save하는 의미가 없어서
								score_board() # G.score_board_value 찍어놓음
								if G.score_now_max <= G.score: # epi안의 max 찍어놓음
									G.score_now_max = G.score # epi안 max 업데이트
									if G.score_now_max > G.score_board_value :
										saver.save(sess, curr_dir, global_step = G.global_step)
								score_board()
							# score 계산 일찍 한다 왜냐? -> 과정이 긴 학습이라
							# 저장 시키려면 일찍 판단해서 넣어야 됨
			else: # 1개짜리  chicken list일 때
				print("  &== In LOOP : {}  PASS  =====".format( while_counter + 1))
			while_counter = while_counter + 1
			F.agent_active(0)
			T.times = T.times + G.increase_time
			
		
		# inside the EPOCH while loop
		i_episode = i_episode + 1 #나중에 average loss print할 때 사용
		
		#while 문 끝, 아직 while(1) 구문 안에 있음
		if (G.loop_counter > G.epoch_counter_tmp) :
			print( "===== Total LOOP : {} ended with score = {}, avg_loss = {} =====".format( i_episode, round(G.score, 2) , round(sum_loss_value / (agent_counter+1), 2) ) )
			time.sleep(3)
		#계속 while(1) 구문 안에 있음
			#G.sum_loss_value_tmp.append(round(sum_loss_value / (agent_counter+1), 2))
			#G.score_queue.append(score)
			if len(G.score_queue) > MAX_SCORE_QUEUE_SIZE : # 최근 지정 값 까지 평균 냄
				G.score_queue.pop(0) # MAX_SCORE_QUEUE_SIZE 유지
				# if np.mean(G.score_queue) > 200 : # ★★★THREASHOLD of being SOLVED by DQN
				# 	learning_finished = True
				# if learning_finished :
				# 	print('Successful Training done')
				# 	#time.sleep(3)
# 				if learning_finished and i_episode % 2 == 0 :
# 					#saver.save(sess, "/checkpoints-order_sorter", global_step = G.global_step)
# 					saver.save(sess, curr_dir, global_step = G.global_step)
					# curr_dir
				
		simulator.sim_fin()
		G.loop_counter = G.loop_counter + 1
	simulator.sim_wrappup()

running_order_sorter()
