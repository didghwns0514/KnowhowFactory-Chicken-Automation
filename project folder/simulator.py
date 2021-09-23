#-*-coding: utf-8-*-
########################sublime text 2용 hotkey#############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################Simulator control##################


normal_worker = 4
fry_worker = 3
delivery_worker = 6

fryer = 6
bike = 6



########################import py field#####################
import worker, order, machine
import log
import gaussian
import task_manager #task를 받아주는 아이 / management

########################import field#######################

from random import randint
import datetime
import numpy as np

########################global value#######################
#아예 시뮬레이터 돌리는 용도로 사용할 python script
import Global as G
import FLAG as F
import DO as do
import TIME as T
#import screen_disp





###########################################################


def create_order(times):
	G.order_instance = None #값 interface 변수 일단 초기화
	#gaussian.main(times) #이 것으로 주문이 몇개가 들어오는지! > 이거 list만드는 쪽에서 해줘야 될 것 같음
	
	#주소 만들어주는 부분, 나중에 값을 받는 것으로...
	#### km 단위로 설정되어있는 것 사실은,....
# 	xa = int(randint(-8,8))
# 	ya = int(randint(-8,8))
	xa = round(np.random.uniform(-2.5,2.5), 2)
	ya = round(np.random.uniform(-2.5,2.5), 2)
	
	whatchicken = int(randint(0,10)) #치킨의 종류
	address = [xa, ya]
	workingstage_template = 1 #2번이 counter state이다, 전화 받고 주문 시작 상태, list에서는 1
	dec_score = None #감소를 위한 점수, address와 연결해서 차등해도 될 듯?
	#어차피 필요 없으면 나중에 없애도 되는 부분
	#work_state # 필요 없는데 이전 버전에서 넘어온 듯
	importance = int(randint(0,10)) #이것도 나중에 튜닝해야됨

	order_instance = order.order(address, whatchicken, workingstage_template, times)
	order_instance.importance = importance #importance 따로
	order_instance.address_to_importance() # 거리를 환산해서 넣어줌
	
	#print('importance what? : ', importance)
	G.order_instance = order_instance #인터페이스에 값 넣어줌
	return order_instance

def create_order_in(times): #인터페이스에 있는 애를 list에 추가
	
	def time_to_whichstep(times):
	# times 받고 가져와서 몇번 째 counter에 넣어야 하는지
		index = int((times - T.times_begin)/(G.increase_time))
		return index
	
	#G.x_t.append(times/(60))
	#분단위로 할 것이므로, global에서 이미 해줌
	
	num_of_loops = gaussian.main(times)
	G.o1[time_to_whichstep(times)] = round(num_of_loops/G.epoch_counter + G.o1[time_to_whichstep(times)], 2)
	# 시간별 주문 갯수 평균내서 계속 더함
	
	if num_of_loops != None :
		for i in range(num_of_loops):
			tmp_order = create_order(times)
			G.list_chicken.append(tmp_order) #만들어진 chicken reference 저장용?
			#G.transition_counter.qput(tmp_order) # 첫 chicken 저장소에 저장
			G.total_order.append(tmp_order)
		#flag올리기
		F.lv_create_order = 1 #flag올린다


def create_worker(): #한번만 부르도록 하기!
	
	for i in range(1,normal_worker + 1):
					#name, worklicense, machine_name, workscore, hurryrate, isworking_max, isworking_template, workingstage_template
		working_personel1 = worker.worker(str(i)+"st_worker_normal",0, None, randint(0,100), randint(0,10), 0, 0, 0)
		G.list_worker_normal.append(working_personel1)

	for i in range(1,fry_worker + 1):
		working_personel2 = worker.worker(str(i)+"st_worker_fryer",1, "jane_doe_machine", randint(0,100), randint(0,10), 0, 0, 0)
		G.list_worker_normal.append(working_personel2)

	for i in range(1,delivery_worker + 1):
		working_personel3 = worker.worker(str(i)+"st_worker_biker",2, "jane_doe_machine", randint(0,100), randint(0,10), 0, 0, 0)
		G.list_worker_biker.append(working_personel3)


def create_machine():

	for i in range(1, fryer + 1):
		fryers = machine.machine_fryer(str(i)+"st_fryer",0)
		G.list_machine_fryer.append(fryers)

	for i in range(1, bike + 1):
		bikes = machine.machine_bike(str(i)+"st_bike",0)
		G.list_machine_bike.append(bikes)

def log_prints():

	def fryer_machine_counter():
		counter = len(G.list_machine_fryer)
		return counter

	def normal_working_counter():
		counter = 0
		for i in range(len(G.list_worker_normal)):
			if((G.list_worker_normal[i].isworking_template == 1)
              and (G.list_worker_normal[i].worklicense == 0)):
				counter = counter + 1
		return counter
    
	def fry_working_counter():
		counter = 0
		for i in range(len(G.list_worker_normal)):
			if(   (G.list_worker_normal[i].isworking_template == 1)
              and (G.list_worker_normal[i].worklicense == 1)
              ): #
				counter = counter + 1
			else:
				pass
		return counter

	def fry_nonworking_counter():
		counter = 0
		for i in range(len(G.list_worker_normal)):
			if(   (G.list_worker_normal[i].isworking_template == 0)
              and (G.list_worker_normal[i].worklicense == 1)
              ): #
				counter = counter + 1
			else:
				pass
		return counter
        
            

	def stage_chicken_counter(stage_num): #stage안에 들어있는 해당 chicken개수 return
		counter = 0
		for i in range(len(G.list_chicken)):
			if G.list_chicken[i].workingstage_template == stage_num:
				counter = counter + 1
			else:
				pass

		return counter

	def stage_working_counter(stage_num):
		counter = 0
		for i in range(len(G.list_worker_normal)):
			#if G.list_worker_normal[i].isworking_template == 1:
			#if G.list_worker_normal[i].chicken_bag[0].workingstage_template == stage_num:
			if G.list_worker_normal[i].workingstage_template == stage_num:

				counter = counter + 1

		return counter

	def stage_working_counter_2(stage_num):
		counter = 0
		for i in range(len(G.list_worker_biker)):
			#if G.list_worker_normal[i].isworking_template == 1:
			#if G.list_worker_normal[i].chicken_bag[0].workingstage_template == stage_num:
			if G.list_worker_biker[i].workingstage_template == stage_num:

				counter = counter + 1

		return counter

	def stage_real_working_counter(stage_num):
		counter = 0
		for i in range(len(G.list_worker_normal)):
			if G.list_worker_normal[i].isworking_template == 1:
			#if G.list_worker_normal[i].chicken_bag[0].workingstage_template == stage_num:
				if G.list_worker_normal[i].workingstage_template == stage_num:

					counter = counter + 1

		return counter

	def stage_real_working_counter_2(stage_num):
		counter = 0
		for i in range(len(G.list_worker_biker)):
			if G.list_worker_biker[i].isworking_template == 1:
			#if G.list_worker_normal[i].chicken_bag[0].workingstage_template == stage_num:
				if G.list_worker_biker[i].workingstage_template == stage_num:

					counter = counter + 1

		return counter
	
	def deliver_worker_tracker():
		for i in range(len(G.list_worker_biker)):
			print(G.list_worker_biker[i].name, ' doing stage : ', G.list_worker_biker[i].workingstage_template)
	
	def deliver_chicken_bag():
		counter = 0
		for j in range(len(G.list_worker_biker)):
			if G.list_worker_biker[j].isworking_template == 1:
				counter = counter + 1
		print('current working deliver worker : ', counter)
		for i in range(len(G.list_worker_biker)):
			if len(G.list_worker_biker[i].chicken_bag) != 0:
				print('name : ', G.list_worker_biker[i].name, 'chicken_bag len : ', len(G.list_worker_biker[i].chicken_bag))
	

	
	def fin_order():
		counter = 0
		for j in range(len(G.list_chicken_finished)):
			counter = counter + 1
		return counter
	
	print('$$$')
	if G.loop_counter <= G.epoch_counter_tmp :
		pass
	else:
		print('♠'*30)
		print('length of chicken : ', len(G.list_chicken))
		if (G.loop_counter > G.epoch_counter_tmp) :
			print('loop counter met epoch condition for AGENT')
			print('Global step number : ', G.global_step)
		print('♠'*30)
	print('total number of normal workers : ', len(G.list_worker_normal))
	print('total number of delivery workers : ', len(G.list_worker_biker))
	print('@')
	print('current simulator time : ', datetime.timedelta(seconds = T.times))
	print('created total order numbers : ', len(G.total_order))
	print('delivered total number of orders : ', fin_order())
	print('=' * 60)
	print('current working fry worker out of 3 : ', fry_working_counter())
	print('current non wokring fry worker : ', fry_nonworking_counter())
	print('current used fryer machine out of 6 : ', fryer_machine_counter())
	print('')
	print('current working normal worker out of 4 : ', normal_working_counter())
	print('')
	deliver_chicken_bag()
	print('')
	deliver_worker_tracker()

	print('=' * 60)


	print('0 - idle : ', stage_chicken_counter(0), '   worker : ', stage_working_counter(0), ' -> R : ',stage_real_working_counter(0))
	print('1 - transition_counter : ', stage_chicken_counter(1), '   worker : ', stage_working_counter(1), ' -> R : ',stage_real_working_counter(1))
	print('2 - transition_counter_order :', stage_chicken_counter(2), '   worker : ', stage_working_counter(2), ' -> R : ',stage_real_working_counter(2))
	print('3 - transition_kitchen_mesh : ', stage_chicken_counter(3), '   worker : ', stage_working_counter(3), ' -> R : ',stage_real_working_counter(3))
	print('-'*35)
	print('#'*35)
	print('4 - transition_kitchen_fry_in : ', stage_chicken_counter(4), '   worker : ', stage_working_counter(4), ' -> R : ',stage_real_working_counter(4))
	print('5 - transition_kitchen_fry_processing : ', stage_chicken_counter(5), '   worker : ', stage_working_counter(5), ' -> R : ',stage_real_working_counter(5))
	print('6 - transition_kitchen_fry_complete : ', stage_chicken_counter(6), '   worker : ', stage_working_counter(6), ' -> R : ',stage_real_working_counter(6))
	print('#'*35)
	print('-'*35)
	print('7 - transition_kitchen_fry_wait : ', stage_chicken_counter(7), '   worker : ', stage_working_counter(7), ' -> R : ',stage_real_working_counter(7))
	print('8 - transition_kitchen_fry_sauce : ', stage_chicken_counter(8), '   worker : ', stage_working_counter(8), ' -> R : ',stage_real_working_counter(8))
	print('9 - transition_packaging : ', stage_chicken_counter(9), '   worker : ', stage_working_counter(9), ' -> R : ',stage_real_working_counter(9))
	print('-'*35)
	print('#'*35)
	print('10 - transition_delivery_wait : ', stage_chicken_counter(10), '   worker : ', stage_working_counter_2(10), ' -> R : ',stage_real_working_counter_2(10))
	

	print('11 - transition_delivery_processing : ', stage_chicken_counter(11), '   worker : ', stage_working_counter_2(11), ' -> R : ',stage_real_working_counter_2(11))
	print('12 - transition_delivery_arrive : ', stage_chicken_counter(12), '   worker : ', stage_working_counter_2(12), ' -> R : ',stage_real_working_counter_2(12))
	print('13 - transition_delivery_comeback : ', stage_chicken_counter(13), '   worker : ', stage_working_counter_2(13), ' -> R : ',stage_real_working_counter_2(13))

	print('#'*35)
	print('-'*35)



	print('\n' * 7)

def fin_order_score():
	for i in range(len(G.list_chicken_finished)):
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and score : ", G.list_chicken_finished[i].score)
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and importance : ", G.list_chicken_finished[i].importance)
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and finished time : ", datetime.timedelta(seconds = G.list_chicken_finished[i].fin_time))
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and food process time : ", datetime.timedelta(seconds = G.list_chicken_finished[i].delivery_start_time - G.list_chicken_finished[i].times))
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and delivery elapse time : ", datetime.timedelta(seconds = (G.list_chicken_finished[i].fin_time - G.list_chicken_finished[i].delivery_start_time)))
		print("order times : ", datetime.timedelta(seconds = G.list_chicken_finished[i].times),"  and total elapse time : ", datetime.timedelta(seconds = (G.list_chicken_finished[i].fin_time - G.list_chicken_finished[i].times)))
		print("")
	
# def queue_prints():
    
#     for i in range(len(G.workingstage)):
#         for j in range(len(G.workingstage[i])):
#             print('value of chicken', G.workingstage[i][j].importance)

def weekday_weekend_rand(): #주말 배달 더 크게 하려고
	G.weekday = 0 # reset -> 0 으로 수정하면 바뀌면서 생성...
	sample = [1,2,3,4,5,6,7]
	result = np.random.choice(sample)
	
	if result >=1 and result <=5 : #weekday
		G.weekday_weekend_choice(0) # 1이면 week day
	else:
		pass # keep 0



def sim_main(): #여기에다가 다른 조건들 추가해도 될듯
	create_order_in(T.times) #loop 돌 때 마다...order 생기는거 list 추가
	#기본 task들 부르기
	task_manager.main()

	#log 들어가는 곳
	log_prints()

	#time updater <= 1. simulator용과 실제 os의 time으로 두가지로
	#T.times = T.times + (15) # 30 * 2 or 15
	#time.sleep(0.01) #이거 시뮬레이터 while문 무거워지면 지워도 될 듯
	#os.system('cls')
	
def main():
	# 한번 돌 때 체크하기 : agent 용
	F.loop(0)
	#############################
	weekday_weekend_rand()
	create_worker()
	create_machine()
	log.logger()
	# Threading으로 loop 밖에서 계속 돌려야 됨
	#task_manager.Agent()
	##########################################
	
	#F.loop(0) # 매 epoch 마다 0으로 다시 set -> task manager clr for epoch
	#sim_main() # simulator 아래 층 로직 도는 부분

			
def sim_fin():
	fin_order_score()
	log.Save_epoch() # global에다가 save하고 나중에 그래프로 출력할 것들
	task_manager.Clear_for_epoch() # epoch 위해 Global, flag clear 필요한 부분
	#G.loop_counter = G.loop_counter + 1
	
	###############################
	# 점수 기록하는 것 필요함,
	# 차후에 learning을 위해서도 적용하는 부분 state_wrapper에 필요
	###############################
	
def sim_wrappup():
	log.Saved_to_visualize() # 그래프 등으로 실제 출력할 부분
	
	log.comments()
	#log.logger_open()
	F.lv_time_off = 1

####################### 할일 ################
#############################################
# 1) action : 취소 요구 들어오거나, 어느 단계서든 끝나면
# 2) fryer 작업자 프라이 튀기고 다른 프라이기 동작 가능
# 3) raise ValueError 한번에 수행할 함수 필요함(검증차원)
# 4) delivery 작업자도 machine에 바이크 넣어서 하기
# 5) 동시에 수행하는거...? 반드시 필요한지는 모르겠음
# 6) 마감시간 도달해서, 일하는 직원들 일하고 끝내는 것 구현
# 7) py file들 포함관계 설정
#############################################
#############################################