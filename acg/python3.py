
_IF = 'if'
_ELIF = 'elif'
_ELSE = 'else'

_WHILE = 'while'
_FOR = 'for'

_COLON = ':'
_SEMICOLON = ';'

class PythonEnvironment:
    def __init__(self, 
            tab = '\t',
            indent = 0,
            ):
        self.tab = tab
        self.indent = 0

    @property
    def tabs(self):
        return self.tab * self.indent

class PythonNode:
    def write(self, outfile, env):
        raise NotImplementedError('write method')

    def format(self, env):
        raise NotImplementedError('format method')

class PythonBlock:
    def write(self, outfile, env):
        raise NotImplementedError('write method')

class String(PythonNode):
    def __init__(self, string):
        self.string = string

    def write(self, outfile, env):
        outfile.write(self.string)

    def format(self, env):
        return self.string

class Statement(PythonNode):
    def __init__(self, statement):
        self.statement = statement

    def write(self, outfile, env):
        outfile.write(self.format(env))

    def format(self, env):
        '{}{}\n'.format(env.tabs, self.statement)

class Indent(PythonNode):
    def write(self, outfile, env):
        env.indent += 1

class Dedent(PythonNode):
    def write(self, outfile, env):
        env.indent -= 1

class If(PythonNode):
    def __init__(
            self, 
            if_test, 
            if_block, 
            elif_test_blocks = (), 
            else_block = None,
            ):

        self.if_test = if_test
        self.if_block = if_block
        self.elif_test_blocks = elif_test_blocks
        self.else_block = else_block

    def write(self, outfile, env):
        # if test
        outfile.write('{}{} {}{}\n'.format(
            env.tabs, 
            _IF, 
            self.if_test.format(env),
            _COLON,
            )
        )

        # if block
        env.indent += 1
        self.if_block.write(outfile, env)
        env.indent -= 1

        for test, block in self.elif_test_blocks:

            # elif test
            outfile.write('{}{} {}{}\n'.format(
                env.tabs, 
                _ELIF, 
                test.format(env),
                _COLON,
                )
            )

            # elif block
            env.indent += 1
            block.write(outfile, env)
            env.indent -= 1

        # else block
        if self.else_block is not None:
            outfile.write('{}{}\n'.format(
                _ELSE,
                _COLON,
                )
            )

            env.indent += 1
            self.else_block.write(outfile, env)
            env.indent -= 1

class While(PythonNode):
    def __init__(
            self,
            test,
            block,
            else_block = None,
            ):
        self.test = test
        self.block = block
        self.else_block = else_block

    def write(self, outfile, env):

        # test
        outfile.write('{}{} {}{}\n'.format(
            env.tabs, 
            _WHILE, 
            self.test.format(env),
            _COLON,
            )
        )

        # block
        env.indent += 1
        self.else_block.write(outfile, env)
        env.indent -= 1

        # else block
        if self.else_block is not None:
            outfile.write('{}{}\n'.format(
                _ELSE,
                _COLON,
                )
            )

            env.indent += 1
            self.else_block.write(outfile, env)
            env.indent -= 1

