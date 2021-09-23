#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################

########################import field#######################
import logging
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math

from time import gmtime, strftime
from pathlib import Path
########################global value#######################
import TIME as T
import Global as G

###########################################################
# https://hamait.tistory.com/880
# https://inma.tistory.com/136

# https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file-in-python-3/48736764

file_path = None
daytime_tmp = str(strftime("%Y-%m-%d %H,%M,%S", gmtime()))

def logger():
# rootlogger = logging.getLogger('simulator log')

# LOG_DIR = os.getcwd() + '/' + 'logging' + '/' + 'simulator_log_folder' #저장을 해놓을 곳
# if not os.path.exists(LOG_DIR):
# os.makedirs(LOG_DIR)

# fileHandler = logging.StreamHandler(LOG_DIR + '/' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + '.txt')

# rootlogger.addHandler(fileHandler)
	LOG_DIR = os.getcwd() + '/' + 'logging' + '/' + 'simulator_log_folder'
	global file_path
	file_path = str( LOG_DIR + '/' + daytime_tmp + "_" + str(G.loop_counter + 1) +'.txt' ).replace('/','\\')

	sys.stdout = open( file_path, 'a')


# with open( file_path , 'a') as f:
# sys.stdout = f

def logger_open():
	global file_path
	os.startfile(file_path)

def comments(): #매번 코멘트 저장하는 곳
	pass

# 	LOG_DIR = os.getcwd() + '/' + 'logging' + '/' + 'comment_folder' #저장을 해놓을 곳
# 	if not os.path.exists(LOG_DIR):
# 		os.makedirs(LOG_DIR)

# 	comment_file_location = LOG_DIR + '/' + 'comment.txt'

# 	if Path(comment_file_location).is_file(): #파일이 존재한다면
# 		with open(comment_file_location, 'a') as f:
# 			inputs = input('write any comments to add to comment log \n')
# 			print('=' * 60, file = f)
# 			print(  daytime_tmp + ' : ' + str(inputs), file = f )
# 			print('\n' * 3, file = f)

# 	else:
# 		with open(comment_file_location, 'w') as f:
# 			inputs = input('write any comments to add to comment log \n')
# 			print('=' * 60, file = f)
# 			print(  daytime_tmp + ' : ' + str(inputs), file = f )
# 			print('\n' * 3, file = f)

#fileHandler = logging.FileHandler(LOG_DIR + '/' + 'comment.txt')




def Save_epoch(): # epoch 매번 저장할 곳
	#### PANDAS 나중에 써야 할 수도
	def average(lister):
	# 리스트 평균 구하는 함수
		if len(lister) != 0 :
			return(sum(lister)/len(lister))
		else:
			return -77

	#bubble_to_dqn_N = int(G.epoch_counter * 0.1 )
	#G.loop_counter 가 증가하는 것임
	
	#치킨 배달 완료 된거 다시 parsing용 함수
	def y1_parser():  #평균 배달 시간
		sum = 0
		for i in range(len(G.list_chicken_finished)):
			tmp_time = G.list_chicken_finished[i].fin_time - G.list_chicken_finished[i].delivery_start_time
			sum = sum + tmp_time
		avg = (sum/60)/len(G.list_chicken_finished)
		return( round(avg,2) )
	
	def y2_parser():#평균 주문 ~ 배달완료 시간
		sum = 0
		for i in range(len(G.list_chicken_finished)):
			tmp_time = G.list_chicken_finished[i].fin_time - G.list_chicken_finished[i].times
			sum = sum + tmp_time
		avg = (sum/60)/len(G.list_chicken_finished)
		return( round(avg,2) )
	
	def y3_parser(): #주문 갯수
		return(int(len(G.list_chicken_finished)))
	
	def t2_parser(): # score
		if G.loop_counter <= G.epoch_counter_tmp :
			return 0
		else:
			if len(G.score_queue) == 0 :
				return -10
			else:
				return average(G.score_queue)
	
	def t1_parser(): # loss
		if G.loop_counter <= G.epoch_counter_tmp :
			return 0
		else:
			if len(G.sum_loss_value_tmp) == 0:
				return -10
			else:
				return average(G.sum_loss_value_tmp)
	
	def o1_parser(): # time 별 주문량 기록
		pass
	
	def o2_parser(): # 주문 늦게 배달 된거 센다
		counter = 0
		for i in range(len(G.list_chicken_finished)):
			if( (G.list_chicken_finished[i].fin_time - G.list_chicken_finished[i].times)/60 >= G.k + 5): # 38분쯤?
				counter = counter + 1
		return counter
	# 이미 시뮬레이터 하면서 parsing까지 다 해놓음, epoch별이 아니라서, 개별 주문마다라서
	
	G.x.append(G.loop_counter + 1)
	G.y1.append(y1_parser())
	G.y2.append(y2_parser())
	G.y3.append(y3_parser())
	G.t1.append(t1_parser())
	G.t2.append(t2_parser())
	G.o2.append(o2_parser())

def Saved_to_visualize():
	# https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure-in-matplotlib
	# https://freeprog.tistory.com/15
	# https://pinkwink.kr/972
	# https://zzsza.github.io/development/2018/08/24/data-visualization-in-python/
	
	# X축
	x = np.array(G.x)
	x_t = np.array(G.x_t)
	
	# Y축
	y1 = np.array(G.y1)
	y2 = np.array(G.y2)
	y3 = np.array(G.y3)
	t1 = np.array(G.t1)
	t2 = np.array(G.t2)
	o1 = np.array(G.o1)
	o2 = np.array(G.o2)
	
	#fig = plt.figure(figsize=(100,50)) / 1920 1080
	# https://codeday.me/ko/qa/20190314/53531.html
	# my dpi
	my_dpi = 96
	fig = plt.figure(figsize = (21*2.5/10, 7*6/10), dpi = 96)
	matplotlib.rcParams.update({'font.size': 3})
	#211
	plt.subplot(621)
	plt.plot(x,y1, label = 'avg deliver T', color = 'r')
	plt.plot(x,y2, label = 'avg total T', color = 'b')
	plt.axvline(x=G.epoch_counter_tmp+1, color='k', linestyle='--')
	plt.legend(loc='upper right')
	plt.ylabel('T in minutes')
	plt.xlabel('Epoch')
	plt.grid()
	plt.tight_layout()

	
# 	plt.subplot(612)
	
# 	plt.legend(loc='upper right')
# 	plt.ylabel('T in minutes')
# 	plt.xlabel('Epoch')
# 	plt.grid()
	
	#212
	plt.subplot(623)
	plt.plot(x,y3, label = 'total Order',color = 'g')
	plt.axvline(x=G.epoch_counter_tmp + 1, color='k', linestyle='--')
	plt.legend(loc='upper right')
	plt.ylabel('Num of order')
	plt.xlabel('Epoch')
	plt.tight_layout()
	plt.grid()
	plt.tight_layout()

	
	#213
	plt.subplot(622)
	plt.plot(x,t1, label = 'loss DQN', color = 'y')
	plt.axvline(x=G.epoch_counter_tmp + 1, color='k', linestyle='--')
	plt.legend(loc='upper right')
	plt.xlabel('Epoch')
	plt.tight_layout()
	plt.grid()
	plt.tight_layout()

	#214
	plt.subplot(624)
	plt.plot(x,t2, label = 'score DQN', color = 'k')
	plt.axvline(x=G.epoch_counter_tmp + 1, color='k', linestyle='--')
	plt.legend(loc='upper right')
	plt.xlabel('Epoch')
	plt.grid()
	plt.tight_layout()
		
	
	plt.subplot(626)
	plt.scatter(x_t,o1, label = 'time & order', color = 'b', s = 1)
	plt.legend(loc='upper right')
	plt.xlabel('Time')
	plt.grid()
	plt.tight_layout()
	
	plt.subplot(625)
	plt.scatter(x,o2, label = 'late orders ~' + str(G.k + 5), color = 'r', s = 1)
	plt.axvline(x=G.epoch_counter_tmp + 1, color='k', linestyle='--')
	plt.legend(loc='upper right')
	plt.xlabel('Epoch')
	plt.grid()
	plt.tight_layout()
	
	
	curr_dir = str(os.getcwd() + "/image").replace('/','\\')
	if not os.path.isdir(curr_dir): # 존재하지 않는 폴더라면
		os.mkdir(curr_dir) #만들어줌
	else:
		# 이미 있으므로
		pass

	location = "image/" + daytime_tmp + ".png"
	plt.savefig(location, dpi = 1000, bbox_inches='tight')
	Location = os.getcwd() + "/" + location
	Location.replace('/','\\')
	os.startfile(Location)
	
	################## 어노테이션 ###############
# 	for i,j in zip(x,y):
# 		if G.result_list_2[i][0]=='S':
# 			plt.annotate(str('S'),xy=(i,j+0.5))
# 			#plt.annotate(str(formatPrice_2(G.result_list_2[i][2])),xy=(i,j+0.5))
# 		elif G.result_list_2[i][0]=='B':
# 			plt.annotate(str('B'),xy=(i,j+0.5))
# 			#plt.annotate(str(formatPrice_2(G.result_list_2[i][2])),xy=(i,j+0.5))
# 		elif G.result_list_2[i][0]=='X':
# 			plt.annotate(str('X'),xy=(i,j+0.5))
# 			#plt.annotate(str(formatPrice_2(G.result_list_2[i][2])),xy=(i,j+0.5))
# 		elif G.result_list_2[i][0]=='H':
# 			pass
# 			#plt.annotate(str('H'),xy=(i,j+0.5))
# 		else:
# 			pass

	
	############################################
	
	
	#plt.show()
	#"result/" + G.list_2_txt_daytime + "__model_ep" + str(G.e) + ".txt"
