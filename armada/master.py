import os
import sys
from twisted.internet.protocol import Protocol
from armada.encoding import Reader, packArray, packUTF8, packPickle, ReadException, packUInt, packByte
import inspect

SUCCESS, FAILURE = range(2)

CONTINUE, KILL = range(2)

class ArmadaMasterProtocol(Protocol):
	def __init__(self):
		self.finished = None
		self.reader = Reader()

	def queueWork(self, finished, function,  *args):
		self.finished = finished
		if hasattr(function, '__call__'):
			if function.__module__ == '__main__':
				function = '.'.join([os.path.splitext(os.path.basename(sys.modules['__main__'].__file__))[0], function.__name__])
			else:
				function = '.'.join([function.__module__, function.__name__])
		self.transport.write(packByte(CONTINUE) + packUTF8(function) + packArray(packUInt, packPickle, args))
		return self.finished

	def kill(self):
		self.transport.write(packByte(KILL))

	def dataReceived(self, data):
		self.reader.addData(data)
		try:
			status = self.reader.readByte()
			result = self.reader.readPickle()
			if status == SUCCESS:
				self.finished.callback(result)
			elif status == FAILURE:
				self.finished.errback(result)
			self.reader.commit()
		except ReadException:
			self.reader.revert()

	@property
	def working(self):
		return self.finished is not None
