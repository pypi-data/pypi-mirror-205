from linqex._typing import *
from linqex.build.iterlistbase import EnumerableListBase

from typing import Dict, List, Callable, Union as _Union, NoReturn, Optional, Tuple, Type, Generic, overload
from collections.abc import Iterable

def EnumerableListCatch(enumerableList:"EnumerableList", iterlist:Optional[List[_TV]], *keyHistoryAdd:_Key, oneValue:bool=False) -> Optional["EnumerableList[_TV]"]:
    if iterlist is None:
        return None
    else:
        newEnumerableList = EnumerableList(iterlist)
        newEnumerableList._main = enumerableList._main
        newEnumerableList._orderby = enumerableList._orderby
        newEnumerableList.keyHistory = enumerableList.keyHistory.copy()
        if keyHistoryAdd != ():
            if isinstance(keyHistoryAdd[0], (list, tuple)) and len(enumerableList.keyHistory) != 0:
                if isinstance(enumerableList.keyHistory[-1], (list, tuple)):
                    newEnumerableList.keyHistory[-1].extend(keyHistoryAdd[0])
                else:
                    newEnumerableList.keyHistory.extend(keyHistoryAdd)
            else:
                newEnumerableList.keyHistory.extend(keyHistoryAdd)
        newEnumerableList._oneValue = oneValue
        return newEnumerableList

def EnumerableListToValue(enumerableListOrValue:_Union["EnumerableList[_TV2]",_TV]) -> _TV:
    if isinstance(enumerableListOrValue, EnumerableList):
        return enumerableListOrValue.ToValue
    else:
        return enumerableListOrValue

class EnumerableList(Iterable[_TV],Generic[_TV]):
    
    def __init__(self, iterlist:List[_TV]=None):
        self.iterlist:List[_TV] = EnumerableListBase(EnumerableListToValue(iterlist)).Get()
        self.keyHistory:list = list()
        self._main:EnumerableList = self
        self._orderby:list = list()
        self._oneValue:bool = False

    def __call__(self, iterlist:List[_TV]=None):
        self.__init__(iterlist)

    def Get(self, *key:int) -> _Union["EnumerableList[_TV]",_TV]:
        iterlist = EnumerableListBase(self.iterlist).Get(*key)
        if isinstance(iterlist,list):
            return EnumerableListCatch(self, iterlist, key)
        else:
            return iterlist
    
    def GetKey(self, value:_TV) -> int:
        return EnumerableListBase(self.iterlist).GetKey(EnumerableListToValue(value))
    
    def GetKeys(self) -> "EnumerableList[int]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).GetKeys())
    
    def GetValues(self) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).GetValues())
    
    def GetItems(self) -> "EnumerableList[Tuple[int,_TV]]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).GetItems())
    
    def Copy(self) -> "EnumerableList[_TV]":
        return EnumerableList(EnumerableListBase(self.iterlist).Copy())



    def Take(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Take(count))
    
    def TakeLast(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).TakeLast(count))
    
    def Skip(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Skip(count))
    
    def SkipLast(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).SkipLast(count))
    
    def Select(self, selectFunc:Callable[[_TV],_TFV]=lambda value: value) -> "EnumerableList[_TFV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Select(selectFunc))
    
    def Distinct(self, distinctFunc:Callable[[_TV],_TFV]=lambda value: value) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Distinct(distinctFunc))
    
    def Except(self, exceptFunc:Callable[[_TV],_TFV]=lambda value: value, *value:_TV) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Except(exceptFunc, *map(EnumerableListToValue, value)))

    def Join(self, iterlist: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue),
        joinType:JoinType=JoinType.INNER
    ) -> "EnumerableList[_TFV2]":
        return EnumerableList(EnumerableListBase(self.iterlist).Join(EnumerableListToValue(iterlist), innerFunc, outerFunc, joinFunc, joinType))
      
    def OrderBy(self, orderByFunc:Callable[[_TV],_Union[Tuple[_TFV],_TFV]], desc:bool=False) -> "EnumerableList[_TV]":
        self._orderby.clear()
        self._orderby.append((orderByFunc, desc))
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).OrderBy((orderByFunc, desc)))

    def ThenBy(self, orderByFunc:Callable[[_TV],_Union[Tuple[_TFV],_TFV]], desc:bool=False) -> "EnumerableList[_TV]":
        self._orderby.append((orderByFunc, desc))
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).OrderBy(*self._orderby))
        
    def GroupBy(self, groupByFunc:Callable[[_TV],_Union[Tuple[_TFV],_TFV]]=lambda value: value) -> "EnumerableList[Tuple[_Union[Tuple[_TFV],_TFV], List[_TV]]]":
        return EnumerableList(EnumerableListBase(self.iterlist).GroupBy(groupByFunc))

    def Reverse(self) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListBase(self.iterlist).Reverse())
        
    def Zip(self, iterlist:List[_TV2], zipFunc:Callable[[_TV,_TV2],_TFV]=lambda inValue, outValue: (inValue, outValue)) -> "EnumerableList[_TFV]":
        return EnumerableList(EnumerableListBase(self.iterlist).Zip(EnumerableListToValue(iterlist), zipFunc))



    def Where(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> "EnumerableList[_TV]":
        items = dict(EnumerableListBase(self.iterlist).Where(conditionFunc))
        return EnumerableListCatch(self, list(items.values()), list(items.keys()))
    
    def OfType(self, *type:Type) -> "EnumerableList[_TV]":
        items = dict(EnumerableListBase(self.iterlist).OfType(*type))
        return EnumerableListCatch(self, list(items.values()), list(items.keys()))
    
    def First(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        firstValue = EnumerableListBase(self.iterlist).First(conditionFunc)
        if firstValue is None:
            return None
        else:
            return EnumerableListCatch(self, [firstValue[1]], firstValue[0], oneValue=True)
    
    def Last(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        lastValue = EnumerableListBase(self.iterlist).Last(conditionFunc)
        if lastValue is None:
            return None
        else:
            return EnumerableListCatch(self, [lastValue[1]], lastValue[0], oneValue=True)
        
    def Single(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        singleValue = EnumerableListBase(self.iterlist).Single(conditionFunc)
        if singleValue is None:
            return None
        else:
            return EnumerableListCatch(self, [singleValue[1]], singleValue[0], oneValue=True)



    def Any(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> bool:
        return EnumerableListBase(self.iterlist).Any(conditionFunc)
    
    def All(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> bool:
        return EnumerableListBase(self.iterlist).All(conditionFunc)
    
    def SequenceEqual(self, iterlist:List[_TV2]) -> bool:
        return EnumerableListBase(self.iterlist).SequenceEqual(EnumerableListToValue(iterlist))



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> "EnumerableList[_TFV]":
        return EnumerableList(EnumerableListBase(self.iterlist).Accumulate(accumulateFunc))

    def Aggregate(self, aggregateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> _TFV:
        return EnumerableListBase(self.iterlist).Aggregate(aggregateFunc)



    def Count(self, value:_TV) -> int:
        return EnumerableListBase(self.iterlist).Count(value)

    @property
    def Lenght(self) -> int:
        return EnumerableListBase(self.iterlist).Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return EnumerableListBase(self.iterlist).Sum()
        
    def Avg(self) -> Optional[_TV]:
        return EnumerableListBase(self.iterlist).Avg()
        
    def Max(self) -> Optional[_TV]:
        return EnumerableListBase(self.iterlist).Max()
        
    def Min(self) -> Optional[_TV]:
        return EnumerableListBase(self.iterlist).Min()

    @overload
    def Set(): ...
    @overload
    def Set(self, value:_Value): ...
    def Set(self, value=...):
        if value is ...:
            self.Set(self.iterlist)
        else:
            value = EnumerableListToValue(value)
            if len(self.keyHistory) == 0:
                self._main.Clear()
                self._main.Concat(value)
            else:
                keyHistory = list(filter(lambda k: not isinstance(k, list),self.keyHistory[:len(self.keyHistory)-1]))
                if isinstance(self.ToKey, list):
                    key = keyHistory[-1]
                    keyHistory = keyHistory[:len(keyHistory)-1]
                    if isinstance(key, list):
                        return None
                else:
                    key = self.ToKey
                self._main.Get(*keyHistory).Update(key, value)
                self.iterlist = value

    def Add(self, value:_Value):
        EnumerableListBase(self.iterlist).Add(EnumerableListToValue(value))

    def Prepend(self, value:_Value):
        EnumerableListBase(self.iterlist).Prepend(EnumerableListToValue(value))

    def Insert(self, key:int, value:_Value):
        EnumerableListBase(self.iterlist).Insert(key, EnumerableListToValue(value))

    def Update(self, key:int, value:_Value):
        EnumerableListBase(self.iterlist).Update(key, EnumerableListToValue(value))

    def Concat(self, *iterlist:List[_TV2]):
        EnumerableListBase(self.iterlist).Concat(*map(EnumerableListToValue, iterlist))

    def Union(self, *iterlist:List[_TV2]):
        EnumerableListBase(self.iterlist).Union(*map(EnumerableListToValue, iterlist))

    @overload
    def Delete(self): ...
    @overload
    def Delete(self, *key:int): ...
    def Delete(self, *key):
        if key == ():
            if isinstance(self.ToKey, (list,tuple)):
                key = self.ToKey
            else:
                key = [self.ToKey]
            self._main.Get(*filter(lambda k: not isinstance(k, (list,tuple)),self.keyHistory[:len(self.keyHistory)-1])).Delete(*key)
        else:
            EnumerableListBase(self.iterlist).Delete(*key)

    def Remove(self, *value:_TV):
        EnumerableListBase(self.iterlist).Remove(*map(EnumerableListToValue, value))

    def RemoveAll(self, *value:_TV):
        EnumerableListBase(self.iterlist).RemoveAll(*map(EnumerableListToValue, value))

    def Clear(self):
        EnumerableListBase(self.iterlist).Clear()



    def Loop(self, loopFunc:Callable[[_TV],NoReturn]=lambda value: print(value)):
        EnumerableListBase(self.iterlist).Loop(loopFunc)



    @property
    def ToKey(self) -> int:
        if self.keyHistory == []:
            return None
        else:
            return self.keyHistory[-1]
    @property
    def ToValue(self) -> _Union[List[_TV],_TV]:
        if len(self.iterlist) == 1 and self._oneValue:
            return self.GetValues().iterlist[0]
        else:
            return self.ToList
    @property
    def ToDict(self) -> Dict[int,_TV]:
        return EnumerableListBase(self.iterlist).ToDict()
    @property
    def ToList(self) -> List[_TV]:
        return EnumerableListBase(self.iterlist).ToList()



    @property
    def IsEmpty(self) -> bool:
        return EnumerableListBase(self.iterlist).IsEmpty()

    def ContainsByKey(self, *key:int) -> bool:
        return EnumerableListBase(self.iterlist).ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return EnumerableListBase(self.iterlist).Contains(*map(EnumerableListToValue, value))



    def __neg__(self) -> "EnumerableList[_TV]":
        return EnumerableList(EnumerableListBase(self.Copy().iterlist).__neg__())
    
    def __add__(self, iterlist:List[_TV]) -> "EnumerableList[_Union[_TV,_TV2]]":
        return EnumerableList(EnumerableListBase(self.Copy().iterlist).__add__(EnumerableListToValue(iterlist)))
    
    def __iadd__(self, iterlist:List[_TV]):
        EnumerableListBase(self.iterlist).__iadd__(EnumerableListToValue(iterlist))
    
    def __sub__(self, iterlist:List[_TV]) -> "EnumerableList[_Union[_TV,_TV2]]":
        return EnumerableList(EnumerableListBase(self.Copy().iterlist).__sub__(EnumerableListToValue(iterlist)))
    
    def __isub__(self, iterlist:List[_TV]):
        EnumerableListBase(self.iterlist).__isub__(EnumerableListToValue(iterlist))

    

    def __eq__(self, iterlist:List[_TV]) -> bool:
        return EnumerableListBase(self.iterlist).__eq__(EnumerableListToValue(iterlist))

    def __ne__(self, iterlist:List[_TV]) -> bool:
        return EnumerableListBase(self.iterlist).__ne__(EnumerableListToValue(iterlist))
    
    def __contains__(self, value:_Value) -> bool:
        return EnumerableListBase(self.iterlist).__contains__(EnumerableListToValue(value))



    def __bool__(self) -> bool:
        return EnumerableListBase(self.iterlist).__bool__()
    
    def __len__(self) -> int:
        return EnumerableListBase(self.iterlist).__len__()



    def __iter__(self) -> Iterable[Tuple[int,_TV]]:
        return EnumerableListBase(self.GetValues().ToValue).__iter__()
    
    def __getitem__(self, key:int) -> _TV:
        return EnumerableListBase(self.iterlist).__getitem__(key)
    
    def __setitem__(self, key:int, value:_Value):
        return EnumerableListBase(self.iterlist).__setitem__(key, EnumerableListToValue(value))

    def __delitem__(self, key:int):
        return EnumerableListBase(self.iterlist).__delitem__(key)



    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> "EnumerableList[int]":
        return EnumerableList(EnumerableListBase.Range(start, stop, step).Get())
    @staticmethod
    def Repeat(value:_Value, count:int) -> "EnumerableList[int]":
        return EnumerableList(EnumerableListBase.Repeat(value, count).Get())



__all__ = ["EnumerableList"]
