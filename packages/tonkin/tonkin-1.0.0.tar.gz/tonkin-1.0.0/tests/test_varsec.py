import countach.parse
from tonkin import datvar, varsec, datfile

# Set up the test datvars in the right order with the extra "time" one at the end
def getTestDatVars():
	tv = countach.parse.parseFile("tests/testdata/test_0.a2l")
	datvars = []
	singleval = tv[8]
	int32val = tv[9]
	uint16val = tv[10]
	int16val = tv[11]
	fixedval = tv[12]
	uint8val = tv[13]
	int8val = tv[14]
	boolval = tv[15]

	testVariables = [uint8val, uint16val, singleval, int8val, int32val, int16val, fixedval, boolval]

	for i in testVariables:
		datvars.append(datvar.Datvar(i.name, i.dataType))
	datvars.append(datvar.Datvar("time", "single"))
	return datvars

testVariables = getTestDatVars()

def test_getVariableListFromA2L():
	global testVariables
	a2ldata = countach.parse.parseFile("tests/testdata/test_0.a2l")
	_, variableSection, _ = datfile.getSectionsFromFile("tests/testdata/multitype.dat")
	realVars = varsec.getVariableListFromA2L(variableSection, a2ldata)
	assert realVars == testVariables
