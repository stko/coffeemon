'''
modified sample from 

https://github.com/dpallot/simple-websocket-server

The MIT License (MIT)

Copyright (c) 2013 Dave P.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import signal, sys, ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
from json import loads , dumps
from base64 import encodestring, decodestring


class SimpleChat(WebSocket):
	def handleMessage(self):
		if self.data is not None:
			try:
				thisMsg=loads(str(self.data))
				print ('message: '+str(self.data))
				try:
					self.channel # has the client already it's channel assigned?
				except:
					self.channel=self.server.base64ToString(thisMsg["channel"])
					if len(self.server.connections)>1:
						self.sendMessage(dumps({'msg': self.server.stringToBase64("Also in the chat: ")}))
					for client in self.server.connections.values():
						try:
							if client != self :
								client.sendMessage(dumps({'msg': self.server.stringToBase64(self.channel+" joins the chat \n")}))
								client.sendMessage(dumps({'state': 'join', 'msg': self.server.stringToBase64(self.channel+" joins the chat \n")}))
								self.sendMessage(dumps({'msg': self.server.stringToBase64(client.channel+" ")}))
						except Exception as n:
							print ("Send join msg Exception: " ,n)
					if len(self.server.connections)>1:
						self.sendMessage(dumps({'msg': self.server.stringToBase64("\n")}))

					return # as this must be the initial channel announce message from the client to the server, no further handling
				# handle an actual value request
				try:
					thisMsg["state"] # checks if variable exists
					thisMsg['state']=self.server.getActualState()
					thisMsg['msg']=server.stringToBase64('Level has changed')
					self.sendMessage(dumps(thisMsg))
					return # no further handling
				except:
					pass
				# handle an actual state request
				try:
					thisMsg["value"] # checks if variable exists
					thisMsg["value"]=self.server.getActualValue()
					self.sendMessage(dumps(thisMsg))
				except: # it's a normal chat message
					#add channel name to message
					thisMsg["msg"]=self.server.stringToBase64(self.channel+": "+self.server.base64ToString(thisMsg["msg"]))
					for client in self.server.connections.values():
						try:
							if client != self :
								#client.sendMessage(str(self.data))
								client.sendMessage(dumps(thisMsg))
						except Exception as n:
							print ("Send normal msg Exception: " ,n)
					
			except Exception as n:
				print ("Exception: " , n)



	def handleConnected(self):
		print (self.address, 'connected')
		# we can't sent a connect message, as in the moment of connection the client didn't sent his channel yet,
		# so we don't know to where the connect message should go to
		
	def handleClose(self):
		print (self.address, 'closed')
		channel=""
		for client in self.server.connections.values():
			if client != self :
				thisMsg={}
				thisMsg['status']='disconnect'
				try:
					#client.sendMessage(dumps(thisMsg))
					client.sendMessage(dumps({'msg': self.server.stringToBase64(self.channel+" left the chat\n")}))
					client.sendMessage(dumps({'state':'leave','msg': self.server.stringToBase64(self.channel+" left the chat\n")}))
				except Exception as n:
					print ("Send left msg Exception: " ,n)
