import io
from typing import *

_IF = 'if'
_ELIF = 'elif'
_ELSE = 'else'
_WHILE = 'while'
_COLON = ':'
_SEMICOLON = ';'


class PythonWriter:
    def __init__(self, outfile: io.TextIOBase, tab='    ',
                 have_semicolon=False):
        self._outfile = outfile
        self.tab = tab
        self.indent = 0
        self.have_semicolon = have_semicolon

    @property
    def tabs(self):
        return self.tab * self.indent

    @property
    def semicolon(self):
        return _SEMICOLON if self.have_semicolon else ''

    def write(self, string):
        self._outfile.write(string)

    def write_token_colon(self, statement: str):
        self._outfile.write('{}{}:\n'.format(self.tabs, statement))

    def write_token_condition_colon(self, token: str, condition):
        self._outfile.write(self.tabs + token + ' ')
        condition.write_into(self)
        self._outfile.write(':\n')

    def write_indent_block(self, block):
        self.indent += 1
        for statement in block:
            statement.write_into(self)
        self.indent -= 1

    def write_statement(self, statement: str):
        self._outfile.write(self.tabs + statement + self.semicolon)


class BaseNode:
    def write_into(self, writer: PythonWriter):
        pass


class String(BaseNode):
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'String({!r})'.format(self.string)

    def write_into(self, writer: PythonWriter):
        writer.write(self.string)


class Statement(BaseNode):
    def __init__(self, statement: str):
        self._statement = statement

    def __str__(self):
        return self._statement

    def __repr__(self):
        return 'Statement({})'.format(self._statement)

    def write_into(self, writer: PythonWriter):
        writer.write_statement(self._statement)


class SmallStatement(Statement):
    pass


Block = NewType('Block', Iterable[Statement])


class Indent(BaseNode):
    def write_into(self, writer: PythonWriter):
        writer.indent += 1


class Dedent(BaseNode):
    def write_into(self, writer: PythonWriter):
        writer.indent -= 1


class CompoundStatement(Statement):
    pass


class If(BaseNode):
    def __init__(self,
                 if_test: BaseNode,
                 if_block: Block,
                 elif_test_blocks: Iterable[Tuple[BaseNode, Block]] = (),
                 else_block: Optional[Block] = None):
        self.if_test = if_test
        self.if_block = if_block
        self.elif_test_blocks = elif_test_blocks
        self.else_block = else_block

    def write_into(self, writer: PythonWriter):
        writer.write_token_condition_colon(_IF, self.if_test)
        writer.write_indent_block(self.if_block)

        for cond, block in self.elif_test_blocks:
            writer.write_token_condition_colon(_ELIF, cond)
            writer.write_indent_block(block)

        if self.else_block:
            writer.write_token_colon(_ELSE)
            writer.write_indent_block(self.else_block)


class For(BaseNode):
    def __init__(self, exprlist, testlist, block, else_block):
        self.exprlist = exprlist
        self.testlist = testlist
        self.block = block
        self.else_block = else_block
