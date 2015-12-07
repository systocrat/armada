# Armada
Armada is a parallel processing library designed to be able to be used both locally and across networks. Currently, locally is the only way that it can be run, but network capabilities are planned for the future.

## Usage
There are two ways to use armada, as it currently stands. One is using the deferToProcess function, and another is using a ProcessPool. Example usage of deferToProcess can be seen below:

    def testMethod(one, two, three):
    	return '{0}, {1}, {2}'.format(one, two, three)

    @inlineCallbacks
    def main(reactor):
    	deferreds = DeferredList([deferToProcess(testMethod, i, i + 1, i + 2) for i in xrange(10)])
    	data = yield deferreds
    	print data

    if __name__ == '__main__':
    	react(main, [])

And example usage of using a ProcessPool can be seen here:

    def testMethod(one, two, three):
    	return '{0}, {1}, {2}'.format(one, two, three)

    @inlineCallbacks
    def main(reactor):
    	pool = ProcessPool(10)
    	work = yield DeferredList([pool.queueWork(testMethod, i, i + 1, i + 2) for i in xrange(20)])
    	print work

    if __name__ == '__main__':
    	react(main, [])

## Caveats
You cannot pass lambdas or functions as arguments to processes, nor can you call them from another process. I chose not to support this because the more complex a dynamic function gets, the less easy it is to serialize in such a way that it can go over a socket or to another process through stdin. This is especially true when using functions that use @inlineCallbacks or other decorators.
You are able to call only functions that can be directly imported by the Python interpreter.