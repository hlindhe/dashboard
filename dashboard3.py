#!/usr/bin/python3
# coding=utf-8

import sys
import time
import pygame
import pygame.gfxdraw
import pygame.freetype
import pprint
import locale
import socket
import json
import array
import paho.mqtt.client as mqtt


# statusline
# x x x 
# 80x80 

# standard color-names

BLACK                = pygame.Color("#000000")
BLUE                 = pygame.Color("#0000FF")
GREEN                = pygame.Color("#008000")
RED                  = pygame.Color("#FF0000")
WHITE                = pygame.Color("#FFFFFF")
YELLOW               = pygame.Color("#FFFF00")
GREY010              = pygame.Color("#101010")
GREY040              = pygame.Color("#404040")
GREY080              = pygame.Color("#808080")
GREY0B0              = pygame.Color("#B0B0B0")
GREY0C0              = pygame.Color("#C0C0C0")
TRANSPARENT          = pygame.Color(0,0,0,0)

#
# globals
#
running=True
menuscreen=0
menubuttons=10
daymode = True
mqttvalues=dict()
featureflags=dict()
featureflags['haveaccelerometer']=False
featureflags['havegps']=False
featureflags['havecanbus']=False
accelerometerxhistory=list()
accelerometeryhistory=list()
accelerometerzhistory=list()
#
# pygame
#
def updateflags():
	if mqttvalues.get('mpu6050/accelerometer_x',False):
		if mqttvalues.get('mpu6050/accelerometer_y',False):
			if mqttvalues.get('mpu6050/accelerometer_z',False):
				featureflags['haveaccelerometer']=True
	
	if featureflags['haveaccelerometer']:
		accelerometerxhistory.append(float(mqttvalues.get('mpu6050/accelerometer_x')))
		accelerometeryhistory.append(float(mqttvalues.get('mpu6050/accelerometer_y')))
		accelerometerzhistory.append(float(mqttvalues.get('mpu6050/accelerometer_z')))
		if len(accelerometerxhistory) > 300:
			accelerometerxhistory.pop(0)
			accelerometeryhistory.pop(0)
			accelerometerzhistory.pop(0)


def displayscreen():
#  screen.fill(BLUE)
#  userscreen.fill(YELLOW)
#  headerscreen.fill(RED)
#  buttonsscreen.fill(GREEN)
	display_headerscreen()
	display_buttonscreen()

	if menuscreen == 0:
		displayscreen_0()
	elif menuscreen == 1:
		displayscreen_1()
	elif menuscreen == 2:
		displayscreen_2()
	elif menuscreen == 3:
		displayscreen_3()
	elif menuscreen == 4:
		displayscreen_4()
	elif menuscreen == 5:
		displayscreen_5()
	elif menuscreen == 6:
		displayscreen_6()
	elif menuscreen == 7:
		displayscreen_7()
	elif menuscreen == 8:
		displayscreen_8()
	elif menuscreen == 9:
		displayscreen_9()

	pygame.display.flip()
	return

def display_headerscreen():
	headerscreen.fill(BLACK)
	timestring=time.strftime('%H:%M:%S')
	timestring_rect=fontsystem48.get_rect('88:88:88')
	timestring_rect.center=headerscreen.get_rect().center
	datestring=time.strftime('%A, %d %B')
	datestring_rect=fontsystem24.get_rect(datestring)
	datestring_rect.bottom=timestring_rect.bottom
	datestring_rect.left=40 #headerscreen.get_rect().centerx/3
	if daymode:
		fontsystem48.render_to(headerscreen,timestring_rect,timestring,WHITE,BLACK)
		fontsystem24.render_to(headerscreen,datestring_rect,datestring,WHITE,BLACK)
	else:
		fontsystem48.render_to(headerscreen,timestring_rect,timestring,RED,BLACK)
		fontsystem24.render_to(headerscreen,datestring_rect,datestring,RED,BLACK)


#TODO: Add icons for gps, network, canbus

	return

def display_buttonscreen():
	buttonsscreen.fill(BLACK)
	for i in range(menubuttons):
		x=i*80
		y=0
		r=pygame.Rect(x,y,80,80)
		#if menuscreen==i:
		#  pygame.draw.rect(buttonsscreen,BLUE,r,0)
		
		menuchar=""
		menutext=""
		if i==0:
			menuchar=u'\uf015'	# Home
		if i==1:
			menutext='Fönster'	# Fönster
		if i==2:
			menutext='Lutning'	# Lutning
		if i==3:
			menutext='Tank'		# Tank
			#menuchar=u'\uf52f'
		if i==4:
			menuchar=u'\uf16d'	# Kamera
		if i==5:
			menuchar=u'\uf201'	# Grafer
		if i==6:
			menuchar=u'\uf0e4'	# Hastighet
		if i==7:
			menuchar=u'\uf1eb'	# Wifi
		if i==8:
			menuchar=u'\uf279'	# Kartor
		if i==9:
			menuchar=u'\uf0ad'	# Settings
		if menuchar != "":
			mr=fontawesome48.get_rect(menuchar)
			mr.center = r.center
			if daymode:
				fontawesome48.render_to(buttonsscreen,mr,menuchar,WHITE,BLACK)    
			else:
				fontawesome48.render_to(buttonsscreen,mr,menuchar,RED,BLACK)
		elif menutext != "":
			mr=fontsystem12.get_rect(menutext)
			mr.center=r.center
			if daymode:
				fontsystem12.render_to(buttonsscreen,mr,menutext,WHITE,BLACK)
			else:
				fontsystem12.render_to(buttonsscreen,mr,menutext,RED,BLACK)
		if menuscreen == i:
			if daymode:
				pygame.draw.line(buttonsscreen,WHITE,r.bottomleft,r.bottomright,4)
			else:
				pygame.draw.line(buttonsscreen,RED,r.bottomleft,r.bottomright,4)

def displayscreen_0():
	userscreen.fill(YELLOW)

	return

def displayscreen_1():
	return

def displayscreen_2():
	userscreen.fill(BLACK)
	if featureflags['haveaccelerometer']: 
		myrect = userscreen.get_rect()
		#print(myrect.midtop)
		pygame.draw.line(userscreen,WHITE,myrect.midtop,myrect.midbottom)
		pygame.draw.line(userscreen,WHITE,myrect.center,myrect.midright)
		centerx=int(myrect.centerx/2)
		centery=int(myrect.centery)
		print(myrect)
		x=int(float(mqttvalues.get('mpu6050/accelerometer_x',"0"))*20)
		y=int(float(mqttvalues.get('mpu6050/accelerometer_y',"0"))*20)
		for r in [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]:
			if r % 20:
				pygame.draw.circle(userscreen, GREY040, (centerx,centery), r, 1) 
			else:
				pygame.draw.circle(userscreen, GREY080, (centerx,centery), r, 1) 

		pygame.draw.circle(userscreen, WHITE, (centerx+x,centery+y), 8, 0)

		for i in range(len(accelerometerxhistory)):
			pygame.draw.line(userscreen, GREY080, (320+i,80), (320+i,80+accelerometerxhistory[i]*20), 1)
			pygame.draw.line(userscreen, GREY080, (320+i,160+80), (320+i,160+80+accelerometeryhistory[i]*20), 1)

	return

def displayscreen_3():
	return

def displayscreen_4():
	return

def displayscreen_5():
	return

def displayscreen_6():
	return

def displayscreen_7():
	return

def displayscreen_8():
	return

def displayscreen_9():
	return

# 
# mqtt
#
def mqtt_on_connect(client, userdata, flags, rc):
	print("Connected MQTT")
	client.subscribe("mpu6050/accelerometer_x")
	client.subscribe("mpu6050/accelerometer_y")
	client.subscribe("mpu6050/accelerometer_z")
	client.subscribe("gps/#")

def mqtt_on_message(client, userdata, msg):
	mqttvalues[msg.topic]=msg.payload
#	print(msg.topic+" "+str(msg.payload))


#
# init python
#
locale.setlocale(locale.LC_ALL,'sv_SE')

#
# init mqtt
#
mqttclient=mqtt.Client()
mqttclient.on_connect = mqtt_on_connect
mqttclient.on_message = mqtt_on_message
mqttclient.connect("localhost")
mqttclient.loop_start()

#
# init pygame
#
pygame.init()
pygame.freetype.init()
mainclock=pygame.time.Clock()

screen = pygame.display.set_mode([0,0],pygame.FULLSCREEN|pygame.NOFRAME)

headerscreen = screen.subsurface([0,0,800,80])
userscreen = screen.subsurface([80,80,640,320])
buttonsscreen = screen.subsurface([0,400,800,80])

fontawesome48=pygame.freetype.Font('fontawesome-webfont.ttf',48)
fontawesome72=pygame.freetype.Font('fontawesome-webfont.ttf',72)
fontsystem12=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)
fontsystem24=pygame.freetype.SysFont(pygame.freetype.get_default_font(),24)
fontsystem48=pygame.freetype.SysFont(pygame.freetype.get_default_font(),48)
#fontsystem12=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)

screen.fill(BLACK)



# 
# main loop
#
while running:
	updateflags()
	displayscreen()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q: running=False
			if event.key == 27: running=False
			if event.key == pygame.K_F10: menuscreen=0
			if event.key == 167: menuscreen=0
			if event.key == pygame.K_F1: menuscreen=1
			if event.key == pygame.K_F2: menuscreen=2
			if event.key == pygame.K_F3: menuscreen=3
			if event.key == pygame.K_F4: menuscreen=4
			if event.key == pygame.K_F5: menuscreen=5
			if event.key == pygame.K_F6: menuscreen=6
			if event.key == pygame.K_F7: menuscreen=7
			if event.key == pygame.K_F8: menuscreen=8
			if event.key == pygame.K_F9: menuscreen=9
			print("key:")
			print(event.key)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			r1=buttonsscreen.get_rect()
			r2=buttonsscreen.get_abs_offset()
			r1.left=r2[0]
			r1.top=r2[1]
			if r1.collidepoint(event.pos):
				menuscreen=int(event.pos[0]/80)
	mainclock.tick(24)
