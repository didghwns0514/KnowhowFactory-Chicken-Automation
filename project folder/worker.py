#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey


########################import py field####################
import multiprocessing
########################import field#######################

########################global value#######################
import Global as G
import FLAG as F
import TIME as T

###########################################################

#https://niceman.tistory.com/196?category=940952
#http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-oop-part-6-%EB%A7%A4%EC%A7%81-%EB%A9%94%EC%86%8C%EB%93%9C-magic-method/
#https://corikachu.github.io/articles/python/python-magic-method
#################   ↑참조할 것, magic method, abstract method
class worker(object) : #작업자 이름 정의하는 부분

	identity = 'worker'

	#working stage의 딕셔너리
	def __init__(self, name, worklicense, machine_name, workscore, hurryrate, isworking_max, isworking_template, workingstage_template) :

		self.time_stamp = None
		self.new_chicken = None
		self.target_chicken = None
		self.chicken_bag = []
		self.location_now = [0,0]
		if ((len(self.chicken_bag) >=2) 
			and (self.worklicense != 2)): #작업 가능 치킨 갯수 검증하기
			raise ValueError('worker Wrong chicken bag length by license')
		if(len(self.chicken_bag)>3 or len(self.chicken_bag)<0):
			raise ValueError('Wrong chicken_bag number')
		#self.workingstage= None
	
						#'idle', 'counter', 'order', 'mesh', 'fry_in', 'processing', 'complete', 'fry_wait', 'sauce', 'packaging','delivery_wait','processing','arrive','comeback'
		self.workingstage_matrix =   [ 
						[   1,       1,         1,      1,      0,          0,           0,          1,       1,       1,           0,            0,            0,        0],#보통사람
						[   1,       1,         1,      1,      1,          1,           1,          1,       1,       1,           0,            0,            0,        0],#프라이
						[   1,       0,         0,      0,      0,          0,           0,          0,       0,       0,           1,            1,            1,        1] #배달
					  ]
				  #마지막으로 order 끝나면 complete 상태로 전환

						#'idle', 'counter', 'order', 'mesh', 'fry_in', 'processing', 'complete', 'fry_wait', 'sauce', 'packaging','delivery_wait','processing','arrive','comeback'
		self.workingstage_duration = [ 
						[   0,       60,      15,     90,      0,          0,           0,          0,         30,        30,           0,            0,            0,        0],#보통사람
						[   0,       60,      15,     90,     60,        720,          30,         15,         30,        30,           0,            0,            0,        0],#프라이
						[   0,       0,        0,      0,      0,          0,           0,          0,          0,         0,          15,         None,         60,     None] #배달
					  ]

		#(1)번 사항 : 기본 인적사항
		#############################################################
		self.name = name #작업자 이름
		self.workingstage_template = workingstage_template
		if(workingstage_template>13 or workingstage_template<0):
			raise ValueError('Wrong working_stage template')

		self.worklicense = worklicense #0,1,2(1.0ver 한정)
		if(worklicense>2 or worklicense<0):
			raise ValueError('Wrong worklicense')
		#0:평범한 일
		#1:튀김
		#2:배달
		##############################################################
		
		
		#(2)번 사항 : 작업 score 시작값, counter 값, score 끝 값
		##############################################################
		self.workscore = workscore #0~100(1.0ver 한정) #작업자의 능력
		self.hurryrate = hurryrate #0~10(1.0ver 한정) #작업자의 능력

		self.isworking_template = isworking_template #0:no,  1:yes 일 여부 표시
		self.isworking_tmp = 0 #시작 stamp 찍는 부분 score 그리고 
		self.isworking_duration = 0 #시간에 대해서 increase할 항목 (T.time - tmp)
		if self.isworking_tmp < 0 :
			raise ValueError('Wrong isworking_tmp')
		self.isworking_max = isworking_max #0:start, isworking이 max이고 이걸 받아서 normalize해주기 100으로
			#초단위로 할 것(평균적으로)
		##############################################################


		if(self.isworking_template>1 or self.isworking_template<0):
			raise ValueError('Wrong isworking_template number')

		self.machine_name = machine_name # 머신 class 상속자를 받는다. list임, 처음에는 None으로 받음, list보다 변수를 집어넣기




		#self.worker_info_to_chicken()
#         self.chicken_bag_push(self.new_chicken)
#         self.chicken_bag_pull(self.target_chicken)
#         self.chicken_bag_out()
#         self.work_start()
#         self.work_progress()
#         self.work_finish()
#         self.update_state()

  #http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-oop-part-4-%ED%81%B4%EB%9E%98%EC%8A%A4-%EB%A9%94%EC%86%8C%EB%93%9C%EC%99%80-%EC%8A%A4%ED%83%9C%ED%8B%B1-%EB%A9%94%EC%86%8C%EB%93%9C-class-method-and-static-method/  
  #https://wayhome25.github.io/cs/2017/04/05/cs-07/
  #https://www.google.com/search?ei=bYBuXc_LIvHKmAXctZ2IBQ&q=nested+function+inside+class+python&oq=function+inside+class+python&gs_l=psy-ab.1.7.0i19j0i5i30i19l9.28519.35919..46506...1.0..0.186.4005.0j29......0....1..gws-wiz.......0i131j0j0i10j0i67j0i70i255j0i30.qnX-qZowxJg

	def work_verify(self, chicken_workingstage_template): #일을 시작할 수 있는지 검증 / push 직전에 검증하는 절차

		def fry_usable_counter(): #사용 가능한 fry있으면 true
#             counter = 0 # 사용 안되고 있는 프라이기 탐색
#             for i in range(len(G.list_machine_fryer)):
#                 if G.list_machine_fryer[i].used == 0 :
#                     counter = counter + 1
#                 else:
#                     pass

#             if counter > 0 :
#                 return True
#             else :
#                 return False
			if len(G.list_machine_fryer) >= 1 :
				return True
			else:
				return False


		if ((self.worklicense == 0) #작업자 어떤 작업을 맡을 수 있는가? #보통 일꾼 
			and (self.workingstage_matrix[self.worklicense][chicken_workingstage_template]) 
			and (len(self.chicken_bag) == 0)
		   ):
			return True


		elif ((self.worklicense == 1) #프라이까지 할 수 있는 사람
			  and (self.workingstage_matrix[self.worklicense][chicken_workingstage_template])
			  and (fry_usable_counter())
			  and ( (chicken_workingstage_template >= 4) and (chicken_workingstage_template <= 6) )
			  and (len(self.chicken_bag) == 0 )
			 ):#머신에서 값을 받음 list형태로 : fryer

			return True
		
		elif ((self.worklicense == 1) #프라이까지 할 수 있는 사람인데 normal_work 담당할 때
			  and (self.workingstage_matrix[self.worklicense][chicken_workingstage_template])
			  and ( (self.workingstage_template <= 3) or (self.workingstage_template >= 7) )
			  and (len(self.chicken_bag) == 0 )
			 ):#머신에서 값을 받음 list형태로 : fryer

			return True
			

		elif ((self.worklicense == 2) #배달만 가능
			  and (self.workingstage_matrix[self.worklicense][chicken_workingstage_template])
			  and (len(self.chicken_bag) <= 2 )
			  and (len(self.chicken_bag) >= 0 )
			 ): #머신에서 값을 받음 list형태로 : bike , len(self.machine_name) != 0 # 항상 참으로

			return True

		else :
			#raise ValueError('worker_name Wrong worker beginning working')
			#pass #안돌림
			return False



	def work_start(self): #일 시작하도록 setting 해준다 worker #flag값 + 맞는지 check
	# fryer 하는 사람은 machine 까지도
	# biker은 굳이 필요 없다.
		def fry_usable_counter(): #사용 가능한 fry있으면 true

			if len(G.list_machine_fryer) >= 1:
				return True
			else:
				return False

		def fry_use_mark():
			if (   (fry_usable_counter())
			   and (self.machine_name != None)
			   ): #사용 가능한 fry가 있다면, 작업자에게 할당된 기계가 없다면
				try:

					tmp_fryer = G.list_machine_fryer[0]
					self.machine_name = G.list_machine_fryer[0]
					G.list_machine_fryer.remove(tmp_fryer)

				except:
					pass
			else : 
				pass



		if len(self.chicken_bag)==0:
			raise ValueError('worker_name Wrong work_start func') #chicken_bag에 작업물이 있어야
		else:
			pass
		
		# 치킨의 stage 사람에게 적용

		self.isworking_tmp = 0 #시작 시간 0으로 검증 차원에서 set
		self.isworking_duration = 0 #경과 시간 0으로 검증 차원에서 set

		self.isworking_tmp = T.times  # 시작 시간 stamp 찍음
			
		#치킨과 작업자에 대한 검증 / 치킨 작업상태로 만들기

		if ((self.worklicense == 0) #작업자 어떤 작업을 맡을 수 있는가? #보통 일꾼 
			and (self.workingstage_matrix[self.worklicense][self.workingstage_template]) 
			and (len(self.chicken_bag) == 1)
		   ):
			self.workingstage_template = self.chicken_bag[0].workingstage_template
			self.isworking_template = 1  #사람 일하는 중으로 만들기

			self.chicken_bag[0].isworking_flag = 1
			self.chicken_bag[0].worker_inwork = 1
			return True

		
		elif ((self.worklicense == 1) #프라이까지 할 수 있는 사람
			  and (self.workingstage_matrix[self.worklicense][self.workingstage_template])
			  and (len(self.chicken_bag) == 1 )
			 ):#머신에서 값을 받음 list형태로 : fryier
			# 4번 stage부터 fry 작업 시작
			#머신을 machine_list에서 빼고 가져온다
			if self.workingstage_template == 4:
				if self.machine_name == None:
					fry_use_mark() # 사용 하겠다는 것을 표시한다

			self.workingstage_template = self.chicken_bag[0].workingstage_template
			self.isworking_template = 1  #사람 일하는 중으로 만들기

			self.chicken_bag[0].isworking_flag = 1
			self.chicken_bag[0].worker_inwork = 1
			return True
			

		elif ((self.worklicense == 2) #배달만 가능
			  and (self.workingstage_matrix[self.worklicense][self.workingstage_template])
			  and (len(self.chicken_bag) <= 3 )
			  and (len(self.chicken_bag) >= 1 )
			 ): #머신에서 값을 받음 list형태로 : bike

			self.workingstage_template = self.chicken_bag[0].workingstage_template
			self.isworking_template = 1  #사람 일하는 중으로 만들기

			self.chicken_bag[0].isworking_flag = 1 #1번 치킨
			#self.chicken_bag[0].worker_inwork = 1
			#self.chicken_bag[1:].worker_inwork = 1 #2,3번 치킨, 여뷰 상관없이 일단 사람 붙음
			for i in range(len(self.chicken_bag)):
				self.chicken_bag[i].worker_inwork = 1
				self.chicken_bag[i].delivery_start_time = T.times
			return True

		else :
			#raise ValueError('worker_name Wrong worker beginning working')
			#pass #안돌림
			return False

		##검증단계

	def work_progress(self): # isworking 값 업데이트 해주어야됨 #chicken.isworking_flag = 1일것

		#isworking_template : 일 시작했다는 flag으로 작용
		if (     (self.isworking_template == 1)
			 and (self.isworking_duration == 0) 
			 ): #일을 시작하였다면, 지금 막
			# state 마다 해당하는 max값을 설정해준다
			self.isworking_max = self.workingstage_duration[self.worklicense][self.workingstage_template]
			# 경과시간 update
			if self.isworking_max == None :
				raise ValueError('wrong isworking_max in worker.py')
		else :
			pass

		if self.isworking_template == 1: #일이 시작이 된것이라면
			if self.isworking_max == None :
				raise ValueError('possible error in isworking_max value assign in worker.py')
			self.isworking_duration = T.times - self.isworking_tmp #계속 업데이트
			#print('duration print : ', self.isworking_duration)

			# importance 증가
			for i in range(len(self.chicken_bag)):
				self.chicken_bag[i].importance_update()

	def work_finish(self): #일 끝내도록 setting 해준다

		def fry_use_release():


			if self.machine_name != None: # 기계가 할당이 되어있다면
				G.list_machine_fryer.append(self.machine_name) # global에 반납하고
				self.machine_name = None # worker안에서 machine표기 초기화 시킴
					


		if(    (len(self.chicken_bag) >= 1)
		   and (self.isworking_template == 1)
		   and (self.workingstage_template == 6)
		  ): #작업 대상이 있는 것을 검증
			# 6번 : fry_complete 부분 끝나면
			if(self.isworking_duration >= self.isworking_max): 
				#치킨 작업이 완료가 되었을 때! : 사람 기준으로 하는 것이 편할 것, 값들이 일치하게 됨

				#작업자
				self.isworking_template = 0 # idle상태로 다시 환원
				self.isworking_tmp = 0 #다시 작업자 tmp 0으로 setting
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = 0 #idle 상태로 만들어줌

				#치킨
				self.chicken_bag[0].isworking_flag = 0 #치킨 일하는 상태 false로
				self.chicken_bag[0].worker_inwork = 0 #치킨에 작업자가 붙었다 false로
				self.chicken_bag[0].move_next_stage = 1 #다음 stage로 옮겨야 됨을 표기
				fry_use_release()
			else:
				pass
			
		elif(  (len(self.chicken_bag) >= 1)
		   and ((self.worklicense == 0) or (self.worklicense == 1))
		   and (self.isworking_template == 1) and (self.worklicense != 2)
		   and (    (self.workingstage_template <= 3 ) 
				 or (self.workingstage_template >= 7 ) )
		  ): #작업 대상이 있는 것을 검증, 배달부 아님
			if(self.isworking_duration >= self.isworking_max):
			# 3: kitchen mesh 까지
			# 7: fry wait 부터
				#작업자
				self.isworking_template = 0 # idle상태로 다시 환원
				self.isworking_tmp = 0 #다시 작업자 tmp 0으로 setting
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = 0 #배달 상태로 만들어줌

				#치킨
				self.chicken_bag[0].isworking_flag = 0 #치킨 일하는 상태 false로
				self.chicken_bag[0].worker_inwork = 0 #치킨에 작업자가 붙었다 false로
				self.chicken_bag[0].move_next_stage = 1 #다음 stage로 옮겨야 됨을 표기
			else:
				pass

		elif(  (len(self.chicken_bag) >= 1)
		   and (self.isworking_template == 1)
		   and ((self.workingstage_template >= 10 ) and (self.workingstage_template <= 11))
		   and (self.worklicense == 2)
		  ): #작업 대상이 있는 것을 검증, 3 or 2 or 1개 담겨있다, 배달부, 일 주문이 2개 이상 남음, 배달 중
			if(self.isworking_duration >= self.isworking_max):
				#작업자
				self.isworking_template = 1 # idle상태로 다시 환원
				self.isworking_tmp = T.times #다시 작업자 tmp 0으로 setting대신 work_start()안거치므로
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = self.workingstage_template + 1 #다음 상태로 만들어줌

				#치킨
				self.chicken_bag[0].isworking_flag = 1 #치킨 일하는 상태 유지
				self.chicken_bag[0].worker_inwork = 1 #치킨에 작업자가 붙었다 유지
				self.chicken_bag[0].workingstage_template = self.chicken_bag[0].workingstage_template + 1 #다음 stage로
				self.chicken_bag[0].move_next_stage = 0 #배달 자체가 끝났음
				#self.chicken_bag[0].arrival_times = T.times # 완료 시점 표기

			else:
				pass

		elif(  (len(self.chicken_bag) >= 2)
		   and (self.isworking_template == 1)
		   and ((self.workingstage_template == 12))
		   and (self.worklicense == 2)
		  ): #작업 대상이 있는 것을 검증, 3 or 2개 담겨있다, 배달부, 일 주문이 2개 이상 남음, 1개 배달 끝남
			if(self.isworking_duration >= self.isworking_max):
				#작업자
				self.isworking_template = 1 # idle상태로 다시 환원
				self.isworking_tmp =  T.times #다시 작업자 tmp 0으로 setting
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = 11 #다음 배달 상태로 환원
				self.location_now = self.chicken_bag[0].address #주소 업데이트
				self.workingstage_duration[2][11] = None #다음 update용을 위해 none으로 바꿔줌, 이건 state_wrapper.py에서 업데이트 해줌

				#치킨
				self.chicken_bag[0].isworking_flag = 0 #치킨 일하는 상태 false로
				self.chicken_bag[0].worker_inwork = 0 #치킨에 작업자가 붙었다 false로
				self.chicken_bag[0].move_next_stage = 1 #배달 자체가 끝났음
				self.chicken_bag[0].arrival_times = T.times # 완료 시점 표기

			else:
				pass

		elif(  (len(self.chicken_bag) == 1)
		   and (self.isworking_template == 1)
		   and ((self.workingstage_template == 12 ) )
		   and (self.worklicense == 2)
		  ): #작업 대상이 있는 것을 검증, 1개 담겨있다, 배달부, 마지막 배달
			if(self.isworking_duration >= self.isworking_max):
				#작업자
				self.isworking_template = 1 # 일하는 상태
				self.isworking_tmp = T.times #다시 작업자 tmp 0으로 setting
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = 13 #13번 # 다음 stage로 이동
				self.location_now = self.chicken_bag[0].address #주소 업데이트
				self.workingstage_duration[2][11] = None

				#치킨
				self.chicken_bag[0].isworking_flag = 0 #치킨 일하는 상태 false로
				self.chicken_bag[0].worker_inwork = 0 #치킨에 작업자가 붙었다 false로
				self.chicken_bag[0].move_next_stage = 1 #다음 stage로 옮겨야 됨을 표기
				self.chicken_bag[0].arrival_times = T.times
			else:
				pass

		elif(  (len(self.chicken_bag) == 0)
		   and (self.isworking_template == 1)
		   and ((self.workingstage_template == 13 ) )
		   and (self.worklicense == 2)
		  ): #0개 담겨있고, 돌아오는 길
			if(self.isworking_duration >= self.isworking_max):
				#작업자
				self.isworking_template = 0 # 일하는 상태
				self.isworking_tmp = 0 #다시 작업자 tmp 0으로 setting
				self.isworking_duration = 0 #경과시간 0으로 setting
				self.workingstage_template = 0 # 다음 stage로 이동
				self.location_now = [0,0] #주소 업데이트, 업장으로 변경
				self.workingstage_duration[2][13] = None

				#치킨
#                 self.chicken_bag[0].isworking_flag = 0 #치킨 일하는 상태 false로
#                 self.chicken_bag[0].worker_inwork = 0 #치킨에 작업자가 붙었다 false로
#                 self.chicken_bag[0].move_next_stage = 1 #다음 stage로 옮겨야 됨을 표기
			else:
				pass
			
		elif(   (len(self.chicken_bag) >= 1) 
			and (self.isworking_template == 1)
			and (self.worklicense == 1)
			and (   (self.workingstage_template >= 4)
				 and (self.workingstage_template <= 5))
		): # fry 작업 과정 중에 있음
			self.chicken_bag[0].workingstage_template = self.chicken_bag[0].workingstage_template + 1 #그냥 다음 것으로 
			self.workingstage_template = self.workingstage_template + 1
			if self.chicken_bag[0].workingstage_template != self.workingstage_template :
				raise ValueError('worker Wrong work_finish func')
			else: pass
			
			#stage올리고 나서 바로 다음 stage에서 수행을 지속하려면 초기화
			self.isworking_duration = 0
			#stage 올리고 나서 stage 진입 시간 기록
			self.isworking_tmp = T.times
			#혹시 몰라 검증
			self.chicken_bag[0].move_next_stage = 0
			

		else:
			pass

				


######################이거 필요#######################
#   def update_state(self): # state를 다음으로 바꿔준다
#     pass
#####################################################   


	def chicken_bag_push(self, new_chicken = None): #chicken_bag에대가 치킨 넣어줌

		if ( (new_chicken != None) and (self.chicken_bag.__contains__(new_chicken)==False)
			and (len(self.chicken_bag)<=2)  and (len(self.chicken_bag)>=0) ) : #flag로 새로운 item은 true, 다르면 false
			self.new_chicken = new_chicken
			#self.new_chicken.workingstage_template = self.workingstage_template #작업자 stage를 갖고있는 치킨에 넣어줌
			#반대로 변했음
			self.workingstage_template = self.new_chicken.workingstage_template

			#self.chicken_bag.extend(self.new_chicken) #new chicken은 반드시 list로 들어올 것
			self.chicken_bag.append(self.new_chicken)

			self.new_chicken = None


	def chicken_bag_sort(self): # 자동으로 완료된 chicken을 return하기 chicken bag 에서
		pass


	def chicken_bag_pull(self, target_chicken = None): #chicken_bag에대가 치킨 빼는 과정 / flag로 전달
		if ((target_chicken != None) and (self.chicken_bag.__contains__(target_chicken)) 
			and (len(self.chicken_bag)<=3)  and (len(self.chicken_bag)>=1) ): # 뺄 수 있는 것이 있다.
			self.target_chicken = target_chicken #class 인스턴스 interface / python 문법이유
			#self.target_chicken.workingstage_template = 1 # idle 상태로 만들어줌 chicken에 대해
			
			if( (len(self.chicken_bag) == 1 )
			and (self.worklicense != 2)
			   ):
				self.workingstage_template = 0 #작업자도 idle 상태로 만들어줌
#             elif((len(self.chicken_bag) == 1)
#              and (self.worklicense == 2)):
#                 self.workingstage_template = 13 #한번 더 확인
			elif(len(self.chicken_bag) >= 2): # 2개이상 들어있다면 계속 작업해야 하므로, 배달부
				pass


			#target_chicken 지워줌, return해줌
			self.chicken_bag.remove(self.target_chicken) #위에 flag에서 이미 검증됨
			self.target_chicken_tmp = self.target_chicken #임시 저장

			self.target_chicken = None  #초기화
			return self.target_chicken_tmp #return시켜줌


