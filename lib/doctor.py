import sys
import os
import subprocess
import platform


def doctor():
    issues = []
    print("Dipjo Doctor")
    print("=" * 50)
    print()

    dipjo_version = "unknown"
    try:
        pkg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "package.json")
        import json
        with open(pkg_path) as f:
            dipjo_version = json.load(f).get("version", "unknown")
    except Exception:
        pass
    print(f"Dipjo version: {dipjo_version}")

    node_ok = False
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            print(f"Node.js: {node_version} [OK]")
            node_ok = True
        else:
            print("Node.js: not found [MISSING]")
            issues.append("Node.js is not installed or not in PATH")
    except Exception:
        print("Node.js: not found [MISSING]")
        issues.append("Node.js is not installed or not in PATH")

    npm_ok = False
    npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
    try:
        result = subprocess.run([npm_cmd, "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            print(f"npm: {npm_version} [OK]")
            npm_ok = True
        else:
            print("npm: not found [MISSING]")
            issues.append("npm is not installed or not in PATH")
    except Exception:
        print("npm: not found [MISSING]")
        issues.append("npm is not installed or not in PATH")

    python_ok = False
    python_cmd = None
    candidates = ["python3", "python", "py"] if platform.system() != "Windows" else ["python", "python3", "py"]
    for cmd in candidates:
        try:
            args = ["-3", "--version"] if cmd == "py" else ["--version"]
            result = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                py_version = result.stdout.strip()
                print(f"Python: {py_version} [OK]")
                python_ok = True
                python_cmd = cmd
                break
        except Exception:
            continue
    if not python_ok:
        print("Python: not found [MISSING]")
        issues.append("Python 3.8+ is required. Install from https://www.python.org/downloads/")

    if python_cmd:
        lib_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")
        test_file = os.path.join(lib_dir, "test_dipjo_interpreter.py")
        try:
            result = subprocess.run(
                [python_cmd, "-c", "import sys; sys.path.insert(0, '.'); from lexer import Lexer; from parser import Parser; print('OK')"],
                capture_output=True, text=True, timeout=5, cwd=lib_dir
            )
            if result.returncode == 0 and "OK" in result.stdout:
                print("Interpreter: loaded [OK]")
            else:
                print(f"Interpreter: error loading [FAIL]")
                issues.append(f"Interpreter failed to load: {result.stderr}")
        except Exception as e:
            print(f"Interpreter: error [FAIL]")
            issues.append(f"Interpreter error: {e}")

    cwd = os.getcwd()
    config = os.path.join(cwd, "dipjo.json")
    if os.path.exists(config):
        print(f"Project config: dipjo.json [OK]")
    else:
        print(f"Project config: not found (optional)")

    print()
    if issues:
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All checks passed!")
    print()
    return len(issues)


if __name__ == "__main__":
    sys.exit(doctor())
