from collections import deque

class DoublelyLinkedList(deque):
    def __init__(self, value=None):
        self.current_index = 0
        if value:
            self.append(value)

    def sanitiseIndex(self):
        self.current_index = max(0, min(self.current_index, len(self)-1))

    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty

    def hasNext(self):
        next_value = (self.current_index + 1)
        is_valid = (next_value < len(self))
        return is_valid

    def hasPrev(self):
        prev_value = (self.current_index - 1)
        is_valid = (prev_value >= 0)
        return is_valid

    def next(self):
        if self.hasNext():
            self.current_index += 1

    def prev(self):
        if self.hasPrev():
            self.current_index -= 1

    def isAtFirst(self):
        is_at_first = (self.current_index == 0)
        return is_at_first

    def isAtEnd(self):
        is_at_end = (self.current_index == len(self)-1)
        return is_at_end

    def toIndex(self, index):
        is_valid = (0 >= index <= len(self)-1)
        if is_valid:
            self.current_index = index
            
    def toBack(self):
        self.current_index = len(self)-1
        self.sanitiseIndex()

    def toFront(self):
        self.current_index = 0

    def addToCurrent(self, new_value):
        self.sanitiseIndex()
        self.insert(self.current_index, new_value)

    def addToFront(self, new_value):
        self.insert(0, new_value)
        self.current_index = 0

    def addToBack(self, new_value):
        self.insert(len(self), new_value)
        self.current_index = len(self)-1

    def addAfterCurrent(self, new_value):
        self.sanitiseIndex()
        self.insert(self.current_index + 1, new_value)
        self.sanitiseIndex()

    def addBeforeCurrent(self, new_value):
        self.sanitiseIndex()
        self.insert(self.current_index - 1, new_value)
        self.sanitiseIndex()

    def removeCurrent(self):
        self.sanitiseIndex()
        del self[self.current_index]
        self.sanitiseIndex()

    def removeAtIndex(self, index: int):
        del self[index]
        self.sanitiseIndex()

    def removeAll(self):
        self.clear()
        self.sanitiseIndex()

    def Append(self, new_value):
        self.append(new_value)
    
    def getItem(self, idx=None):
        is_use_idx = (bool(idx) and (0 >= idx <= len(self)-1))
        if is_use_idx:
            return self[idx]
        else:
            self.sanitiseIndex()
            return self[self.current_index]

    def getItemAtIndex(self, index):
        return self[index]

    def getAtRange(self, from_idx, to_idx):
        return self[from_idx: to_idx]

    def Pop(self):
        item = self.pop()
        self.sanitiseIndex()
        return item
