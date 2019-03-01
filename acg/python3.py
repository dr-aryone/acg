import io


class PythonWriter:
    def __init__(self, outfile: io.TextIOBase, tab='\t'):
        self._outfile = outfile
        self.tab = tab
        self.indent = 0

    @property
    def tabs(self):
        return self.tab * self.indent

    def write_statement_colon(self, statement: BaseNode):
        self._outfile.write(self.tabs)
        statement.write(self)
        self._outfile.write(':\n')

    def write_token_condition_colon(self, token: str, condition: BaseNode):
        self._outfile.write(self.tabs)
        self._outfile.write()

    def write(self, string):
        self._outfile.write(string)


class BaseNode:
    def write_into(self, writer: PythonWriter):
        pass


_IF = 'if'
_ELIF = 'elif'


class String(BaseNode):
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'String({!r})'.format(self.string)

    def write_into(self, writer: PythonWriter):
        writer.write(self.string)


class If(BaseNode):
    def __init__(self,
                 if_cond: BaseNode,
                 if_block: BaseNode,
                 elif_cond_blocks,
                 else_block):
        self.if_cond = if_cond
        self.if_block = if_block
        self.elif_cond_blocks = elif_cond_blocks
        self.else_block = else_block

    def write_into(self, outfile, options: PythonOptions):
        pass
