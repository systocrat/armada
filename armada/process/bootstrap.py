from twisted.internet import stdio
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import react
import sys
from armada.slave import ArmadaSlaveProtocol

@inlineCallbacks
def main(reactor, procIn, procOut):
	workProtocol = ArmadaSlaveProtocol()
	stdio.StandardIO(workProtocol, procIn, procOut)
	yield workProtocol.killed

if __name__ == '__main__':
	react(main, [int(sys.argv[1]), int(sys.argv[2])])