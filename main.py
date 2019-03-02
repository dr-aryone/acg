from acg.python3 import *
import sys


def main():
    writer = PythonWriter(sys.stdout)
    node = If(
        if_test=String('num < 10'),
        if_block=[
            Statement('num = 10'),
        ]
    )
    node.write_into(writer)


if __name__ == '__main__':
    main()
