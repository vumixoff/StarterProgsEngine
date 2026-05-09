import os
import shutil
import random
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# =========================
# COLORS
# =========================

BG = "#0f1117"
CARD = "#1a1d26"

BLUE = "#3b82f6"
RED = "#ef4444"
PURPLE = "#8b5cf6"
ORANGE = "#f59e0b"
GREEN = "#22c55e"

TEXT = "white"

# =========================
# DATA
# =========================

apps = []
output_dir = os.getcwd()
icon_path = ""

# =========================
# FUNCTIONS
# =========================

def get_filename():

    name = filename_entry.get().strip()

    if not name:
        name = f"Launcher_{random.randint(1000,9999)}"

    return name

def add_programs():

    files = filedialog.askopenfilenames(
        title="Выберите программы",
        filetypes=[
            ("Programs", "*.exe *.bat *.cmd *.vbs")
        ]
    )

    for file in files:

        if file not in apps:

            apps.append(file)

            listbox.insert(
                tk.END,
                os.path.basename(file)
            )

def remove_selected():

    selected = listbox.curselection()

    for index in reversed(selected):

        apps.pop(index)
        listbox.delete(index)

def select_output():

    global output_dir

    folder = filedialog.askdirectory(
        title="Папка сохранения"
    )

    if folder:

        output_dir = folder

        output_label.config(
            text=f"📁 {output_dir}"
        )

def select_icon():

    global icon_path

    file = filedialog.askopenfilename(
        title="Выберите иконку",
        filetypes=[
            ("ICO files", "*.ico")
        ]
    )

    if file:

        icon_path = os.path.abspath(file)

        icon_label.config(
            text=f"🖼 {os.path.basename(file)}",
            fg="#8fff91"
        )

def create_bat():

    if not apps:

        messagebox.showerror(
            "Ошибка",
            "Добавьте программы"
        )

        return

    filename = get_filename()

    path = os.path.join(
        output_dir,
        f"{filename}.bat"
    )

    content = "@echo off\n\n"

    for app in apps:

        content += f'start "" "{app}"\n'

    with open(path, "w", encoding="utf-8") as f:

        f.write(content)

    messagebox.showinfo(
        "Готово",
        f"BAT создан:\n{path}"
    )

def create_vbs():

    if not apps:

        messagebox.showerror(
            "Ошибка",
            "Добавьте программы"
        )

        return

    filename = get_filename()

    path = os.path.join(
        output_dir,
        f"{filename}.vbs"
    )

    content = 'Set WshShell = CreateObject("WScript.Shell")\n\n'

    for app in apps:

        content += (
            f'WshShell.Run Chr(34) & "{app}" & Chr(34), 0, False\n'
        )

        content += 'WScript.Sleep 1000\n\n'

    with open(path, "w", encoding="utf-8") as f:

        f.write(content)

    messagebox.showinfo(
        "Готово",
        f"VBS создан:\n{path}"
    )

def create_exe():

    if not apps:

        messagebox.showerror(
            "Ошибка",
            "Добавьте программы"
        )

        return

    launcher_code = r'''
import subprocess
import time

CREATE_NO_WINDOW = 0x08000000

programs = [
%s
]

for prog in programs:

    try:

        subprocess.Popen(
            prog,
            creationflags=CREATE_NO_WINDOW
        )

        time.sleep(1)

    except:
        pass
''' % "\n".join(
        [f'    r"{p}",' for p in apps]
    )

    temp_py = os.path.join(
        output_dir,
        "launcher_temp.py"
    )

    with open(temp_py, "w", encoding="utf-8") as f:

        f.write(launcher_code)

    exe_name = get_filename()

    cmd = [
        "python",
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noupx",
        "--name",
        exe_name,
        "--distpath",
        output_dir,
        "--workpath",
        os.path.join(output_dir, "temp_build"),
        "--specpath",
        os.path.join(output_dir, "temp_spec")
    ]

    if icon_path and os.path.isfile(icon_path):

        cmd += [
            "--icon",
            icon_path
        ]

    cmd.append(temp_py)

    try:

        subprocess.run(
            cmd,
            check=True
        )

        # CLEANUP

        if os.path.exists(temp_py):
            os.remove(temp_py)

        build_dir = os.path.join(
            output_dir,
            "temp_build"
        )

        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        spec_dir = os.path.join(
            output_dir,
            "temp_spec"
        )

        if os.path.exists(spec_dir):
            shutil.rmtree(spec_dir)

        messagebox.showinfo(
            "Готово",
            f"EXE создан:\n{output_dir}\\{exe_name}.exe"
        )

    except Exception as e:

        messagebox.showerror(
            "Ошибка",
            str(e)
        )

# =========================
# WINDOW
# =========================

root = tk.Tk()

root.title("StarterProgsEngine")
root.geometry("1000x720")
root.minsize(900, 650)
root.configure(bg=BG)

# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="StarterProgsEngine",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 26, "bold")
)

title.pack(
    pady=(15, 10)
)

# =========================
# LISTBOX FRAME
# =========================

list_frame = tk.Frame(
    root,
    bg=CARD
)

list_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

listbox = tk.Listbox(
    list_frame,
    bg=CARD,
    fg="white",
    relief="flat",
    borderwidth=0,
    selectbackground=BLUE,
    font=("Consolas", 12)
)

listbox.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================
# INFO FRAME
# =========================

info_frame = tk.Frame(
    root,
    bg=BG
)

info_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

output_label = tk.Label(
    info_frame,
    text=f"📁 {output_dir}",
    bg=CARD,
    fg="#8fd3ff",
    anchor="w",
    padx=12,
    pady=10,
    font=("Consolas", 10)
)

output_label.pack(
    fill="x",
    pady=5
)

icon_label = tk.Label(
    info_frame,
    text="🖼 Иконка не выбрана",
    bg=CARD,
    fg="#ff8f8f",
    anchor="w",
    padx=12,
    pady=10,
    font=("Consolas", 10)
)

icon_label.pack(
    fill="x",
    pady=5
)

# =========================
# FILE NAME
# =========================

name_frame = tk.Frame(
    root,
    bg=BG
)

name_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

name_label = tk.Label(
    name_frame,
    text="📄 Название файла",
    bg=BG,
    fg="white",
    font=("Segoe UI", 11, "bold")
)

name_label.pack(
    anchor="w"
)

filename_entry = tk.Entry(
    name_frame,
    bg=CARD,
    fg="white",
    insertbackground="white",
    relief="flat",
    font=("Consolas", 12)
)

filename_entry.pack(
    fill="x",
    pady=8,
    ipady=10
)

filename_entry.insert(
    0,
    "StarterLauncher"
)

# =========================
# BUTTONS
# =========================

buttons_frame = tk.Frame(
    root,
    bg=BG
)

buttons_frame.pack(
    pady=10
)

top_buttons = tk.Frame(
    buttons_frame,
    bg=BG
)

top_buttons.pack(
    pady=5
)

bottom_buttons = tk.Frame(
    buttons_frame,
    bg=BG
)

bottom_buttons.pack(
    pady=5
)

def make_button(parent, text, command, color):

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        font=("Segoe UI", 11, "bold"),
        padx=18,
        pady=10
    )

    btn.pack(
        side="left",
        padx=6
    )

    return btn

# TOP BUTTONS

make_button(
    top_buttons,
    "➕ Добавить",
    add_programs,
    BLUE
)

make_button(
    top_buttons,
    "🗑 Удалить",
    remove_selected,
    RED
)

make_button(
    top_buttons,
    "📁 Папка",
    select_output,
    PURPLE
)

make_button(
    top_buttons,
    "🖼 Иконка",
    select_icon,
    ORANGE
)

# BOTTOM BUTTONS

make_button(
    bottom_buttons,
    "📄 BAT",
    create_bat,
    "#4b5563"
)

make_button(
    bottom_buttons,
    "👻 VBS",
    create_vbs,
    "#6b7280"
)

exe_button = tk.Button(
    bottom_buttons,
    text="🚀 СОЗДАТЬ EXE",
    command=create_exe,
    bg=GREEN,
    fg="white",
    activebackground=GREEN,
    activeforeground="white",
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    font=("Segoe UI", 11, "bold"),
    padx=30,
    pady=10
)

exe_button.pack(
    side="left",
    padx=6
)

root.mainloop()