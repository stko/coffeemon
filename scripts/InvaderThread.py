import threading
try:
	import Queue as q
except:
	import queue as q
class CMSocketChat(threading.Thread):
	""" thread running as Websocket chat client to 

	Input is done by placing command (as strings) into the
	Queue passed in dir_q.

	Output is done by placing tuples into the Queue passed in result_q.
	Each tuple is (thread name, command, answer).

	Ask the thread to stop by calling its join() method.
	"""
	def __init__(self, server,data_queue):
		super(CMSocketChat, self).__init__()
		self.server = server
		self.data_queue = data_queue
		self.is_runnning=True

	def run(self):
		print (' Thread starts..' )
		while(self.is_runnning):
			self.server.serveonce()
			try:
				command = self.data_queue.get(True, 0.05)
				for client in self.server.connections.values():
				#for client in self.server.connections:
				#			print ('actual client: '+ client.channel)
					try:
						#if client != self and client.channel == prefix+thisMsg['channel'] :
						#client.sendMessage(str('{data:{msg:"cCAwIDAgMA0=",channel:"MQ=="}}'))
						#thisMsg={}
						#thisMsg['status']='disconnect'
						#client.sendMessage(dumps(thisMsg))
						client.sendMessage(command)
						pass

					except Exception as n:
						print ("Send Exception: " ,n)
			except q.Empty:
				continue

		print (' Thread dies..' )

	def join(self, timeout=None):
		self.is_runnning=False
		self.server.close()
		print (' Thread joined..' )
		super(CMSocketChat, self).join(timeout)

	def _do_command(self, command):
		""" Given a directory name, yields the names of all files (not dirs)
		contained in this directory and its sub-directories.
		"""
		return "done..."
