from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ProcessProtocol
import sys, os
from armada.master import ArmadaMasterProtocol

CHILD_IN, CHILD_OUT = range(30, 32)

class ArmadaMasterProcessProtocol(ProcessProtocol):
	def __init__(self):
		self.protocol = ArmadaMasterProtocol()
		self.onconnect = Deferred()

	def queueWork(self, finished, function, *args):
		self.protocol.queueWork(finished, function, *args)
		return finished

	def write(self, data):
		self.transport.writeToChild(CHILD_IN, data)

	def connectionMade(self):
		self.protocol.makeConnection(self)
		self.onconnect.callback(self)

	def childDataReceived(self, childFD, data):
		if childFD in (1, 2):
			print data
		if childFD == CHILD_OUT:
			self.protocol.dataReceived(data)

	@property
	def working(self):
		return self.protocol.working

def spawnProcess():
	procArgs = (sys.executable, '-m', 'armada.process.bootstrap', str(CHILD_IN), str(CHILD_OUT))
	proto = ArmadaMasterProcessProtocol()
	reactor.spawnProcess(proto, sys.executable, procArgs, os.environ, path=None, uid=None, gid=None, usePTY=0, childFDs={0: 'w', 1:'r', 2:'r', CHILD_IN: 'w', CHILD_OUT: 'r'} )
	return proto

def deferToProcess(function, *args):
	d = Deferred()
	proto = spawnProcess()
	def queueWorkWhenConnected(obj):
		proto.queueWork(d, function, *args)
		return obj
	proto.onconnect.addCallback(queueWorkWhenConnected)
	def finishProcess(result):
		proto.protocol.kill()
		proto.transport.loseConnection()
		return result
	d.addCallback(finishProcess)
	return d