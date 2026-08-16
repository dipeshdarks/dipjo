const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const { execFileSync, execSync } = require("child_process");
const path = require("path");

const BIN = path.join(__dirname, "..", "bin", "dipjo.js");
const LIB = path.join(__dirname, "..", "lib");

function run(args, opts = {}) {
  try {
    const stdout = execFileSync(process.execPath, [BIN, ...args], {
      encoding: "utf8",
      timeout: 15000,
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

function runPython(args, opts = {}) {
  try {
    const stdout = execFileSync("python", [path.join(LIB, "search_cli.py"), ...args], {
      encoding: "utf8",
      timeout: 15000,
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

const fs = require("fs");

function cleanSearchDb(name) {
  const dbDir = path.join(__dirname, "..", ".dipjo", "data", "search");
  const dbPath = path.join(dbDir, `${name}.db`);
  try {
    if (fs.existsSync(dbPath)) fs.unlinkSync(dbPath);
  } catch (e) {}
}

describe("DipjoSearch CLI", () => {
  it("shows search help", () => {
    const { stdout, stderr, exitCode } = run(["search"]);
    assert.equal(exitCode, 1);
    assert.match((stdout + stderr), /search/);
  });

  it("creates a search index", () => {
    cleanSearchDb("cli_test");
    const { stdout, exitCode } = run(["search", "create", "cli_test"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Created search index/);
    cleanSearchDb("cli_test");
  });

  it("lists search indexes", () => {
    cleanSearchDb("cli_list_test");
    run(["search", "create", "cli_list_test"]);
    const { stdout, exitCode } = run(["search", "list"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /cli_list_test/);
    cleanSearchDb("cli_list_test");
  });

  it("adds a document via key-value pairs", () => {
    cleanSearchDb("cli_add_test");
    run(["search", "create", "cli_add_test"]);
    const { stdout, exitCode } = run([
      "search", "add", "cli_add_test",
      "id", "1",
      "title", "Test Document",
      "content", "This is a test document for DipjoSearch."
    ]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Added document/);
    cleanSearchDb("cli_add_test");
  });

  it("queries a search index", () => {
    cleanSearchDb("cli_query_test");
    run(["search", "create", "cli_query_test"]);
    run(["search", "add", "cli_query_test", "id", "1", "title", "Dipjo Search", "content", "Full text search engine."]);
    run(["search", "add", "cli_query_test", "id", "2", "title", "Python Guide", "content", "Learn Python programming."]);
    const { stdout, exitCode } = run(["search", "query", "cli_query_test", "dipjo"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /total/);
    assert.match(stdout, /Dipjo Search/);
    cleanSearchDb("cli_query_test");
  });

  it("shows index stats", () => {
    cleanSearchDb("cli_stats_test");
    run(["search", "create", "cli_stats_test"]);
    run(["search", "add", "cli_stats_test", "id", "1", "title", "Test", "content", "Content."]);
    const { stdout, exitCode } = run(["search", "stats", "cli_stats_test"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /documents/);
    assert.match(stdout, /unique_terms/);
    cleanSearchDb("cli_stats_test");
  });

  it("deletes a search index", () => {
    cleanSearchDb("cli_delete_test");
    run(["search", "create", "cli_delete_test"]);
    const { stdout, exitCode } = run(["search", "delete", "cli_delete_test"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Deleted search index/);
  });
});

describe("DipjoSearch Python CLI", () => {
  it("creates an index", () => {
    cleanSearchDb("py_create");
    const { stdout, exitCode } = runPython(["create", "py_create"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Created search index/);
    cleanSearchDb("py_create");
  });

  it("adds and queries documents", () => {
    cleanSearchDb("py_query");
    runPython(["create", "py_query"]);
    runPython(["add", "py_query", "id", "1", "title", "Dipjo Language", "content", "Human-readable programming."]);
    runPython(["add", "py_query", "id", "2", "title", "JavaScript Guide", "content", "Web development with JS."]);
    const { stdout, exitCode } = runPython(["query", "py_query", "dipjo"]);
    assert.equal(exitCode, 0);
    const result = JSON.parse(stdout);
    assert.equal(result.total >= 1, true);
    assert.equal(result.results.length >= 1, true);
    assert.equal(result.results[0].document.title, "Dipjo Language");
    cleanSearchDb("py_query");
  });

  it("handles pagination", () => {
    cleanSearchDb("py_pagination");
    runPython(["create", "py_pagination"]);
    for (let i = 1; i <= 5; i++) {
      runPython(["add", "py_pagination", "id", String(i), "title", `Doc ${i}`, "content", "Test document."]);
    }
    const { stdout } = runPython(["query", "py_pagination", "test"]);
    const result = JSON.parse(stdout);
    assert.equal(result.total, 5);
    cleanSearchDb("py_pagination");
  });

  it("shows stats", () => {
    cleanSearchDb("py_stats");
    runPython(["create", "py_stats"]);
    runPython(["add", "py_stats", "id", "1", "title", "Hello", "content", "World."]);
    const { stdout } = runPython(["stats", "py_stats"]);
    const stats = JSON.parse(stdout);
    assert.equal(stats.documents, 1);
    assert.ok(stats.unique_terms > 0);
    cleanSearchDb("py_stats");
  });

  it("rebuilds an index", () => {
    cleanSearchDb("py_rebuild");
    runPython(["create", "py_rebuild"]);
    runPython(["add", "py_rebuild", "id", "1", "title", "Test", "content", "Content."]);
    const { stdout, exitCode } = runPython(["rebuild", "py_rebuild"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Rebuilt index/);
    cleanSearchDb("py_rebuild");
  });

  it("deletes an index", () => {
    cleanSearchDb("py_delete");
    runPython(["create", "py_delete"]);
    const { stdout, exitCode } = runPython(["delete", "py_delete"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Deleted search index/);
  });

  it("lists indexes", () => {
    cleanSearchDb("py_list1");
    cleanSearchDb("py_list2");
    runPython(["create", "py_list1"]);
    runPython(["create", "py_list2"]);
    const { stdout, exitCode } = runPython(["list"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /py_list1/);
    assert.match(stdout, /py_list2/);
    cleanSearchDb("py_list1");
    cleanSearchDb("py_list2");
  });
});

describe("DipjoSearch Dipjo Integration", () => {
  it("runs search tests from Dipjo code", () => {
    const { stdout, exitCode } = run(["tests/test_search.dipjo"]);
    assert.equal(exitCode, 0);
    assert.match(stdout, /Created index/);
    assert.match(stdout, /Added 5 documents/);
    assert.match(stdout, /Committed index/);
    assert.match(stdout, /All search tests passed!/);
    cleanSearchDb("test_articles");
  });
});

describe("DipjoSearch Ranking", () => {
  it("ranks documents by relevance", () => {
    cleanSearchDb("rank_test");
    runPython(["create", "rank_test"]);
    runPython(["add", "rank_test", "id", "1", "title", "Dipjo Programming", "content", "Dipjo is a programming language."]);
    runPython(["add", "rank_test", "id", "2", "title", "Python Guide", "content", "Python is a programming language."]);
    runPython(["add", "rank_test", "id", "3", "title", "Dipjo Tutorial", "content", "Learn Dipjo step by step."]);
    const { stdout } = runPython(["query", "rank_test", "dipjo programming"]);
    const result = JSON.parse(stdout);
    assert.ok(result.results.length >= 2);
    const titles = result.results.map(r => r.document.title);
    assert.ok(titles.includes("Dipjo Programming"));
    cleanSearchDb("rank_test");
  });
});

describe("DipjoSearch Field Search", () => {
  it("searches specific fields", () => {
    cleanSearchDb("field_test");
    runPython(["create", "field_test"]);
    runPython(["add", "field_test", "id", "1", "title", "Python Guide", "content", "Learn Dipjo programming."]);
    runPython(["add", "field_test", "id", "2", "title", "Dipjo Guide", "content", "Learn Python programming."]);
    const { stdout } = runPython(["query", "field_test", "title:dipjo"]);
    const result = JSON.parse(stdout);
    assert.ok(result.results.length >= 1);
    assert.equal(result.results[0].document.title, "Dipjo Guide");
    cleanSearchDb("field_test");
  });
});
