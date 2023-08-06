import tonkin.listops as lops
import tonkin.fileops as fops
from typing import Tuple

def extractHeaderSection(fileBytes: bytearray) -> bytearray:
	return fileBytes[0:228]

def extractVariablesSection(fileBytes: bytearray) -> bytearray:
	withoutHeader = fileBytes[228:]
	end = lops.getSubListIndex(list(withoutHeader), [0x43, 0x47, 0x1A])
	return withoutHeader[:end]

def extractDataSection(fileBytes: bytearray) -> bytearray:
	headerLength = len(extractHeaderSection(fileBytes))
	variableLength = len(extractVariablesSection(fileBytes))
	upperLength = headerLength + variableLength
	output = fileBytes[upperLength:]
	# The sequence of bytes that marks the start of the data stream
	startMarker = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	# The index of the first byte of the data stream
	start = lops.getSubListIndex(list(output), list(startMarker)) + 1
	return output[start:]

def splitFileBytes(fileBytes: bytearray) -> Tuple[bytearray, bytearray, bytearray]:
	headerSection = extractHeaderSection(fileBytes)
	variableSection = extractVariablesSection(fileBytes)
	dataSection = extractDataSection(fileBytes)
	return headerSection, variableSection, dataSection

def getSectionsFromFile(fileName: str) -> Tuple[bytearray, bytearray, bytearray]:
	fileBytes = fops.importFileAsBytes(fileName)
	return splitFileBytes(fileBytes)
