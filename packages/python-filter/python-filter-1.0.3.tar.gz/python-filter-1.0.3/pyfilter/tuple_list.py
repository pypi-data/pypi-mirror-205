from pydantic import validate_arguments
from typing import Optional

class FromTupleList:
    @validate_arguments
    def __init__(self, list_: list[tuple]) -> None:
        self.__list = list_

    def get_with_value(self, value) -> Optional[tuple]:
        for x in self.__list:
            if value in x:
                return x

__all__ = [ "FromTupleList" ]