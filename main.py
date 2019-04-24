#!/usr/bin/python3

from acg.python3 import *
import sys

def main():

    node = \
        Block(
            If(
                String('num < 10'),
                Block(
                    Statement('print("hello world")'),
                ),
            ),
            While(
                String('num != 0'),
                Block(
                    Statement('num -= 1'),
                ),
            ),
        )


    env = PythonEnvironment(' ' * 4)

    node.write(sys.stdout, env)

if __name__ == '__main__':
    main()
