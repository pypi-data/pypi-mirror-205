import tonkin.listops
import tonkin.datvar
from typing import List

def _calculatePacketLength(vars: List[tonkin.datvar.Datvar]) -> int:
	length = 0
	for var in vars:
		length += var.getLength()
	return length

def splitStreamToPackets(stream: bytearray, vars: List[tonkin.datvar.Datvar]):
	packetLength = _calculatePacketLength(vars)
	return tonkin.listops.splitListIntoLengths(list(stream), packetLength)
