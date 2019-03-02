import io
from typing import *


class CWriter:
    def __init__(self, outfile: io.TextIOBase, tab='\t'):
        self._outfile = outfile
        self.tab = tab


class CNode:
    def write_into(self, writer: CWriter):
        pass


Condition = NewType('Condition', str)

Block = NewType('Block', Iterable[str])

ConditionBlock = NewType('ConditionBlock', Tuple[Condition, Block])


class If(CNode):
    def __init__(self,
                 if_cond: Condition,
                 if_block: Block,
                 elif_cond_blocks: Iterable[ConditionBlock] = (),
                 else_block: Optional[Block] = None):
        self.if_cond = if_cond
        self.if_block = if_block
        self.elif_cond_blocks = elif_cond_blocks
        self.else_block = else_block
