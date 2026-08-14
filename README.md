# Dipjo

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.0-00f5d4?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-00f5d4?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Node.js-14+-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
</p>

<h2 align="center">A human-readable programming language with English-like syntax.</h2>

<p align="center">
  Dipjo uses natural English keywords instead of cryptic symbols.<br>
  Write code that reads like instructions. Build real applications.
</p>

---

## What is Dipjo?

Dipjo is a programming language designed to be **intuitive and easy to read**. Instead of `def`, `print`, `for`, `if`, Dipjo uses English words like `define`, `say`, `repeat`, `if`.

```dipjo
note Hello World in Dipjo.

say "Hello, World!".

define function greet using person.
    say "Hello, ", person, "!".
finish function.

run function greet using "Dipjo".
```

### Why Dipjo?

- **Readable** — Code reads like English instructions
- **Simple** — Minimal syntax, easy to learn
- **Real** — Built-in database, HTTP server, file I/O, JSON
- **Fast to write** — Less boilerplate, more logic

---

## Installation

### Prerequisites

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** — [Download Node.js](https://nodejs.org/)

### Install from npm (Recommended)

```bash
npm install -g dipjo
```

### Install from Source

```bash
git clone https://github.com/dipeshdarks/dipjo.git
cd dipjo
npm install -g .
```

### Verify Installation

```bash
dipjo --version
```

Output: `0.1.0`

---

## Quick Start

### 1. Create a Dipjo File

Create `hello.dipjo`:

```dipjo
say "Hello, World!".
```

### 2. Run It

```bash
dipjo hello.dipjo
```

Output: `Hello, World!`

### 3. Interactive REPL

```bash
dipjo repl
```

Type Dipjo code directly and see results instantly.

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `dipjo new <name>` | Create a new Dipjo project |
| `dipjo init` | Initialize dipjo.json in current directory |
| `dipjo run <file.dipjo>` | Run a Dipjo source file |
| `dipjo repl` | Start an interactive REPL |
| `dipjo build` | Build and validate project files |
| `dipjo test` | Run Dipjo tests |
| `dipjo check <file>` | Check syntax without running |
| `dipjo format [file\|dir]` | Format Dipjo code |
| `dipjo lint [file\|dir]` | Lint Dipjo code |
| `dipjo add <package>` | Add a dependency |
| `dipjo remove <package>` | Remove a dependency |
| `dipjo install` | Install dependencies |
| `dipjo update` | Update dependencies |
| `dipjo list` | List dependencies |
| `dipjo clean` | Remove generated files (dist/, build/, cache/) |
| `dipjo docs` | Generate documentation |
| `dipjo serve` | Start HTTP server |
| `dipjo doctor` | Diagnose installation |
| `dipjo version` | Show version number |
| `dipjo help` | Show help message |

### CLI Usage Examples

```bash
# Create a new project
dipjo new my-app
cd my-app

# Initialize a project
dipjo init

# Run a file
dipjo run src/main.dipjo
dipjo hello.dipjo

# Start REPL
dipjo repl

# Check syntax
dipjo check src/main.dipjo

# Format code
dipjo format src/

# Lint code
dipjo lint src/

# Build and validate
dipjo build

# Run tests
dipjo test

# Manage dependencies
dipjo add mypackage
dipjo remove mypackage
dipjo list

# Clean generated files
dipjo clean

# Generate documentation
dipjo docs

# Diagnose installation
dipjo doctor
```

---

## Language Syntax

### Variables

```dipjo
note Create variables with a type.
create number age as 25.
create text name as "Dipjo".
create truth is_cool as true.

note Shorthand creation (type inferred as number).
remember counter as 0.
remember message as "Hello".

note Reassign variables.
set age to 26.
age = 30.

note Direct assignment.
name = "Updated".
```

### Output

```dipjo
say "Hello, World!".
say "Hello", name.
say "Age is", age.
```

### Input

```dipjo
ask "Enter your name" and save in name.
say "Hello, ", name.

note Or use input() directly.
remember user_input as input().
remember prompted as input("Enter value").
```

### Conditionals

```dipjo
note Basic if.
if age is greater than 18,
    say "Adult".
finish condition.

note If-otherwise.
if age is greater than 18,
    say "Adult".
otherwise,
    say "Minor".
finish condition.
```

### Comparisons

| Operator | Syntax |
|----------|--------|
| Equal to | `a is equal to b` |
| Not equal to | `a is not equal to b` |
| Greater than | `a is greater than b` |
| Less than | `a is less than b` |
| Greater or equal | `a is greater than or equal to b` |
| Less or equal | `a is less than or equal to b` |

### Logical Operators

```dipjo
if age is greater than 18 and age is less than 65,
    say "Working age".
finish condition.

if age is less than 18 or age is greater than 65,
    say "Not working age".
finish condition.

if not is_cool,
    say "Dipjo is cool".
finish condition.
```

### Loops

```dipjo
note Repeat N times.
repeat 5 times,
    say "Hello".
finish repeat.

note Repeat with range.
repeat from 1 to 10,
    say number.
finish repeat.

note While loop.
remember counter as 0.
while counter is less than 10,
    say counter.
    increase counter by 1.
finish while.

note For-each loop.
create list fruits as "Apple", "Banana", "Orange".
for every fruit in fruits,
    say fruit.
finish loop.
```

### Functions

```dipjo
note Define a function.
define function greet using person.
    say "Hello, ", person.
finish function.

note Call a function.
run function greet using "World".

note Function with return value.
define function add using a, b.
    give back a plus b.
finish function.

remember sum as run function add using 3, 4.
say "Sum is", sum.
```

### Lists

```dipjo
create list colors as "red", "green", "blue".
put "yellow" into colors.
remove "red" from colors.

note Access by index.
say colors[0].
```

### Dictionaries

```dipjo
remember user as {"name": "Dipesh", "age": 21}.
say user.name.
say user.age.

note Update dictionary.
set user.name to "Dipesh Darks".
```

### Method Calls

```dipjo
note Database methods.
remember users as database("users").
users.create({"name": "Dipesh"}).
remember all as users.find().
users.update({"id": 1}, {"name": "New Name"}).
users.delete({"id": 1}).

note Built-in methods on objects.
```

### Arithmetic

| Operator | Syntax |
|----------|--------|
| Add | `a plus b` |
| Subtract | `a minus b` |
| Multiply | `a times b` |
| Divide | `a divided by b` |

```dipjo
note Arithmetic shorthand.
increase counter by 1.
decrease counter by 1.
add 5 to total.
subtract 3 from total.
multiply x by 2.
divide x by 4.
```

### Comments

```dipjo
note This is a comment. Everything after 'note' until the period is ignored.
```

### Imports

```dipjo
import "helpers.dipjo".
import "modules/utils.dipjo".
```

---

## Built-in Functions

### Core

| Function | Syntax | Description |
|----------|--------|-------------|
| `database()` | `database("name")` | Create a SQLite database collection |
| `now()` | `now()` | Get current timestamp (`YYYY-MM-DD HH:MM:SS`) |
| `len()` | `len(value)` | Get length of a string or list |
| `str()` | `str(value)` | Convert value to string |
| `num()` | `num(value)` | Convert string to number (int or float) |
| `input()` | `input("prompt")` | Read user input from stdin |
| `env()` | `env("VAR_NAME")` | Get environment variable |

```dipjo
remember ts as now().
remember length as len("hello").
remember text as str(42).
remember number as num("3.14").
remember cwd as env("DIPJO_CWD").
```

### HTTP Server

| Function | Syntax | Description |
|----------|--------|-------------|
| `http_server()` | `http_server(port)` | Create an HTTP server on the given port |

```dipjo
remember server as http_server(3000).

note Register route handlers (function names as strings).
server.get("/", "handle_home").
server.post("/api/data", "handle_post").
server.delete("/api/data/:id", "handle_delete").

note Set static file directory.
server.set_static("/path/to/public").

note Start the server (blocks).
server.start().
```

**Route parameters** use `:param` syntax:

```dipjo
server.get("/users/:id", "handle_user").
```

Access params in the handler:

```dipjo
define function handle_user.
    remember params as request("params").
    remember user_id as params.id.
    give back {"status": 200, "body": {"id": user_id}}.
finish function.
```

### Request

| Function | Syntax | Description |
|----------|--------|-------------|
| `request()` | `request()` | Get the full request object |
| `request()` | `request("method")` | Get HTTP method |
| `request()` | `request("path")` | Get request path |
| `request()` | `request("body")` | Get request body (string) |
| `request()` | `request("params")` | Get route parameters (dict) |
| `request()` | `request("query")` | Get query string parameters |
| `request()` | `request("headers")` | Get request headers |

### JSON

| Function | Syntax | Description |
|----------|--------|-------------|
| `json_stringify()` | `json_stringify(obj)` | Convert object to JSON string |
| `json_parse()` | `json_parse(string)` | Parse JSON string to object |

```dipjo
remember data as {"name": "Dipesh", "age": 21}.
remember json as json_stringify(data).
say json.

remember parsed as json_parse(json).
say parsed.name.
```

### File I/O

| Function | Syntax | Description |
|----------|--------|-------------|
| `file_read()` | `file_read("path")` | Read entire file as string |
| `file_write()` | `file_write("path", content)` | Write string to file |
| `file_exists()` | `file_exists("path")` | Check if file exists |

```dipjo
remember content as file_read("data.txt").
file_write("output.txt", "Hello, World!").
if file_exists("config.txt"),
    remember config as file_read("config.txt").
finish condition.
```

### Random

| Function | Syntax | Description |
|----------|--------|-------------|
| `random_code()` | `random_code(length)` | Generate random alphanumeric string |
| `random_code()` | `random_code(length, charset)` | Generate with custom character set |

```dipjo
remember code as random_code(6).
remember custom as random_code(8, "abcdef0123456789").
```

### String Operations

| Function | Syntax | Description |
|----------|--------|-------------|
| `string_split()` | `string_split(str, delimiter)` | Split string into list |
| `string_contains()` | `string_contains(str, substring)` | Check if substring exists |
| `string_starts_with()` | `string_starts_with(str, prefix)` | Check if string starts with prefix |
| `string_trim()` | `string_trim(str)` | Remove leading/trailing whitespace |

```dipjo
remember parts as string_split("a,b,c", ",").
remember has as string_contains("hello world", "world").
remember starts as string_starts_with("https://example.com", "https://").
remember clean as string_trim("  hello  ").
```

### CLI Arguments

| Function | Syntax | Description |
|----------|--------|-------------|
| `args_get()` | `args_get(index)` | Get CLI argument by index |
| `args_len()` | `args_len()` | Get number of CLI arguments |

```dipjo
note Run with: dipjo app.dipjo 8080

remember port as args_get(0).
if port is not equal to null,
    set port to num(port).
otherwise,
    set port to 3000.
finish condition.
```

---

## Database (SQLite)

Dipjo has a built-in SQLite database. Data persists between runs.

### Create a Collection

```dipjo
remember users as database("users").
```

### Create Records

```dipjo
remember user as users.create({"name": "Dipesh", "email": "dipesh@example.com", "age": 21}).
say user.id.
```

### Find Records

```dipjo
note Find all records.
remember all as users.find().

note Find by field.
remember results as users.find({"email": "dipesh@example.com"}).

note Find with multiple conditions.
remember results as users.find({"name": "Dipesh", "age": 21}).
```

### Update Records

```dipjo
users.update({"id": 1}, {"name": "Dipesh Darks", "age": 22}).
```

First argument is the filter, second is the changes.

### Delete Records

```dipjo
users.delete({"id": 1}).
```

### Count Records

```dipjo
remember count as users.count().
```

### Check Existence

```dipjo
remember exists as users.exists({"email": "dipesh@example.com"}).
```

### Clear All Records

```dipjo
users.clear().
```

### Database Location

Data is stored in `.dipjo/data/dipjo.db` relative to the script's directory.

---

## HTTP Server

Build web applications and APIs with Dipjo.

### Basic Server

```dipjo
remember server as http_server(3000).

define function handle_home.
    give back {"status": 200, "body": {"message": "Hello!"}}.
finish function.

server.get("/", "handle_home").
server.start().
```

### API with JSON

```dipjo
remember server as http_server(3000).

define function handle_create.
    remember body as request("body").
    remember data as json_parse(body).
    remember record as users.create(data).
    give back {"status": 201, "body": record}.
finish function.

server.post("/api/users", "handle_create").
server.start().
```

### Redirects

```dipjo
define function handle_redirect.
    give back {"status": 302, "headers": {"Location": "https://example.com"}, "body": ""}.
finish function.
```

### Static Files

```dipjo
server.set_static("./public").
```

Serves files from the `public` directory. Requests for `/` serve `index.html`.

### Return HTML

```dipjo
define function handle_page.
    remember html as "<!DOCTYPE html><html><body><h1>Hello</h1></body></html>".
    give back {"status": 200, "body": html, "content_type": "text/html"}.
finish function.
```

---

## Examples

### Hello World

```dipjo
say "Hello, World!".
```

Run: `dipjo examples/welcome.dipjo`

### Fibonacci

```dipjo
define function fibonacci using n.
    if n is equal to 0,
        give back 0.
    finish condition.
    if n is equal to 1,
        give back 1.
    finish condition.
    create number a as 0.
    create number b as 1.
    repeat from 2 to n,
        create number temp as a plus b.
        set a to b.
        set b to temp.
    finish repeat.
    give back b.
finish function.

repeat from 0 to 10,
    say "Fibonacci(", number, ") = ", run function fibonacci using number.
finish repeat.
```

Run: `dipjo examples/fibonacci.dipjo`

### CRUD App

A complete contact manager with database operations:

```dipjo
contacts = database("contacts").
remember record as contacts.create({"name": "Dipesh", "email": "dipesh@example.com"}).
remember all as contacts.find().
```

Run: `dipjo examples/crud-app/app.dipjo`

### URL Shortener

A full URL shortening service with HTTP server, database, and web interface:

```dipjo
remember server as http_server(3000).
remember urls as database("urls").

define function handle_shorten.
    remember body as request("body").
    remember data as json_parse(body).
    remember code as random_code(6).
    remember record as urls.create({"code": code, "url": data.url, "clicks": 0}).
    give back {"status": 201, "body": {"code": code, "short_url": "http://localhost:3000/" plus code}}.
finish function.

server.post("/api/shorten", "handle_shorten").
server.start().
```

Run: `dipjo examples/url-shortener/app.dipjo`

---

## VS Code Extension

### Installation

Install the Dipjo VS Code extension for syntax highlighting and the Jellyfish color theme.

```bash
code --install-extension dipjo-0.1.0.vsix
```

Or from VS Code:
1. Open Extensions (`Ctrl+Shift+X`)
2. Search for "Dipjo"
3. Install

### Select Theme

`Ctrl+K Ctrl+T` → select **Dipjo Jellyfish**

### Features

- Syntax highlighting for `.dipjo` files
- Jellyfish color theme (deep ocean + bioluminescent)
- Bracket matching
- Comment toggling (`note`)
- Auto-closing pairs

### Theme Colors

| Element | Color | Hex |
|---------|-------|-----|
| Background | Deep Ocean | `#07111F` |
| Keywords | Jellyfish Purple | `#A855F7` |
| Functions | Bioluminescent Cyan | `#22D3EE` |
| Function Names | Jellyfish Blue | `#38BDF8` |
| Strings | Seafoam | `#5EEAD4` |
| Numbers | Soft Purple | `#C084FC` |
| Booleans | Pink Glow | `#F472B6` |
| Comments | Muted Blue-Gray | `#64748B` |
| Variables | Warm White | `#F8FAFC` |
| Operators | Cyan | `#67E8F9` |
| Database Methods | Jellyfish Pink | `#F0ABFC` |

---

## Project Structure

```
dipjo/
├── bin/
│   └── dipjo.js              # Node.js CLI wrapper
├── lib/
│   ├── main.py               # Python entry point
│   ├── interpreter.py         # Interpreter (built-in functions)
│   ├── parser.py              # Recursive descent parser
│   ├── lexer.py               # Tokenizer
│   ├── ast_nodes.py           # AST node definitions
│   ├── database.py            # SQLite database abstraction
│   ├── http_server.py         # HTTP server
│   └── repl.py                # Interactive REPL
├── syntaxes/
│   └── dipjo.tmLanguage.json  # TextMate grammar
├── themes/
│   └── dipjo-jellyfish-color-theme.json
├── examples/
│   ├── welcome.dipjo
│   ├── fibonacci.dipjo
│   ├── test_all.dipjo
│   ├── password.dipjo
│   ├── guessing_game.dipjo
│   ├── crud-app/
│   └── url-shortener/
├── tests/
│   └── cli.test.js
├── package.json
├── language-configuration.json
└── README.md
```

---

## All Keywords Reference

### Variable Keywords
| Keyword | Usage |
|---------|-------|
| `create` | `create number name as 0.` |
| `remember` | `remember name as value.` |
| `set` | `set name to value.` |

### Type Keywords
| Keyword | Usage |
|---------|-------|
| `number` | `create number x as 42.` |
| `text` | `create text x as "hello".` |
| `truth` | `create truth x as true.` |
| `list` | `create list x as "a", "b".` |

### Control Flow Keywords
| Keyword | Usage |
|---------|-------|
| `if` | `if condition,` |
| `otherwise` | `otherwise,` |
| `finish condition` | `finish condition.` |
| `while` | `while condition,` |
| `finish while` | `finish while.` |
| `repeat` | `repeat 5 times,` / `repeat from 1 to 10,` |
| `finish repeat` | `finish repeat.` |
| `for` | `for every item in list,` |
| `finish loop` | `finish loop.` |

### Function Keywords
| Keyword | Usage |
|---------|-------|
| `define` | `define function name using param.` |
| `function` | (part of `define function`) |
| `using` | (part of `define function ... using`) |
| `finish function` | `finish function.` |
| `run` | `run function name using arg.` |
| `give back` | `give back value.` |

### I/O Keywords
| Keyword | Usage |
|---------|-------|
| `say` | `say "Hello".` |
| `ask` | `ask "Name?" and save in name.` |

### List Keywords
| Keyword | Usage |
|---------|-------|
| `put` | `put "item" into list.` |
| `remove` | `remove "item" from list.` |

### Arithmetic Keywords
| Keyword | Usage |
|---------|-------|
| `plus` | `a plus b` |
| `minus` | `a minus b` |
| `times` | `a times b` |
| `divided by` | `a divided by b` |
| `increase` | `increase x by 1.` |
| `decrease` | `decrease x by 1.` |
| `add` | `add 5 to x.` |
| `subtract` | `subtract 3 from x.` |
| `multiply` | `multiply x by 2.` |
| `divide` | `divide x by 4.` |

### Comparison Keywords
| Keyword | Usage |
|---------|-------|
| `is` | (comparison operator) |
| `equal to` | `a is equal to b` |
| `not equal to` | `a is not equal to b` |
| `greater than` | `a is greater than b` |
| `less than` | `a is less than b` |
| `or` | (in `greater than or equal to`) |

### Logical Keywords
| Keyword | Usage |
|---------|-------|
| `and` | `a is greater than 0 and a is less than 10` |
| `or` | `a is equal to 1 or a is equal to 2` |
| `not` | `if not condition,` |

### Other Keywords
| Keyword | Usage |
|---------|-------|
| `note` | `note This is a comment.` |
| `import` | `import "file.dipjo".` |
| `true` | `create truth x as true.` |
| `false` | `create truth x as false.` |
| `and save in` | (part of `ask` statement) |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with care for the Dipjo community.<br>
  <sub>If you find Dipjo useful, please give it a star on GitHub!</sub>
</p>
