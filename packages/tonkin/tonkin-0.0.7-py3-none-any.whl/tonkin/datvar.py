from dataclasses import dataclass
import tonkin.fixed

# A variable as it appears in the header section
@dataclass
class Datvar:
	name: str
	dataType: str

	def getLength(self) -> int:
		if "fix" in self.dataType:
			return tonkin.fixed.getByteLengthFromFixedTypeStr(self.dataType)
		elif "int8" in self.dataType:
			return 1
		elif "int16" in self.dataType:
			return 2
		elif "int32" in self.dataType:
			return 4
		elif self.dataType == "single":
			return 4
		elif self.dataType == "boolean":
			return 1
		elif self.dataType == "time":
			return 4
		else:
			raise ValueError(f"{self.dataType} is not a valid type string")
