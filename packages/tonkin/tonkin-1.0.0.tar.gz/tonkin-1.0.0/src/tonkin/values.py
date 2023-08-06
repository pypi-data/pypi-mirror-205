import struct
from typing import Union

def convertint8(int8B: bytearray) -> int:
	return int.from_bytes(int8B, "little", signed=True)

def convertint16(int16B: bytearray) -> int:
	return int.from_bytes(int16B, "little", signed=True)

def convertint32(int32B: bytearray) -> int:
	return int.from_bytes(int32B, "little", signed=True)

def convertuint8(uint8B: bytearray) -> int:
	return int.from_bytes(uint8B, "little", signed=False)

def convertuint16(uint16B: bytearray) -> int:
	return int.from_bytes(uint16B, "little", signed=False)

def convertSingle(singleB: bytearray) -> float:
	return float(struct.unpack("f", singleB)[0])

def convertBoolean(boolB: bytearray) -> bool:
	if boolB == b'\x01':
		return True
	else:
		return False

# Given a series of bytes representing a value within a packet
# and a variable dict, return the value of the 
def readRawValue(rawValue: bytearray, varType: str) -> Union[int, float, bool]:
	if varType == "int8":
		return convertint8(rawValue)
	elif varType == "int16":
		return convertint16(rawValue)
	elif varType == "int32":
		return convertint32(rawValue)
	elif varType == "uint8":
		return convertuint8(rawValue)
	elif varType == "uint16":
		return convertuint16(rawValue)
	elif varType == "single":
		return convertSingle(rawValue)
	elif varType == "boolean":
		return convertBoolean(rawValue)
	elif "fix" in varType:
		raise NotImplementedError("Fixed-point decoding not supported yet")
	else:
		raise ValueError("No valid type found in varType")
