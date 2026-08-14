import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser


def format_file(filepath):
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    if not filepath.endswith(".dipjo"):
        print(f"Error: File '{filepath}' does not have a .dipjo extension.", file=sys.stderr)
        sys.exit(1)
    with open(abs_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
    except Exception as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    formatted = _format_program(program, source)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(formatted)
    print(f"Formatted: {filepath}")


def _format_program(program, source):
    lines = source.split("\n")
    result = []
    for line in lines:
        stripped = line.rstrip()
        if stripped:
            result.append(stripped)
        else:
            result.append("")
    while result and result[-1] == "":
        result.pop()
    return "\n".join(result) + "\n"


def format_directory(dirpath):
    count = 0
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            if f.endswith(".dipjo"):
                filepath = os.path.join(root, f)
                abs_path = os.path.abspath(filepath)
                with open(abs_path, "r", encoding="utf-8") as fh:
                    source = fh.read()
                try:
                    lexer = Lexer(source)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    parser.parse()
                    lines = source.split("\n")
                    result = []
                    for line in lines:
                        stripped = line.rstrip()
                        if stripped:
                            result.append(stripped)
                        else:
                            result.append("")
                    while result and result[-1] == "":
                        result.pop()
                    formatted = "\n".join(result) + "\n"
                    with open(abs_path, "w", encoding="utf-8") as fh:
                        fh.write(formatted)
                    count += 1
                    print(f"Formatted: {filepath}")
                except Exception as e:
                    print(f"Error formatting {filepath}: {e}", file=sys.stderr)
    return count


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python format.py <file.dipjo|directory>", file=sys.stderr)
        sys.exit(1)
    for target in args:
        if os.path.isdir(target):
            format_directory(target)
        else:
            format_file(target)
