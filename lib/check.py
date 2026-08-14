import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser, ParseError


def check_file(filepath):
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        return {"file": filepath, "ok": False, "error": f"File not found: {filepath}"}
    if not filepath.endswith(".dipjo"):
        return {"file": filepath, "ok": False, "error": f"Not a .dipjo file: {filepath}"}
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            source = f.read()
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()
        return {"file": filepath, "ok": True}
    except ParseError as e:
        return {"file": filepath, "ok": False, "error": str(e)}
    except Exception as e:
        return {"file": filepath, "ok": False, "error": str(e)}


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python check.py <file.dipjo> [...]", file=sys.stderr)
        sys.exit(1)
    had_error = False
    for f in args:
        result = check_file(f)
        if result["ok"]:
            print(f"OK: {result['file']}")
        else:
            print(f"ERROR: {result['file']}", file=sys.stderr)
            print(f"  {result['error']}", file=sys.stderr)
            had_error = True
    sys.exit(1 if had_error else 0)
