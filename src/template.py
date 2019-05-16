
## lang_name = 'C'

_IF = 'if'
_ELIF = 'elif'
_WHILE = 'while'

## import collections

# --- initials ---

class ${lang_name}Environment:

    ## kwargs = [
    ##  ('tab',         '\t'),
    ##  ('indent',      0),
    ##  ]
    def __init__(
            self,

            #@ for name, value in kwargs:
            ${name} = $${{ repr(value) }},
            #@ end for
            ):

        #@ for name, value in kwargs:
        self.${name} = ${name}
        #@ end for

    def tabs(self):
        return self.tab * self.indent

class ${lang_name}Node:
    def format(self, env):
        raise NotImplementedError('format method')

class ${lang_name}Block:
    def write(self, outfile, env):
        raise NotImplementedError('write method')

# --- contents ---

class String(${lang_name}Node):
    def __init__(self, string):
        self.string = string

    def format(self, env):
        return self.string

