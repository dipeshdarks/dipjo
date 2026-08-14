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
    const result = spawnSync(cmd, args, { stdio: "pipe", timeout: 5000 });
    if (result.status === 0) return cmd;
  }
  return null;
}

function requirePython() {
  const python = findPython();
  if (!python) {
    console.error("Error: Python 3.8+ is required but was not found.");
    console.error("");
    console.error("Install Python from https://www.python.org/downloads/");
    console.error("Make sure 'python' or 'python3' is in your PATH.");
    process.exit(1);
  }
  return python;
}

function runPythonScript(script, args, python) {
  python = python || requirePython();
  const scriptPath = path.join(LIB_DIR, script);
  const child = spawn(python, [scriptPath, ...args], { stdio: "inherit" });
  child.on("close", (code) => process.exit(code !== null ? code : 1));
  child.on("error", (err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
}

function findProjectRoot() {
  let dir = process.cwd();
  while (dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, "dipjo.json"))) return dir;
    dir = path.dirname(dir);
  }
  if (fs.existsSync(path.join(process.cwd(), "dipjo.json"))) return process.cwd();
  return null;
}

function readConfig() {
  const root = findProjectRoot();
  if (!root) return null;
  const configPath = path.join(root, "dipjo.json");
  try {
    return JSON.parse(fs.readFileSync(configPath, "utf-8"));
  } catch {
    return null;
  }
}

function writeConfig(config) {
  const root = process.cwd();
  fs.writeFileSync(path.join(root, "dipjo.json"), JSON.stringify(config, null, 2) + "\n");
}

// ── Commands ──────────────────────────────────────────

function cmdNew(args) {
  const name = args[0];
  if (!name) {
    console.error("Usage: dipjo new <project-name>");
    process.exit(1);
  }
  const projectDir = path.resolve(process.cwd(), name);
  if (fs.existsSync(projectDir)) {
    console.error(`Error: Directory '${name}' already exists.`);
    process.exit(1);
  }
  fs.mkdirSync(projectDir, { recursive: true });
  fs.mkdirSync(path.join(projectDir, "src"), { recursive: true });
  fs.mkdirSync(path.join(projectDir, "tests"), { recursive: true });
  fs.mkdirSync(path.join(projectDir, "examples"), { recursive: true });

  const config = {
    name: name,
    version: "0.1.0",
    description: "",
    main: "src/main.dipjo",
    dependencies: {},
  };
  fs.writeFileSync(path.join(projectDir, "dipjo.json"), JSON.stringify(config, null, 2) + "\n");

  fs.writeFileSync(
    path.join(projectDir, "src", "main.dipjo"),
    'note Hello World in Dipjo.\n\nsay "Hello from ' + name + "!\".\n"
  );

  fs.writeFileSync(
    path.join(projectDir, "README.md"),
    `# ${name}\n\nA Dipjo project.\n\n## Run\n\n\`\`\`bash\ndipjo run src/main.dipjo\n\`\`\`\n`
  );

  console.log(`Created project: ${name}`);
  console.log(`  ${name}/`);
  console.log(`  ├── dipjo.json`);
  console.log(`  ├── src/main.dipjo`);
  console.log(`  ├── tests/`);
  console.log(`  ├── examples/`);
  console.log(`  └── README.md`);
}

function cmdInit() {
  const configPath = path.join(process.cwd(), "dipjo.json");
  if (fs.existsSync(configPath)) {
    console.error("Error: dipjo.json already exists. Use --force to overwrite.");
    process.exit(1);
  }
  const dirName = path.basename(process.cwd());
  const config = {
    name: dirName,
    version: "0.1.0",
    description: "",
    main: "src/main.dipjo",
    dependencies: {},
  };
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + "\n");
  console.log("Created dipjo.json");
}

function cmdRun(args) {
  if (args.length === 0) {
    console.error("Usage: dipjo run <file.dipjo>");
    process.exit(1);
  }
  const filepath = args[0];
  const resolved = path.resolve(filepath);
  if (!fs.existsSync(resolved)) {
    console.error(`Error: File '${filepath}' not found.`);
    process.exit(1);
  }
  if (!resolved.endsWith(".dipjo")) {
    console.error(`Error: File '${filepath}' does not have a .dipjo extension.`);
    process.exit(1);
  }
  const python = requirePython();
  const mainPy = path.join(LIB_DIR, "main.py");
  const child = spawn(python, [mainPy, resolved, ...args.slice(1)], {
    stdio: "inherit",
    cwd: LIB_DIR,
  });
  child.on("close", (code) => process.exit(code !== null ? code : 1));
  child.on("error", (err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
}

function cmdRepl() {
  const python = requirePython();
  const replPy = path.join(LIB_DIR, "repl.py");
  const child = spawn(python, [replPy], { stdio: "inherit", cwd: LIB_DIR });
  child.on("close", (code) => process.exit(code !== null ? code : 0));
  child.on("error", (err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
}

function cmdBuild() {
  const config = readConfig();
  const root = findProjectRoot() || process.cwd();
  console.log("Dipjo Build");
  console.log("==========");
  console.log();
  console.log("Checking project files...");
  const srcDir = path.join(root, "src");
  let dipjoFiles = [];
  if (fs.existsSync(srcDir)) {
    dipjoFiles = fs.readdirSync(srcDir).filter((f) => f.endsWith(".dipjo"));
  }
  if (dipjoFiles.length === 0) {
    console.log("No .dipjo files found in src/");
    process.exit(0);
  }
  const python = findPython();
  const checkPy = path.join(LIB_DIR, "check.py");
  let allOk = true;
  for (const file of dipjoFiles) {
    const filepath = path.join(srcDir, file);
    const result = spawnSync(python, [checkPy, filepath], { stdio: "pipe" });
    if (result.status === 0) {
      console.log(`  OK: src/${file}`);
    } else {
      console.error(`  FAIL: src/${file}`);
      console.error(result.stderr ? result.stderr.toString() : "Unknown error");
      allOk = false;
    }
  }
  console.log();
  if (allOk) {
    console.log("Build successful! All files parsed correctly.");
  } else {
    console.error("Build failed. Fix errors above.");
    process.exit(1);
  }
}

function cmdTest() {
  const root = findProjectRoot() || process.cwd();
  const testsDir = path.join(root, "tests");
  let testFiles = [];
  if (fs.existsSync(testsDir)) {
    testFiles = fs.readdirSync(testsDir).filter((f) => f.endsWith(".dipjo"));
  }
  const testAll = path.join(root, "examples", "test_all.dipjo");
  if (fs.existsSync(testAll)) {
    testFiles.push(testAll);
  }
  if (testFiles.length === 0) {
    console.log("No test files found.");
    process.exit(0);
  }
  console.log(`Running ${testFiles.length} test(s)...`);
  console.log();
  const python = requirePython();
  const mainPy = path.join(LIB_DIR, "main.py");
  let passed = 0;
  let failed = 0;
  for (const file of testFiles) {
    const filepath = path.isAbsolute(file) ? file : path.join(root, file);
    const result = spawnSync(python, [mainPy, filepath], { stdio: "pipe" });
    if (result.status === 0) {
      passed++;
      console.log(`  PASS: ${path.relative(root, filepath)}`);
    } else {
      failed++;
      console.error(`  FAIL: ${path.relative(root, filepath)}`);
      if (result.stderr) console.error(result.stderr.toString());
      if (result.stdout) console.error(result.stdout.toString());
    }
  }
  console.log();
  console.log(`${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);
}

function cmdCheck(args) {
  if (args.length === 0) {
    const config = readConfig();
    if (config && config.main) {
      args = [config.main];
    } else {
      console.error("Usage: dipjo check <file.dipjo> [...]");
      process.exit(1);
    }
  }
  runPythonScript("check.py", args);
}

function cmdFormat(args) {
  const target = args[0] || ".";
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    runPythonScript("format.py", [target]);
  } else {
    runPythonScript("format.py", args.length > 0 ? args : ["."]);
  }
}

function cmdLint(args) {
  if (args.length === 0) {
    const config = readConfig();
    if (config && config.main) {
      args = [config.main];
    } else {
      args = ["."];
    }
  }
  runPythonScript("lint.py", args);
}

function cmdAdd(args) {
  if (args.length === 0) {
    console.error("Usage: dipjo add <package>");
    process.exit(1);
  }
  const pkgName = args[0];
  const config = readConfig();
  if (!config) {
    console.error("Error: No dipjo.json found. Run 'dipjo init' first.");
    process.exit(1);
  }
  if (!config.dependencies) config.dependencies = {};
  if (config.dependencies[pkgName]) {
    console.log(`Package '${pkgName}' is already a dependency.`);
    return;
  }
  config.dependencies[pkgName] = "latest";
  writeConfig(config);
  console.log(`Added '${pkgName}' to dependencies.`);
  console.log("Note: Dipjo package registry is not yet available.");
}

function cmdRemove(args) {
  if (args.length === 0) {
    console.error("Usage: dipjo remove <package>");
    process.exit(1);
  }
  const pkgName = args[0];
  const config = readConfig();
  if (!config) {
    console.error("Error: No dipjo.json found.");
    process.exit(1);
  }
  if (!config.dependencies || !config.dependencies[pkgName]) {
    console.error(`Error: Package '${pkgName}' is not a dependency.`);
    process.exit(1);
  }
  delete config.dependencies[pkgName];
  writeConfig(config);
  console.log(`Removed '${pkgName}' from dependencies.`);
}

function cmdInstall() {
  const config = readConfig();
  if (!config) {
    console.error("Error: No dipjo.json found. Run 'dipjo init' first.");
    process.exit(1);
  }
  const deps = config.dependencies || {};
  const names = Object.keys(deps);
  if (names.length === 0) {
    console.log("No dependencies to install.");
    return;
  }
  console.log("Dependencies:");
  for (const name of names) {
    console.log(`  ${name}: ${deps[name]}`);
  }
  console.log();
  console.log("Note: Dipjo package registry is not yet available.");
  console.log("Dependencies are configured but cannot be downloaded yet.");
}

function cmdUpdate() {
  const config = readConfig();
  if (!config) {
    console.error("Error: No dipjo.json found.");
    process.exit(1);
  }
  console.log("Note: Dipjo package registry is not yet available.");
}

function cmdList() {
  const config = readConfig();
  if (!config) {
    console.log("No dipjo.json found. Not in a Dipjo project.");
    return;
  }
  const deps = config.dependencies || {};
  const names = Object.keys(deps);
  if (names.length === 0) {
    console.log("No dependencies configured.");
    return;
  }
  console.log("Dependencies:");
  for (const name of names) {
    console.log(`  ${name}: ${deps[name]}`);
  }
}

function cmdClean() {
  const root = findProjectRoot() || process.cwd();
  const dirs = ["dist", "build", "cache"];
  let removed = 0;
  for (const dir of dirs) {
    const dirPath = path.join(root, dir);
    if (fs.existsSync(dirPath)) {
      fs.rmSync(dirPath, { recursive: true, force: true });
      console.log(`Removed: ${dir}/`);
      removed++;
    }
  }
  if (removed === 0) {
    console.log("Nothing to clean.");
  } else {
    console.log(`Cleaned ${removed} directory(ies).`);
  }
}

function cmdDocs() {
  const root = findProjectRoot() || process.cwd();
  const srcDir = path.join(root, "src");
  const outputDir = path.join(root, "docs");
  const docsDir = fs.existsSync(srcDir) ? srcDir : root;
  runPythonScript("docs.py", [docsDir, outputDir]);
}

function cmdServe() {
  const root = findProjectRoot() || process.cwd();
  const config = readConfig();
  const mainFile = config && config.main ? path.join(root, config.main) : null;
  if (mainFile && !fs.existsSync(mainFile)) {
    console.error(`Error: Main file '${config.main}' not found.`);
    process.exit(1);
  }
  const python = requirePython();
  if (mainFile) {
    const mainPy = path.join(LIB_DIR, "main.py");
    const child = spawn(python, [mainPy, mainFile], { stdio: "inherit", cwd: LIB_DIR });
    child.on("close", (code) => process.exit(code !== null ? code : 1));
    child.on("error", (err) => {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    });
  } else {
    console.log("Starting HTTP server on http://localhost:3000");
    console.log("Configure your Dipjo app with: run function start using 3000.");
  }
}

function cmdDoctor() {
  runPythonScript("doctor.py", []);
}

function cmdVersion() {
  console.log(`Dipjo ${VERSION}`);
}

function cmdHelp() {
  console.log(`
Dipjo Programming Language v${VERSION}

Usage:
  dipjo <command> [options]

Commands:
  new <name>          Create a new Dipjo project
  init                Initialize dipjo.json in current directory
  run <file.dipjo>    Run a Dipjo source file
  repl                Start an interactive REPL
  build               Build and validate project files
  test                Run Dipjo tests
  check <file>        Check syntax without running
  format [file|dir]   Format Dipjo code
  lint [file|dir]     Lint Dipjo code
  add <package>       Add a dependency
  remove <package>    Remove a dependency
  install             Install dependencies
  update              Update dependencies
  list                List dependencies
  clean               Remove generated files (dist/, build/, cache/)
  docs                Generate documentation
  serve               Start HTTP server
  doctor              Diagnose installation
  version             Show version number
  help                Show this help message

Examples:
  dipjo new my-app
  dipjo run hello.dipjo
  dipjo repl
  dipjo check src/main.dipjo
  dipjo test
  dipjo serve
  dipjo doctor

For more information, visit: https://github.com/dipeshdarks/dipjo
`);
}

// ── Main ──────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    cmdHelp();
    process.exit(0);
  }

  const cmd = args[0].toLowerCase();
  const cmdArgs = args.slice(1);

  switch (cmd) {
    case "new":
      cmdNew(cmdArgs);
      break;
    case "init":
      cmdInit();
      break;
    case "run":
      cmdRun(cmdArgs);
      break;
    case "repl":
      cmdRepl();
      break;
    case "build":
      cmdBuild();
      break;
    case "test":
      cmdTest();
      break;
    case "check":
      cmdCheck(cmdArgs);
      break;
    case "format":
      cmdFormat(cmdArgs);
      break;
    case "lint":
      cmdLint(cmdArgs);
      break;
    case "add":
      cmdAdd(cmdArgs);
      break;
    case "remove":
      cmdRemove(cmdArgs);
      break;
    case "install":
      cmdInstall();
      break;
    case "update":
      cmdUpdate();
      break;
    case "list":
      cmdList();
      break;
    case "clean":
      cmdClean();
      break;
    case "docs":
      cmdDocs();
      break;
    case "serve":
      cmdServe();
      break;
    case "doctor":
      cmdDoctor();
      break;
    case "version":
      cmdVersion();
      break;
    case "help":
      cmdHelp();
      break;
    case "--version":
    case "-v":
      cmdVersion();
      break;
    case "--help":
    case "-h":
      cmdHelp();
      break;
    default:
      if (cmd.endsWith(".dipjo")) {
        cmdRun([cmd, ...cmdArgs]);
      } else {
        console.error(`Unknown command: ${cmd}`);
        console.error("Run 'dipjo help' for usage information.");
        process.exit(1);
      }
      break;
  }
}

main();
