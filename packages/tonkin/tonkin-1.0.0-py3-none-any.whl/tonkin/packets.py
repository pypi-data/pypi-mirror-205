import tonkin.datvar
import tonkin.values
from typing import List, Dict, Union

def _splitPacket(rawPacket: bytearray, vars: List[tonkin.datvar.Datvar]) -> List[bytearray]:
	splitPacket = []
	for var in vars:
		splitPacket.append(bytearray(rawPacket[:var.getLength()]))
		rawPacket = rawPacket[var.getLength():]
	return splitPacket

def readRawPacket(rawPacket: bytearray, vars: List[tonkin.datvar.Datvar]) -> Dict[str, Union[int, float, bool]]:
	vals = _splitPacket(rawPacket, vars)
	packet = {}
	for index, var in enumerate(vars):
		varName = var.name
		value = tonkin.values.readRawValue(vals[index], var.dataType)
		packet[varName] = value
	return packet

def readPackets(packets: List[bytearray], vars: List[tonkin.datvar.Datvar]) -> List[Dict[str, Union[int, float, bool]]]:
	output = []
	for packet in packets:
		output.append(readRawPacket(packet, vars))
	return output
