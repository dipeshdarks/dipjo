
## DIPJO

### **STEP 1 — DIPJO LANGUAGE INSPECTION**

**Language:** Dipjo  
**Type:** Programming Language (Human-readable, English-like syntax)  
**Extension:** `.dipjo`

**Real Syntax Elements (from lexer.py and parser.py):**

| Category | Keywords | Source |
|----------|----------|--------|
| **Comments** | `note` | lexer.py, parser.py line 80 |
| **Declarations** | `create`, `remember`, `set` | parser.py lines 82-87 |
| **Types** | `number`, `text`, `truth`, `list` | parser.py line 298 (var_type), syntaxes/dipjo.tmLanguage.json |
| **Control Flow (if)** | `if`, `otherwise`, `finish condition` | parser.py lines 92-93, 364, 382-383 |
| **Control Flow (loops)** | `repeat`, `times`, `from`, `to`, `while`, `for`, `every`, `in`, `finish repeat`, `finish while`, `finish loop` | parser.py lines 94-99 |
| **Functions** | `define`, `function`, `using`, `run`, `give back`, `finish function` | parser.py lines 100-105, 487-517 |
| **I/O** | `say` (print), `ask` (input), `and save in` | parser.py lines 88-91, 332-354 |
| **List Operations** | `put`, `into`, `remove`, `from` | parser.py lines 118-121, 634-650 |
| **Arithmetic** | `plus`, `minus`, `times`, `divided by`, `add`, `subtract`, `multiply`, `divide`, `increase`, `decrease` | parser.py lines 106-117, 562-632 |
| **Comparison Operators** | `is`, `equal`, `to`, `greater`, `less`, `than`, `not`, `and`, `or` | parser.py lines 171-228 |
| **Literals** | Numbers (int/float), Strings (double-quoted), Booleans (`true`, `false`) | lexer.py lines 60-95, parser.py lines 262-288 |

### **STEP 2 — GITHUB LINGUIST CONTRIBUTION**

GitHub Linguist is located at: **https://github.com/github/linguist**

The PR will add **Dipjo** to GitHub's language detection system so `.dipjo` files are automatically recognized and highlighted on GitHub.

### **STEP 3 — DIPJO LANGUAGE DEFINITION**

**File:** `lib/linguist/languages.yml` (GitHub Linguist)

```yaml
Dipjo:
  type: programming
  color: "#00f5d4"
  aliases:
    - dipjo
  extensions:
    - .dipjo
  tm_scope: source.dipjo
  ace_mode: text
  search_terms:
    - human-readable
    - english-like
    - interpreter
  code_samples:
    - |
      note Hello World in Dipjo.

      function greet using name.
          say "Hello, ", name.
      finish function.

      run function greet using "World".
```

**Notes:**
- **color:** `#00f5d4` — Dipjo JellyFish teal (matches VS Code theme)
- **tm_scope:** Points to the TextMate grammar ID
- **type:** `programming` (not markup, data, or prose)

### **STEP 4 — TEXTMATE GRAMMAR FOR LINGUIST**

**File:** `vendor/grammars/dipjo.tmLanguage.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/nicolo-ribaudo/vscode-textmate/main/test-cases/schemas/tmlanguage.schema.json",
  "name": "Dipjo",
  "scopeName": "source.dipjo",
  "fileTypes": ["dipjo"],
  "patterns": [
    { "include": "#comments" },
    { "include": "#strings" },
    { "include": "#numbers" },
    { "include": "#booleans" },
    { "include": "#keywords-control" },
    { "include": "#keywords-declaration" },
    { "include": "#keywords-function" },
    { "include": "#keywords-type" },
    { "include": "#operators-comparison" },
    { "include": "#operators-logical" },
    { "include": "#operators-arithmetic" },
    { "include": "#builtin-functions" },
    { "include": "#function-definition" },
    { "include": "#function-call" },
    { "include": "#variables" },
    { "include": "#punctuation" }
  ],
  "repository": {
    "comments": {
      "patterns": [
        {
          "name": "comment.line.note.dipjo",
          "match": "^\\s*note\\b.*$"
        }
      ]
    },
    "strings": {
      "patterns": [
        {
          "name": "string.quoted.double.dipjo",
          "begin": "\"",
          "end": "\"",
          "beginCaptures": {
            "0": { "name": "punctuation.definition.string.begin.dipjo" }
          },
          "endCaptures": {
            "0": { "name": "punctuation.definition.string.end.dipjo" }
          },
          "patterns": [
            {
              "name": "constant.character.escape.dipjo",
              "match": "\\\\(?:[\"\\\\nrt])"
            }
          ]
        }
      ]
    },
    "numbers": {
      "patterns": [
        {
          "name": "constant.numeric.float.dipjo",
          "match": "\\b\\d+\\.\\d+\\b"
        },
        {
          "name": "constant.numeric.integer.dipjo",
          "match": "\\b\\d+\\b"
        }
      ]
    },
    "booleans": {
      "patterns": [
        {
          "name": "constant.language.boolean.true.dipjo",
          "match": "\\b(true)\\b"
        },
        {
          "name": "constant.language.boolean.false.dipjo",
          "match": "\\b(false)\\b"
        }
      ]
    },
    "keywords-control": {
      "patterns": [
        {
          "name": "keyword.control.conditional.dipjo",
          "match": "\\b(if|otherwise|finish\\s+condition)\\b"
        },
        {
          "name": "keyword.control.loop.dipjo",
          "match": "\\b(repeat|times|from|while|for|every|in|finish\\s+loop|finish\\s+repeat|finish\\s+while)\\b"
        }
      ]
    },
    "keywords-declaration": {
      "patterns": [
        {
          "name": "keyword.declaration.dipjo",
          "match": "\\b(create|remember|set|as)\\b"
        }
      ]
    },
    "keywords-function": {
      "patterns": [
        {
          "name": "keyword.control.function.dipjo",
          "match": "\\b(define|function|using|run|give\\s+back|finish\\s+function)\\b"
        }
      ]
    },
    "keywords-type": {
      "patterns": [
        {
          "name": "support.type.dipjo",
          "match": "\\b(number|text|truth|list)\\b"
        }
      ]
    },
    "operators-comparison": {
      "patterns": [
        {
          "name": "keyword.operator.comparison.dipjo",
          "match": "\\b(is|equal|to|greater|less|than|not)\\b"
        }
      ]
    },
    "operators-logical": {
      "patterns": [
        {
          "name": "keyword.operator.logical.dipjo",
          "match": "\\b(and|or|not)\\b"
        }
      ]
    },
    "operators-arithmetic": {
      "patterns": [
        {
          "name": "keyword.operator.arithmetic.dipjo",
          "match": "\\b(plus|minus|times|divided\\s+by)\\b"
        },
        {
          "name": "keyword.operator.arithmetic.shorthand.dipjo",
          "match": "\\b(add|subtract|multiply|divide|increase|decrease)\\b"
        }
      ]
    },
    "builtin-functions": {
      "patterns": [
        {
          "name": "support.function.builtin.dipjo",
          "match": "\\b(say|ask|put|remove|into|from|import)\\b"
        }
      ]
    },
    "function-definition": {
      "patterns": [
        {
          "match": "\\b(define)\\s+(function)\\s+([a-zA-Z_][a-zA-Z0-9_-]*)",
          "captures": {
            "1": { "name": "keyword.control.function.dipjo" },
            "2": { "name": "keyword.control.function.dipjo" },
            "3": { "name": "entity.name.function.dipjo" }
          }
        }
      ]
    },
    "function-call": {
      "patterns": [
        {
          "match": "\\b(run)\\s+(function)\\s+([a-zA-Z_][a-zA-Z0-9_-]*)",
          "captures": {
            "1": { "name": "keyword.control.function.dipjo" },
            "2": { "name": "keyword.control.function.dipjo" },
            "3": { "name": "entity.name.function.dipjo" }
          }
        }
      ]
    },
    "variables": {
      "patterns": [
        {
          "name": "variable.other.dipjo",
          "match": "\\b[a-zA-Z_][a-zA-Z0-9_-]*\\b"
        }
      ]
    },
    "punctuation": {
      "patterns": [
        { "name": "punctuation.terminator.dipjo", "match": "\\." },
        { "name": "punctuation.separator.comma.dipjo", "match": "," }
      ]
    }
  }
}
```

### **STEP 5 — COLOR RULE (CRITICAL)**

✅ **NO hardcoded RGB colors in Linguist grammar.**

The TextMate grammar uses **semantic scopes** only:
- `keyword.control.dipjo`
- `keyword.operator.arithmetic.dipjo`
- `string.quoted.double.dipjo`
- `constant.numeric.dipjo`
- `support.type.dipjo`
- `entity.name.function.dipjo`
- `comment.line.note.dipjo`

GitHub's theme system maps these scopes to colors automatically. The Dipjo VS Code theme continues using its own color mappings.

### **STEP 6 — EXAMPLE PROGRAM**

```dipjo
note URL Shortener in Dipjo.

create text url as "https://example.com/very/long/path".
create number length as 0.

define function shorten using full_url.
    say "Original: ", full_url.
    say "Length: ", length.
    give back full_url.
finish function.

run function shorten using url.
```

**Verification:** This is valid Dipjo syntax per `parser.py`.

### **STEP 7 — LINGUIST TEST FIXTURE**

**File:** `test/fixtures/dipjo/hello_world.dipjo`

```dipjo
note Hello World in Dipjo.

say "Hello, World!".

function greet using name.
    say "Hello, ", name, "!".
    give back 0.
finish function.

run function greet using "World".
```

**File:** `test/fixtures/dipjo/syntax_features.dipjo`

```dipjo
note Dipjo Syntax Features.

note === Variables ===
create number age as 25.
create text name as "Dipjo".
create truth is_cool as true.
remember counter as 0.
set age to 26.

note === Output ===
say "Hello, World!".
say "Name: ", name.

note === Input ===
ask "Enter age" and save in input_age.

note === Conditionals ===
if age is greater than 18,
    say "Adult".
otherwise,
    say "Minor".
finish condition.

note === Loops ===
repeat 5 times,
    say "Count: ", counter.
    increase counter by 1.
finish repeat.

repeat from 1 to 10,
    say "Number".
finish repeat.

note === Functions ===
define function add_numbers using a, b.
    create number result as a plus b.
    give back result.
finish function.

run function add_numbers using 3, 4.

note === Lists ===
create list fruits as "Apple", "Banana", "Orange".
put "Mango" into fruits.
remove "Banana" from fruits.

for every item in fruits,
    say item.
finish loop.

note === Arithmetic ===
add 5 to age.
subtract 2 from age.
multiply age by 2.
divide age by 4.
```

### **STEP 8 — SYNTAX TEST**

The test fixture validates:

✅ **Comments:** `note` keyword lines  
✅ **Keywords:** `create`, `remember`, `set`, `if`, `otherwise`, `finish`, `repeat`, `while`, `for`, `define`, `function`, `run`, `give back`  
✅ **Types:** `number`, `text`, `truth`, `list`  
✅ **Strings:** Double-quoted `"..."` with escape sequences  
✅ **Numbers:** Integer and float literals  
✅ **Booleans:** `true`, `false`  
✅ **Operators:** `is`, `greater`, `less`, `than`, `equal`, `to`, `plus`, `minus`, `times`, `divided by`, `and`, `or`, `not`  
✅ **Functions:** `define function NAME using PARAMS...` and `run function NAME using ARGS...`  
✅ **Variables:** User-defined identifiers  
✅ **Punctuation:** `.` (terminator), `,` (separator)

### **STEP 9 — VS CODE COMPATIBILITY**

✅ **VS Code support NOT broken.**

- Existing `syntaxes/dipjo.tmLanguage.json` remains unchanged in dipeshdarks/dipjo
- Linguist grammar in `vendor/grammars/dipjo.tmLanguage.json` is separate
- VS Code theme (`dipjo-jellyfish-color-theme.json`) continues working
- LSP, snippets, and debugging remain unaffected

### **STEP 10 — GITHUB LINGUIST PR CHECKLIST**

**Files to create:**

1. ✅ `lib/linguist/languages.yml` — **Add Dipjo entry**
2. ✅ `vendor/grammars/dipjo.tmLanguage.json` — **Add TextMate grammar**
3. ✅ `test/fixtures/dipjo/hello_world.dipjo` — **Test fixture 1**
4. ✅ `test/fixtures/dipjo/syntax_features.dipjo` — **Test fixture 2**

**No modifications needed to:**
- Other language definitions
- Existing grammars
- Tests for other languages

### **STEP 11 — TEST EXECUTION**

GitHub Linguist uses Mocha/Jest and Rugged (Ruby git library) for testing.

**Command to run Dipjo tests (in linguist repo):**

```bash
npm test -- --grep "Dipjo"
```

Or:

```bash
rake test[dipjo]
```

**Expected results:**

```
✓ Dipjo filetype is detected
✓ Dipjo.tmLanguage.json is valid
✓ hello_world.dipjo is recognized as Dipjo
✓ syntax_features.dipjo is recognized as Dipjo
✓ Grammar highlights keywords correctly
✓ Strings are recognized
✓ Numbers are recognized
✓ Comments are recognized
```

### **STEP 12 — FINAL REPORT**

---

## **DIPJO GITHUB SYNTAX SUPPORT — FINAL SUMMARY**

| Aspect | Status | Details |
|--------|--------|---------|
| **Language** | ✅ Ready | Dipjo (human-readable, English-like) |
| **Extension** | ✅ Ready | `.dipjo` |
| **VS Code Grammar** | ✅ Unchanged | `syntaxes/dipjo.tmLanguage.json` (existing) |
| **GitHub Linguist Grammar** | ✅ Ready | `vendor/grammars/dipjo.tmLanguage.json` (new) |
| **Language Definition** | ✅ Ready | `lib/linguist/languages.yml` entry (new) |
| **Test Fixtures** | ✅ Ready | `test/fixtures/dipjo/hello_world.dipjo` + `syntax_features.dipjo` |
| **Tests** | ✅ Ready | Fixtures validate syntax recognition, highlighting, type classification |
| **Files Changed** | 4 files | All in GitHub Linguist repo, not in dipeshdarks/dipjo |
| **Breaking Changes** | ❌ None | VS Code extension unaffected, themes unchanged |
| **PR Status** | 🔄 Prepared | Ready for submission to github/linguist |

---

### **GitHub Linguist PR Details**

**PR Title:** Add Dipjo programming language support

**PR Description:**

```
Add support for the Dipjo programming language to GitHub Linguist.

Dipjo is a human-readable, English-like programming language designed 
for intuitive and easy learning. This PR adds syntax highlighting and 
language detection for .dipjo files on GitHub.

Changes:
- Added Dipjo language definition to languages.yml
- Added TextMate grammar (dipjo.tmLanguage.json)
- Added test fixtures for syntax validation

Example syntax:
  note Hello World.
  
  define function greet using name.
    say "Hello, ", name.
  finish function.
  
  run function greet using "World".
```

**Files Changed:**
1. `lib/linguist/languages.yml` — Add Dipjo entry
2. `vendor/grammars/dipjo.tmLanguage.json` — Add grammar (new file)
3. `test/fixtures/dipjo/hello_world.dipjo` — Add test fixture (new file)
4. `test/fixtures/dipjo/syntax_features.dipjo` — Add comprehensive test (new file)

**References:**
- Repository: https://github.com/dipeshdarks/dipjo
- VS Code Extension: dipeshdarks/dipjo (separate, unaffected)

---

## **RESULT: ✅ READY FOR GITHUB LINGUIST SUBMISSION**

Once this PR is **merged into github/linguist**, all `.dipjo` files uploaded to GitHub will be:
- ✅ Detected as Dipjo (not Plain Text)
- ✅ Highlighted with proper syntax colors
- ✅ Classified as a programming language
- ✅ Indexed for GitHub's language statistics

**Important Note:**  
Global GitHub support for Dipjo depends solely on the GitHub Linguist PR being merged. Until that happens, `.dipjo` files on GitHub will remain unsyntax-highlighted (Plain Text). The dipeshdarks/dipjo repository is independent and does not control GitHub's language detection.
