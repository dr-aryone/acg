
_IF = 'if'
_ELIF = 'elif'
_ELSE = 'else'

_WHILE = 'while'
_FOR = 'for'

_PASS = 'pass'
_RAISE = 'raise'
_BREAK = 'break'
_CONTINUE = 'continue'

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
    def format(self, env):
        raise NotImplementedError('format method')

class String(PythonNode):
    def __init__(self, string):
        self.string = string

    def format(self, env):
        return self.string

class PythonBlock:
    def write(self, outfile, env):
        raise NotImplementedError('write method')

class Statement(PythonBlock):
    def __init__(self, statement):
        self.statement = statement

    def write(self, outfile, env):
        outfile.write(
            '{}{}\n'.format(env.tabs, self.statement.format(env))
        )

class Indent(PythonBlock):
    def write(self, outfile, env):
        env.indent += 1

class Dedent(PythonBlock):
    def write(self, outfile, env):
        env.indent -= 1

class Pass(PythonBlock):
    def write(self, outfile, env):
        outfile.write('{}{}\n'.format(env.tabs, _PASS))

class Break(PythonBlock):
    def write(self, outfile, env):
        outfile.write('{}{}\n'.format(env.tabs, _BREAK))

class Continue(PythonBlock):
    def write(self, outfile, env):
        outfile.write('{}{}\n'.format(env.tabs, _CONTINUE))

class Raise(PythonBlock):
    def __init__(self, exc):
        self.exc = exc

    def write(self, outfile, env):
        outfile.write(
            '{}{} {}'.format(env.tabs, _RAISE, self.exc.format(env))
        )

class Block(PythonBlock):
    def __init__(self, *statements):
        self.statements = list(statements) or [Pass()]

    def write(self, outfile, env):
        for statement in self.statements:
            statement.write(outfile, env)

class If(PythonBlock):
    def __init__(self,
            if_test,
            if_block,
            *elifs_else,
            ):

        self.if_test = if_test
        self.if_block = if_block
        self.elifs_else = elifs_else

    def write(self, outfile, env):
        # if test
        outfile.write(
            '{}{} {}{}\n'.format(
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

        # elif test block
        for i in range(0, (len(self.elifs_else) // 2) * 2, 2):
            # elif test
            outfile.write(
                '{}{} {}{}\n'.format(
                    env.tabs,
                    _ELIF,
                    self.elifs_else[i].format(env),
                    _COLON,
                )
            )
            # elif block
            env.indent += 1
            self.elifs_else[i + 1].write(outfile, env)
            env.indent -= 1

        # else block
        if len(self.elifs_else) % 2:
            # else
            outfile.write(
                '{}{}{}\n'.format(
                    env.tabs,
                    _ELSE,
                    _COLON,
                )
            )
            # else block
            env.indent += 1
            self.elifs_else[-1].write(outfile, env)
            env.indent -= 1
