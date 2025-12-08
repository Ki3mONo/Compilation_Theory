import sys
from scanner import Scanner
from parser import Mparser
import TreePrinter


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()


    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    if ast:
        ast.printTree()
