from twisted.internet.defer import DeferredSemaphore, DeferredQueue, Deferred, inlineCallbacks, returnValue

from armada.process.master import spawnProcess


class ProcessPool(object):
	def __init__(self, count=10):
		self.limiter = DeferredSemaphore(count)
		self.processes = [spawnProcess() for _ in xrange(count)]
		self.workQueue = DeferredQueue()

		for process in self.processes:
			process.onconnect.addCallback(self._prepareForWork)

	@inlineCallbacks
	def _prepareForWork(self, proto):
		deferred, func, args = yield self.workQueue.get()
		proto.queueWork(deferred, func, *args)
		def requeue(result):
			self._prepareForWork(proto)
			return result
		deferred.addCallback(requeue)
		returnValue(proto)

	def queueWork(self, function, *args):
		resultDeferred = Deferred()
		innerDeferred = Deferred()
		self.workQueue.put((innerDeferred, function, args))
		def callResult(obj):
			resultDeferred.callback(obj)
			return obj
		innerDeferred.addCallback(callResult)
		return resultDeferred

	def stop(self):
		for process in self.processes:
			process.protocol.kill()
			process.transport.loseConnection()
