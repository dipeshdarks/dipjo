import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, RuntimeError


def run_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter()
        interpreter.run(program)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        run_file(filepath)
    else:
        from repl import run_repl
        run_repl()


if __name__ == "__main__":
    main()
