from enum import Enum


class EnumWithEquality(Enum):
    def __eq__(self, other):
        if issubclass(other, Enum):
            return other.__class__ is self.__class__

        if isinstance(other, str):
            return self.value == other

        return False
