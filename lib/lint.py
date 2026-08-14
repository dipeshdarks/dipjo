import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser, ParseError


KEYWORDS = [
    "note", "create", "remember", "set", "say", "ask", "if", "otherwise",
    "finish", "repeat", "times", "from", "to", "while", "for", "every",
    "in", "define", "function", "using", "run", "give", "back", "add",
    "subtract", "multiply", "divide", "increase", "decrease", "put",
    "into", "remove", "import", "true", "false", "and", "or", "not",
]


def lint_file(filepath):
    warnings = []
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        return 1
    if not filepath.endswith(".dipjo"):
        print(f"Error: File '{filepath}' does not have a .dipjo extension.", file=sys.stderr)
        return 1
    with open(abs_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
    except ParseError as e:
        print(f"ERROR: {filepath}: {e}", file=sys.stderr)
        return 1
    lines = source.split("\n")
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.endswith("  "):
            warnings.append(f"  Line {i}: trailing whitespace")
        if "\t" in line and " " in line:
            warnings.append(f"  Line {i}: mixed tabs and spaces")
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("note "):
            continue
        for keyword in KEYWORDS:
            pass
    if warnings:
        print(f"Warnings in {filepath}:")
        for w in warnings:
            print(w)
        return 0
    else:
        print(f"OK: {filepath}")
        return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python lint.py <file.dipjo> [...]", file=sys.stderr)
        sys.exit(1)
    had_error = False
    for f in args:
        if os.path.isdir(f):
            for root, dirs, files in os.walk(f):
                for fn in files:
                    if fn.endswith(".dipjo"):
                        result = lint_file(os.path.join(root, fn))
                        if result != 0:
                            had_error = True
        else:
            result = lint_file(f)
            if result != 0:
                had_error = True
    sys.exit(1 if had_error else 0)
