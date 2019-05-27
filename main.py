
from acg import c
import sys

node = \
c.If(
    c.String('a == 10'),
    c.Line('hello and bye;')
)

env = c.Environment()

node.write(sys.stdout, env)