from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_repl():
    print("Dipjo Programming Language v1.0")
    print("Type 'exit' or 'quit' to leave.")
    print()

    interpreter = Interpreter()
    buffer = ""

    while True:
        try:
            if buffer:
                prompt = "  ... > "
            else:
                prompt = "Dipjo > "

            line = input(prompt)

            if line.strip().lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            if not line.strip():
                continue

            buffer += line + "\n"

            if "." not in line and not any(
                line.strip().lower().startswith(kw)
                for kw in ["repeat", "while", "if", "for", "define"]
            ):
                continue

            try:
                lexer = Lexer(buffer)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                program = parser.parse()
                interpreter.run(program)
                buffer = ""
            except Exception as e:
                print(f"Error: {e}")
                buffer = ""

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    run_repl()
