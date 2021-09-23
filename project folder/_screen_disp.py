#-*-coding: utf-8-*-
#######################sublime text 2용 hotkey##############
#ctrl + / => block comment hotkey
#shift + tab or tab => indent hotkey

########################import py field####################
import pygame
import tkinter
import time
import os
from tkinter import *
from tkinter import ttk

########################import field#######################

########################global value#######################
import Global as G

###########################################################


def workers_load():
	normal_Img = pygame.image.load( str(os.getcwd() + '/normal.png').replace('/','\\') )
	fryer_Img = pygame.image.load( str(os.getcwd() + '/fryer.png').replace('/','\\') )
	driver_Img = pygame.image.load(str(os.getcwd() + '/driver.png').replace('/','\\'))

def main():
	# initialize pygame
	pygame.init()

	#Title and Icon
	pygame.display.set_caption("chicken-simulator")
	icon = pygame.image.load("C:\\Users\\82102\\Desktop\\knowhow_factory\\code\\version_4.0\\chicken_4.0.6\\logos_pygame\\fried-chicken.png")
		#icon = pygame.image.load('logo.png')
	pygame.display.set_icon(icon)
	# create screen
	screen = pygame.display.set_mode((1200, 900))
	running = True

	# GAME loop : infinite loop, opening the game
	while running :
		for event in pygame.event.get() :
		# for any event parameter happening while game is running, we loop
			if event.type == pygame.QUIT :
			# ex) if ESC is pressed
				running = False
	# anything that has to continuously happen in the screen
	# add value of RGB 0~255
		screen.fill((220, 220, 240))

		# always needed
		pygame.display.update()


#main()
'''
https://www.youtube.com/watch?v=FfWpgLFMI7w
'''