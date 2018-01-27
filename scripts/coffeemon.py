import os, time, ssl, signal, sys
import queue as q
import threading
from optparse import OptionParser
from json import loads , dumps
#from base64 import encodestring, decodestring
import base64

import wsserverthread
from wsserver import SimpleSSLWebSocketServer, SimpleWebSocketServer,SimpleChat

class SimpleCoffeeMonServer(SimpleWebSocketServer):
	def setActualValue(self,actual_value):
		self.actual_value=actual_value
	def getActualValue(self):
		return self.actual_value
	def stringToBase64(self,s):
		'''
			The hell of type conversion!!!
			When using str() without charset parameter it generates a binary string type, see https://docs.python.org/3/library/stdtypes.html#str
			
			>>> str(b'Zoot!')
			"b'Zoot!'"
			>>> str(b'Zoot!',"ascii")
			'Zoot!'
			>>> str(b'Zoot!',"utf8")
			'Zoot!'

			where the binary type make the websocket interface to generate a blob object websocket packet instead of a TEXT object,
			which then finally crashes in the browser client, which expect TEXT, but no binary blob
			
			That gave two days of debugging, so it's better to drop this down as a note here ;-)
		
		'''
		return str(base64.b64encode(s.encode('utf-8')),'utf-8')

	def base64ToString(self,b):
		return base64.b64decode(b).decode('utf-8')


	
class SSLCoffeeMonServer(SimpleSSLWebSocketServer):
	def setActualValue(self,actual_value):
		self.actual_value=actual_value
	def getActualValue(self):
		return self.actual_value
	def stringToBase64(self,s):
		'''
			The hell of type conversion!!!
			When using str() without charset parameter it generates a binary string type, see https://docs.python.org/3/library/stdtypes.html#str
			
			>>> str(b'Zoot!')
			"b'Zoot!'"
			>>> str(b'Zoot!',"ascii")
			'Zoot!'
			>>> str(b'Zoot!',"utf8")
			'Zoot!'

			where the binary type make the websocket interface to generate a blob object websocket packet instead of a TEXT object,
			which then finally crashes in the browser client, which expect TEXT, but no binary blob
			
			That gave two days of debugging, so it's better to drop this down as a note here ;-)
		
		'''
		return str(base64.b64encode(s.encode('utf-8')),'utf-8')

	def base64ToString(self,b):
		return str(base64.b64decode(b).decode('utf-8'),'utf-8')



	
if __name__ == '__main__':
	parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
	parser.add_option("--host", default='localhost', type='string', action="store", dest="host", help="hostname (localhost)")
	parser.add_option("--port", default=9000, type='int', action="store", dest="port", help="port (9000)")
	parser.add_option("--type", default='chat', type='string', action="store", dest="example", help="echo, chat")
	parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
	parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
	parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
   
	(options, args) = parser.parse_args()	

	if options.ssl == 1:
		server = SSLCoffeeMonServer(options.host, options.port, SimpleChat, options.cert, options.cert, version=options.ver)
	else:	
		server = SimpleCoffeeMonServer(options.host, options.port, SimpleChat)

	def close_sig_handler(signal, frame):
		this_thread.join()
		sys.exit()

	signal.signal(signal.SIGINT, close_sig_handler)
	data_queue = q.Queue()
	this_thread=wsserverthread.CMSocketChat(server,data_queue)
	this_thread.start()
	thisMsg={}
	thisMsg['msg']=server.stringToBase64('test')
	states=["full","normal","empty","nopot"]
	stCount=0
	server.setActualValue(8899)
	while True:
		time.sleep(5)
		thisMsg['state']=states[stCount]
		stCount+=1
		if stCount>=len(states):
			stCount=0
		data_queue.put((thisMsg))
