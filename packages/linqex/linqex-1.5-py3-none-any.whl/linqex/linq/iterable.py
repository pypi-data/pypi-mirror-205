from linqex._typing import *
from linqex.linq.iterdict import EnumerableDict
from linqex.linq.iterlist import EnumerableList
from linqex.linq.iteritem import EnumerableItem

from typing import Dict, List, Union, Generic


class Enumerable(Generic[_TK,_TV]):
    def __new__(cls, iterable:Union[List[_TV],Dict[_TK,_TV]]):
        return cls.Iterable(iterable)
    @classmethod
    def Iterable(cls, iterable:Union[List[_TV],Dict[_TK,_TV]]) -> Union[EnumerableItem[_TV], EnumerableDict[_TK,_TV]]:
        if isinstance(iterable, list):
            return cls.Item(iterable)
        elif isinstance(iterable, dict):
            return cls.Dict(iterable)
        else:
            raise TypeError()

    @classmethod
    def Item(cls, iteritem:List[_TV]=None) -> EnumerableItem[_TV]:
        if iteritem is None:
            iteritem:List[_TV]=list()
        return EnumerableItem(iteritem)

    @classmethod
    def List(cls, iterlist:List[_TV]=None) -> EnumerableList[_TV]:
        if iterlist is None:
            iterlist:List[_TV]=list()
        return EnumerableList(iterlist)

    @classmethod
    def Dict(cls, iterdict:Dict[_TK,_TV]=None) -> EnumerableDict[_TK,_TV]:
        if iterdict is None:
            iterdict:Dict[_TK,_TV]=dict()
        return EnumerableDict(iterdict)


__all__ = ["Enumerable"]
