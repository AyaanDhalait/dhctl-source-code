import os
import subprocess
import shutil
import json
from pathlib import Path
import webbrowser

SHORTCUT_FILE = "dhctl_shortcuts.json"

def run(cmd):
    subprocess.run(cmd, check=True)

def load_shortcuts():
    if not os.path.exists(SHORTCUT_FILE):
        return {}
    with open(SHORTCUT_FILE, "r") as f:
        return json.load(f)

def save_shortcuts(data):
    with open(SHORTCUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def git_commit(file, repo):
    if not os.path.exists(".git"):
        run(["git", "init"])

    run(["git", "add", file])
    run(["git", "commit", "-m", "dhctl commit"])

    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout

    if "origin" not in remotes:
        run(["git", "remote", "add", "origin", repo])

    run(["git", "branch", "-M", "main"])
    run(["git", "push", "-u", "origin", "main"])

    print("Pushed via dhctl")

def add_shortcut(path, name):
    shortcuts = load_shortcuts()
    shortcuts[name] = path
    save_shortcuts(shortcuts)
    print("Shortcut added")

def open_shortcut(name):
    shortcuts = load_shortcuts()
    if name not in shortcuts:
        print("Shortcut not found")
        return
    os.startfile(shortcuts[name])

def run_server(file_path):
    if not os.path.exists(file_path):
        print("File not found")
        return

    folder = os.path.dirname(os.path.abspath(file_path))
    os.chdir(folder)

    url = f"http://localhost:8000/{os.path.basename(file_path)}"
    print("Running server:", url)

    webbrowser.open(url)
    run(["python", "-m", "http.server", "8000"])

def init_project(project_type):
    name = input("Project name: ").strip()
    os.makedirs(name, exist_ok=True)
    os.chdir(name)

    if project_type == "python":
        Path("main.py").write_text('print("Hello World")\n')

    elif project_type == "web":
        Path("index.html").write_text("<h1>Hello</h1>")

    elif project_type == "backend":
        os.makedirs("app", exist_ok=True)
        Path("app/main.py").write_text('print("Backend")\n')

    elif project_type == "api":
        os.makedirs("api", exist_ok=True)
        Path("api/main.py").write_text('print("API")\n')

    else:
        print("Unknown type")
        os.chdir("..")
        return

    Path("README.md").write_text("# " + name)
    run(["git", "init"])
    os.chdir("..")
    print("Project created")

def install_deps():
    if os.path.exists("requirements.txt"):
        run(["pip", "install", "-r", "requirements.txt"])
        print("Installed")
    elif os.path.exists("package.json"):
        run(["npm", "install"])
        print("Installed")
    else:
        print("No deps")

def clean_project():
    removed = 0
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d in ["__pycache__", "node_modules"]:
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                removed += 1
        for f in files:
            if f.endswith(".pyc") or f == ".DS_Store":
                try:
                    os.remove(os.path.join(root, f))
                    removed += 1
                except:
                    pass
    print("Cleaned:", removed)

def analyze_project():
    total = 0
    count = 0
    biggest = ("", 0)

    for root, dirs, files in os.walk("."):
        for f in files:
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
                if size > biggest[1]:
                    biggest = (path, size)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    total += len(file.readlines())
                    count += 1
            except:
                pass

    print("Files:", count)
    print("Lines:", total)
    print("Largest:", biggest[0])

def shell():
    print("dhctl interactive mode started")

    while True:
        q = input(">> ").strip()

        if q == "exit":
            break

        elif q == "help":
            print("init <type>")
            print("install")
            print("clean")
            print("analyze")
            print("git --commit <file> <repo>")
            print("add --shortcut <path> <name>")
            print("--open <name>")
            print("--run server <file>")
            print("exit")

        elif q.startswith("init"):
            parts = q.split()
            if len(parts) > 1:
                init_project(parts[1])

        elif q == "install":
            install_deps()

        elif q == "clean":
            clean_project()

        elif q == "analyze":
            analyze_project()

        elif q.startswith("git --commit"):
            parts = q.split()
            if len(parts) >= 4:
                git_commit(parts[2], parts[3])

        elif q.startswith("add --shortcut"):
            parts = q.split()
            if len(parts) >= 4:
                add_shortcut(parts[2], parts[3])

        elif q.startswith("--open"):
            parts = q.split()
            if len(parts) >= 2:
                open_shortcut(parts[1])

        elif q.startswith("--run server"):
            parts = q.split()
            if len(parts) >= 3:
                run_server(parts[2])

        else:
            print("Unknown command")

def handle(cmd):
    cmd = cmd.strip().lower()

    if cmd == "help":
        print("dhctl init <type>")
        print("dhctl install")
        print("dhctl clean")
        print("dhctl analyze")
        print("dhctl deploy")
        print("dhctl git --commit <file> <repo>")
        print("dhctl add --shortcut <path> <name>")
        print("dhctl --open <name>")
        print("dhctl --run server <file>")
        print("exit")
        return True

    if cmd.startswith("dhctl init"):
        parts = cmd.split()
        if len(parts) > 2:
            init_project(parts[2])
        return True

    if cmd == "dhctl install":
        install_deps()
        return True

    if cmd == "dhctl clean":
        clean_project()
        return True

    if cmd == "dhctl analyze":
        analyze_project()
        return True

    if cmd == "dhctl deploy":
        shell()
        return True

    if cmd.startswith("dhctl git --commit"):
        parts = cmd.split()
        if len(parts) >= 5:
            git_commit(parts[3], parts[4])
        return True

    if cmd.startswith("dhctl add --shortcut"):
        parts = cmd.split()
        if len(parts) >= 5:
            add_shortcut(parts[3], parts[4])
        return True

    if cmd.startswith("dhctl --open"):
        parts = cmd.split()
        if len(parts) >= 3:
            open_shortcut(parts[2])
        return True

    if cmd.startswith("dhctl --run server"):
        parts = cmd.split()
        if len(parts) >= 4:
            run_server(parts[3])
        return True

    if cmd == "exit":
        return False

    print("Unknown command")
    return True

print("© dhctl")
print("Enter help")

while True:
    q = input(">> ")
    if not handle(q):
        break