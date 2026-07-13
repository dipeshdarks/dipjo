<p align="center">
  <img src="https://img.shields.io/badge/VS%20Code-1.85+-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white" alt="VS Code">
  <img src="https://img.shields.io/badge/TypeScript-5.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/LSP-9.0-007ACC?style=for-the-badge" alt="LSP">
  <img src="https://img.shields.io/badge/Version-1.0.0-00f5d4?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-00f5d4?style=for-the-badge" alt="License">
</p>

<h1 align="center"> Dipjo Language — VS Code Extension </h1>

<p align="center">
  Complete language support for the <strong>Dipjo</strong> programming language in Visual Studio Code.<br>
  Syntax highlighting, IntelliSense, debugging, themes, and more.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#commands">Commands</a> •
  <a href="#themes">Themes</a> •
  <a href="#snippets">Snippets</a> •
  <a href="#settings">Settings</a> •
  <a href="#language-server">Language Server</a> •
  <a href="#debugging">Debugging</a> •
  <a href="#development">Development</a> •
  <a href="#changelog">Changelog</a> •
  <a href="#license">License</a>
</p>

---

## What is Dipjo?

Dipjo is a **human-readable programming language** designed to be intuitive and easy to learn. Instead of cryptic syntax, Dipjo uses English-like keywords:

```dipjo
note Hello World in Dipjo.

function greet using name.
    print "Hello, ", name, "!".
    return 0.
end.

run function greet using "World".
```

This extension brings a **modern IDE experience** to Dipjo development.

---

## Features

### Syntax Highlighting

Full TextMate grammar with **92 keywords** organized into semantic categories:

| Category | Tokens | Example Colors |
|----------|--------|----------------|
| **Keywords** | `if`, `else`, `repeat`, `while`, `for`, `function`, `class`, `return`, `try`, `catch` | Purple, Bold |
| **Declarations** | `create`, `set`, `remember`, `define`, `import`, `module` | Blue, Bold |
| **Types** | `number`, `text`, `boolean`, `list`, `dictionary` | Red |
| **Built-in Functions** | `print`, `input`, `length`, `sqrt`, `random`, `time`, `date` | Teal, Bold |
| **Operators** | `is`, `equal`, `greater`, `less`, `and`, `or`, `not`, `+`, `-`, `*`, `/` | Yellow / Purple |
| **Strings** | `"Hello, World!"` | Teal |
| **Numbers** | `42`, `3.14` | Yellow |
| **Booleans** | `true`, `false` | Red Bold / Teal Bold |
| **Null** | `null` | Pink Bold |
| **Comments** | `note This is a comment` | Gray, Italic |
| **Function Names** | `greet`, `add_numbers` | Blue Bold |
| **Class Names** | `Person`, `Database` | Yellow Bold |
| **Variables** | `age`, `name`, `counter` | Light |
| **Decorators** | `@deprecated` | Pink |
| **Constants** | `MAX_SIZE`, `PI` | Yellow Bold |

### IntelliSense

Auto-completion triggered on `.` and ` ` (space):

```
┌──────────────────────────────────────────────────────┐
│  create  ●  keyword.declaration.dipjo                │
│  number  ●  support.type.dipjo                       │
│  print   ●  support.function.builtin.dipjo           │
│  greet   ●  function (user-defined)                  │
│  Person  ●  class (user-defined)                     │
│  age     ●  variable (user-defined)                  │
└──────────────────────────────────────────────────────┘
```

**Completion sources:**
- All 80+ language keywords
- 28 built-in functions
- 5 type keywords
- User-defined functions (parsed from document)
- User-defined classes (parsed from document)
- User-defined variables (parsed from document)

### Hover Information

Hover over any keyword for instant documentation:

```
┌─────────────────────────────────────────┐
│  function                               │
│                                         │
│  Defines a reusable function            │
│                                         │
│  Syntax:                                │
│  function <name> using <params>.        │
│      <body>                             │
│  end.                                   │
│                                         │
│  Example:                               │
│  function greet using name.             │
│      print "Hello, ", name.             │
│  end.                                   │
└─────────────────────────────────────────┘
```

**60+ keywords documented** with description, syntax, and examples.

### Diagnostics (Real-time Error Detection)

| Diagnostic | Severity | Description |
|-----------|----------|-------------|
| Unclosed string literal | Error | Missing closing `"` |
| Missing period | Warning | Statement doesn't end with `.` |
| Missing `end` keyword | Error | Unbalanced block (if/function/loop) |
| Unknown keyword | Warning | Typo detection with suggestions |
| Undefined variable | Info | Variable used before declaration |

### Code Actions (Quick Fixes)

| Action | Trigger | Result |
|--------|---------|--------|
| Add missing period | `Missing period` warning | Appends `.` |
| Close string | `Unclosed string` error | Adds `"` |
| Change to "..." | Unknown keyword | Suggests similar keywords |
| Create variable | Undefined variable | Adds `create number x as 0.` |
| Wrap in print | Selected code | `print <code>.` |
| Wrap in if | Selected code | `if true, <code>\nend.` |
| Extract to function | Selected code | Creates function + call |

### Code Formatting

Automatic indentation based on block structure:

```dipjo
note Before formatting:              note After formatting:
                                     
if age is greater than 18,           if age is greater than 18,
print "Adult".                           print "Adult".
otherwise,                           otherwise,
print "Minor".                           print "Minor".
end.                                 end.
```

**Configurable:** `dipjo.indentSize` (default: 4 spaces)

### Go to Definition

`Ctrl+Click` or `F12` on any function/variable to jump to its declaration.

### Find References

`Shift+F12` to find all references to a function/variable across the file.

### Rename Symbol

`F2` to rename a function/variable across the entire file.

### Document Symbols (Outline)

```
Explorer Panel → Outline
├── greet          (function)  line 3
├── Person         (class)     line 8
├── age            (variable)  line 1
└── name           (variable)  line 5
```

### Semantic Highlighting

10 token types for meaning-based coloring (works alongside TextMate grammar):

1. `keyword` — Language keywords
2. `type` — Type names
3. `string` — String literals
4. `number` — Numeric literals
5. `comment` — Comments
6. `function` — Function names
7. `variable` — Variable names
8. `operator` — Operators
9. `decorator` — Decorators
10. `class` — Class names

---

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/dipjo-lang/dipjo-vscode.git
cd dipjo-vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Open in VS Code
code .

# Press F5 to launch Extension Development Host
```

### From VSIX Package

```bash
# Package the extension
npm install
npm run compile
npx vsce package

# Install the .vsix file
code --install-extension dipjo-lang-1.0.0.vsix
```

### Manual Installation

```bash
# Copy to VS Code extensions directory
# Windows:
cp -r dipjo-vscode/ "$USERPROFILE/.vscode/extensions/dipjo-lang-1.0.0/"

# macOS:
cp -r dipjo-vscode/ ~/.vscode/extensions/dipjo-lang-1.0.0/

# Linux:
cp -r dipjo-vscode/ ~/.vscode/extensions/dipjo-lang-1.0.0/
```

---

## Quick Start

### 1. Create a Dipjo File

Create a file named `hello.dipjo`:

```dipjo
note Hello World program.

print "Hello, World!".

function greet using name.
    print "Hello, ", name, "!".
    return 0.
end.

run function greet using "Dipjo".
```

### 2. Select Theme

`Ctrl+K Ctrl+T` → select **Dipjo JellyFish**

### 3. Run

Press `Ctrl+F5` or click the **▶** button in the title bar.

---

## Commands

Open the Command Palette (`Ctrl+Shift+P`) and type `Dipjo`:

| Command | Keybinding | Description |
|---------|-----------|-------------|
| `Dipjo: Run File` | `Ctrl+F5` | Run the current `.dipjo` file |
| `Dipjo: Run Selection` | `Ctrl+Shift+F5` | Run selected code |
| `Dipjo: Open REPL` | `Ctrl+Shift+R` | Open interactive REPL |
| `Dipjo: Create Project` | — | Generate project scaffold |
| `Dipjo: Format Document` | `Shift+Alt+F` | Auto-format with indentation |
| `Dipjo: Compile` | — | Run file (interpreted) |
| `Dipjo: Show Welcome` | — | Open welcome page |
| `Dipjo: Run Tests` | — | Run tests from `tests/` directory |
| `Dipjo: Create Module` | — | Create `modules/xxx.dipjo` |
| `Dipjo: Generate Documentation` | — | Extract docs from comments |

---

## Themes

### Dipjo Dark

Catppuccin Mocha-inspired dark theme.

| Element | Color |
|---------|-------|
| Background | `#1e1e2e` |
| Foreground | `#cdd6f4` |
| Keywords | `#cba6f7` (Purple) |
| Strings | `#a6e3a1` (Green) |
| Numbers | `#fab387` (Peach) |
| Functions | `#89b4fa` (Blue) |
| Types | `#f38ba8` (Red) |
| Comments | `#6c7086` (Gray) |

### Dipjo Light

Clean Catppuccin Latte-inspired light theme.

| Element | Color |
|---------|-------|
| Background | `#ffffff` |
| Foreground | `#4c4f69` |
| Keywords | `#8839ef` (Purple) |
| Strings | `#40a02b` (Green) |
| Numbers | `#fe640b` (Orange) |
| Functions | `#1e66f5` (Blue) |
| Types | `#d20f39` (Red) |
| Comments | `#9ca0b0` (Gray) |

### Dipjo High Contrast

WCAG-accessible high contrast theme for accessibility.

| Element | Color |
|---------|-------|
| Background | `#000000` |
| Foreground | `#ffffff` |
| Keywords | `#ff88ff` (Bright Purple) |
| Strings | `#00ff00` (Bright Green) |
| Numbers | `#ffaa00` (Bright Orange) |
| Functions | `#8888ff` (Bright Blue) |
| Types | `#ff6666` (Bright Red) |

### Dipjo JellyFish

Deep ocean dark theme with bioluminescent accents.

| Element | Color |
|---------|-------|
| Background | `#0a0a2e` |
| Foreground | `#e0e0ff` |
| Keywords | `#9b5de5` (Purple) |
| Strings | `#00f5d4` (Teal) |
| Numbers | `#ffbe0b` (Yellow) |
| Functions | `#00bbf9` (Blue) |
| Types | `#ff6b6b` (Red) |
| Comments | `#5a5a8e` (Gray) |
| Cursor | `#00f5d4` (Teal) |

---

## Snippets

Type the prefix and press `Tab`:

| Prefix | Description | Expands To |
|--------|-------------|------------|
| `create` | Variable declaration | `create number name as 0.` |
| `set` | Variable assignment | `set name to value.` |
| `remember` | Shorthand declaration | `remember name as value.` |
| `print` | Print statement | `print "Hello, World!".` |
| `printm` | Print multiple | `print "Hello", name.` |
| `input` | User input | `remember name as input.` |
| `if` | If statement | Full if block |
| `ifelse` | If-else statement | Full if-else block |
| `while` | While loop | Full while loop |
| `repeat` | Repeat N times | `repeat 10 times,` |
| `repeatfrom` | Repeat range | `repeat from 0 to 10,` |
| `foreach` | For each loop | `for every item in list,` |
| `function` | Function definition | Full function block |
| `functionnp` | Function (no params) | `function name.` |
| `return` | Return statement | `return value.` |
| `class` | Class definition | Full class block |
| `list` | Create list | `create list name as "a", "b".` |
| `append` | Append to list | `append "item" to list.` |
| `removelist` | Remove from list | `remove "item" from list.` |
| `try` | Try-catch block | Full try-catch |
| `note` | Comment | `note comment.` |
| `import` | Import module | `import module.` |
| `main` | Main program | Full program template |
| `helloworld` | Hello World | Minimal program |
| `switch` | Switch-like | if-elseif-else chain |

---

## Language Server

The extension includes a full **Language Server Protocol (LSP)** implementation:

### Capabilities

| Capability | Status | Description |
|-----------|--------|-------------|
| Text Sync | Full | Syncs on every change |
| Completion | 100+ items | Keywords, builtins, user-defined |
| Hover | 60+ docs | Description, syntax, example |
| Diagnostics | Real-time | Errors and warnings |
| Semantic Tokens | 10 types | Meaning-based highlighting |
| Document Symbols | Outline | Functions, classes, variables |
| Definition | Jump | Go to declaration |
| References | Find | All usages in file |
| Rename | Workspace | Rename across file |
| Formatting | Auto | Indentation alignment |

### Architecture

```
VS Code                    Language Server
┌──────────┐               ┌──────────────┐
│ Editor   │◄─── IPC ───► │ server.ts    │
│          │               │              │
│ Client   │               │ - Parser     │
│          │               │ - Validator  │
│ Providers│               │ - Analyzer   │
└──────────┘               └──────────────┘
```

---

## Debugging

### Setup

1. Open a `.dipjo` file
2. Press `F5` or go to Run → Start Debugging
3. Select "Debug Dipjo File"

### Features

| Feature | Support |
|---------|---------|
| Launch | Program path, args, cwd |
| Breakpoints | Via debug adapter |
| Step Over | Execute next line |
| Step Into | Enter function |
| Continue | Run to next breakpoint |
| Watch | Variable inspection |
| Call Stack | Function trace |
| Console | Output panel |

### Launch Configuration

```json
{
    "type": "dipjo",
    "request": "launch",
    "name": "Debug Dipjo File",
    "program": "${file}",
    "cwd": "${workspaceFolder}",
    "args": []
}
```

---

## Settings

Open Settings (`Ctrl+,`) and search for "Dipjo":

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `dipjo.interpreterPath` | string | `python` | Path to Python interpreter |
| `dipjo.mainPyPath` | string | `""` | Custom path to main.py |
| `dipjo.enableLSP` | boolean | `true` | Enable Language Server |
| `dipjo.formatOnSave` | boolean | `false` | Format on save |
| `dipjo.indentSize` | number | `4` | Spaces per indent level |
| `dipjo.enableDiagnostics` | boolean | `true` | Enable error diagnostics |
| `dipjo.diagnosticsOnType` | boolean | `true` | Diagnostics while typing |
| `dipjo.theme` | enum | `dipjo-jellyfish` | Color theme |
| `dipjo.enableSnippets` | boolean | `true` | Enable code snippets |
| `dipjo.enableCodeActions` | boolean | `true` | Enable quick fixes |

### Example Settings

```json
{
    "dipjo.interpreterPath": "python3",
    "dipjo.mainPyPath": "/path/to/Dipjo-py/main.py",
    "dipjo.enableLSP": true,
    "dipjo.formatOnSave": true,
    "dipjo.indentSize": 4,
    "dipjo.theme": "dipjo-jellyfish"
}
```

---

## Project Structure

```
dipjo-vscode/
├── src/                            # TypeScript source
│   ├── extension.ts                # Entry point
│   ├── commands/index.ts           # 10 commands
│   ├── lsp/
│   │   ├── server.ts               # Language Server
│   │   ├── definitionProvider.ts   # Go to Definition
│   │   ├── referenceProvider.ts    # Find References
│   │   ├── renameProvider.ts       # Rename Symbol
│   │   └── documentSymbolProvider.ts
│   ├── hover/hoverProvider.ts      # Hover docs
│   ├── formatter/index.ts          # Code formatter
│   ├── diagnostics/
│   │   └── codeActionProvider.ts   # Quick fixes
│   └── debug/                      # Debug adapter
│
├── syntaxes/
│   └── dipjo.tmLanguage.json       # TextMate grammar
│
├── themes/                         # 4 color themes
│   ├── dipjo-dark.json
│   ├── dipjo-light.json
│   ├── dipjo-high-contrast.json
│   └── dipjo-jellyfish.json
│
├── snippets/dipjo.json             # 25 code snippets
├── images/icons/                   # File icon theme
├── language-configuration.json     # Language config
├── package.json                    # Extension manifest
├── tsconfig.json                   # TypeScript config
├── README.md
├── CHANGELOG.md
└── LICENSE
```

---

## Development

### Prerequisites

- Node.js 18+
- npm 9+
- VS Code 1.85+

### Build

```bash
npm install
npm run compile
```

### Watch Mode

```bash
npm run watch
```

### Lint

```bash
npm run lint
```

### Package for Marketplace

```bash
npm install -g @vscode/vsce
vsce package
```

### Publish to Marketplace

```bash
vsce publish
```

---

## Changelog

### 1.0.0 (2026-07-13)

**Initial Release**

- Syntax highlighting with 92 keywords
- Language Server Protocol (LSP) support
- Auto-completion for keywords, functions, variables, classes
- Hover documentation for 60+ keywords
- Real-time diagnostics and error detection
- Code formatting with automatic indentation
- Code actions (quick fixes and refactoring)
- Go to Definition support
- Find References support
- Rename Symbol support
- Document Symbols for outline view
- Semantic token highlighting (10 types)
- 4 color themes (Dark, Light, High Contrast, JellyFish)
- Custom file icons for `.dipjo` files
- 25 code snippets
- Debug adapter for running Dipjo programs
- Project generator command
- Module creation command
- Documentation generator
- Welcome page

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/dipjo-lang/dipjo-vscode.git
cd dipjo-vscode
npm install
npm run compile
code .
# Press F5 to launch Extension Development Host
```

---

## Requirements

| Requirement | Version |
|-------------|---------|
| VS Code | 1.85+ |
| Python | 3.8+ |
| Node.js | 18+ (for development) |

---

## Related Projects

- [Dipjo Language](https://github.com/dipjo-lang/dipjo) — The Dipjo interpreter
- [Dipjo Docs](https://github.com/dipjo-lang/docs) — Official documentation
- [Dipjo Packages](https://github.com/dipjo-lang/packages) — Package registry

---

## Support

- [GitHub Issues](https://github.com/dipjo-lang/dipjo-vscode/issues) — Bug reports & feature requests
- [Discord](https://discord.gg/dipjo) — Community chat
- [Documentation](https://dipjo-lang.github.io/docs) — Official docs

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with care for the Dipjo community.<br>
  <sub>If you find this extension useful, please give it a star on GitHub!</sub>
</p>
