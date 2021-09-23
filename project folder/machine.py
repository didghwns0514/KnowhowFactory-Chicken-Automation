#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################

########################import field#######################

########################global value#######################
import Global as G
import FLAG as F
###########################################################
class machine_fryer(object) : 
	def __init__(self, whatfryer, used):
		#super(machine_fryer,self).__init__()
		self.whatfryer = whatfryer
		self.used = used
		#0 : not used, #1 : used
		#self.whatstage1 = whatstage1
		#0~100: 완성단계를 표시하는 부분

		#return NotImplemented

			
class machine_bike(object) :
	def __init__(self, whatbike, used):
		#super(machine_bike, self).__init__()
		self.whatbike = whatbike
		self.used = used
		#0 : not used, #1 : used
		#self.whatstage2 = whatstage2
		#0~100: 완성단계를 표시하는 부분

		