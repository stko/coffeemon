import os, time, ssl, signal, sys
try:
	import Queue as q
except:
	import queue as q
import threading
from optparse import OptionParser
from json import loads , dumps
import InvaderThread
from wsserver import SimpleSSLWebSocketServer, SimpleWebSocketServer,SimpleEcho,SimpleChat

	
if __name__ == '__main__':
	parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
	parser.add_option("--host", default='localhost', type='string', action="store", dest="host", help="hostname (localhost)")
	parser.add_option("--port", default=9000, type='int', action="store", dest="port", help="port (9000)")
	parser.add_option("--type", default='chat', type='string', action="store", dest="example", help="echo, chat")
	parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
	parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
	parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
   
	(options, args) = parser.parse_args()
	cls = SimpleEcho
	if options.example == 'chat':
		cls = SimpleChat	

	if options.ssl == 1:
		server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
	else:	
		server = SimpleWebSocketServer(options.host, options.port, cls)

	def close_sig_handler(signal, frame):
		this_thread.join()
		#server.close()
		sys.exit()

	signal.signal(signal.SIGINT, close_sig_handler)
	#server.serveforever()
	data_queue = q.Queue()

	this_thread=InvaderThread.CMSocketChat(server,data_queue)
	this_thread.start()
	thisMsg={}
	thisMsg['msg']='test'
	while True:
		time.sleep(1)
		#data_queue.put(str(u"invader"))
		print(str(thisMsg))
		data_queue.put(str(thisMsg))

		#for client in server.connections.itervalues():
		#			print ('actual client: '+ client.channel)
			#try:
				#if client != self and client.channel == prefix+thisMsg['channel'] :
				#client.sendMessage(str('{data:{msg:"cCAwIDAgMA0=",channel:"MQ=="}}'))
				#thisMsg={}
				#thisMsg['status']='disconnect'
				#client.sendMessage(dumps(thisMsg))
				#client.sendMessage(str(client.data))

			#except Exception as n:
				#print ("Send Exception: " ,n)
		