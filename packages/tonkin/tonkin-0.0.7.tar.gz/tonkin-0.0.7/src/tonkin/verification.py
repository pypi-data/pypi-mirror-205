def verifyASCII(source: bytearray, result: str, start: int, stop: int) -> bool:
	return source[start:stop].decode("ASCII") == result

# Check if the file uses the MDF format
def checkFormat(header: bytearray) -> bool:
	return verifyASCII(header, "MDF", 0, 3)

# Check if the file uses MDF 3.00
def checkVersion(header: bytearray) -> bool:
	return verifyASCII(header, "3.00", 8, 12)

# Check if the vendor is Ecotrons
def checkVendor(header: bytearray) -> bool:
	return verifyASCII(header, "Ecotrons", 16, 24)

# Check if the file was created by EcoCAL
def checkSoftware(header: bytearray) -> bool:
	return verifyASCII(header, "EcoCAL", 100, 106)

# Check that the second vendor is Ecotrons
def checkSecondVendor(header: bytearray) -> bool:
	return verifyASCII(header, "Ecotrons", 132, 140)

def checkHeader(header: bytearray) -> bool:
	if not checkFormat(header):
		return False
	elif not checkVersion(header):
		return False
	elif not checkVendor(header):
		return False
	elif not checkSoftware(header):
		return False
	elif not checkSecondVendor(header):
		return False
	return True
