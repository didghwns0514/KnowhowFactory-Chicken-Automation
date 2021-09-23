#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey


########################import py field####################

########################import field#######################
import numpy as np
import datetime
from random import choice
# import matplotlib.pyplot as plt
# import matplotlib.style as sty
# sty.use(['seaborn-notebook', 'ggplot'])
########################global value#######################
import Global as G
import FLAG as F
import TIME as T

########################################################### 
from pylab import *
from scipy.optimize import curve_fit

# https://stackoverflow.com/questions/35990467/fit-two-gaussians-to-a-histogram-from-one-set-of-data-python
# https://smlee729.github.io/python/simulation/2015/03/25/2-curve_fitting.html

gauss_times = T.times_begin
print('gauss_times : ', datetime.timedelta(seconds = gauss_times), '  simulator started')

def straight_func(x1,y1, x2,y2):
	global gauss_times
	output = 0
	if T.times < x1 :
		pass
	elif T.times >= x2 :
		pass
	else:
		#tmp_times = ( (times - (11*60*60)) % (2*60) ) #나머지 계산, 경과시간 계산, 초단위로 
		tmp_times = ( (T.times - (gauss_times)) % (2*60) ) #나머지 계산, 경과시간 계산, 초단위로
		if(tmp_times == 0):
			output = ( (y2-y1)/(x2-x1) ) * (T.times - x1) + y1
			return int(output)
		else:
			return output

def main(times):
	global total_order_numb

# 	f1=straight_func(10*60*60,0,12*60*60,5)
# 	f2=straight_func(12*60*60,5,15*60*60,2)
# 	f3=straight_func(15*60*60,2,19*60*60,8)
# 	f4=straight_func(19*60*60,8,23*60*60,2)
			# 주문 시작은 11시, 23시에 끝남
			
	output_val = 0
	if (  (times >= 11 * 60 * 60)
	   and(times < 12 * 60 * 60)):
		output_val = straight_func( 11 * 60 * 60, 0, 12 * 60 * 60, 5)
		
	
	elif(  (times >= 12* 60 * 60)
		and(times < 15* 60 * 60)):
		ouput_val = straight_func(12 * 60 * 60, 5, 15*60*60, 1)
	
	elif(  (times >= 15* 60 * 60)
		and(times < 19* 60 * 60)):
		output_val = straight_func(15 * 60 * 60, 2, 19*60*60, 7)
	
	elif(  (times >= 19* 60 * 60)
		and(times < 23* 60 * 60)):
		output_val = straight_func(19 * 60 * 60, 8, 23*60*60, 2)
	else:
		pass
	
	randseed = np.random.randint(output_val - 1, output_val + 1, size = 1)
	if randseed > 0 :
		ouput_val = randseed
	else:
		pass
	
	#ans_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1, output_val]
	if G.weekday == 0 : # 주말이면
		ans_list = [0]*97
		#ans_list = [0]*95
		#ans_list = [0]*80
	else:
		ans_list = [0]*110
	ans_list.extend([2,2,1, output_val])
	tmp_output = np.random.choice( ans_list, 1 )[0]
	total_order_numb = total_order_numb + tmp_output
	#print('tmp out : ', tmp_output)

	return tmp_output



total_order_numb = 0

