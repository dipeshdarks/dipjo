const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const { execFileSync, execSync } = require("child_process");
const path = require("path");

const BIN = path.join(__dirname, "..", "bin", "dipjo.js");
const EXAMPLES = path.join(__dirname, "..", "examples");

function run(args, opts = {}) {
  try {
    const stdout = execFileSync(process.execPath, [BIN, ...args], {
      encoding: "utf8",
      timeout: 10000,
      ...opts,
    });
    return { stdout, exitCode: 0 };
  } catch (err) {
    return {
      stdout: err.stdout || "",
      stderr: err.stderr || "",
      exitCode: err.status,
    };
  }
}

describe("dipjo --version", () => {
  it("prints the version number", () => {
    const { stdout, exitCode } = run(["--version"]);
    assert.equal(exitCode, 0);
    assert.match(stdout.trim(), /^\d+\.\d+\.\d+$/);
  });

  it("prints version with -v flag", () => {
    const { stdout, exitCode } = run(["-v"]);
    assert.equal(exitCode, 0);
    assert.match(stdout.trim(), /^\d+\.\d+\.\d+$/);
  });
});

describe("dipjo --help", () => {
  it("prints usage information", () => {
    const { stdout, exitCode } = run(["--help"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Dipjo Programming Language/);
    assert.match(stdout, /dipjo <file\.dipjo>/);
    assert.match(stdout, /dipjo repl/);
  });

  it("prints usage with -h flag", () => {
    const { stdout, exitCode } = run(["-h"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Dipjo Programming Language/);
  });
});

describe("dipjo with no arguments", () => {
  it("prints usage information", () => {
    const { stdout, exitCode } = run([]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Dipjo Programming Language/);
  });
});

describe("file execution", () => {
  it("runs a non-interactive program", () => {
    const { stdout, exitCode } = run(["examples/test_all.dipjo"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Welcome to Dipjo/);
    assert.match(stdout, /All tests passed!/);
  });

  it("runs fibonacci program", () => {
    const { stdout, exitCode } = run(["examples/fibonacci.dipjo"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Fibonacci sequence/);
  });
});

describe("error handling", () => {
  it("exits with error for nonexistent file", () => {
    const { stderr, exitCode } = run(["nonexistent.dipjo"]);
    assert.notEqual(exitCode, 0);
    assert.match(stderr, /not found/);
  });

  it("exits with error for wrong extension", () => {
    const { stderr, exitCode } = run(["README.md"]);
    assert.notEqual(exitCode, 0);
    assert.match(stderr, /does not have a \.dipjo extension/);
  });
});

describe("database operations", () => {
  const fs = require("fs");
  const dbDir = path.join(__dirname, "..", ".dipjo");

  function cleanDb() {
    try {
      fs.rmSync(dbDir, { recursive: true, force: true });
    } catch (e) {}
  }

  it("runs database CRUD test", () => {
    cleanDb();
    const { stdout, exitCode } = run(["test_database.dipjo"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Created:/);
    assert.match(stdout, /Updated:/);
    assert.match(stdout, /Deleted:/);
    assert.match(stdout, /All tests passed!/);
    cleanDb();
  });

  it("persists data between runs", () => {
    cleanDb();
    const createCode = `
users = database("persist_test").
users.create({"name": "TestUser", "email": "test@example.com"}).
say "created".
`;
    const fs2 = require("fs");
    const testFile = path.join(__dirname, "..", "test_persist.dipjo");
    fs2.writeFileSync(testFile, createCode);
    const r1 = run(["test_persist.dipjo"]);
    assert.equal(r1.exitCode, 0);
    assert.match(r1.stdout, /created/);

    const findCode = `
users = database("persist_test").
remember all as users.find().
say all.
`;
    fs2.writeFileSync(testFile, findCode);
    const r2 = run(["test_persist.dipjo"]);
    assert.equal(r2.exitCode, 0);
    assert.match(r2.stdout, /TestUser/);

    fs2.unlinkSync(testFile);
    cleanDb();
  });
});
