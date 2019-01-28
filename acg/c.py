from .core import BaseNode
import re
import string
import typing
import io

_nondigit = '_' + string.ascii_letters
_digit = string.digits
_nonzero_digit = string.digits[1:]
_hexadecimal_digit = string.digits + string.ascii_lowercase[:6] + \
                     string.ascii_uppercase[:6]
_octal_digit = string.digits[:8]

_identifier_pattern = re.compile(
    '[{}][{}]*'.format(_nondigit, _digit + _nondigit))


class Identifier(BaseNode):
    def __init__(self, name):
        if _identifier_pattern.fullmatch(name):
            raise ValueError('invalid identifier: {}'.format(name))
        self.name = name

    @staticmethod
    def is_valid(name):
        return bool(_identifier_pattern.fullmatch(name))

    def read(self, infile: io.BufferedReader, options):
        

    def write(self, outfile: io.BufferedWriter, options):
        outfile.write(self.name)


Constant = typing.NewType('Constant', BaseNode)

_decimal_constant_pattern = re.compile(
    '[{}][{}]*'.format(_nonzero_digit, _digit))

_octal_constant_pattern = re.compile('0[{}]'.format(_octal_digit))


class IntegerConstant(Constant):
    pass
