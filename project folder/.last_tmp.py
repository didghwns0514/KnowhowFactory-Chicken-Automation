#-*-coding: utf-8-*-
########################sublime text 2용 hotkey#############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey
########################global value#######################
#아예 시뮬레이터 돌리는 용도로 사용할 python script
clock_global = 15
#전체 주문 갯수를 세는 용도
total_order_list=[]
#시작, 끝 시간
#end time 도달하면 전체 프로세스 종료해야됨l
start_time = 0
current_time = 0
end_time = 10
#end_time = (clock_global*4)*60*12 #clock global곱하고 4배=> 60분

########################Simulator control##################
normal_worker = 10
fry_worker = 2
delivery_worker = 6
########################import py field#####################
import work_names, work_state_process, worker_name
import coming_order
import state
import log
########################import field#######################
#import random # import randit
from random import uniform
#import time
###########################################################

def create_order (time):
	if(uniform(0,1)==1):
		#50퍼의 확률임, 나중에 업데이트 해서 점심 저녁 맞춰가지고 모델링해야됨
		#crerate order and append
		######################################################
		#coming_order에서 랜덤으로 넣어주는란
		number = uniform(0,3) #갯수
		what = uniform(0,10)
		address = create_address()

		return coming_order.order(time, number, what, address)
	

def create_address():
	#치킨집을 기준으로 (0,0)에서 xy 좌표로 나타낸주는 함수
	x = uniform(-100,100)
	y = uniform(-100,100)
	return (x,y)


def create_worker ():
	###worker 자동 생성 함수	
	worker_list = []
	for i in range(1,normal_worker + 1):
		working_personel1 = worker_name.worker(str(i)+"st_worker",0,uniform(0,100),
			uniform(0,10))
		worker_list.append(working_personel1)

	for i in range(1,fry_worker + 1):
		working_personel2 = worker_name.worker(str(i)+"st_worker",1,uniform(0,100),
			uniform(0,10)) 
		worker_list.append(working_personel2)

	for i in range(1,delivery_worker + 1):
		working_personel3 = worker_name.worker(str(i)+"st_worker",1,uniform(0,100),
			uniform(0,10)) 
		worker_list.append(working_personel3)

	return worker_list


def main (time):
	###1 loop용 작성 창
	#print create_worker()[11].worklicense
	worker_name = create_worker()
	coming_order = create_order(time)

	#global에다 만들어진 오더를 넣는다
	total_order_list.append(coming_order)
	work_state_process.process(time, worker_name, total_order_list)
	#work_state_process 사용되어야함


if __name__ == '__main__':
	ts = start_time
	print ("starting the store")
	while (current_time <= end_time):
		#start_time = start_time + clock_global
		current_time = current_time + clock_global
		main(current_time) #여기에 돌릴게 아예 들어가야된다
	print ("closing the store")