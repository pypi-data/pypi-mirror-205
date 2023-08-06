from typing import Tuple, Union

def isSigned(typeStr: str) -> bool:
	if typeStr[0] == "u":
		signed = False
	elif typeStr[0] == "s":
		signed = True
	else:
		raise ValueError("Sign indication not found in type string")
	return signed

def getWordLength(typeStr: str) -> int:
	typeStr = typeStr[4:]
	splitTypeStr = typeStr.split("_")
	return int(splitTypeStr[0])

def getTotalSlope(typeStr: str) -> int:
	totalSlope = 1
	if "S" in typeStr:
		totalSlopeIndex = typeStr.index("S") + 1
		totalSlope = int(typeStr[totalSlopeIndex])
	elif "E" in typeStr:
		totalSlopeIndex = typeStr.index("E") + 1
		totalSlope = 2 ** int(typeStr[totalSlopeIndex])
	return totalSlope

def getBias(typeStr: str) -> int:
	bias = 0
	if "B" in typeStr:
		biasIndex = typeStr.index("B") + 1
		bias = int(typeStr[biasIndex])
	return bias

def getPropertiesFromFixedTypeStr(typeStr: str) -> Tuple[bool, int, int, int]:
	signed = isSigned(typeStr)
	wordLength = getWordLength(typeStr)
	totalSlope = getTotalSlope(typeStr)
	bias = getBias(typeStr)
	return signed, wordLength, totalSlope, bias

# Round n up to the nearest multiple
def roundUp(n: Union[int, float, bool], multiple: Union[int, float, bool]) -> Union[int, float, bool]:
	if multiple == 0:
		return n

	remainder = n % multiple

	if remainder == 0:
		return n

	return n + multiple - remainder

def getByteLength(bitLength: int) -> int:
	totalBits = roundUp(bitLength, 8)
	return int(totalBits / 8)

def getByteLengthFromFixedTypeStr(typeStr: str) -> int:
	_, wordLength, _, _ = getPropertiesFromFixedTypeStr(typeStr)
	return getByteLength(wordLength)

# Remove the extra bits from the start of a fixdt value
def chopExtraBits(value: int, wordLength: int, byteLength: int) -> int:
	# The case where the wordLength is a multiple of 8
	if wordLength / 8 == byteLength:
		return value
	
	bitsToChop = (byteLength * 8) - wordLength
	binary = bin(value)
	# Chop an extra 2 chars for "0b"
	chopped = binary[bitsToChop + 2:]
	return int(chopped)
