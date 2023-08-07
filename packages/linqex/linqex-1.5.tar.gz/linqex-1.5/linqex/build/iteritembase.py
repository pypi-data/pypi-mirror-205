from linqex._typing import *
from linqex.build.iterlistbase import EnumerableListBase

from typing import Dict, List, Callable, Union as _Union, NoReturn, Optional, Tuple, Type, Generic
from numbers import Number
from collections.abc import Iterable
import itertools

class EnumerableItemBase(EnumerableListBase,Iterable[Tuple[int,_TV]],Generic[_TV]):
        
    def __init__(self, iterlist:Optional[List[_TV]]=None):
        super().__init__(iterlist)

    def Get(self, *key:int) -> _Union[List[_TV],_TV]:
        return super().Get(*key)
    
    def GetKey(self, value:_TV) -> int:
        return super().GetKey(value)
    
    def GetKeys(self) -> List[int]:
        return super().GetKeys()
    
    def GetValues(self) -> List[_TV]:
        return super().GetValues()
    
    def GetItems(self) -> List[Tuple[int,_TV]]:
        return super().GetItems()
    
    def Copy(self) -> List[_TV]:
        return super().Copy()



    def Take(self, count:int) -> List[_TV]:
        return super().Take(count)
    
    def TakeLast(self, count:int) -> List[_TV]:
        return super().TakeLast(count)
    
    def Skip(self, count:int) -> List[_TV]:
        return super().Skip(count)
    
    def SkipLast(self, count:int) -> List[_TV]:
        return super().SkipLast(count)

    def Select(self, selectFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> List[_TFV]:
        return list(map(selectFunc, self.GetKeys(), self.GetValues()))
    
    def Distinct(self, distinctFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> List[_TV]:
        newIterlist = self.Copy()
        for key, value in self.GetItems():
            if EnumerableItemBase(EnumerableItemBase(newIterlist).Select(distinctFunc)).Count(distinctFunc(key, value)) > 1:
                EnumerableItemBase(newIterlist).Remove(value)
        return newIterlist
    
    def Except(self, exceptFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, *value:_TV) -> List[_TV]:
        newIterlist = EnumerableItemBase()
        for k, v in self.GetItems():
            if not exceptFunc(k, v) in value:
                newIterlist.Add(k, v)
        return newIterlist.Get()

    def Join(self, iterlist: List[_TV2], 
        innerFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[int,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[int,_TV,int,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinType:JoinType=JoinType.INNER
    ) -> List[_TFV2]:
        def innerJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableItemBase[Tuple[_TV,_TV2]]):
            nonlocal outerFunc, innerFunc
            for inKey, inValue in EnumerableItemBase(innerIterlist).GetItems():
                outer = EnumerableItemBase(outerIterlist).Where(lambda outKey, outValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
                if outer != []:
                    for out in outer:
                        newIterlist.Add(-1,(inKey, inValue, out[0], out[1]))
        def leftJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableItemBase[Tuple[_TV,Optional[_TV2]]]):
            nonlocal outerFunc, innerFunc
            for inKey, inValue in EnumerableItemBase(innerIterlist).GetItems():
                outer = EnumerableItemBase(outerIterlist).Where(lambda outKey, outValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
                if outer is None:
                    newIterlist.Add(-1,(inKey, inValue, None, None))
                else:
                    newIterlist.Add((inKey, inValue, outer[0], outer[1]))
        def rightJoin(innerIterlist:List[_TV], outerIterlist:List[_TV2], newIterlist:EnumerableItemBase[Tuple[_TV2,Optional[_TV]]]):
            nonlocal outerFunc, innerFunc
            for outKey, outValue in EnumerableItemBase(outerIterlist).GetItems():
                inner = EnumerableItemBase(innerIterlist).First(lambda inKey, inValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
                if inner is None:
                    newIterlist.Add(-1,(None, None, outKey, outValue))
                else:
                    newIterlist.Add(-1,(inner[0], inner[1], outKey, outValue))
        newIterlist = EnumerableItemBase()
        if joinType == JoinType.INNER:
            joinTypeFunc = innerJoin
        elif joinType == JoinType.LEFT:
            joinTypeFunc = leftJoin
        elif joinType == JoinType.RIGHT:
            joinTypeFunc = rightJoin
        joinTypeFunc(self.Get(), iterlist, newIterlist)
        return newIterlist.Select(lambda key, value: joinFunc(value[0], value[1], value[2], value[3]))         
      
    def OrderBy(self, *orderByFunc:Tuple[Callable[[int,_TV],_Union[Tuple[_TFV],_TFV]],_Desc]) -> List[_TV]:
        if orderByFunc == ():
            orderByFunc = ((lambda key, value: value))
        iterlist = self.GetItems()
        orderByFunc = list(reversed(orderByFunc))
        for func, desc in orderByFunc:
            iterlist = sorted(iterlist, key=lambda v: func(v[0], v[1]), reverse=desc)
        return list(zip(*iterlist))[1]
        
    def GroupBy(self, groupByFunc:Callable[[int,_TV],_Union[Tuple[_TFV],_TFV]]=lambda value: value) -> List[Tuple[_Union[Tuple[_TFV],_TFV], List[_TV]]]:
        iterlist = EnumerableItemBase(self.OrderBy((groupByFunc, False))).GetItems()
        iterlist = itertools.groupby(iterlist, lambda items: groupByFunc(items[0], items[1]))
        return [(keys, list(zip(*list(group)))[1]) for keys, group in iterlist]
    
    def Reverse(self) -> List[_TV]:
        return super().Reverse()
          
    def Zip(self, iterlist:List[_TV2], zipFunc:Callable[[int,_TV,int,_TV2],_TFV]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)) -> List[_TFV]:
        newIterlist = EnumerableItemBase(list(zip(self.GetValues(), EnumerableItemBase(iterlist).GetKeys(), EnumerableItemBase(iterlist).GetValues())))
        return newIterlist.Select(lambda key, value: zipFunc(key, value[0], value[1], value[2]))



    def Where(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> List[Tuple[int,_TV]]:
        result = list()
        for index, value in self.GetItems():
            if conditionFunc(index, value):
                result.append((index, value))
        return result
    
    def OfType(self, *type:Type) -> List[Tuple[int,_TV]]:
        return self.Where(lambda key, value: isinstance(value,type))
    
    def First(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        for index, value in self.GetItems():
            if conditionFunc(index, value):
                return (index,value)
        return None
    
    def Last(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) == 0:
            return None
        else:
            return result[-1]
        
    def Single(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) != 1:
            return None
        else:
            return result[0]



    def Any(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> bool:
        result = False
        for key, value in self.GetItems():
            if conditionFunc(key, value):
                result = True
                break
        return result
    
    def All(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> bool:
        result = True
        for key, value in self.GetItems():
            if not conditionFunc(key, value):
                result = False
                break
        return result
 
    def SequenceEqual(self, iterlist:List[_TV2]) -> bool:
        return super().SequenceEqual(iterlist)



    def Accumulate(self, accumulateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> List[_TFV]:
        firstTemp:bool = True
        def FirstTemp(temp):
            nonlocal firstTemp
            if firstTemp:
                firstTemp = False
                return temp[1]
            else:
                return temp
        if not self.IsEmpty():
            result = [self.GetValues()[0]]
            result.extend(list(itertools.accumulate(self.GetItems(), lambda temp, next: accumulateFunc(FirstTemp(temp), next[0], next[1])))[1:])
            return result
        else:
            return []

    def Aggregate(self, accumulateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> _TFV:
        return self.Accumulate(accumulateFunc)[-1]



    def Count(self, value:_TV) -> int:
        return super().Count(value)
        
    def Lenght(self) -> int:
        return super().Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return super().Sum()
        
    def Avg(self) -> Optional[_TV]:
        return super().Avg()
        
    def Max(self) -> Optional[_TV]:
        return super().Max()
        
    def Min(self) -> Optional[_TV]:
        iterlist = self.GetValues()
        return super().Min()



    def Add(self, key:Optional[int], value:_Value):
        if key is None:
            super().Add(value)
        else:
            self.Insert(key, value)

    def Prepend(self, key:Optional[int], value:_Value):
        if key is None:
            super().Prepend(value)
        else:
            self.Insert(key, value)

    def Insert(self, key:_Key, value:_Value):
        super().Insert(key, value)

    def Update(self, key:_TK, value:_Value):
        super().Update(key, value)

    def Concat(self, *iterlist:List[_Value]):
        super().Concat(*iterlist)

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
        super().Delete(*key)

    def Remove(self, *value:_TV):
        super().Remove(*value)

    def RemoveAll(self, *value:_TV):
        super().RemoveAll(*value)

    def Clear(self):
        super().Clear()



    def Loop(self, loopFunc:Callable[[_TV],NoReturn]=lambda value: print(value)):
        for key, value in self.GetItems():
            loopFunc(key, value)



    def ToDict(self) -> Dict[int,_TV]:
        return super().ToDict()

    def ToList(self) -> List[_TV]:
        return super().ToList()



    def IsEmpty(self) -> bool:
        return super().IsEmpty()

    def ContainsByKey(self, *key:int) -> bool:
        return super().ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return super().Contains(*value)



    def __neg__(self) -> List[_TV]:
        return super().__neg__()
    
    def __add__(self, iterlist:List[_TV2]) -> List[_Union[_TV,_TV2]]:
        return super().__add__(iterlist)
    
    def __iadd__(self, iterlist:List[_TV2]):
        super().__iadd__(iterlist)

    def __sub__(self, iterlist:List[_TV2]) -> List[_Union[_TV,_TV2]]:
        return super().__sub__(iterlist)
    
    def __isub__(self, iterlist:List[_TV2]):
        super().__isub__(iterlist)

    

    def __eq__(self, iterlist:List[_TV2]) -> bool:
        return super().__eq__(iterlist)

    def __ne__(self, iterlist:List[_TV2]) -> bool:
        return super().__eq__(iterlist)
    
    def __contains__(self, value:_Value) -> bool:
        return super().__sub__(value)



    def __bool__(self) -> bool:
        return super().__bool__()
    
    def __len__(self) -> int:
        return super().__len__()



    def __iter__(self) -> Iterable[Tuple[int,_TV]]:
        return iter(self.GetItems())
    
    def __getitem__(self, key:int) -> _TV:
        return self.Get(key)
    
    def __setitem__(self, key:int, value:_Value):
        self.Update(key, value)

    def __delitem__(self, key:int):
        self.Delete(key)

    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> "EnumerableListBase[int]":
        return EnumerableListBase.Range(start, stop, step)
    
    @staticmethod
    def Repeat(value:_Value, count:int) -> "EnumerableListBase[int]":
        return EnumerableListBase.Repeat(value, count)




__all__ = ["EnumerableItemBase"]
