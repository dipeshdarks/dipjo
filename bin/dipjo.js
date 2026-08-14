#!/usr/bin/env node

"use strict";

const { spawn, spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const pkg = require("../package.json");
const VERSION = pkg.version;
const LIB_DIR = path.join(__dirname, "..", "lib");

function findPython() {
  const candidates =
    process.platform === "win32"
      ? ["python", "python3", "py"]
      : ["python3", "python"];

  for (const cmd of candidates) {
    const args = cmd === "py" ? ["-3", "--version"] : ["--version"];
    const result = spawnSync(cmd, args, {
      stdio: "pipe",
      timeout: 5000,
    });
    if (result.status === 0) {
      return cmd;
    }
  }
  return null;
}

function printUsage() {
  console.log(`
Dipjo Programming Language v${VERSION}

Usage:
  dipjo <file.dipjo>     Run a Dipjo source file
  dipjo repl             Start an interactive REPL
  dipjo --version, -v    Show version number
  dipjo --help, -h       Show this help message

Examples:
  dipjo hello.dipjo
  dipjo repl

For more information, visit: https://github.com/dipeshdarks/dipjo
`);
}

function runFile(filepath, python) {
  const resolved = path.resolve(filepath);

  if (!fs.existsSync(resolved)) {
    console.error(`Error: File '${filepath}' not found.`);
    process.exit(1);
  }

  if (!resolved.endsWith(".dipjo")) {
    console.error(
      `Error: File '${filepath}' does not have a .dipjo extension.`
    );
    process.exit(1);
  }

  const mainPy = path.join(LIB_DIR, "main.py");
  const args = [mainPy, resolved];
  const child = spawn(python, args, {
    stdio: "inherit",
    cwd: LIB_DIR,
  });

  child.on("close", (code) => {
    process.exit(code !== null ? code : 1);
  });

  child.on("error", (err) => {
    console.error(`Error: Failed to run Python: ${err.message}`);
    process.exit(1);
  });
}

function runRepl(python) {
  const replPy = path.join(LIB_DIR, "repl.py");
  const child = spawn(python, [replPy], {
    stdio: "inherit",
    cwd: LIB_DIR,
  });

  child.on("close", (code) => {
    process.exit(code !== null ? code : 0);
  });

  child.on("error", (err) => {
    console.error(`Error: Failed to run Python: ${err.message}`);
    process.exit(1);
  });
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    printUsage();
    process.exit(0);
  }

  const arg = args[0];

  if (arg === "--version" || arg === "-v") {
    console.log(VERSION);
    process.exit(0);
  }

  if (arg === "--help" || arg === "-h") {
    printUsage();
    process.exit(0);
  }

  const python = findPython();
  if (!python) {
    console.error("Error: Python 3.8+ is required but was not found.");
    console.error("");
    console.error("Please install Python from https://www.python.org/downloads/");
    console.error("");
    console.error("After installing, make sure 'python' or 'python3' is in your PATH.");
    process.exit(1);
  }

  if (arg === "repl") {
    runRepl(python);
  } else {
    runFile(arg, python);
  }
}

main();
