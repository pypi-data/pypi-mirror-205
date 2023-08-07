from linqex._typing import *

from typing import Dict, List, Callable, Union as _Union, NoReturn, Optional, Tuple, Type, Generic
from numbers import Number
from collections.abc import Iterable
import itertools

class EnumerableListBase(Iterable[_TV],Generic[_TV]):
    
    def __init__(self, iterlist:Optional[List[_TV]]=None):
        if iterlist is None:
            iterlist:List[_TV] = list()
        if isinstance(iterlist, list):
            self.iterlist:List[_TV] = iterlist
        elif isinstance(iterlist, (tuple, set)):
            self.iterlist:List[_TV] = list(iterlist)
        else:
            raise TypeError(iterlist)

    def Get(self, *key:int) -> _Union[List[_TV],_TV]:
        iterlist = self.iterlist
        for k in key:
            if  k < len(iterlist):
                iterlist = iterlist[k]
            else:
                raise KeyError()
        return iterlist
    
    def GetKey(self, value:_TV) -> int:
        return self.iterlist.index(value)
    
    def GetKeys(self) -> List[int]:
        return list(range(len(self.Get())))
    
    def GetValues(self) -> List[_TV]:
        return self.Get()
    
    def GetItems(self) -> List[Tuple[int,_TV]]:
        return list(enumerate(self.Get()))
    
    def Copy(self) -> List[_TV]:
        return self.Get().copy()



    def Take(self, count:int) -> List[_TV]:
        return self.Get()[:count]
    
    def TakeLast(self, count:int) -> List[_TV]:
        return self.Skip(self.Lenght()-count)
    
    def Skip(self, count:int) -> List[_TV]:
        return self.Get()[count:]
    
    def SkipLast(self, count:int) -> List[_TV]:
        return self.Take(self.Lenght()-count)
    
    def Select(self, selectFunc:Callable[[_TV],_TFV]=lambda value: value) -> List[_TFV]:
        return list(map(selectFunc,self.Get()))
    
    def Distinct(self, distinctFunc:Callable[[_TV],_TFV]=lambda value: value) -> List[_TV]:
        newIterlist = self.Copy()
        for value in self.Get():
            if EnumerableListBase(EnumerableListBase(newIterlist).Select(distinctFunc)).Count(distinctFunc(value)) > 1:
                EnumerableListBase(newIterlist).Remove(value)
        return newIterlist
    
    def Except(self, exceptFunc:Callable[[_TV],_TFV]=lambda value: value, *value:_TV) -> List[_TV]:
        newIterlist = EnumerableListBase()
        for v in self.Get():
            if not exceptFunc(v) in value:
                newIterlist.Add(v)
        return newIterlist.Get()

    def Join(self, iterlist: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue),
        joinType:JoinType=JoinType.INNER
    ) -> List[_TFV2]:
        def innerJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableListBase[Tuple[_TV,_TV2]]):
            nonlocal outerFunc, innerFunc
            for inValue in innerIterlist:
                outer = EnumerableListBase(outerIterlist).Where(lambda outValue: outerFunc(outValue) == innerFunc(inValue))
                if outer != []:
                    for out in outer:
                        newIterlist.Add((inValue, out[1]))
        def leftJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableListBase[Tuple[_TV,Optional[_TV2]]]):
            nonlocal outerFunc, innerFunc
            for inValue in innerIterlist:
                outer = EnumerableListBase(outerIterlist).First(lambda outValue: outerFunc(outValue) == innerFunc(inValue))
                if outer is None:
                    newIterlist.Add((inValue, None))
                else:
                    newIterlist.Add((inValue, outer[1]))
        def rightJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableListBase[Tuple[_TV2,Optional[_TV]]]):
            nonlocal outerFunc, innerFunc
            for outValue in outerIterlist:
                inner = EnumerableListBase(innerIterlist).First(lambda inValue: outerFunc(outValue) == innerFunc(inValue))
                if inner is None:
                    newIterlist.Add((None, outValue))
                else:
                    newIterlist.Add((inner[1], outValue))
        newIterlist = EnumerableListBase()
        if joinType == JoinType.INNER:
            joinTypeFunc = innerJoin
        elif joinType == JoinType.LEFT:
            joinTypeFunc = leftJoin
        elif joinType == JoinType.RIGHT:
            joinTypeFunc = rightJoin
        joinTypeFunc(self.Get(), iterlist, newIterlist)
        return newIterlist.Select(lambda value: joinFunc(value[0], value[1]))         
      
    def OrderBy(self, *orderByFunc:Tuple[Callable[[_TV],_Union[Tuple[_TFV],_TFV]],_Desc]) -> List[_TV]:
        if orderByFunc == ():
            orderByFunc = ((lambda value: value, False))
        iterlist = self.Get()
        orderByFunc:list = list(reversed(orderByFunc))
        for func, desc in orderByFunc:
            iterlist = sorted(iterlist, key=func, reverse=desc)
        return list(iterlist)
        
    def GroupBy(self, groupByFunc:Callable[[_TV],_Union[Tuple[_TFV],_TFV]]=lambda value: value) -> List[Tuple[_Union[Tuple[_TFV],_TFV], List[_TV]]]:
        iterlist = self.OrderBy((groupByFunc, False))
        iterlist = itertools.groupby(iterlist, groupByFunc)
        return [(keys, list(group)) for keys, group in iterlist]

    def Reverse(self) -> List[_TV]:
        return list(reversed(self.Get()))
        
    def Zip(self, iterlist:List[_TV2], zipFunc:Callable[[_TV,_TV2],_TFV]=lambda inValue, outValue: (inValue, outValue)) -> List[_TFV]:
        newIterlist = EnumerableListBase(list(zip(self.GetValues(), EnumerableListBase(iterlist).GetValues())))
        return newIterlist.Select(lambda value: zipFunc(value[0], value[1]))



    def Where(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> List[Tuple[int,_TV]]:
        result = list()
        for index, value in self.GetItems():
            if conditionFunc(value):
                result.append((index, value))
        return result
    
    def OfType(self, *type:Type) -> List[Tuple[int,_TV]]:
        return self.Where(lambda value: isinstance(value,type))
    
    def First(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        for index, value in self.GetItems():
            if conditionFunc(value):
                return (index,value)
        return None
    
    def Last(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) == 0:
            return None
        else:
            return result[-1]
        
    def Single(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) != 1:
            return None
        else:
            return result[0]



    def Any(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> bool:
        result = False
        for value in self.Get():
            if conditionFunc(value):
                result = True
                break
        return result
    
    def All(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> bool:
        result = True
        for value in self.Get():
            if not conditionFunc(value):
                result = False
                break
        return result
    
    def SequenceEqual(self, iterlist:List[_TV2]) -> bool:
        if self.Lenght() != len(iterlist):
            return False
        for value in self.Get():
            if not value in iterlist:
                return False
        return True



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> List[_TFV]:
        return list(itertools.accumulate(self.Get(), lambda temp, next: accumulateFunc(temp, next)))

    def Aggregate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> _TFV:
        return self.Accumulate(accumulateFunc)[-1]




    def Count(self, value:_TV) -> int:
        return self.Get().count(value)
        
    def Lenght(self) -> int:
        return len(self.Get())
    
    def Sum(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.Get())
        else:
            return None
        
    def Avg(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.Get()) / self.Lenght()
        else:
            return None
        
    def Max(self) -> Optional[_TV]:
        if self.OfType(Number):
            return max(self.Get())
        else:
            return None
        
    def Min(self) -> Optional[_TV]:
        iterlist = self.GetValues()
        if self.OfType(Number):
            return min(iterlist)
        else:
            return None



    def Add(self, value:_Value):
        self.Get().append(value)

    def Prepend(self, value:_Value):
        newIterlist = [value]
        self.Clear()
        self.Concat(newIterlist)

    def Insert(self, key:_Key, value:_Value):
        self.Get().insert(key, value)

    def Update(self, key:_TK, value:_Value):
        self.Get()[key] = value

    def Concat(self, *iterlist:List[_Value]):
        for i in iterlist:
            self.Get().extend(i)

    def Union(self, *iterlist:List[_Value]):
        if not iterlist in [(),[]]:
            iterlist:list = list(iterlist)
            newIterlist = EnumerableListBase()
            filter = dict(self.Where(lambda v: v in iterlist[0]))
            EnumerableListBase(filter).Loop(lambda v: newIterlist.Add(v))
            iterlist.pop(0)
            self.Clear()
            self.Concat(newIterlist.Get())
            self.Union(*iterlist)

    def Delete(self, *key:_TK):
        i = 0
        for k in sorted(key):
            k -= i
            self.Get().pop(k)
            i += 1

    def Remove(self, *value:_TV):
        for v in value:
            self.Get().remove(v)

    def RemoveAll(self, *value:_TV):
        for v in value:
            while True:
                if self.Contains(v):
                    self.Remove(v)
                else:
                    break

    def Clear(self):
        self.Get().clear()



    def Loop(self, loopFunc:Callable[[_TV],NoReturn]=lambda value: print(value)):
        for value in self.Get():
            loopFunc(value)



    def ToDict(self) -> Dict[int,_TV]:
        return dict(self.GetItems())

    def ToList(self) -> List[_TV]:
        return self.Get()



    def IsEmpty(self) -> bool:
        return self.Get() in [[],{},None]

    def ContainsByKey(self, *key:int) -> bool:
        iterlist = self.GetKeys()
        for k in key:
            if not k in iterlist:
                return False
        return True

    def Contains(self, *value:_TV) -> bool:
        iterlist = self.GetValues()
        for v in value:
            if not v in iterlist:
                return False
        return True



    def __neg__(self) -> List[_TV]:
        newIterlist = EnumerableListBase(self.Copy())
        newIterlist.Reverse()
        return newIterlist.Get()
    
    def __add__(self, iterlist:List[_TV2]) -> List[_Union[_TV,_TV2]]:
        newIterlist = EnumerableListBase(self.Copy())
        newIterlist.Concat(iterlist)
        return newIterlist.Get()
    
    def __iadd__(self, iterlist:List[_TV2]):
        self.Concat(iterlist)
    
    def __sub__(self, iterlist:List[_TV2]) -> List[_Union[_TV,_TV2]]:
        newIterlist = EnumerableListBase(self.Copy())
        newIterlist.Union(iterlist)
        return newIterlist.Get()
    
    def __isub__(self, iterlist:List[_TV2]):
        self.Union(iterlist)

    

    def __eq__(self, iterlist:List[_TV2]) -> bool:
        return self.SequenceEqual(iterlist)

    def __ne__(self, iterlist:List[_TV2]) -> bool:
        return not self.SequenceEqual(iterlist)
    
    def __contains__(self, value:_Value) -> bool:
        return self.Contains(value)



    def __bool__(self) -> bool:
        return not self.IsEmpty()
    
    def __len__(self) -> int:
        return self.Lenght()



    def __iter__(self) -> Iterable[_TV]:
        return iter(self.GetValues())
    
    def __getitem__(self, key:int) -> _TV:
        return self.Get(key)
    
    def __setitem__(self, key:int, value:_Value):
        self.Update(key, value)

    def __delitem__(self, key:int):
        self.Delete(key)

    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> "EnumerableListBase[int]":
        return EnumerableListBase(list(range(start,stop,step))) 
    @staticmethod
    def Repeat(value:_Value, count:int) -> "EnumerableListBase[int]":
        return EnumerableListBase(list(itertools.repeat(value, count)))



__all__ = ["EnumerableListBase"]
