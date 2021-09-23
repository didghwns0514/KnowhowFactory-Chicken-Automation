#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
import threading
import time
from msvcrt import getch #key input 받는 역할
########################import field#######################

########################global value#######################

###########################################################

def check(values): #flag 값을 체크해주는 기능
	if ((values != 0) and (values != 1)):
		raise ValueError('FLAG Wrong')


###########################################################
###########################################################
#FLAG관련을 모두 정의하려고 넣은 것임
## SIMULATOR

lv_create_order = 0
check(lv_create_order)

lv_time_off = 0
check(lv_create_order)


# 1 번
###########################
lv_loop_flag = 0
def loop(flag):
	global lv_loop_flag
	
	check(lv_loop_flag)
	lv_loop_flag = flag # loop문 초마다 1번 실행되게
	check(lv_loop_flag)



###########################################################
###########################################################
#FLAG관련을 모두 정의하려고 넣은 것임
## TASK MANAGER


# 1) del, key 'D'를 받아서 실행하도록 하자
#################### 이거는 jupyter lab에서는 띄워서 안된다. rand로 하던가..
# del_key = "init"
# lv_del_request = 0
# check(lv_del_request)

# def del_key_action():
# 	global del_key
# 	lock = threading.Lock()
# 	while True:
# 		with lock:
# 			time.sleep(1)
# 			del_key = getch()

# threading.Thread(target = del_key_action).start()

# while True:
# 	time.sleep(1)
# 	if ((del_key == "d")
# 	   or (del_key == "D")):
# 		print(del_key)
# 		lv_del_request = 1




###########################################################
###########################################################
#FLAG관련을 모두 정의하려고 넣은 것임
## STATE WRAPPER






###########################################################
###########################################################
#FLAG관련을 모두 정의하려고 넣은 것임
## WORKER, ORDER, GAUSSIAN, MACHINE

lv_order_cancle = 0
check(lv_order_cancle)




###########################################################
###########################################################
#FLAG관련을 모두 정의하려고 넣은 것임
## SIMULATOR






###########################################################
###########################################################
## AGENT
lv_agent_active = 0
def agent_active(flag):
	global lv_agent_active
	check(lv_agent_active)
	lv_agent_active = flag
	check(lv_agent_active)
	
lv_score_board_fix = 0
# 한번 불러온 과거 epi 값 최대, 고정시킬 용도
# 0이면 load안됨, 1이면 로드 됨
def score_board_fix(flag):
	global lv_score_board_fix
	check(lv_score_board_fix)
	lv_score_board_fix = flag
	check(lv_score_board_fix)
