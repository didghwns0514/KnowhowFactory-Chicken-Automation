#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
import time
import threading
import math
########################import field#######################

########################global value#######################
import FLAG as F
###########################################################



###########################################################
#시간, time 관련


# def main():
    
#     time_start = 0
#     flag_begin = 1

#     if flag_begin == 1 :
#         time_start = time.time() #시작 시간 stamp 찍어놓음
#         flag_begin = 0

#  #시간 계산기
# def call_time_1s():
#     if(F.lv_time_off == 0): #simulator 끝나면 꺼짐
#         global time_start
#         time_current = time.time()
#         global times
#         times = 0
#         times =  time_current - time_start #계속 업데이트 시킨다 / 실시간
#         print(times)
#         #threading.Timer(1,self.TaskA).start()

# def call_time():
#     threading.Timer(1,call_time_1s).start()

class time_cal():
	def __init__(self, time_acc):
		self.time_start = 0
		self.flag_begin = 1
		self.time_start = 0
		self.times = 0
		self.time_acc = time_acc #배속을 위한 장치
        
		self.start_stamp()  #돌지 않을까? -> init시에 그냥 돌아버림
        #self.stamp()
		self.curr_stamp_1s()
        
	def start_stamp(self): 
		if self.flag_begin == 1:
			self.flag_begin = 0
			self.time_start = time.time() #시작시간
			print('time start, initialized')
            
#     def stamp(self):
#         threading.Timer(1,self.curr_stamp_1s()).start()
        
	def curr_stamp_1s(self): #현재 시간 계속
		self.times = math.trunc( (time.time() - self.time_start) * self.time_acc )
		global times
		times = self.times
        #print(times)
		threading.Timer(1,self.curr_stamp_1s).start()
        
times = 11 * 60 * 60 #11시 부터 초로 표시해서 시작
times_begin = 11*60*60
time_acc = 1
#at = time_cal(time_acc) 시뮬레이터 작업에는 꺼두는 것으로


        
        
        
