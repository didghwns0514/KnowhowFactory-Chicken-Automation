#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey


########################import py field####################
import os
import threading
import queue as Q
import collections
import math
import time


########################import field#######################
#import state
import worker
import order
import machine
#import agent as A
########################global value#######################
import Global as G
import FLAG as F
import TIME as T

###########################################################

#@ 두 그룹으로 나누기 @#
##보통일꾼 + 튀김기
##베딜부

################# multi processing으로 처리####################################
#https://hashcode.co.kr/questions/691/파이썬으로-멀티프로세싱-vs-멀티-스레딩
#https://inma.tistory.com/103
#@멀티 프로세싱이 python에서 더 권장 됨, shared variable 사용 가능 <- 반드시 필요 flag등
#@@https://stackoverflow.com/questions/17377426/shared-variable-in-pythons-multiprocessing
#https://m.blog.naver.com/townpharm/220951524843
#https://blog.naver.com/townpharm/221242852808

#
################################################################
#idle chicken waiting Que 및 다른 step들 모두 Que로 해결
#사람도 idel Q에서 빼고 넣는 수순으로 + driving Que

# https://www.python-course.eu/python3_multiple_inheritance.php
# https://m.blog.naver.com/PostView.nhn?blogId=dudwo567890&logNo=130165707606&proxyReferer=https%3A%2F%2Fwww.google.com%2F
# https://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing
# https://blog.ruanbekker.com/blog/2019/02/19/sharing-global-variables-in-python-using-multiprocessing/

		

		
################################################################################################

# def order_importance_sort():
# 	## bubble sorting 방식
# 	## 전체 epoch의 10%를 기존 bubble sort로 돌린다
	
# 	if len(G.list_chicken) == 1: # 한개면 sorting할 필요가 없으므로
# 		pass
	
# 	elif(
# 		    (G.loop_counter <= G.epoch_counter_tmp) 
# 		and (len(G.list_chicken) >= 2)
# 	) : # 10번까지는 이걸 돌린다 아니면 한마리 있는 경우 -> 시작 빼고는 거의 없을 것임
# 		order_length = len(G.list_chicken)

# 		#앞쪽 item인 경우에 chicken importance가 높은 애들을 배치
# 		for i in range(order_length - 1, 0, 1):
# 			for j in range(i):
# 				if G.list_chicken[j].importance < G.list_chicken[j+1].importance :
# 					list_buffer = G.list_chicken[j]
# 					G.list_chicken[j] = G.list_chicken[j+1]
# 					G.list_chicken[j+1] = list_buffer
# 	elif(
# 		    (G.loop_counter > G.epoch_counter_tmp)
# 		and (len(G.list_chicken) >= 2)
# 	):
# 		order_length = len(G.list_chicken)
# 		for i in range(order_length - 1, 0, 1):
# 			for j in range(i):
# 				A.running_order_sorter(j, j+1)
	
# 	## 너무 많이 돌리면 안되니깐 sleep 도입
# 	time.sleep(0.02)
		

def driver_workscore_sort(): # 배달부 빠르기 순으로 정렬하기, 이거 update 때 사용 해야됨. single_updater도 마찬가지
	##bubble sorting 방식
	worker_length = len()

def Worker_sort_single() : #큐에 치킨들이 대기 상태일 때 큐들에 적절히 사람 배치시키는 class
	#나중에 machine learning으로 할 부분
	#지금은 사람에다가 random으로 chicken importance sort해서 넣어주고 있음
	
	#importance 순으로, transition_packaging까지, 그게 10부터이다

	## worker에게 일을 할당하는 수순이 맞는 것 같다, 다 되면 list로 다시 반환해주고
	#order_importance_sort()
	
	list_max_counter = len(G.list_chicken) #remove 되는 애들 맞춰서 실행하기 위함
	i = 0

	while (i<list_max_counter):

		if ( (G.list_chicken[i].workingstage_template <= 10 ) ):  #10 까지 돌리는 과정 0~10까지 delivery wait
			for j in range(len(G.list_worker_normal)): #가능한 작업자들에 대해서
				if ( (G.list_worker_normal[j].isworking_template == 0) ):  # 0번 이여야 일을 안하는 생태
					
					if( G.list_worker_normal[j].work_verify(G.list_chicken[i].workingstage_template) == True ) : #일을 할 수 있는 작업자라면, chicken 받을 수 있음
						G.list_worker_normal[j].chicken_bag_push(G.list_chicken[i]) #전체 치킨을 하나씩 다 넣어보게 되어있음
						G.list_chicken.remove(G.list_chicken[i]) #chicken list에서 담았던 치킨 제거
						list_max_counter = list_max_counter - 1
						i = i -1
							
							#시작 했다는 것을 표기하기
						G.list_worker_normal[j].work_start() # 일을 시작하도록 한다, 사람 세팅
						break #해당 worker 일 할당 더이상 안하고 넘어감
					
						#raise ValueError('state_wrapper Wrong Worker_sort_single()')
				else:
					pass

		else:
			pass
		i = i + 1


			
		
def score_update_single(): # 점수 update
	#for the workers that are working

	for i in range(len(G.list_worker_normal)): # 모든 작업자들에 대해서
		#작업 chicken 1마리, state 0~10까지, 실제 작업자 일 시작 상태일 때
		if(     (len(G.list_worker_normal[i].chicken_bag) == 1)
			and (G.list_worker_normal[i].workingstage_template <= 10)
			and (G.list_worker_normal[i].isworking_template == 1)
			):
			#print("progress in state_wrapper in", flush=True)
			G.list_worker_normal[i].work_progress() #개별 점수 상승을 시키는게 끝까지 마무리 되어야 돌지 않는가?

		else:
			pass


def Worker_remove_single(): #완료된 애들 빼줌
	#일이 끝났다면은, duration > max 일 때, isworking에 대해서
	#실상은 chicken 꺼내는 작업임 worker에서

	#일하는 중이고, 작업이 완료 되었다면(work progress가 max를 쳤다)
	for i in range(len(G.list_worker_normal)):
		if(     (G.list_worker_normal[i].isworking_template == 1)
			and (G.list_worker_normal[i].workingstage_template <= 10)
			and (G.list_worker_normal[i].isworking_duration >= G.list_worker_normal[i].isworking_max)
		):
		#일 끝났을 때 setting작업
			G.list_worker_normal[i].work_finish()
			if G.list_worker_normal[i].chicken_bag[0].move_next_stage == 1: #다음 stage로 가기 위해 chick을 제거해야 한다면
				G.list_chicken.append(G.list_worker_normal[i].chicken_bag_pull( G.list_worker_normal[i].chicken_bag[0] ))

		#chicken을 돌려준다


def state_change_single(): #다음 stage로 치킨을 바꿔준다 0~10까지-> 그래야 11로 들어감 delivery_wait
	#11까지 채워주는 , 11부터는 biker작업만 하는 것으로

	for i in range(len(G.list_chicken)):
		if(     (G.list_chicken[i].move_next_stage == 1 ) ):
			#다음 stage로 이동
			G.list_chicken[i].workingstage_template = G.list_chicken[i].workingstage_template + 1
			G.list_chicken[i].move_next_stage = 0 # reset해줌
		
		else:
			pass


def Worker_sort_tripple() : #치킨 3개를 driver에 할당 / 치킨 고르는 것 /// 나중에 machine learning으로 코딩 할 부분
	########################################################################################
	
	#order_importance_sort() # 결국 이 순서대로 일단 배달원한테 담기는 중
	########################################################################################

	bag_input = 3 # 가방에 넣어서 배달 할 갯수
	list_deliverwait_order = [] # 해당하는 주문(베달 직전)의 list numb를 넣어주는 부분
	
	def actual_list_update():
		global list_deliverwait_order
		list_deliverwait_order = [] #초기화 진행
		
		list_max_len = len(G.list_chicken)
		#len_possible_deliver_numb = 0 # 카운터용 init 선언

		for ii in range(list_max_len): # list 숫자 marking 시작
			if (
				(G.list_chicken[ii].workingstage_template == 10)
			and (G.list_chicken[ii].isworking_flag == 0)
			and (G.list_chicken[ii].worker_inwork == 0)): # 사람도 안붙었고, 일하고 있는 중도 표시 안되어있으면, 바로 도달해 있는 거면
				# stage에 막 도달해 있을 때는, move_next_stage = 0 인 상태
				list_deliverwait_order.append(ii)
				#len_possible_deliver_numb = len_possible_deliver_numb + 1 # 갯수 카운터 올려줌
			else:
				pass

	def Switcher():
		global list_deliverwait_order
		actual_list_update()
		cut = len(list_deliverwait_order)//bag_input
		moduler = len(list_deliverwait_order)%bag_input
		#print('cut, moduler :', cut, moduler)
		
# 		if ((cut >= 1) and (moduler ==0)): # 3개 이상
# 			return 3
# 		elif ((cut == 0) and (moduler ==0)): #0개
# 			return 0
# 		elif moduler == 1: #1개
# 			return 1
# 		elif moduler == 2: #2개
# 			return 2

		if ((cut >= 1)): # 3개 이상
			return 3
		elif ((cut == 0) and (moduler ==0)): #0개
			return 0
		elif((moduler == 1) and (cut == 0)): #1개
			return 1
		elif((moduler == 2) and ( cut == 0)): #2개
			return 2
		else: # 나머지 필요 없는 else로 처리되는 논리 구조, 아무것도 수행 안한다.
			return 0

	def F_order_in(j,switch):
		global list_deliverwait_order
# 		for i in range(switch):
# 			k = list_deliverwait_order[i]  # 할당 가능한 치킨으로 다시 변환(list 를 통해서)
# 			print('k, i : ', k, i)
# 			if (G.list_worker_biker[j].work_verify(G.list_chicken[k].workingstage_template) == True):
# 				print('k,i loop has been approached')
# 				G.list_worker_biker[j].chicken_bag_push(G.list_chicken[k])
# 				G.list_chicken.remove(G.list_chicken[k])
# 				actual_list_update() # k항에서 오더가 제거되서 다시  업데이트 해야되는 것임
# 			else:
# 				pass
		i = 0
		
			
		while( i < switch ):
			#print(list_deliverwait_order)
			k = list_deliverwait_order[0]  # 할당 가능한 치킨으로 다시 변환(list 를 통해서)
			# 계속 앞에있는 것만 꺼내면 되니깐... [0]으로 설정
			#print('k, i, switch : ', k, i, switch)
			if (G.list_worker_biker[j].work_verify(G.list_chicken[k].workingstage_template) == True):
				#print('k,i loop has been approached')
				G.list_worker_biker[j].chicken_bag_push(G.list_chicken[k])
				G.list_chicken.remove(G.list_chicken[k])
				actual_list_update() # k항에서 오더가 제거되서 다시  업데이트 해야되는 것임
				#i = i - 1
			else:
				pass
			i = i + 1 # switch 만큼 돌리기 위한 장치
		########################################################################################
		G.list_worker_biker[j].chicken_bag_sort()
		########################################################################################
		G.list_worker_biker[j].work_start()
		actual_list_update()
		

	 #맨 처음 시행
	for j in range(len(G.list_worker_biker)):
		if(   (G.list_worker_biker[j].isworking_template == 0)
		  ): # 배달 상태가 아니면, j도 나중에 수정 가능.....
			switcher = Switcher()
			if switcher == 0 : # 0개 들어있음
				#print('0'*50)
				pass
			elif switcher == 1:
				#print('1'*50)
				F_order_in(j,1)
			elif switcher == 2:
				#print('2'*50)
				F_order_in(j,2)
			elif switcher == 3:
				#print('3'*50)
				F_order_in(j,3)
			else:
				pass
				#print('7'*50)




def score_update_tripple(): 
	# chicken_bag안에 순서 정렬 -> 이거 Worker_sort_tripple 함수 첫부분이랑 맞물려서
	# order_importance_sort
	# chickenbag_sort 위에서 시행
	#############################################################################
	# 3마리 있을 떄
	# 2마리 있을 때
	# 1마리 있을 때
	# 10(delivery_wait), 11, 12, 13
	def duration_processing_update(num): # worker.py 업데이트
		road_len = None
		##############################
		## 예상 km 당 분 배달시간 변환
		#mapping = (30/7.5)* 60 # 초변환
		mapping = ( 8/2.2 )*60 # 10km, 10km라서  14.xxxxx로 나오고 1분 mapping해야됨
		##############################
		#print('num in state_wrapper, duration_processing_update fct : ', num)
		if (
			   (G.list_worker_biker[num].workingstage_duration[2][11] == None)
		   and (G.list_worker_biker[num].workingstage_template == 11)
		   ):
			# 11번 stage에서 update는 꾸준히 불리니깐, 검증
			# 0번 째 list를 업데이트를 해준다
			if (    (len(G.list_worker_biker[num].chicken_bag) >= 1) 
				and (G.list_worker_biker[num].workingstage_template >= 10)
			    and (G.list_worker_biker[num].workingstage_template <= 12)
			   ) :
				road_len = (G.list_worker_biker[num].chicken_bag[0].address[0] - G.list_worker_biker[num].location_now[0])**2 + (G.list_worker_biker[num].chicken_bag[0].address[1] - G.list_worker_biker[num].location_now[1])**2
				road_len = math.sqrt(road_len)
				G.list_worker_biker[num].workingstage_duration[2][11] = road_len * mapping
			else:
				pass
			
		elif (  
			     (len(G.list_worker_biker[num].chicken_bag) == 0)
			 and (G.list_worker_biker[num].workingstage_template == 13)) :
			road_len = (G.list_worker_biker[num].location_now[0])**2 + (G.list_worker_biker[num].location_now[1])**2
			road_len = math.sqrt(road_len)
			G.list_worker_biker[num].workingstage_duration[2][13] = road_len * mapping # arrival
		
		else:
			pass #raise ValueError('possible road_len assign error in state_wrapper.py')
		try:
			#print('road_len mapping value : ', road_len * mapping, '  by worker :', G.list_worker_biker[num].name)
			pass
		except:
			pass

	for i in range(len(G.list_worker_biker)):
		if(
			    (len(G.list_worker_biker[i].chicken_bag) >= 1)
			and (len(G.list_worker_biker[i].chicken_bag) <= 3)
			and ((G.list_worker_biker[i].workingstage_template >= 10) and (G.list_worker_biker[i].workingstage_template <= 12))
			and (G.list_worker_biker[i].isworking_template == 1)
		): # 위에서는 11로 설정하였다...
			######
			#and ((G.list_worker_biker[i].workingstage_template >= 10) and (G.list_worker_biker[i].workingstage_template <= 12))
			######
			duration_processing_update(i) # workingstage_duration먼저 만들어주고 밑에 함수 수행
			G.list_worker_biker[i].work_progress() # self.isworking_duration 업데이트
		
		elif (  (G.list_worker_biker[i].isworking_template == 1)
			and (len(G.list_worker_biker[i].chicken_bag) == 0)
			and (G.list_worker_biker[i].workingstage_template == 13)
			 ):
			duration_processing_update(i) # workingstage_duration먼저 만들어주고 밑에 함수 수행
			G.list_worker_biker[i].work_progress()
		
		else:
			pass
		
		
def state_change_tripple():
	pass
	# G.list_worker_biker[i].work_finish() 에서 수행하는 것으로
	
	
def Worker_remove_tripple():


	for i in range(len(G.list_worker_biker)):
		if(
			(G.list_worker_biker[i].isworking_template == 1)
		and (G.list_worker_biker[i].workingstage_template >= 10)
		and (G.list_worker_biker[i].isworking_duration >= G.list_worker_biker[i].isworking_max)
		):
			G.list_worker_biker[i].work_finish()
			if(len(G.list_worker_biker[i].chicken_bag) != 0): # 일단 가방에 담겨 잇을 때
				if( (G.list_worker_biker[i].chicken_bag[0].move_next_stage == 1)): #배달이 완료 대상에 대해서 표기, 어차피 바로 밑에서 pop되기 때문에 신경 안써도 됨
					#  완료가 된 경우만... 뽑아서 완료된 list에 넣어줌
					# 13번 stage에서는 chicken이 없으니깐
					G.list_worker_biker[i].chicken_bag[0].fin_time = T.times
					G.list_chicken_finished.append(G.list_worker_biker[i].chicken_bag_pull(G.list_worker_biker[i].chicken_bag[0]))

					
					
# def score_calculator(): # 나중에 score 계산해서 reward로 줄 것, 기준을 잡아서 판별하려고 만든 것
# 	def score_to_reward(): # 리워드로 mapping, 중간 reward
# 		pass 
	
# 	### loop 돌기위해 만들어야 하는 개별 task 별 def
	
	
	
# # def time_to_reward(): # 배달 끝난 애로 reward
	
# # 	def reward_function(x): # reward 계산용, 13분 미만이 목적
# # 		y = None
# # 		# 20분 넘기면 안된다 
# # 		if x <= 20 :
# # 			y = -(10/(13*13))*(x+13)*(x-13)
# # 		elif x > 20:
# # 			y = -100
# # 		return y
	
# # 	return_sum = 0 # reward 합계로 해서 전달할 목적
# # 	if len(G.list_chicken_finished) >= 1:
# # 		for i in range(len(G.list_chicken_finished)) : 
# # 			# 루프 돌면서 업데이트 할 것임
# # 			if G.list_chicken_finished[i].fin_time != None :
# # 				# 값을 할당을 하였다면
# # 				end_time = G.list_chicken_finished[i].fin_time
# # 				elapsed_time = end_time - T.times # 경과 시간
				
# # 				return_sum = return_sum + reward_function(elapsed_time)
	
# # 	return return_sum



	
	
	





# class Wrap_Q_single(Worker_sort_single, Chicken_sort_single, Swap_single, Swap_tripple, Update):
# 	pass

#def main(): 여기서 global로 받고 밑에서도 global로 쓰는 것이?

def main():
	
	###############################################################################
# 	p1 = threading.Thread(target=Worker_sort_single, args =[]) #사람들을 que의 chicken에 할당
# 	t1 = threading.Thread(target=score_update_single, args=[]) # score update 해주는 부분
	
# 	p2 = threading.Thread(target=Worker_remove_single, args=[]) # 완료된 작업 사람 빼줘서 idle로 배치
# 	t2 = threading.Thread(target=state_change_single, args=[]) # 완료된 애들을 다음 stage로
	
# 	d1 = threading.Thread(target=Worker_sort_tripple, args=[]) #배달부 배치 치킨 3마리 배치 + 순서 sorting
# 	d2 = threading.Thread(target=score_update_tripple, args=[]) #배달부 score update 해주는 부분
# 	d3 = threading.Thread(target=state_change_tripple, args=[]) #배달부 가진 chicken 상태 변화
# 	d4 = threading.Thread(target=Worker_remove_tripple, args =[]) #완료된 배달부 재 배치
	
# 	t1.start()
# 	t2.start()
# 	p1.start()
# 	p2.start()
# 	d1.start()
# 	d2.start()
# 	d3.start()
# 	d4.start()

	################################################################################
	
	Worker_sort_single() #사람들을 que의 chicken에 할당
	score_update_single() # score update 해주는 부분
	
	Worker_remove_single() # 완료된 작업 사람 빼줘서 idle로 배치
	state_change_single() # 완료된 애들을 다음 stage로
	
	Worker_sort_tripple() #배달부 배치 치킨 3마리 배치 + 순서 sorting
	score_update_tripple() #배달부 score update 해주는 부분
	state_change_tripple() #배달부 가진 chicken 상태 변화
	Worker_remove_tripple() #완료된 배달부 재 배치
	




