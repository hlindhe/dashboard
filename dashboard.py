#!/usr/bin/python2
# coding=utf-8
import sys
import time
import pygame
import pygame.gfxdraw
import pygame.freetype
from pprint import pprint
import locale
import socket
import json
import array

# statusline
# x x x 
# 80x80 

locale.setlocale(locale.LC_ALL,'sv_SE')

screensizex = 0
screensizey = 0
mainmenubuttons=10
mainmenubuttonsize = 80
TRANSPARENT          = pygame.Color(0,0,0,0)

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





display=1
pygame.init()
screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN|pygame.NOFRAME)
screensizex,screensizey = screen.get_size()
userscreen = screen.subsurface([0,mainmenubuttonsize+1,screensizex,screensizey-mainmenubuttonsize-1])
userscreensizex,userscreensizey = userscreen.get_size()
#pygame.mouse.set_visible(False)
pygame.freetype.init()
fa=pygame.freetype.Font('fontawesome-webfont.ttf',48)
fa72=pygame.freetype.Font('fontawesome-webfont.ttf',72)
sf=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)
sf12=pygame.freetype.SysFont(pygame.freetype.get_default_font(),12)
sf24=pygame.freetype.SysFont(pygame.freetype.get_default_font(),24)
sf48=pygame.freetype.SysFont(pygame.freetype.get_default_font(),48)
caddyback=pygame.image.load('caddy back.png')
caddyside=pygame.image.load('caddy side.png')

caddyback = caddyback.convert_alpha()
caddyside = caddyside.convert_alpha()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.1)
dl_gyro=dict(asd=0)
dl_wifi=dict(asd=0)

def update_datalogger():
  global dl_gyro,dl_wifi
  sock.sendto('mpu6050',('localhost',18600))
  r=sock.recv(1024)
  dl_gyro=json.loads(r)
  sock.sendto('wifi',('localhost',18600))
  r=sock.recv(4000)
  dl_wifi=json.loads(r)

def displayscreenheader():
#    pygame.gfxdraw.rectangle(screen,(0,0,screensizex,mainmenubuttonsize),YELLOW)
    timestring=time.strftime('%H:%M:%S')
    r=sf48.get_rect('88:88:88')
    textbottom=mainmenubuttonsize/2+r.h/2
    sf48.render_to(screen,[screensizex/2-(r.w/2),textbottom-r.h],timestring,WHITE,GREY010)
    datestring=time.strftime('%A, %d %B')
#    datestring=dl_gyro[u'temperature']
#    pprint(dl_gyro)
    r=sf24.get_rect(datestring)
    sf24.render_to(screen,[mainmenubuttonsize/2,textbottom-r.h],datestring,WHITE,GREY010)
    pygame.draw.line(screen,WHITE,(0,mainmenubuttonsize),(screensizex,mainmenubuttonsize) )
    return

def displayscreenfooter():
    pygame.draw.line(screen,WHITE,(0,screensizey-mainmenubuttonsize),(screensizex,screensizey-mainmenubuttonsize) )
    for i in range(mainmenubuttons):
        x=i*(screensizex/mainmenubuttons)
        y=screensizey-mainmenubuttonsize
#        pygame.gfxdraw.box(screen,(x,y,mainmenubuttonsize,mainmenubuttonsize),GREY080)
#        pygame.draw.line(screen,GREY0B0,(x,y),(x+mainmenubuttonsize-1,y),2)
#        pygame.draw.line(screen,GREY0B0,(x,y),(x,y+mainmenubuttonsize-1),2)
#        pygame.draw.line(screen,GREY040,(x+mainmenubuttonsize-1,y+mainmenubuttonsize-1),(x,y+mainmenubuttonsize-1),2)
#        pygame.draw.line(screen,GREY040,(x+mainmenubuttonsize-1,y+mainmenubuttonsize-1),(x+mainmenubuttonsize-1,y),2)
        menuchar=""
        menutext=""
        if i==0:
          menuchar=u'\uf015'
        if i==1:
          menutext=u'Fönster'
#          fa.render_to(screen,[x+0,y+0],u'\uf3fd',WHITE,BLACK)
        if i==2:
          menutext='Lutning'
#          fa.render_to(screen,[x+0,y+0],u'\uf52f',WHITE,BLACK)
        if i==3:
          menutext='Tank'
#          fa.render_to(screen,[x+0,y+0],u'\uf5df',WHITE,BLACK)
#        if i==4:
#          fa.render_to(screen,[x+0,y+0],u'\uf279',WHITE,BLACK)
#        if i==5:
#          fa.render_to(screen,[x+0,y+0],u'\uf279',WHITE,BLACK)
#        if i==6:
#          fa.render_to(screen,[x+0,y+0],u'\uf279',WHITE,BLACK)
        if i==4:
          menuchar=u'\uf16d'
        if i==5:
          menuchar=u'\uf201'
        if i==6:
          menuchar=u'\uf0e4'
        if i==7:
          menuchar=u'\uf1eb'
        if i==8:
          menuchar=u'\uf279'
        if i==9:
          menuchar=u'\uf0ad'
        if menuchar != "":
          r=fa.get_rect(menuchar)
          fa.render_to(screen,[x+mainmenubuttonsize/2-(r.w/2),y+mainmenubuttonsize/2-(r.h/2)],menuchar,WHITE,BLACK)
        elif menutext !="":
          r=sf12.get_rect(menutext)
          sf12.render_to(screen,[x+mainmenubuttonsize/2-(r.w/2),y+mainmenubuttonsize/2-(r.h/2)],menutext,WHITE,BLACK)
        if display == i:
          pygame.draw.line(screen,WHITE,(x,y+mainmenubuttonsize-2),(x+mainmenubuttonsize,y+mainmenubuttonsize-2),2)
    return

def displayscreen_1():
  # stop f04d
  # single up f106
  # single down f107
  # double up  f102
  # double down f103
  # split screen 2x2
  pygame.gfxdraw.vline(userscreen,200,0,319,WHITE)
  pygame.gfxdraw.vline(userscreen,userscreensizex-200,0,319,WHITE)
  pygame.gfxdraw.hline(userscreen,0,userscreensizex,320/2,WHITE)
  up = u'\uf102'
  r=fa72.get_rect(up)
  fa72.render_to(userscreen,[100-(r.w/2),mainmenubuttonsize/2+r.h/2],up,WHITE,BLACK)
  fa72.render_to(userscreen,[400-(r.w/2),mainmenubuttonsize/2+r.h/2],up,WHITE,BLACK)
  fa72.render_to(userscreen,[700-(r.w/2),mainmenubuttonsize/2+r.h/2],up,WHITE,BLACK)

  down= u'\uf103'
  r=fa72.get_rect(down)
  fa72.render_to(userscreen,[100-(r.w/2),userscreensizey/2+mainmenubuttonsize/2-r.h/2],down,WHITE,BLACK)
  fa72.render_to(userscreen,[400-(r.w/2),userscreensizey/2+mainmenubuttonsize/2-r.h/2],down,WHITE,BLACK)
  fa72.render_to(userscreen,[700-(r.w/2),userscreensizey/2+mainmenubuttonsize/2-r.h/2],down,WHITE,BLACK)
  return

def displayscreen_2():
  global dl_gyro
  #Result := ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow;
  sidled=0-float(dl_gyro['accelerometerx'])*9  # -10 - +10
  lutning=float(dl_gyro['accelerometery'])*9 # -10 - +10
  menutext=str(lutning)+ ' ' + str(sidled)
  r=sf12.get_rect(menutext)
  sf12.render_to(userscreen,[screensizex/2-(r.w/2),screensizey/8-(r.h/2)],menutext,WHITE,BLACK)
#  sida = pygame.transform.rotate(caddyside,lutning)
#  userscreen.blit(sida,[50,50])
#  back = pygame.transform.rotate(caddyback,sidled)
#  userscreen.blit(back,[500,50])
  return


tmp_wifi=dict()
rssi_wifi=dict()
def displayscreen_7():
  global dl_wifi,tmp_wifi,rssi_wifi
  i=0
#  pprint(dl_wifi['0'])
  for k in dl_wifi.keys():
    w=dl_wifi[k]
    tmp_wifi[ w['bssid']+'-'+w['ssid'] ] = w
    if rssi_wifi.has_key(w['bssid']+'-'+w['ssid']):
      rssi_wifi[ w['bssid']+'-'+w['ssid'] ].append( w['rssi'] )
    else:
      rssi_wifi[ w['bssid']+'-'+w['ssid'] ]=[w['rssi']]
    
  for wifi in rssi_wifi.keys():
    found=False
    for k in dl_wifi.keys():
      w=dl_wifi[k]
      if wifi == w['bssid']+'-'+w['ssid']:
        found=True
    if found == False:
      rssi_wifi[wifi].append(None)
    
#  tmp_wifi[dl_wifi['pitimestamp']]=dl_wifi
  # sort wifi
  wifis=tmp_wifi.keys()
  wifis.sort(reverse=True)
  i=0
  for wifi in wifis:
#    menutext=tmp_wifi[wifi]['ssid']+" "+str(tmp_wifi[wifi]['rssi'])
#    pygame.gfxdraw.hline(userscreen,0,screensizex,i*20+20,GREY040)
    pygame.gfxdraw.hline(userscreen,0,screensizex,i*20+20+10,GREY040)
    sf12.render_to(userscreen,[0,i*20+20],tmp_wifi[wifi]['ssid'],WHITE,BLACK)
    sf12.render_to(userscreen,[370,i*20+20],str(tmp_wifi[wifi]['rssi']),WHITE,BLACK)
    xoffset=400
    x=0
    for r in rssi_wifi[wifi]:
      v=0
      c=BLACK
      if r != None:
        v=int((100 - abs(r) ) / 10)
        c=RED
      if v>=1:
        c=YELLOW
      if v>=5:
        c=GREEN
      pygame.gfxdraw.vline(userscreen,xoffset+x,i*20+20+10,i*20+20+10-v,c)
      x=x+1
    i=i+1

  for wifi in wifis:
    if len(rssi_wifi[wifi]) > 300:
      rssi_wifi[wifi].pop(0)

  removewifi=[]
  for wifi in tmp_wifi:
    if len(rssi_wifi[wifi]) >= 300:
      if rssi_wifi[wifi].count(None)==300:
        removewifi.append(wifi)

  for wifi in removewifi:
    rssi_wifi.pop(wifi)
    tmp_wifi.pop(wifi)

def displayscreen():
    screen.fill(BLACK)
    # draw header
    displayscreenheader()
    # draw footer
    displayscreenfooter()
    # display main part
    if display == 0:
        #
        a=2
#        pygame.gfxdraw.rectangle(screen,(0,80,800,200),(255,255,255))
#        pygame.gfxdraw.rectangle(screen,(0,80,320,200),(255,255,255))
#        pygame.gfxdraw.rectangle(screen,(500-20,80,320,320),(255,255,255))
    elif display == 1:
        displayscreen_1()
    elif display == 2:
        displayscreen_2()
    elif display == 7:
        displayscreen_7()
    # show screen on display
    pygame.display.flip()





while 1:
    update_datalogger()
    displayscreen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: sys.exit()
            if event.key == 167: display=0
            if event.key == pygame.K_0: display=0
            if event.key == pygame.K_1: display=1
            if event.key == pygame.K_2: display=2
            if event.key == pygame.K_3: display=3
            if event.key == pygame.K_4: display=4
            if event.key == pygame.K_5: display=5
            if event.key == pygame.K_6: display=6
            if event.key == pygame.K_7: display=7
            if event.key == pygame.K_8: display=8
            if event.key == pygame.K_9: display=9
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.pos[1] >=screensizey-mainmenubuttonsize:
            display=event.pos[0]/mainmenubuttonsize
    time.sleep(0.001)
