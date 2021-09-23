#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey


########################import py field####################
import sched
import time

import multiprocessing
import threading
########################import field#######################
import state_wrapper
########################global value#######################
import Global as G
import FLAG as F
import TIME as T
import DO as D

########################################################### 
# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
# https://www.programering.com/a/MjMyETNwATY.html
# https://docs.python.org/2/library/sched.html
# https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python

# @@@@@ real time tasking -> action based?
# https://www.google.com/search?q=python+real+time+task&rlz=1C1GCEV_enKR831KR831&oq=python+real+time+task&aqs=chrome..69i57j0.6356j0j7&sourceid=chrome&ie=UTF-8

#★★★★★★★★★
# https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/
#@@@@@ Condition of threading
# https://docs.python.org/ko/3/library/asyncio-sync.html
# https://stackoverflow.com/questions/7424590/threading-condition-vs-threading-event
# https://soooprmx.com/archives/8834

def Actions():
	pass  #이거 잘 돌아가는 것 확인하였음
	# 여기에서 action 수행을 시켜야 되는데, 
	# deletion 구현하기
	# value error 계속 체크하는 함수 구현하기

def Normal():
	#모든 stage에 대해서
	## 전체 que 통째로 넣어서 작업 가능하게 만드는게... , 하기 1/2/3 필요한거
	#작업 순서는 생각을 더 해보고, input은 que 전체로 해서 쪼개는 방식으로
    # 1) 전 stage에서 완성된 것 가져오기
	# 2) 현재 stage에서 해당하는 만큼 작업 완성도 올려야 된다
	# 3) 완료된 애들 다음 stage로 올려주어야됨, 배달 대기 stage까지 (1) 번 수행이랑 다른게..
	if T.times >= G.times_max :
		F.loop(1) # 학습을 끝내기 위함
	else:
		pass
	
	state_wrapper.main()

def Agent():
	
	# 참고 자료
	# https://realpython.com/intro-to-python-threading/
	
	#state_wrapper.order_importance_sort() # 밖으로 빼내서 해야 됨
	# epoch 끝날 때 끝나야 하므로 deamon = True 설정
	# 안에서 트레이닝이나 log는 남길 것은 최대한 남기고 버리는 형식
	a1 = threading.Thread(target=state_wrapper.order_importance_sort, args=[], daemon = False)
	a1.start()
	a1.join()  #-> over-rides deamon flag... waits for the either threads to be finished

def Clear_for_epoch(): #global들, agent 관리
	
	F.loop(0)
	F.score_board_fix(0)
	###########################
	# GLOBAL 도 죄다 수정해줄 부분은 해주어야됨
	# Agent꺼는 수정 안해줘도 됨
	###########################
	# AGENT
# 	G.obs_queue = None
# 	G.act_queue = None
# 	G.rwd_queue = None
# 	G.next_obs_queue = None
# 	G.score_queue = None
# 	G.global_step = None
	G.score_now_max = 0
	
	##########################
	# SIMULATOR
	T.times = 11 * 60 * 60
	G.total_order = []
	G.list_chicken = []
	G.list_chicken_finished = []
	G.list_worker_normal = []
	G.list_worker_biker = []
	G.list_machine_fryer = []
	G.list_machine_bike = []
	
	##########################
	# LOGING
	#G.sum_loss_value_tmp = None
	G.sum_loss_value_tmp = []
	G.score_queue = []
	
	
	
def main():
	#Action과 Normal을 동시에 수행해야된다.
	#Actions(), join 들어가면 수행이 안된다 이유는 모름
	#-------------------------------------------------------
# 	t1 = threading.Thread(target=Actions, args=[] )
# 	t2 = threading.Thread(target=Normal, args=[] )
# 	t1.start()
# 	t2.start()
	#-------------------------------------------------------
	#t1.deamon = False #계속 돌릴 것인가? main이 끝나더라도
	#t1.join() #join으로 끝날 때 까지 thread를 기다린다


###################################### multiprocess lock 찾아보기
	Actions()
	Normal()




# def main():
# 	#Action과 Normal을 동시에 수행해야된다.
# 	#Actions()
# 	procs = []
# 	procs.append(multiprocessing.Process(target = Actions, args=[]))
# 	procs.append(multiprocessing.Process(target = Normal, args=[]))
# 	map(lambda x: x.start(), procs)
# 	map(lambda x: x.join(), procs)
    
# main()
        
# def main():
# 	#Action과 Normal을 동시에 수행해야된다.
# 	#Actions()
# 	p1 = multiprocessing.Process(target=Actions, args = [] )
# 	p1.start()
# 	p1.join() #join으로 끝날 때 까지 thread를 기다린다
	
# 	#Normal()
# 	p2 = multiprocessing.Process(target=Normal, args = [] )
# 	p2.start()
# 	p2.join()  #join으로 끝날 때 까지 thread를 기다린다
	        
        

        

