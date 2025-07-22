from dataclasses import dataclass
from typing import Dict


class Block:

    def __init__(self, start: int, size: int):
        self.start: int = start
        self.size: int = size
        self.end: int = start + size

    def contains(self, point: int):
        return point >= self.start and point <= self.end 


    def intersects(self, other: "Block"):
        return not (self.end < other.start or other.end < self.start)
    

class Allocator:

    _instance: "Allocator"

    def __init__(self):
        if Allocator._instance:
            raise Exception("An instance of Allocator has already been initialized.")
        Allocator._instance = self
        self._addressed: Dict[int, Block] = {}
        return

    @staticmethod
    def get_instance():
        return Allocator._instance

    def assign(self, size: int, start: int = None, auto=True):
        if auto:
            starts = list(self._addressed.keys())
            starts.sort()
            free_start = starts[len(starts) - 1] + 1
            safe_block = Block(free_start, size)
            self._addressed[free_start] = safe_block
            return safe_block
        
        if not start: raise Exception(f"Error in Assign(): If a start parameter must be provided if auto=False.")

        b1 = Block(start, size)
        is_free = True
        if start in self._addressed:
            raise Exception(
                f"Error in Assign(): Row: {start} has already be allocated to."
            )
        for block in self._addressed.values():
            if block.intersects(b1):
                is_free = False
        if is_free:
            self._addressed[b1.start] = b1
            return b1
        raise Exception(f"Error in Assign(): Row: {start} has already be allocated to. To safely alloc, use auto=Free.")

    def free_block(self, block: Block):
        if block.start not in self._addressed: raise Exception(f"Error in free_block(): Address '{block.start}' is not addressed.")
        # do terminal line removal in renderer not here
        block = self._addressed[block.start]
        del self._addressed[block.start]
        return block

    def get_block(self, start: int):
        return self._addressed.get(start)
    
    def get_contains(self, point: int):
        for block in self._addressed.values():
            if block.contains(point): return True, block


def alloc(size: int, start=None, auto=True) -> Block:
    return Allocator.get_instance().assign(size, start, auto)

def free(block: Block):
    return Allocator.get_instance().free_block(block)