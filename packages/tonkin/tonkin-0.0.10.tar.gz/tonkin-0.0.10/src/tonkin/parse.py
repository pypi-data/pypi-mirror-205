import countach.parse
import tonkin.fileops as fops
import tonkin.verification
import tonkin.datfile
import tonkin.varsec
import tonkin.datastream
import tonkin.packets
import csv
from typing import List, Dict, Tuple, Union

def readDatFileWithA2L(datFile: str, a2lFile: str) -> List[Dict[str, Union[int, float, bool]]]:
	# Extract the data from the file
	a2lData = countach.parse.parseFile(a2lFile)
	fileBytes = fops.importFileAsBytes(datFile)
	headerSection, varSection, streamSection = tonkin.datfile.splitFileBytes(fileBytes)

	# Verify the file
	headerStatus = tonkin.verification.checkHeader(headerSection)
	if headerStatus == False:
		raise ValueError("File is not in valid EcoCAL .dat format")

	# Extract the data
	vars = tonkin.varsec.getVariableListFromA2L(varSection, a2lData)
	rawPackets = tonkin.datastream.splitStreamToPackets(streamSection, vars)
	return tonkin.packets.readPackets(rawPackets, vars)

# Write the data to a CSV file
def datToCSVWithA2L(datFile: str, a2lFile: str, outputFile: str):
	data = readDatFileWithA2L(datFile, a2lFile)
	headers = data[0].keys()
	with open(outputFile, "w") as csvFile:
		writer = csv.DictWriter(csvFile, fieldnames=headers)
		writer.writeheader()
		for row in data:
			writer.writerow(row)

def datTo2DWithA2L(datFile: str, a2lFile: str) -> List[List[Union[int, float, bool]]]:
	data = readDatFileWithA2L(datFile, a2lFile)
	headers = list(data[0].keys())
	output = []
	output.append(headers)
	for i in data:
		row = [i.get(key, "") for key in headers]
		output.append(row)
	return output
