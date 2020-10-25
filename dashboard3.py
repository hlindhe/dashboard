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
TRANSPARENT          = pygame.Color(0,0,0,0)

#
# globals
#
running=True
menuscreen=1


#
# pygame
#
def displayscreen():
  screen.fill(BLACK)
  screen.fill(BLUE)
  userscreen.fill(YELLOW)
  headerscreen.fill(RED)
  buttonsscreen.fill(GREEN)

  display_headerscreen()
  pygame.display.flip()
  return

def display_headerscreen():
  headerscreen.fill(GREY040)
  timestring=time.strftime('%H:%M:%S')
  timestring_rect=fontsystem48.get_rect('88:88:88')
  timestring_rect.center=headerscreen.get_rect().center
  datestring=time.strftime('%A, %d %B')
  datestring_rect=fontsystem24.get_rect(datestring)
  datestring_rect.bottom=timestring_rect.bottom
  datestring_rect.left=40 #headerscreen.get_rect().centerx/3
  
  fontsystem48.render_to(headerscreen,timestring_rect,timestring,WHITE,GREY040)
  fontsystem24.render_to(headerscreen,datestring_rect,datestring,WHITE,GREY040)
#  print(timestring_rect)
#  print(datestring_rect)
  return

# 
# mqtt
#
def mqtt_on_connect(client, userdata, flags, rc):
  print("Connected MQTT")
#  client.subscribe("mpu6050/#")

def mqtt_on_message(client, userdata, msg):
  print(msg.topic+" "+str(msg.payload))


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

print(pygame.font.SysFont(None,48))

fontawesome48=pygame.freetype.Font('fontawesome-webfont.ttf',48)
fontawesome72=pygame.freetype.Font('fontawesome-webfont.ttf',72)
fontsystem12=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)
fontsystem24=pygame.freetype.SysFont(pygame.freetype.get_default_font(),24)
fontsystem48=pygame.freetype.SysFont(pygame.freetype.get_default_font(),48)
#fontsystem12=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)
# 
# main loop
#
while running:
  displayscreen()
  for event in pygame.event.get():
    if event.type == pygame.QUIT: running=False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q: running=False
  mainclock.tick(50)
