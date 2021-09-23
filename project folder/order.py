#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
#from state import state_input
########################import field#######################
import math
########################global value#######################
import Global as G
import FLAG as F
import TIME as T
###########################################################
class order(object):

	identify = 'chicken'
	
	lv_order_cancle_request = 0 #1이면 cancle flag 올린다
	if not( (lv_order_cancle_request == 0)
		or (lv_order_cancle_request == 1)
	   ):
		raise ValueError('order Wrong lv_order_cancle value')
	
	if( (lv_order_cancle_request == 1) 
		
	  ):
		F.lv_order_cancle = 1
		
	

	def __init__(self, address, whatchicken, workingstage_template, times):
		
		
        #여기 workingstage1 들어갔었음
		self.workingstage_template = workingstage_template #Gobal의 state와 맞춤

		#다음 stage넘어가야 하면 flag올리기
		self.move_next_stage = 0
        
        #times로 라벨링 기능 / 언제 오더가 들어왔는지
		self.times = times
		self.arrival_times = 0 # 도착 시간 finished list에 기록할 용도
        #self.number = number #이거 각각 개별 오더로 수행하면 된다

        ####차후에 nuber와 what을 마음대로 할 수 있어야 => 양념1개 후라이드 3개 어떻게 넣을까?
		self.address = address
		self.whatchicken = whatchicken
        #self.workername = workername #worker name 넣는 공간  ::::::::::::::::::::::: 사람한테 할당해서 넘겨주는 것으로 전환
        #########################################################################
        #self.workingstage = workingstage1
        #self.state_input = state_input
        ########################working stage를 class로 state changer넣어서 해야될 듯?

		self.importance = 0 #order 개수 판단해서 정해줌
		self.importance_base = self.importance #변수 불러서 init되자마자 저장
		##################################################################
		self.score = 0 ## 이 값은 차후에 setting 해야된다 기준 값임
		# 0 부터 해서 올라가는 식으로 할꺼임 / 어디까지일 지는 나도 잘 ?
		##################################################################
		self.dec_score = 1 #이 값은 감소하는 정도, 나중에 function만들어서 차감하면 됨
		
		self.fin_time = None #완료 된 시점 기록
		self.delivery_start_time = None
		self.lv_rwd_finished = 0 # 1이면 완료되었고 reward까지 agent가 받아감


		self.isworking_flag = 0 ## 일을 하겠다는 flag 담아놓기
		if not(self.isworking_flag == 0 or self.isworking_flag == 1 ):
			raise ValueError('Wrong isworking_flag')
		self.worker_inwork = 0 ##사람이 붙어서 일을 한다는 flag
		if not(self.worker_inwork == 0 or self.worker_inwork == 1 ):
			raise ValueError('Wrong worker_inwork')
		

	def importance_update(self): #state 지나면서 score update할 부분, worker에다가?
		stage_val = ( self.workingstage_template * 5 ) # stage 값 계속 더함
		time_val = (T.times - self.times) % (60*60) #1시간 단위로 측정
		self.importance = round(self.importance_base + stage_val + time_val, 2)
		
	def address_to_importance(self): #주소를 adress로 변환
		update_val = round(math.sqrt( self.address[0]**2 + self.address[1]**2 ), 2)
		self.importance = round(self.importance + update_val, 2)
		
	def order_deduct_score(self):
		self.score = self.score # - work_state 관련 해서 deduct
		self.importance = self.importance # - importance 관련해서 function logic 구현

	def time_to_reward(self): # 배달 끝난 애로 reward

		def reward_function(x): # reward 계산용, 13분 미만이 목적
			G.k = 33 # 이차함수 0되는 지점
			y = None
			positive_reward_mult = 4.5
			# 6배 올려준다 60 밑으로 유지 
			# 30분 넘기면 안된다 
			
			if x <= 20  and x >= 0:
				
				y = 10 * positive_reward_mult
			elif x > 20 and x <= (G.k+5):
			# 32까지 양수로 받음
				y = (-(10 / ((G.k-20)**2))*((x-20)**2) + 10) * positive_reward_mult
			elif x > (G.k + 5):
				
				y = (-(10 / ((G.k-20)**2))*(((G.k+5)-20)**2) + 10) * 3
				if y < -20 :
					y = -20
				else:
					pass
				# -20으로 고정
			else :
				y = 0
			return round(y, 2)
			# round 함수로 float 자리수 2 까지 제한

		if (self.fin_time != None ):
			# 값을 할당을 하였다면
			elapsed_time = self.fin_time - self.times # 경과 시간 (배달완료 - 주문시간) -> 초시간 ??
			# 초로 설정이 되어있다
			return reward_function(elapsed_time/60)
		else:
			err = input('Wrong reward function in order.py')
			raise ValueError('wrong calling of time_to_reward in order.py')

