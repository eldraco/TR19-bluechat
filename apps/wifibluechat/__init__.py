# This file is part is an addon app of the Troopers 19 Badge project, https://troopers.de/troopers19/

import display
import network
import system
import socket
import time

from system import app, screen, Kernel
from machine import Pin,I2C

class StartScreen(screen.Screen):
    ACTION_ACTIVATE    = 0
    ACTION_FIND    = 1

    MENU_ITEMS = [

        {'text': 'Activate my server...', 'action': ACTION_ACTIVATE},
        {'text': 'Find others...', 'action': ACTION_FIND},
    ]

    def on_menu_selection(self, item):
        if item['action'] == self.ACTION_ACTIVATE:
            return Kernel.ACTION_LOAD_SCREEN, 1
        elif item['action'] == self.ACTION_FIND:
            return Kernel.ACTION_LOAD_SCREEN, 2

class FindOthersScreen(screen.Screen):

    def http_get(url):
	_, _, host, path = url.split('/', 3)
	addr = socket.getaddrinfo(host, 80)[0][-1]
	s = socket.socket()
	s.connect(addr)
	s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
	while True:
	    data = s.recv(100)
	    if data:
		print(str(data, 'utf8'), end='')
	    else:
		break
	s.close()

    def update(self):
        self.display.fill(display.BACKGROUND)
        self.display.text('Finding the top 5 badges around you...', 0, y=0, wrap=display.WRAP_INDENT,update=True)

        # Create the nic object
        nic = network.WLAN(network.STA_IF)
        nic.active(True)
        aps = nic.scan()
        for i in range(len(aps)):
            text = str(aps[i][0].decode('utf-8'))
            pos = 10* (i + 1)
            self.display.text(text, 0, y=pos, wrap=display.WRAP_INDENT,update=True)
            if i > 3:
                break
        # connect
        nic.connect('latinos-badge', 'chingatumadre')
        if not nic.isconnected():
            return self.back()
        #self.display.fill(display.BACKGROUND)
        #ip = nic.ifconfig()[0]
        #self.display.text('Connected! We have IP {}'.format(ip), 0, y=0, wrap=display.WRAP_INDENT,update=True)
        
        # Send text
        self.display.fill(display.BACKGROUND)
        self.display.text('Sending...', 0, y=0, wrap=display.WRAP_INDENT,update=True)
	s = socket.socket()
        host = '192.168.4.1'
	addr = socket.getaddrinfo(host, 80)[0][-1]
	s.connect(addr)
        self.display.text('Done...', 0, y=0, wrap=display.WRAP_INDENT,update=True)

        #while True:
        """
        s.send(bytes('hola de sebas', 'utf8'))
        self.display.text('Receiving...', 0, y=10, wrap=display.WRAP_INDENT,update=True)
        data = s.recv(100)
        self.display.text(str(data), 0, y=20, wrap=display.WRAP_INDENT,update=True)

        return self.back()
        """


    def on_text(self,event):
        if event.value is None:
            return self.back()

    def back(self, event):
        self.RENDER = True
        return Kernel.ACTION_LOAD_SCREEN, 0


class ActivateScreen(screen.Screen):

    def update(self):
        self.display.fill(display.BACKGROUND)
        self.display.text('Activating your Wifi...', 0, y=0, wrap=display.WRAP_INDENT,update=True)

    def on_text(self,event):
        if event.value is None:
            return self.back()

        return Kernel.ACTION_RELOAD

    def back(self, event):
        self.RENDER = True
        return Kernel.ACTION_LOAD_SCREEN, 0


class App(app.App):
    VERSION = 1

    screens = [
        StartScreen(),
        ActivateScreen(),
        FindOthersScreen(),
    ]


