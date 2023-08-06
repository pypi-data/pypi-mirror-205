from typing import List, Any, Iterator

def shiftListLeft(input: List[Any], shift: int) -> List[Any]:
	# Bring large numbers down to smaller equivalents
	# and handle negatives for shifts right
	shift = shift % len(input)

	for i in range(0, shift):
		input.append(input.pop(0))
	return input

# Given a source list and a target list, returns the index of where the target
# list appears within the source list (returns the index of the final value)
def getSubListIndex(source: List[Any], target: List[Any]) -> int:
	# TODO: Ensure that the buffer items don't appear in split
	buffer = [None] * len(target)
	
	for j, i in enumerate(source):
		buffer = shiftListLeft(buffer, 1)
		buffer[-1] = i

		if buffer == target:
			return j
	
	raise ValueError("Sub-list not found")

def getSubListIndices(source: List[Any], target: List[Any]) -> List[int]:
	output = []

	# TODO: Ensure that the buffer items don't appear in split
	buffer = [None] * len(target)
	
	for j, i in enumerate(source):
		buffer = shiftListLeft(buffer, 1)
		buffer[-1] = i

		if buffer == target:
			output.append(j)
	
	return output

# TODO: Test for different first elements of source
def splitListBySub(source: List[Any], target: List[Any]) -> List[List[Any]]:
	output = []
	indices = getSubListIndices(source, target)
	
	# The case where the target does not appear
	if indices == []:
		return [source]

	for j, i in enumerate(indices):
		startOfBlock = i - len(target) + 1
		
		if j < len(indices) - 1:
			endOfBlock = indices[j+1] - len(target) + 1
		else:
			endOfBlock = len(source)

		output.append(source[startOfBlock:endOfBlock])

	return output

def splitListIntoLengthsGen(input: List[Any], lengths: int) -> Iterator[List[Any]]:
	for i in range(0, len(input), lengths):
		yield input[i:i + lengths]

def splitListIntoLengths(input: List[Any], lengths: int) -> List[Any]:
	return list(splitListIntoLengthsGen(input, lengths))
