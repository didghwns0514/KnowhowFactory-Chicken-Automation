#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
import time
########################import field#######################

########################global value#######################
import TIME as T
###########################################################
#time 관련
times_max = 60 * 60 * 12 + (T.times_begin) #시작 시간 오전 11시
#times_max = 60 * 60 * 2.5 + (T.times_begin) # 시뮬레이터 용 시간, 4시간 정도만 돌려보기
#60초 * 8시간   //장사가 11시 부터 시작되는 것

###########################################################
###########################################################




###############################################################################
###############################################################################
#일단 redundant 한 애들 갖다 놓기

return_val = None
input_val = None





###############################################################################
###############################################################################
## SIMULATOR

increase_time = 0
def increase_times(num):
	global increase_time
	increase_time = num

#초기 simulator 관련
order_instance = None
total_order = []

list_chicken = [] #초기 생성 치킨 받아줌, 저장
list_chicken_finished = [] #배달 완료 된 치킨

list_worker_normal = [] #idle 상태에 있는 작업자들 list
list_worker_biker = []
list_machine_fryer = []
list_machine_bike = []

loop_counter = 0 # 학습을 위한...
epoch_counter = 0 # 몇번 돌리려고 하는 것인지?..
epoch_counter_tmp = 0
log_graph_list = [] # 저장 / 출력용

weekday = 0 # flag for weekday weekend 0 : weekend, 1 : weekday

def epoch_counters(num):
	global epoch_counter
	global log_graph_list
	epoch_counter = num
	log_graph_list = [0]*num
	
def epoch_counter_tmps(percent): # DQN 넘어갈 때  parameter
	global epoch_counter_tmp
	global epoch_counter
	epoch_counter_tmp = int(epoch_counter * percent)
	
def weekday_weekend_choice(num):
	global weekday
	weekday = num

##https://bytes.com/topic/python/answers/858499-convert-string-name-variable-name
# 	#idle.main.extend(global list_worker) #worker 만들어가지고 list로 할당해주어야됨
# 	for var in zip(G.workingstage, QUE(G.workingstage.name)):
		


###############################################################################
###############################################################################
## TASK MANAGER





###############################################################################
###############################################################################
## STATE WRAPPER

reward_from_finished = 0


###############################################################################
###############################################################################
## AGENT - running_order_sorter
obs_queue = None
act_queue = None
rwd_queue = None
next_obs_queue = None
score_queue = None

global_step = 0

#log 용
sum_loss_value_tmp = None

#score 용
score_board_value = 0 # 과거부터 포함해서 최대 스코어 고정
score_now_max = 0 # epi 안의 최대 스코어
score = 0 # 현재 현시점 정확한 점수

# read write용
content = None
# 점수 마커
curr_dir = None
# 지금 작업중인 경로
curr_dir_f = None
# 파일까지의 경로
file_exist = None
# 논리값 return, 파일이 있는가 없는가

###############################################################################
###############################################################################
## WORKER, ORDER, GAUSSIAN, MACHINE

#order:
k = 0


###############################################################################
############################################################################### 
## LOG
x = []  #epochy
y1 = [] #평균 배달 시간
y2 = [] #평균 주문 ~ 배달완료 시간
y3 = [] #주문 갯수

t1 = [] # loss
t2 = [] # score

x_t = [] # 시간 별
o1 = [] # 주문량
o2 = [] # 늦은 주문
o_counter = 0
#전체 timestep 갯수, 11시->1
def time_step_orders_1():
# 모든 epoch 당 시간별 주문 모아서 평균 내기위함
	global increase_time
	global o1
	global o_counter
	global x_t
	global times_max

	
	#시작 시간 mark
	#lister = []
	
	for begin in range(T.times_begin ,times_max + increase_time, increase_time ):
	# simulator과 같은 만큼 돌아간다
		o1.append(0)
		#x_t.append((begin - T.times_begin)/60) 
		x_t.append((begin)/(60*60)) 
		# 시간으로 환산
		begin = begin + increase_time
		o_counter = o_counter + 1
		
def time_step_orders_2():
	global o1
	if len(o1)==0 and times_max != 0 and increase_time != 0:
# 바로 x_t 크기 생성
		time_step_orders_1()
	
	
o = [] # 주문 갯수 새

