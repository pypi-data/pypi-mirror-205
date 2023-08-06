import tonkin.listops as lops
import tonkin.datvar as datvar
from typing import List, Union
from countach import measurement as mea
from countach import characteristic as cha

# Split the variables section into individual definitions
def splitVarSectionToDefs(varSection: bytearray) -> List[List[int]]:
	return lops.splitListBySub(list(varSection), [0x43, 0x43, 0x3E])

# Extract a variable name from a definition
def extractVariableName(varDef: List[int]) -> str:
	outputBytes = []
	# Remove data before variable name
	varDef = varDef[66:]

	# Extract name
	for i in varDef:
		if i == 0x00:
			break
		outputBytes.append(chr(i))

	return "".join(outputBytes)

# Get a list of variable names from a list of definitions (ignores the last one)
def extractVariableNames(varDefs: List[List[int]]) -> List[str]:
	# Don't get the "time" variable
	varDefs.pop(-1)
	output = []
	for var in varDefs:
		output.append(extractVariableName(var))
	return output

# Given a variable name and the A2L data, return a datvar object representing the variable
def getDatVarFromA2L(variableName: str, a2lData: List[Union[mea.Measurement, cha.Characteristic]]) -> datvar.Datvar:
	for i in a2lData:
		rightCategory = type(i) == mea.Measurement
		rightName = i.name == variableName
		if rightCategory and rightName:
			return datvar.Datvar(variableName, i.dataType)
	raise ValueError("Variable " + variableName + " not found in A2L data")

def getDatVarsFromA2L(variableNames: List[str], a2lData: List[Union[mea.Measurement, cha.Characteristic]]) -> List[datvar.Datvar]:
	output = []
	for variableName in variableNames:
		output.append(getDatVarFromA2L(variableName, a2lData))
	return output

def getVariableListFromA2L(varSection: bytearray, a2lData: List[Union[mea.Measurement, cha.Characteristic]]) -> List[datvar.Datvar]:
	defs = splitVarSectionToDefs(varSection)
	variableNames = extractVariableNames(defs)
	variableList = getDatVarsFromA2L(variableNames, a2lData)
	variableList.append(datvar.Datvar("time", "single"))
	variableList.reverse()
	return variableList
