from .core import BaseNode
import typing


class FileInput(BaseNode):
    def __init__(self, statements: typing.Iterable[Statement]):
        self.statements = statements

    def write(self, outfile: typing.TextIO):
        pass


Statement = typing.NewType('Statement', BaseNode)

SmallStatement = typing.NewType('SmallStatement', Statement)


class Expr(SmallStatement):
    pass


CompoundStatement = typing.NewType('CompoundStatement', Statement)
