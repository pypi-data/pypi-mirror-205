def importFileAsBytes(fileName: str) -> bytearray:
	output = None
	with open(fileName, "rb") as file:
		output = bytearray(file.read())
	return output
