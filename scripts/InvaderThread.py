import threading
try:
	import Queue as q
except:
	import queue as q
class CMSocketChat(threading.Thread):
	""" thread running as Websocket chat client to 

	Input is done by placing data objects into the
	Queue passed in data_queue.

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
					try:
						client.sendMessage(str(command['value']))
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
