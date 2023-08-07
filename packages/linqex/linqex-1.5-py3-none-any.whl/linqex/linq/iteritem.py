from linqex._typing import *
from linqex.build.iteritembase import EnumerableItemBase
from linqex.linq.iterlist import EnumerableList

from typing import Dict, List, Callable, Union as _Union, NoReturn, Optional, Tuple, Type, Generic, overload
from collections.abc import Iterable

def EnumerableItemCatch(enumerableItem:"EnumerableItem", iterlist:Optional[List[_TV]], *keyHistoryAdd:_Key, oneValue:bool=False) -> Optional["EnumerableItem[_TV]"]:
    if iterlist is None:
        return None
    else:
        newEnumerableItem = EnumerableItem(iterlist)
        newEnumerableItem._main = enumerableItem._main
        newEnumerableItem._orderby = enumerableItem._orderby
        newEnumerableItem.keyHistory = enumerableItem.keyHistory.copy()
        if keyHistoryAdd != ():
            if isinstance(keyHistoryAdd[0], (list, tuple)) and len(enumerableItem.keyHistory) != 0:
                if isinstance(enumerableItem.keyHistory[-1], (list, tuple)):
                    newEnumerableItem.keyHistory[-1].extend(keyHistoryAdd[0])
                else:
                    newEnumerableItem.keyHistory.extend(keyHistoryAdd)
            else:
                newEnumerableItem.keyHistory.extend(keyHistoryAdd)
        newEnumerableItem._oneValue = oneValue
        return newEnumerableItem

def EnumerableItemToValue(enumerableItemOrValue:_Union["EnumerableItem[_TV]",List[_TV]]) -> List[_TV]:
    if isinstance(enumerableItemOrValue, EnumerableItem):
        return enumerableItemOrValue.ToValue
    else:
        return enumerableItemOrValue

class EnumerableItem(EnumerableList,Iterable[Tuple[int,_TV]],Generic[_TV]):
    
    def __init__(self, iterlist:List[_TV]=None):
        self.iterlist:List[_TV] = EnumerableItemBase(EnumerableItemToValue(iterlist)).iterlist
        self.keyHistory:list = list()
        self._main:EnumerableItem = self
        self._orderby:list = list()
        self._oneValue:bool = False

    def __call__(self, iterlist:List[_TV]=None):
        self.__init__(iterlist)

    def Get(self, *key:int) -> _Union["EnumerableItem[_TV]",_TV]:
        iterlist = EnumerableItemBase(self.iterlist).Get(*key)
        if isinstance(iterlist,list):
            return EnumerableItemCatch(self, iterlist, key)
        else:
            return iterlist
    
    def GetKey(self, value:_TV) -> int:
        return EnumerableItemBase(self.iterlist).GetKey(EnumerableItemToValue(value))
    
    def GetKeys(self) -> "EnumerableItem[int]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).GetKeys())
    
    def GetValues(self) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).GetValues())
    
    def GetItems(self) -> "EnumerableItem[Tuple[int,_TV]]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).GetItems())
    
    def Copy(self) -> "EnumerableItem[_TV]":
        return EnumerableItem(EnumerableItemBase(self.iterlist).Copy())



    def Take(self, count:int) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Take(count))
    
    def TakeLast(self, count:int) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).TakeLast(count))
    
    def Skip(self, count:int) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Skip(count))
    
    def SkipLast(self, count:int) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).SkipLast(count))
    
    def Select(self, selectFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> "EnumerableItem[_TFV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Select(selectFunc))
    
    def Distinct(self, distinctFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Distinct(distinctFunc))
    
    def Except(self, exceptFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, *value:_TV) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Except(exceptFunc, *map(EnumerableItemToValue, value)))

    def Join(self, iterlist: List[_TV2], 
        innerFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[int,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[int,_TV,int,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinType:JoinType=JoinType.INNER
    ) -> "EnumerableItem[_TFV2]":
        return EnumerableItem(EnumerableItemBase(self.iterlist).Join(EnumerableItemToValue(iterlist), innerFunc, outerFunc, joinFunc, joinType))
      
    def OrderBy(self, orderByFunc:Callable[[int,_TV],_Union[Tuple[_TFV],_TFV]], desc:bool=False) -> "EnumerableItem[_TV]":
        self._orderby.clear()
        self._orderby.append((orderByFunc, desc))
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).OrderBy((orderByFunc, desc)))

    def ThenBy(self, orderByFunc:Callable[[int,_TV],_Union[Tuple[_TFV],_TFV]], desc:bool=False) -> "EnumerableItem[_TV]":
        self._orderby.append((orderByFunc, desc))
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).OrderBy(*self._orderby))
        
    def GroupBy(self, groupByFunc:Callable[[int,_TV],_Union[Tuple[_TFV],_TFV]]=lambda key, value: value) -> "EnumerableItem[Tuple[_Union[Tuple[_TFV],_TFV], List[_TV]]]":
        return EnumerableItem(EnumerableItemBase(self.iterlist).GroupBy(groupByFunc))

    def Reverse(self) -> "EnumerableItem[_TV]":
        return EnumerableItemCatch(self,EnumerableItemBase(self.iterlist).Reverse())
        
    def Zip(self, iterlist:List[_TV2], zipFunc:Callable[[int,_TV,int,_TV2],_TFV]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)) -> "EnumerableItem[_TFV]":
        return EnumerableItem(EnumerableItemBase(self.iterlist).Zip(EnumerableItemToValue(iterlist), zipFunc))



    def Where(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> "EnumerableItem[_TV]":
        items = dict(EnumerableItemBase(self.iterlist).Where(conditionFunc))
        return EnumerableItemCatch(self, list(items.values()), list(items.keys()))
    
    def OfType(self, *type:Type) -> "EnumerableItem[_TV]":
        items = dict(EnumerableItemBase(self.iterlist).OfType(*type))
        return EnumerableItemCatch(self, list(items.values()), list(items.keys()))
    
    def First(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional["EnumerableItem[_TV]"]:
        firstValue = EnumerableItemBase(self.iterlist).First(conditionFunc)
        if firstValue is None:
            return None
        else:
            return EnumerableItemCatch(self, [firstValue[1]], firstValue[0], oneValue=True)
    
    def Last(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional["EnumerableItem[_TV]"]:
        lastValue = EnumerableItemBase(self.iterlist).Last(conditionFunc)
        if lastValue is None:
            return None
        else:
            return EnumerableItemCatch(self, [lastValue[1]], lastValue[0], oneValue=True)
        
    def Single(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional["EnumerableItem[_TV]"]:
        singleValue = EnumerableItemBase(self.iterlist).Single(conditionFunc)
        if singleValue is None:
            return None
        else:
            return EnumerableItemCatch(self, [singleValue[1]], singleValue[0], oneValue=True)



    def Any(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> bool:
        return EnumerableItemBase(self.iterlist).Any(conditionFunc)
    
    def All(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> bool:
        return EnumerableItemBase(self.iterlist).All(conditionFunc)
    
    def SequenceEqual(self, iterlist:List[_TV2]) -> bool:
        return EnumerableItemBase(self.iterlist).SequenceEqual(EnumerableItemToValue(iterlist))



    def Accumulate(self, accumulateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> "EnumerableItem[_TFV]":
        return EnumerableItem(EnumerableItemBase(self.iterlist).Accumulate(accumulateFunc))

    def Aggregate(self, aggregateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> _TFV:
        return EnumerableItemBase(self.iterlist).Aggregate(aggregateFunc)



    def Count(self, value:_TV) -> int:
        return EnumerableItemBase(self.iterlist).Count(value)

    @property
    def Lenght(self) -> int:
        return EnumerableItemBase(self.iterlist).Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return EnumerableItemBase(self.iterlist).Sum()
        
    def Avg(self) -> Optional[_TV]:
        return EnumerableItemBase(self.iterlist).Avg()
        
    def Max(self) -> Optional[_TV]:
        return EnumerableItemBase(self.iterlist).Max()
        
    def Min(self) -> Optional[_TV]:
        return EnumerableItemBase(self.iterlist).Min()

    @overload
    def Set(): ...
    @overload
    def Set(self, value:_Value): ...
    def Set(self, value=...):
        super().Set(value)

    def Add(self, key:Optional[int], value:_Value):
        EnumerableItemBase(self.iterlist).Add(key, EnumerableItemToValue(value))

    def Prepend(self, key:Optional[int], value:_Value):
        EnumerableItemBase(self.iterlist).Prepend(key, EnumerableItemToValue(value))

    def Insert(self, key:int, value:_Value):
        EnumerableItemBase(self.iterlist).Insert(key, EnumerableItemToValue(value))

    def Update(self, key:int, value:_Value):
        EnumerableItemBase(self.iterlist).Update(key, EnumerableItemToValue(value))

    def Concat(self, *iterlist:List[_TV2]):
        EnumerableItemBase(self.iterlist).Concat(*map(EnumerableItemToValue, iterlist))

    def Union(self, *iterlist:List[_TV2]):
        EnumerableItemBase(self.iterlist).Union(*map(EnumerableItemToValue, iterlist))

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
            EnumerableItemBase(self.iterlist).Delete(*key)

    def Remove(self, *value:_TV):
        EnumerableItemBase(self.iterlist).Remove(*map(EnumerableItemToValue, value))

    def RemoveAll(self, *value:_TV):
        EnumerableItemBase(self.iterlist).RemoveAll(*map(EnumerableItemToValue, value))

    def Clear(self):
        EnumerableItemBase(self.iterlist).Clear()



    def Loop(self, loopFunc:Callable[[int,_TV],NoReturn]=lambda key, value: print(value)):
        EnumerableItemBase(self.iterlist).Loop(loopFunc)



    @property
    def ToKey(self) -> int:
        return super().ToKey
    @property
    def ToValue(self) -> _Union[List[_TV],_TV]:
        return super().ToValue
    @property
    def ToDict(self) -> Dict[int,_TV]:
        return EnumerableItemBase(self.iterlist).ToDict()
    @property
    def ToList(self) -> List[_TV]:
        return EnumerableItemBase(self.iterlist).ToList()



    @property
    def IsEmpty(self) -> bool:
        return EnumerableItemBase(self.iterlist).IsEmpty()

    def ContainsByKey(self, *key:int) -> bool:
        return EnumerableItemBase(self.iterlist).ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return EnumerableItemBase(self.iterlist).Contains(*map(EnumerableItemToValue, value))



    def __neg__(self) -> "EnumerableItem[_TV]":
        return EnumerableItem(EnumerableItemBase(self.Copy().iterlist).__neg__())
    
    def __add__(self, iterlist:List[_TV]) -> "EnumerableItem[_Union[_TV,_TV2]]":
        return EnumerableItem(EnumerableItemBase(self.Copy().iterlist).__add__(EnumerableItemToValue(iterlist)))
    
    def __iadd__(self, iterlist:List[_TV]):
        EnumerableItemBase(self.iterlist).__iadd__(EnumerableItemToValue(iterlist))
    
    def __sub__(self, iterlist:List[_TV]) -> "EnumerableItem[_Union[_TV,_TV2]]":
        return EnumerableItem(EnumerableItemBase(self.Copy().iterlist).__sub__(EnumerableItemToValue(iterlist)))
    
    def __isub__(self, iterlist:List[_TV]):
        EnumerableItemBase(self.iterlist).__isub__(EnumerableItemToValue(iterlist))

    

    def __eq__(self, iterlist:List[_TV]) -> bool:
        return EnumerableItemBase(self.iterlist).__eq__(EnumerableItemToValue(iterlist))

    def __ne__(self, iterlist:List[_TV]) -> bool:
        return EnumerableItemBase(self.iterlist).__ne__(EnumerableItemToValue(iterlist))
    
    def __contains__(self, value:_Value) -> bool:
        return EnumerableItemBase(self.iterlist).__contains__(EnumerableItemToValue(value))



    def __bool__(self) -> bool:
        return EnumerableItemBase(self.iterlist).__bool__()
    
    def __len__(self) -> int:
        return EnumerableItemBase(self.iterlist).__len__()



    def __iter__(self) -> Iterable[Tuple[int,_TV]]:
        return EnumerableItemBase(self.GetItems().ToValue).__iter__()
    
    def __getitem__(self, key:int) -> _TV:
        return EnumerableItemBase(self.iterlist).__getitem__(key)
    
    def __setitem__(self, key:int, value:_Value):
        return EnumerableItemBase(self.iterlist).__setitem__(key, EnumerableItemToValue(value))

    def __delitem__(self, key:int):
        return EnumerableItemBase(self.iterlist).__delitem__(key)



    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> "EnumerableItem[int]":
        return EnumerableItem(EnumerableItemBase.Range(start, stop, step).Get())
    @staticmethod
    def Repeat(value:_Value, count:int) -> "EnumerableItem[int]":
        return EnumerableItem(EnumerableItemBase.Repeat(value, count).Get())



__all__ = ["EnumerableItem"]
