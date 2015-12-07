from twisted.internet.defer import inlineCallbacks, Deferred
from twisted.internet.protocol import Protocol

from armada.encoding import Reader, packByte, packPickle
from armada.master import CONTINUE, SUCCESS, FAILURE, KILL


class ArmadaSlaveProtocol(Protocol):
	def __init__(self):
		self.reader = Reader()
		self.killed = Deferred()

	@inlineCallbacks
	def dataReceived(self, data):
		self.reader.addData(data)
		status = self.reader.readByte()
		if status == CONTINUE:
			function = self.reader.readUTF8().split('.')
			package, function = '.'.join(function[:-1]), function[-1]
			module = __import__(package, globals(), locals(), ['*'], -1)
			function = getattr(module, function)
			args = self.reader.readArray(self.reader.readUInt, self.reader.readPickle)
			try:
				result = function(*args)
				if isinstance(result, Deferred):
					result = yield result
				self.transport.write(packByte(SUCCESS) + packPickle(result))
			except Exception as ex:
				self.transport.write(packByte(FAILURE) + packPickle(ex))
		elif status == KILL:
			self.transport.loseConnection()
			self.killed.callback(True)