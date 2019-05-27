
# --- constants ---

_IF = 'if'
_ELSE_IF = 'else if'
_LPAR = '('
_RPAR = ')'
_LBRACE = '{'
_RBRACE = '}'

# --- initials ---

class Environment:
    def __init__(self,
            tab = (' ' * 4),
            indent = 0,
            ):
    
        self.tab = tab
        self.indent = indent

class Node:
    def format(self, env):
        raise NotImplementedError('format method')

class BlockNode:
    def write(self, outfile, env):
        raise NotImplementedError('write method')

# --- contents ---

# --- nodes ---

class String(Node):
    def __init__(self, string = ''):
        self.string = string

    def format(self, env):
        return self.string

# --- block nodes ---

class Line(BlockNode):
    def __init__(self, line = ''):
        self.line = line

    def write(self, outfile, env):
        outfile.write(
            '{}{}\n'.format(
                env.tab * env.indent,
                self.line,
            )
        )

class List(BlockNode):
    def __init__(self, *items):
        self.items = items
    
    def write(self, outfile, env):
        if self.items:

            outfile.write(
                '{}{}\n'.format(
                    env.tab * env.indent, _LBRACE
                )
            )

            env.indent += 1
            for item in self.items:
                item.write(outfile, env)
            env.indent -= 1

            outfile.write(
                '{}{}\n'.format(
                    env.tab * env.indent, _RBRACE
                )
            )
        
        else:
            outfile.write(
                '{}{} {}\n'.format(
                    env.tab * env.indent, _LBRACE, _RBRACE
                )
            )

class If(BlockNode):
    def __init__(self,
            cond, 
            block,
            else_block = None
            ):

        self.cond = cond
        self.block = block
        self.else_block = else_block

    def write(self, outfile, env):
        # cond
        outfile.write(
            '{}{} {}{}{}\n'.format(
                env.tab * env.indent,
                _IF, _LPAR, self.cond.format(env), _RPAR
            )
        )

        # block
        self.block.write(outfile, env)

        # else block
        if self.else_block is not None:

            else_block = self.else_block
            while isinstance(else_block, If):

                # cond
                outfile.write(
                    '{}{} {}{}{}\n'.format(
                        env.tab * env.indent,
                        _ELSE_IF, _LPAR, else_block.cond.format(env), _RPAR
                    )
                )

                # block
                else_block.block.write(outfile, env)

                else_block = else_block.else_block
            
            # else
            else_block.write(outfile, env)



