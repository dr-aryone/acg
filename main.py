from acg.python import *
import sys


def main():
    env = PythonEnvironment(' ' * 4)
    node = If(
        String("hello"),
        Block(
            Statement("goodbye"),
        ),
        String("Bye"),
            Block(),
    )
    node.write(sys.stdout, env)


if __name__ == '__main__':
    main()
