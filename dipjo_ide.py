"""
Dipjo IDE - Full GUI Interface
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import subprocess


class DipjoIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Dipjo IDE")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0a0a2e")

        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dipjo.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.environ.get("USERPROFILE", ""), "Dipjo", "dipjo.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.current_file = None
        self.setup_ui()
        self.setup_tags()

    def setup_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg="#060618", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="Dipjo IDE", font=("Segoe UI", 16, "bold"),
                 fg="#00f5d4", bg="#060618").pack(side=tk.LEFT, padx=20, pady=10)

        # Menu buttons
        btn_style = {"bg": "#1a1a4e", "fg": "#00f5d4", "font": ("Segoe UI", 10),
                     "bd": 0, "padx": 15, "pady": 5, "cursor": "hand2"}

        tk.Button(title_frame, text="New", command=self.new_file, **btn_style).pack(side=tk.RIGHT, padx=5, pady=10)
        tk.Button(title_frame, text="Open", command=self.open_file, **btn_style).pack(side=tk.RIGHT, padx=5, pady=10)
        tk.Button(title_frame, text="Save", command=self.save_file, **btn_style).pack(side=tk.RIGHT, padx=5, pady=10)
        tk.Button(title_frame, text="Run", command=self.run_file, bg="#00f5d4", fg="#0a0a2e",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=5, cursor="hand2").pack(side=tk.RIGHT, padx=5, pady=10)

        # Main container
        main_frame = tk.Frame(self.root, bg="#0a0a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left panel - File explorer
        left_panel = tk.Frame(main_frame, bg="#080822", width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        tk.Label(left_panel, text="Files", font=("Segoe UI", 11, "bold"),
                 fg="#00f5d4", bg="#080822", anchor="w").pack(fill=tk.X, padx=10, pady=5)

        self.file_list = tk.Listbox(left_panel, bg="#080822", fg="#a0a0d0",
                                     selectbackground="#1a1a4e", selectforeground="#00f5d4",
                                     font=("Consolas", 10), bd=0, highlightthickness=0)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_list.bind("<<ListboxSelect>>", self.on_file_select)

        self.load_files()

        # Center panel - Code editor
        center_panel = tk.Frame(main_frame, bg="#0a0a2e")
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Editor header
        editor_header = tk.Frame(center_panel, bg="#0d0d2b")
        editor_header.pack(fill=tk.X)

        self.file_label = tk.Label(editor_header, text="untitled.dipjo",
                                    font=("Consolas", 10), fg="#5a5a8e", bg="#0d0d2b", anchor="w")
        self.file_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Line numbers
        line_frame = tk.Frame(center_panel, bg="#0a0a2e")
        line_frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(line_frame, width=4, bg="#060618", fg="#5a5a8e",
                                     font=("Consolas", 11), bd=0, highlightthickness=0,
                                     state="disabled", padx=5)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Code editor
        self.editor = scrolledtext.ScrolledText(line_frame, bg="#0d0d2b", fg="#e0e0ff",
                                                 insertbackground="#00f5d4",
                                                 selectbackground="#3a3a7e",
                                                 font=("Consolas", 11), bd=0,
                                                 highlightthickness=0, wrap=tk.NONE,
                                                 undo=True)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<ButtonRelease-1>", self.on_key_release)
        self.editor.bind("<MouseWheel>", self.on_scroll)

        # Right panel - Output
        right_panel = tk.Frame(main_frame, bg="#080822", width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

        tk.Label(right_panel, text="Output", font=("Segoe UI", 11, "bold"),
                 fg="#00f5d4", bg="#080822", anchor="w").pack(fill=tk.X, padx=10, pady=5)

        self.output = scrolledtext.ScrolledText(right_panel, bg="#060618", fg="#e0e0ff",
                                                 font=("Consolas", 10), bd=0,
                                                 highlightthickness=0, state="disabled")
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bottom bar
        bottom_bar = tk.Frame(self.root, bg="#060618", height=30)
        bottom_bar.pack(fill=tk.X)
        bottom_bar.pack_propagate(False)

        tk.Label(bottom_bar, text="Dipjo v1.0", font=("Segoe UI", 9),
                 fg="#5a5a8e", bg="#060618").pack(side=tk.LEFT, padx=10)
        tk.Label(bottom_bar, text="Language: Dipjo", font=("Segoe UI", 9),
                 fg="#5a5a8e", bg="#060618").pack(side=tk.RIGHT, padx=10)

    def setup_tags(self):
        # Syntax highlighting tags
        self.editor.tag_configure("keyword", foreground="#9b5de5")
        self.editor.tag_configure("declaration", foreground="#00bbf9")
        self.editor.tag_configure("string", foreground="#00f5d4")
        self.editor.tag_configure("number", foreground="#ffbe0b")
        self.editor.tag_configure("boolean", foreground="#ff6b6b")
        self.editor.tag_configure("comment", foreground="#5a5a8e", font=("Consolas", 11, "italic"))
        self.editor.tag_configure("function", foreground="#00bbf9")
        self.editor.tag_configure("operator", foreground="#ffbe0b")
        self.editor.tag_configure("type", foreground="#ff6b6b")

        self.output.tag_configure("prompt", foreground="#00f5d4")
        self.output.tag_configure("output", foreground="#a0a0d0")
        self.output.tag_configure("error", foreground="#ff6b6b")
        self.output.tag_configure("success", foreground="#00f5d4")

    def highlight_syntax(self):
        code = self.editor.get("1.0", tk.END)

        for tag in ["keyword", "declaration", "string", "number", "boolean",
                     "comment", "function", "operator", "type"]:
            self.editor.tag_remove(tag, "1.0", tk.END)

        keywords = ["if", "otherwise", "finish", "repeat", "while", "for", "every",
                     "define", "function", "give", "back", "run", "return"]
        declarations = ["create", "remember", "set", "as"]
        types = ["number", "text", "truth", "list", "letter"]
        operators = ["add", "subtract", "multiply", "divide", "increase", "decrease",
                     "plus", "minus", "times", "divided", "by", "to", "from", "into"]
        comparisons = ["is", "equal", "not", "greater", "less", "than", "or", "and"]
        builtins = ["say", "ask", "put", "remove", "save", "in", "note", "using"]
        booleans = ["true", "false"]

        lines = code.split("\n")
        for i, line in enumerate(lines):
            line_num = f"{i+1}.0"

            if line.strip().startswith("note"):
                self.editor.tag_add("comment", line_num, f"{line_num}+{len(line)}c")
                continue

            for word in keywords:
                start = "1.0"
                while True:
                    pos = self.editor.search(rf"\b{word}\b", start, stopindex=tk.END, regexp=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    self.editor.tag_add("keyword", pos, end)
                    start = end

            for word in declarations:
                start = "1.0"
                while True:
                    pos = self.editor.search(rf"\b{word}\b", start, stopindex=tk.END, regexp=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    self.editor.tag_add("declaration", pos, end)
                    start = end

            for word in types:
                start = "1.0"
                while True:
                    pos = self.editor.search(rf"\b{word}\b", start, stopindex=tk.END, regexp=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    self.editor.tag_add("type", pos, end)
                    start = end

            for word in booleans:
                start = "1.0"
                while True:
                    pos = self.editor.search(rf"\b{word}\b", start, stopindex=tk.END, regexp=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    self.editor.tag_add("boolean", pos, end)
                    start = end

        # Highlight strings
        start = "1.0"
        while True:
            pos = self.editor.search('"', start, stopindex=tk.END)
            if not pos:
                break
            end = self.editor.search('"', f"{pos}+1c", stopindex=tk.END)
            if end:
                self.editor.tag_add("string", pos, f"{end}+1c")
                start = f"{end}+1c"
            else:
                break

        # Highlight numbers
        start = "1.0"
        while True:
            pos = self.editor.search(r"\b\d+\.?\d*\b", start, stopindex=tk.END, regexp=True)
            if not pos:
                break
            match_end = pos
            while True:
                next_char = self.editor.get(match_end)
                if next_char.isdigit() or next_char == ".":
                    match_end = f"{match_end}+1c"
                else:
                    break
            self.editor.tag_add("number", pos, match_end)
            start = match_end

    def update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        line_count = self.editor.get("1.0", tk.END).count("\n")
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")

    def on_key_release(self, event=None):
        self.highlight_syntax()
        self.update_line_numbers()

    def on_scroll(self, event):
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
        self.editor.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def load_files(self):
        self.file_list.delete(0, tk.END)
        self.file_list.insert(tk.END, "hello.dipjo")
        self.file_list.insert(tk.END, "welcome.dipjo")
        self.file_list.insert(tk.END, "fibonacci.dipjo")
        self.file_list.insert(tk.END, "test_all.dipjo")

    def on_file_select(self, event):
        selection = self.file_list.curselection()
        if selection:
            filename = self.file_list.get(selection[0])
            self.load_example(filename)

    def load_example(self, filename):
        examples_dir = os.path.join(os.environ["USERPROFILE"], "Dipjo", "examples")
        filepath = os.path.join(examples_dir, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.file_label.config(text=filename)
            self.current_file = filepath
            self.on_key_release()

    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.file_label.config(text="untitled.dipjo")
        self.current_file = None

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Dipjo files", "*.dipjo"), ("All files", "*.*")]
        )
        if filepath:
            with open(filepath, "r") as f:
                content = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.file_label.config(text=os.path.basename(filepath))
            self.current_file = filepath
            self.on_key_release()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.editor.get("1.0", tk.END))
        else:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".dipjo",
                filetypes=[("Dipjo files", "*.dipjo"), ("All files", "*.*")]
            )
            if filepath:
                with open(filepath, "w") as f:
                    f.write(self.editor.get("1.0", tk.END))
                self.current_file = filepath
                self.file_label.config(text=os.path.basename(filepath))

    def run_file(self):
        code = self.editor.get("1.0", tk.END)

        if not code.strip():
            return

        # Save to temp file
        temp_file = os.path.join(os.environ["USERPROFILE"], "Dipjo", "_temp_run.dipjo")
        with open(temp_file, "w") as f:
            f.write(code)

        # Run
        main_py = os.path.join(os.environ["USERPROFILE"], "Dipjo", "main.py")

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Running...\n", "prompt")
        self.output.config(state="disabled")

        try:
            result = subprocess.run(
                [sys.executable, main_py, temp_file],
                capture_output=True, text=True, timeout=10
            )

            self.output.config(state="normal")
            self.output.delete("1.0", tk.END)

            if result.stdout:
                self.output.insert(tk.END, result.stdout, "output")
            if result.stderr:
                self.output.insert(tk.END, result.stderr, "error")

            self.output.config(state="disabled")

        except subprocess.TimeoutExpired:
            self.output.config(state="normal")
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Error: Execution timed out\n", "error")
            self.output.config(state="disabled")

        except Exception as e:
            self.output.config(state="normal")
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Error: {str(e)}\n", "error")
            self.output.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = DipjoIDE(root)
    root.mainloop()
