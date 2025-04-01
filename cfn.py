import tkinter as tk
from tkinter import font, messagebox, filedialog, ttk
import random
import math
import time
from datetime import datetime
import os
import sys
import webbrowser
import string
import pyperclip
import requests
import zxcvbn
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# ==== NINJA MASTER CONSTANTS ==== #
THEMES = {
    "NEO-TOKYO": {
        "background": "#0A0A12",
        "primary": "#FF2A6D",
        "secondary": "#05D9E8",
        "accent": "#D300C5",
        "text": "#E0E0E0",
        "warning": "#FF2C55",
        "terminal": "#05D9E8",
        "highlight": "#00D1FF",
        "panel": "#1A1A2E",
        "scanline": "#004D2E",
        "button_bg": "#252538",
        "button_text": "#FFFFFF",
        "title_bar": "#1A1A2E",
        "border": "#05D9E8",
        "input_bg": "#2A2A3A",
        "placeholder": "#666677"
    },
    "MATRIX": {
        "background": "#000000",
        "primary": "#00FF41",
        "secondary": "#008F11",
        "accent": "#00FF41",
        "text": "#00FF41",
        "warning": "#FF2C55",
        "terminal": "#00FF41",
        "highlight": "#00FF41",
        "panel": "#0A0A0A",
        "scanline": "#003B00",
        "button_bg": "#0A0A0A",
        "button_text": "#00FF41",
        "title_bar": "#0A0A0A",
        "border": "#008F11",
        "input_bg": "#0F0F0F",
        "placeholder": "#007700"
    },
    "CYBERPUNK": {
        "background": "#121230",
        "primary": "#FF2A6D",
        "secondary": "#18FFDB",
        "accent": "#FF2A6D",
        "text": "#FFFFFF",
        "warning": "#FF2C55",
        "terminal": "#18FFDB",
        "highlight": "#FF2A6D",
        "panel": "#1E1E3E",
        "scanline": "#004D4D",
        "button_bg": "#252545",
        "button_text": "#FFFFFF",
        "title_bar": "#1E1E3E",
        "border": "#18FFDB",
        "input_bg": "#2A2A4A",
        "placeholder": "#666688"
    }
}

COLOR_SCHEME = THEMES["NEO-TOKYO"]

FONTS = {
    "main": ("Consolas", "Courier New", "monospace", 12),
    "title": ("OCR A Extended", "Consolas", "Courier New", "monospace", 22),
    "button": ("Consolas", "Courier New", "monospace", 11),
    "tutorial": ("Segoe UI", "Arial", "Helvetica", 10)
}

LEET_LEVELS = {
    1: {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'},
    2: {'a': '@', 'b': '8', 'e': '3', 'g': '9', 'i': '1', 'o': '0', 's': '5', 't': '7', 'z': '2'},
    3: {'a': '@', 'b': '|3', 'e': '3', 'g': '9', 'i': '!', 'o': '0', 's': '§', 't': '+', 'z': '2'},
    4: {'a': '4', 'b': 'ß', 'e': '€', 'g': '6', 'i': '1', 'o': 'ø', 's': 'z', 't': '†', 'z': '7'},
    5: {'a': 'λ', 'b': 'β', 'e': 'ε', 'g': 'ϑ', 'i': 'ι', 'o': 'Ω', 's': 'σ', 't': 'τ', 'z': 'ζ'},
    6: {'a': '₳', 'b': '฿', 'e': '£', 'g': '₲', 'i': 'ł', 'o': 'Ø', 's': '₴', 't': '₮', 'z': '☡'},
    7: {'a': '∀', 'b': 'ᙠ', 'e': '∃', 'g': 'Ꮹ', 'i': 'ꟾ', 'o': '⊗', 's': 'ᙣ', 't': '⟙', 'z': 'ꙁ'}
}

PREFIXES = ["Cyber", "Null", "Ghost", "Crypto", "Neo", "Byte", "Phantom", "Stealth", "Digital", "Quantum", "Neuro", "Synth"]
SUFFIXES = ["X", "H4X", "1337", "Virus", "Crypto", "Root", "Exploit", "Bot", "Overlord", "Killer", "Worm", "RAT"]

EXPORT_FOLDER = "CyberForge_Exports"
DEFAULT_BULK_COUNT = 10
MAX_HISTORY = 50

# ==== NINJA AI INTEGRATION ==== #
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/chat/completions"
DEEPSEEK_API_KEY = ""

class CyberButton(tk.Canvas):
    def __init__(self, master, text, command, width=140, height=45, **kwargs):
        super().__init__(master, highlightthickness=0, width=width, height=height, **kwargs)
        self.command = command
        self.text = text
        self.active = False
        
        # Glowing button effect
        self.glow = self.create_oval(0, 0, width, height, 
                                   fill=COLOR_SCHEME["button_bg"], outline="")
        self.button = self.create_rectangle(5, 5, width-5, height-5, 
                                          fill=COLOR_SCHEME["button_bg"], outline=COLOR_SCHEME["border"])
        
        # Holographic text
        self.text_id = self.create_text(width/2, height/2, 
                                      text=text, fill=COLOR_SCHEME["button_text"],
                                      font=("Courier New", 11, "bold"))
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def on_click(self, event):
        self.itemconfig(self.button, fill=COLOR_SCHEME["panel"])
        self.flash()
        
    def on_release(self, event):
        self.itemconfig(self.button, fill=COLOR_SCHEME["button_bg"])
        self.command()
        
    def on_enter(self, event):
        self.active = True
        self.itemconfig(self.button, outline=COLOR_SCHEME["highlight"])
        self.start_glow()
        
    def on_leave(self, event):
        self.active = False
        self.itemconfig(self.button, outline=COLOR_SCHEME["border"])
        self.itemconfig(self.button, fill=COLOR_SCHEME["button_bg"])
        self.itemconfig(self.glow, fill=COLOR_SCHEME["button_bg"])
        
    def flash(self):
        colors = [COLOR_SCHEME["highlight"], COLOR_SCHEME["accent"]]
        for i, color in enumerate(colors * 2):
            self.after(i * 100, lambda c=color: self.itemconfig(self.button, outline=c))
            
    def start_glow(self):
        if self.active:
            alpha = 100 + 155 * abs(math.sin(time.time() * 2))
            glow_color = self.blend_colors(COLOR_SCHEME["primary"], COLOR_SCHEME["button_bg"], alpha/255)
            self.itemconfig(self.glow, fill=glow_color)
            self.after(50, self.start_glow)
            
    def blend_colors(self, color1, color2, ratio):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 * ratio + r2 * (1 - ratio))
        g = int(g1 * ratio + g2 * (1 - ratio))
        b = int(b1 * ratio + b2 * (1 - ratio))
        return f"#{r:02x}{g:02x}{b:02x}"

class HackerNameGenerator:
    def __init__(self):
        self.settings = {
            "leet_level": 3,
            "use_prefix": True,
            "use_suffix": True,
            "add_numbers": False,
            "random_case": True,
            "double_transform": False,
            "add_special_chars": False,
            "military_style": False,
            "separator": "_"
        }
        self.history = []

    def generate(self, name):
        if not name.strip(): return "NULL_INPUT_ERROR"
        
        leet_map = LEET_LEVELS.get(self.settings["leet_level"], LEET_LEVELS[3])
        result = []
        
        for char in name.lower():
            if char in leet_map and random.random() < 0.75:
                transformed = leet_map[char]
                if self.settings["double_transform"] and random.random() < 0.3:
                    transformed = self.double_transform(transformed)
                result.append(transformed)
            else:
                if self.settings["random_case"] and random.random() > 0.5:
                    result.append(char.upper())
                else:
                    result.append(char)
        
        generated = ''.join(result)
        
        # Add components
        sep = self.settings["separator"]
        
        if self.settings["use_prefix"] and random.random() < 0.5:
            prefix = random.choice(PREFIXES)
            if self.settings["military_style"]:
                prefix = prefix.upper()[:3] + "-"
            generated = f"{prefix}{sep}{generated}"
            
        if self.settings["use_suffix"] and random.random() < 0.5:
            suffix = random.choice(SUFFIXES)
            if self.settings["military_style"]:
                suffix = "-" + suffix.upper()[:3]
            generated = f"{generated}{sep}{suffix}"
            
        if self.settings["add_numbers"]:
            generated += str(random.choice([random.randint(0,9), random.randint(10,99), random.randint(100,999)]))
            
        if self.settings["add_special_chars"] and random.random() < 0.3:
            generated = self.add_special_chars(generated)
            
        # Add to history
        self.history.append(generated.replace(" ", "_"))
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)
            
        return self.history[-1]
    
    def double_transform(self, char):
        transformations = {
            '@': '4',
            '3': 'ε',
            '1': '|',
            '0': '()',
            '$': '§',
            '7': '⊥'
        }
        return transformations.get(char, char)
    
    def add_special_chars(self, text):
        specials = ["!", "#", "$", "%", "&", "*", "+", "-", ":", ";", "=", "?", "@", "~"]
        pos = random.randint(1, len(text)-1)
        return text[:pos] + random.choice(specials) + text[pos:]

class PasswordGenerator:
    def __init__(self):
        self.settings = {
            "length": 12,
            "use_uppercase": True,
            "use_lowercase": True,
            "use_digits": True,
            "use_special": True,
            "avoid_ambiguous": False,
            "no_repeating": True
        }
        self.history = []
    
    def generate(self):
        characters = ""
        
        if self.settings["use_lowercase"]:
            characters += string.ascii_lowercase
        if self.settings["use_uppercase"]:
            characters += string.ascii_uppercase
        if self.settings["use_digits"]:
            characters += string.digits
        if self.settings["use_special"]:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if self.settings["avoid_ambiguous"]:
            characters = characters.replace('l', '').replace('1', '').replace('I', '')
            characters = characters.replace('O', '').replace('0', '')
            characters = characters.replace('|', '').replace('\\', '').replace('/', '')
        
        if not characters:
            return "NO_CHARACTERS_SELECTED"
        
        password = []
        last_char = None
        
        for _ in range(self.settings["length"]):
            char = random.choice(characters)
            if self.settings["no_repeating"] and char == last_char:
                while char == last_char:
                    char = random.choice(characters)
            password.append(char)
            last_char = char
        
        generated = ''.join(password)
        self.history.append(generated)
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)
            
        return generated

class CyberForge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CYBERFORGE NINJA v12.0")
        self.geometry("1200x900")
        self.minsize(1000, 750)
        
        # Custom title bar
        self.overrideredirect(True)
        self.create_title_bar()
        
        # Core components
        self.generator = HackerNameGenerator()
        self.password_gen = PasswordGenerator()
        self.create_widgets()
        self.setup_cyber_effects()
        self.create_footer()
        
        # Show tutorial on first run
        self.first_run = True
        self.after(1000, self.show_tutorial)
        
        # Zoom level
        self.zoom_level = 1.0
        self.bind("<Control-MouseWheel>", self.zoom)
        
        # Make window draggable
        self.bind("<B1-Motion>", self.move_window)
        self.bind("<Button-1>", self.get_pos)

    def create_title_bar(self):
        title_bar = tk.Frame(self, bg=COLOR_SCHEME["title_bar"], height=30)
        title_bar.pack(fill=tk.X)
        
        title_label = tk.Label(title_bar, text="⌘ CYBERFORGE NINJA v12.0", 
                             bg=COLOR_SCHEME["title_bar"], fg=COLOR_SCHEME["primary"],
                             font=("Courier New", 10, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Label(title_bar, text="✕", bg=COLOR_SCHEME["title_bar"],
                           fg=COLOR_SCHEME["text"], font=("Courier New", 12))
        close_btn.pack(side=tk.RIGHT, padx=10)
        close_btn.bind("<Button-1>", lambda e: self.destroy())
        
        title_bar.bind("<B1-Motion>", self.move_window)
        title_bar.bind("<Button-1>", self.get_pos)
        
    def move_window(self, event):
        self.geometry(f"+{event.x_root-self.x}+{event.y_root-self.y}")
        
    def get_pos(self, event):
        self.x = event.x
        self.y = event.y
        
    def create_widgets(self):
        # Main container with notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=(32,2))
        
        # Main tab
        self.main_frame = tk.Frame(self.notebook, bg=COLOR_SCHEME["background"])
        self.notebook.add(self.main_frame, text="Hacker ID")
        
        # Password Generator tab
        self.password_frame = tk.Frame(self.notebook, bg=COLOR_SCHEME["background"])
        self.notebook.add(self.password_frame, text="Password Gen")
        self.create_password_generator()
        
        # Tutorial tab
        self.tutorial_frame = tk.Frame(self.notebook, bg=COLOR_SCHEME["background"])
        self.notebook.add(self.tutorial_frame, text="Tutorial")
        self.create_tutorial_content()
        
        # Stats tab
        self.stats_frame = tk.Frame(self.notebook, bg=COLOR_SCHEME["background"])
        self.notebook.add(self.stats_frame, text="Stats")
        self.create_stats_content()
        
        # AI Settings tab
        self.ai_frame = tk.Frame(self.notebook, bg=COLOR_SCHEME["background"])
        self.notebook.add(self.ai_frame, text="AI Settings")
        self.create_ai_settings()
        
        # Header with cyber effects
        self.header = tk.Canvas(self.main_frame, bg=COLOR_SCHEME["background"],
                              height=80, highlightthickness=0)
        self.header.pack(fill=tk.X, pady=(0,10))
        
        self.header.create_text(600, 40, text="HACKER IDENTITY GENERATOR",
                              font=("OCR A Extended", 20, "bold"),
                              fill=COLOR_SCHEME["primary"])
        
        # Input section
        input_frame = tk.Frame(self.main_frame, bg=COLOR_SCHEME["background"])
        input_frame.pack(pady=10)
        
        self.entry = tk.Entry(input_frame, width=30, 
                            font=("Courier New", 12),
                            bg=COLOR_SCHEME["input_bg"], fg=COLOR_SCHEME["placeholder"],
                            insertbackground=COLOR_SCHEME["primary"],
                            relief=tk.FLAT, highlightthickness=1,
                            highlightbackground=COLOR_SCHEME["border"],
                            highlightcolor=COLOR_SCHEME["highlight"])
        self.entry.pack(side=tk.LEFT, padx=5, ipady=5)
        self.entry.insert(0, "Enter your name")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.add_placeholder)
        self.entry.bind("<Return>", lambda e: self.generate_name())
        
        self.gen_btn = CyberButton(input_frame, "GENERATE", self.generate_name, width=120, height=40)
        self.gen_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings panel
        self.create_hacker_settings(self.main_frame)
        
        # Output terminal with scrollbar
        output_frame = tk.Frame(self.main_frame, bg=COLOR_SCHEME["panel"])
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output = tk.Text(output_frame, height=12, width=60,
                            bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["terminal"],
                            font=("Courier New", 12), 
                            wrap=tk.WORD,
                            insertbackground=COLOR_SCHEME["primary"],
                            relief=tk.FLAT, yscrollcommand=scrollbar.set,
                            padx=10, pady=10)
        self.output.pack(fill=tk.BOTH, expand=True)
        
        self.output_menu = tk.Menu(self.output, tearoff=0)
        self.output_menu.add_command(label="Copy", command=self.copy_output)
        self.output_menu.add_command(label="Clear", command=self.clear_output)
        self.output_menu.add_command(label="Edit Last", command=self.edit_last_output)
        self.output.bind("<Button-3>", self.show_output_menu)
        
        scrollbar.config(command=self.output.yview)
        
        self.cursor_visible = True
        self.blink_cursor()
        
    def create_password_generator(self):
        settings_frame = tk.Frame(self.password_frame, bg=COLOR_SCHEME["panel"])
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Length control
        length_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        length_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(length_frame, text="Length:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 9)).pack(side=tk.LEFT)
        
        self.pwd_length = tk.IntVar(value=12)
        
        # Fixed slider to prevent window dragging
        def on_slider_move(event):
            # Prevent window dragging when interacting with slider
            return "break"
        
        self.pwd_length_slider = tk.Scale(length_frame, from_=8, to=64, orient=tk.HORIZONTAL,
                                        variable=self.pwd_length, bg=COLOR_SCHEME["panel"],
                                        fg=COLOR_SCHEME["text"], highlightthickness=0,
                                        sliderrelief=tk.FLAT)
        self.pwd_length_slider.bind("<B1-Motion>", on_slider_move)
        self.pwd_length_slider.bind("<ButtonPress-1>", on_slider_move)
        self.pwd_length_slider.bind("<ButtonRelease-1>", on_slider_move)
        self.pwd_length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Character types
        types_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        types_frame.pack(fill=tk.X, pady=5)
        
        self.pwd_upper = tk.BooleanVar(value=True)
        tk.Checkbutton(types_frame, text="Uppercase", variable=self.pwd_upper,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        self.pwd_lower = tk.BooleanVar(value=True)
        tk.Checkbutton(types_frame, text="Lowercase", variable=self.pwd_lower,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        self.pwd_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(types_frame, text="Digits", variable=self.pwd_digits,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        self.pwd_special = tk.BooleanVar(value=True)
        tk.Checkbutton(types_frame, text="Special", variable=self.pwd_special,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        # Options
        options_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        options_frame.pack(fill=tk.X, pady=5)
        
        self.pwd_no_ambiguous = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Avoid Ambiguous", variable=self.pwd_no_ambiguous,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        self.pwd_no_repeat = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="No Repeating", variable=self.pwd_no_repeat,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        # Dark Web Mode toggle
        self.darkweb_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="DARK WEB MODE", variable=self.darkweb_var,
                     bg=COLOR_SCHEME["panel"], fg="#FF2C55", font=("Courier New", 9, "bold"),
                     selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT, padx=5)
        
        # Password strength meter
        self.strength_frame = tk.Frame(options_frame, bg=COLOR_SCHEME["panel"])
        self.strength_frame.pack(side=tk.RIGHT, padx=5)
        
        self.strength_label = tk.Label(self.strength_frame, text="STRENGTH:", 
                                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"])
        self.strength_label.pack(side=tk.LEFT)
        
        self.strength_meter = tk.Canvas(self.strength_frame, width=200, height=20, 
                                      bg=COLOR_SCHEME["panel"], highlightthickness=0)
        self.strength_meter.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        btn_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.pwd_generate_btn = CyberButton(btn_frame, "GENERATE PASSWORD", self.generate_password, width=180, height=40)
        self.pwd_generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.pwd_bulk_btn = CyberButton(btn_frame, "BULK GENERATE", self.bulk_generate_passwords, width=150, height=40)
        self.pwd_bulk_btn.pack(side=tk.LEFT, padx=5)
        
        # Password display
        display_frame = tk.Frame(self.password_frame, bg=COLOR_SCHEME["panel"])
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pwd_output = tk.Text(display_frame, height=12, width=60,
                                bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["terminal"],
                                font=("Courier New", 12), 
                                wrap=tk.WORD,
                                insertbackground=COLOR_SCHEME["primary"],
                                relief=tk.FLAT, yscrollcommand=scrollbar.set,
                                padx=10, pady=10)
        self.pwd_output.pack(fill=tk.BOTH, expand=True)
        
        self.pwd_output_menu = tk.Menu(self.pwd_output, tearoff=0)
        self.pwd_output_menu.add_command(label="Copy", command=lambda: self.copy_output(self.pwd_output))
        self.pwd_output_menu.add_command(label="Clear", command=lambda: self.clear_output(self.pwd_output))
        self.pwd_output.bind("<Button-3>", lambda e: self.show_output_menu(e, self.pwd_output_menu))
        
        scrollbar.config(command=self.pwd_output.yview)
        
    def create_ai_settings(self):
        settings_frame = tk.Frame(self.ai_frame, bg=COLOR_SCHEME["panel"])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        api_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        api_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(api_frame, text="DeepSeek API Key:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 10)).pack(side=tk.LEFT)
        
        self.api_key_entry = tk.Entry(api_frame, width=50, show="*",
                                    bg=COLOR_SCHEME["input_bg"], fg=COLOR_SCHEME["text"],
                                    font=("Courier New", 10))
        self.api_key_entry.pack(side=tk.LEFT, padx=5)
        
        self.show_key_var = tk.BooleanVar(value=False)
        tk.Checkbutton(api_frame, text="Show", variable=self.show_key_var,
                      command=self.toggle_api_key_visibility,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(side=tk.LEFT)
        
        test_btn = CyberButton(settings_frame, "TEST CONNECTION", self.test_ai_connection, width=180, height=35)
        test_btn.pack(pady=10)
        
        self.ai_status = tk.Label(settings_frame, text="Status: Disconnected", 
                                bg=COLOR_SCHEME["panel"], fg="#FF2C55",
                                font=("Courier New", 10))
        self.ai_status.pack(pady=5)
        
        self.ai_backstory_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings_frame, text="Generate Backstory with AI", 
                      variable=self.ai_backstory_var,
                      bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      selectcolor=COLOR_SCHEME["panel"]).pack(pady=10)
        
        custom_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        custom_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(custom_frame, text="Backstory Style:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 9)).pack(side=tk.LEFT)
        
        self.backstory_style = tk.StringVar(value="cyberpunk")
        styles = ["cyberpunk", "military", "spy", "hacker", "fantasy", "sci-fi"]
        style_menu = tk.OptionMenu(custom_frame, self.backstory_style, *styles)
        style_menu.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                        activebackground=COLOR_SCHEME["panel"],
                        activeforeground=COLOR_SCHEME["text"],
                        highlightthickness=0)
        style_menu.pack(side=tk.LEFT, padx=5)
        
        # AI Features Frame
        ai_features_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        ai_features_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(ai_features_frame, text="AI Features:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 10)).pack(side=tk.LEFT)
        
        # Password Suggestion Button
        self.ai_password_suggest = CyberButton(ai_features_frame, "PASSWORD SUGGEST", 
                                             self.ai_suggest_password, width=180, height=35)
        self.ai_password_suggest.pack(side=tk.LEFT, padx=5)
        
        # Name Analysis Button
        self.ai_name_analyze = CyberButton(ai_features_frame, "NAME ANALYSIS", 
                                         self.ai_analyze_name, width=150, height=35)
        self.ai_name_analyze.pack(side=tk.LEFT, padx=5)
        
        # AI Output Display
        ai_output_frame = tk.Frame(settings_frame, bg=COLOR_SCHEME["panel"])
        ai_output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(ai_output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ai_output = tk.Text(ai_output_frame, height=10, width=60,
                               bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["terminal"],
                               font=("Courier New", 10), 
                               wrap=tk.WORD,
                               insertbackground=COLOR_SCHEME["primary"],
                               relief=tk.FLAT, yscrollcommand=scrollbar.set,
                               padx=10, pady=10)
        self.ai_output.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.ai_output.yview)
        
    def toggle_api_key_visibility(self):
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
            
    def test_ai_connection(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            self.ai_status.config(text="Status: No API key provided", fg="#FF2C55")
            return
            
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [{
                    "role": "user",
                    "content": "Test connection"
                }],
                "max_tokens": 5
            }
            
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                self.ai_status.config(text="Status: Connected", fg="#2CFF5A")
                global DEEPSEEK_API_KEY
                DEEPSEEK_API_KEY = api_key
                self.ai_output.insert(tk.END, "> AI Connection Successful!\n")
            else:
                self.ai_status.config(text=f"Status: Error {response.status_code}", fg="#FF2C55")
                self.ai_output.insert(tk.END, f"> Connection Error: {response.status_code}\n")
        except Exception as e:
            self.ai_status.config(text=f"Status: Connection failed - {str(e)}", fg="#FF2C55")
            self.ai_output.insert(tk.END, f"> Connection Failed: {str(e)}\n")
            
    def generate_hacker_backstory(self, name, alias):
        if not DEEPSEEK_API_KEY or not self.ai_backstory_var.get():
            return ""
            
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        style = self.backstory_style.get()
        prompt = f"Generate a {style} backstory for {name} aka '{alias}' in 50 words. Include: origin, signature hacks, enemies, and a cryptic warning."
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.9
        }
        
        try:
            self.ai_output.insert(tk.END, "> Generating backstory...\n")
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                self.ai_output.insert(tk.END, f"> Backstory generated successfully!\n")
                return result
            else:
                return f"> BACKSTORY ERROR: API returned {response.status_code}"
        except Exception as e:
            return f"> BACKSTORY ERROR: {str(e)}"
            
    def ai_suggest_password(self):
        if not DEEPSEEK_API_KEY:
            self.ai_output.insert(tk.END, "> ERROR: No API key configured\n")
            return
            
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = ("Suggest 3 highly secure passwords with these requirements:\n"
                 f"- Length: {self.pwd_length.get()}\n"
                 f"- Uppercase: {'Yes' if self.pwd_upper.get() else 'No'}\n"
                 f"- Lowercase: {'Yes' if self.pwd_lower.get() else 'No'}\n"
                 f"- Digits: {'Yes' if self.pwd_digits.get() else 'No'}\n"
                 f"- Special: {'Yes' if self.pwd_special.get() else 'No'}\n"
                 f"- Avoid ambiguous: {'Yes' if self.pwd_no_ambiguous.get() else 'No'}\n"
                 "Format as a numbered list with entropy estimates")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            self.ai_output.insert(tk.END, "> Requesting password suggestions from AI...\n")
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                self.ai_output.insert(tk.END, f"\n> AI Password Suggestions:\n{result}\n")
                
                # Extract passwords and add to history
                lines = result.split('\n')
                for line in lines:
                    if any(c.isupper() for c in line) and any(c.islower() for c in line) and len(line) >= 8:
                        pwd = line.split('. ')[-1].strip()
                        if len(pwd) == self.pwd_length.get():
                            self.password_gen.history.append(pwd)
                            if len(self.password_gen.history) > MAX_HISTORY:
                                self.password_gen.history.pop(0)
            else:
                self.ai_output.insert(tk.END, f"> Error: {response.status_code}\n")
        except Exception as e:
            self.ai_output.insert(tk.END, f"> Error: {str(e)}\n")
            
    def ai_analyze_name(self):
        if not DEEPSEEK_API_KEY:
            self.ai_output.insert(tk.END, "> ERROR: No API key configured\n")
            return
            
        name = self.entry.get().strip()
        if not name or name == "Enter your name":
            self.ai_output.insert(tk.END, "> ERROR: No name to analyze\n")
            return
            
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = (f"Analyze the name '{name}' for hacker alias potential. Consider:\n"
                 "- Phonetic qualities\n"
                 "- Ease of memorization\n"
                 "- Potential leet transformations\n"
                 "- Cultural/linguistic associations\n"
                 "- Suggested improvements\n"
                 "Provide a detailed analysis in 100 words or less")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.8,
            "max_tokens": 300
        }
        
        try:
            self.ai_output.insert(tk.END, f"> Analyzing name '{name}'...\n")
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                self.ai_output.insert(tk.END, f"\n> Name Analysis:\n{result}\n")
            else:
                self.ai_output.insert(tk.END, f"> Error: {response.status_code}\n")
        except Exception as e:
            self.ai_output.insert(tk.END, f"> Error: {str(e)}\n")
            
    def darkweb_transform(self, text):
        """Apply military-grade obfuscation"""
        if not self.darkweb_var.get():
            return text
            
        self.pwd_output.insert(tk.END, self.show_darkweb_loading())
        
        # AES-256 Encryption
        key = os.urandom(32)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(pad(text.encode(), AES.block_size))
        encrypted = base64.b64encode(ciphertext).decode()[:24]
        return f"DARK:{encrypted}"
        
    def show_darkweb_loading(self):
        return """
        █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
        █                                █
        █   ENTERING DARK WEB MODE...    █
        █   ✓ TOR Routing Activated      █
        █   ✓ MAC Spoofing Enabled       █
        █   ✓ Encryption Protocols Init  █
        █                                █
        █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
        \n"""
        
    def update_strength_display(self, password):
        self.strength_meter.delete("all")
        if not password:
            return
            
        result = zxcvbn.zxcvbn(password)
        colors = ["#FF2C55", "#FF7D45", "#FFC945", "#2CFF5A", "#00D1FF"]
        width = 40 * (result['score'] + 1)
        
        self.strength_meter.create_rectangle(0, 0, width, 20, fill=colors[result['score']], outline="")
        self.strength_meter.create_text(100, 10, text=f"{result['guesses_log10']:.1f} entropy bits", 
                                      fill=COLOR_SCHEME["text"])

    def create_hacker_settings(self, parent):
        settings = tk.Frame(parent, bg=COLOR_SCHEME["panel"])
        settings.pack(fill=tk.X, padx=10, pady=5)
        
        # Theme selector
        theme_frame = tk.Frame(settings, bg=COLOR_SCHEME["panel"])
        theme_frame.grid(row=0, column=0, padx=5)
        
        tk.Label(theme_frame, text="Theme:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 9)).pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar(value="NEO-TOKYO")
        theme_menu = tk.OptionMenu(theme_frame, self.theme_var, "NEO-TOKYO", "MATRIX", "CYBERPUNK", command=self.change_theme)
        theme_menu.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                         activebackground=COLOR_SCHEME["panel"],
                         activeforeground=COLOR_SCHEME["text"],
                         highlightthickness=0)
        theme_menu.pack(side=tk.LEFT)
        
        # Leet level
        leet_frame = tk.Frame(settings, bg=COLOR_SCHEME["panel"])
        leet_frame.grid(row=0, column=1, padx=5)
        
        tk.Label(leet_frame, text="Leet Level:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 9)).pack(side=tk.LEFT)
        
        self.leet_scale = tk.Scale(leet_frame, from_=1, to=7, orient=tk.HORIZONTAL,
                                 bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                                 highlightthickness=0)
        self.leet_scale.set(3)
        self.leet_scale.pack(side=tk.LEFT)
        self.leet_scale.bind("<ButtonRelease-1>", lambda e: self.update_leet())
        self.leet_scale.bind("<B1-Motion>", lambda e: "break")
        
        # Separator option
        sep_frame = tk.Frame(settings, bg=COLOR_SCHEME["panel"])
        sep_frame.grid(row=0, column=2, padx=5)
        
        tk.Label(sep_frame, text="Separator:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 9)).pack(side=tk.LEFT)
        
        self.separator_var = tk.StringVar(value="_")
        sep_menu = tk.OptionMenu(sep_frame, self.separator_var, "_", "-", ".", "|", " ", command=self.update_separator)
        sep_menu.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                      activebackground=COLOR_SCHEME["panel"],
                      activeforeground=COLOR_SCHEME["text"],
                      highlightthickness=0)
        sep_menu.pack(side=tk.LEFT)
        
        # Options row 1
        self.prefix_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings, text="Prefixes", variable=self.prefix_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=0, padx=5)
        
        self.suffix_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings, text="Suffixes", variable=self.suffix_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=1, padx=5)
        
        self.number_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings, text="Numbers", variable=self.number_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=2, padx=5)
        
        # Options row 2
        self.random_case_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings, text="Random Case", variable=self.random_case_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=3, padx=5)
        
        self.double_transform_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings, text="Double Transform", variable=self.double_transform_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=4, padx=5)
        
        self.special_chars_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings, text="Special Chars", variable=self.special_chars_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=5, padx=5)
        
        self.military_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings, text="Military Style", variable=self.military_var,
                     bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                     selectcolor=COLOR_SCHEME["panel"]).grid(row=1, column=6, padx=5)
        
        settings.columnconfigure(2, weight=1)
        
    def create_tutorial_content(self):
        content_frame = tk.Frame(self.tutorial_frame, bg=COLOR_SCHEME["background"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tutorial_text = """
        WELCOME TO CYBERFORGE NINJA v12.0
        
        
██████╗███████╗███╗   ██╗    ██╗   ██╗ ██╗██████╗ 
██╔════╝██╔════╝████╗  ██║    ██║   ██║███║╚════██╗
██║     █████╗  ██╔██╗ ██║    ██║   ██║╚██║ █████╔╝
██║     ██╔══╝  ██║╚██╗██║    ╚██╗ ██╔╝ ██║██╔═══╝ 
╚██████╗██║     ██║ ╚████║     ╚████╔╝  ██║███████╗
 ╚═════╝╚═╝     ╚═╝  ╚═══╝      ╚═══╝   ╚═╝╚══════╝
                                                   

╔════════════════════════════════════════════════╗
  █▀▀▀▀▀▀▀▀▀▀ CYBERFORGE NINJA v12.0 ▀▀▀▀▀▀▀▀▀▀█
                                                 
    >>-{ PASSWORD ENTROPY DECRYPTION }-<<        
                                                 
    64-BIT ENTROPY = QUANTUM-LOCKED SECURITY     
    ■ Each bit doubles cracking time             
    ■ 2⁶⁴ guesses required (18.4 quintillion)    
    ■ NSA-grade at 128+ bits                     
                                                 
    [SECURITY MATRIX]                            
    ■ 12-char mixed = ~78 bits                   
    ■ 16-char = 100+ bits (heat death safe)      
    ■ DarkWeb Mode = ENCRYPTION THEATER        
      ✓ AES-256 facade                         
      ✗ No actual TOR routing                  
  █                                            █
  ▀▀▀▀▀▀▀▀▀▀                          ▀▀▀▀▀▀▀▀▀▀                
╚════════════════════════════════════════════════╝

▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

[0]  ⚡ＣＯＰＹ_ＯＰΞＲΛＴＩＯＮ
  ├─» Double LMB to select line
  └─» RMB → "Copy"


[1]  ＨΛＣＫΞＲ ＩＤ ＧΞＮΞＲΛＴＯＲ  ▼▲▼▲▼▲▼▲▼▲▼▲▼▲
  ├─[INPUT] » Type name → [GΞＮΞＲΛＴΞ] or [ENTER]
  ├─[BULK] » Generate 100 IDs/sec (MAX:500)
  ├─[LEET ENGINE v7.0] 
     ├─L1: Basic (@,3) → L7: Crypto-glyphic (∀,ꟾ)
     └─[MILSPEC] Format: [PH4-7ØM] [N3T-5PY]
  ├─[AI BACKSTORY MODULE] 
     ├─Style: » Cyberpunk » Military » Spy » Sci-Fi
     └─Output: 50-word procedurally-generated origins

[2]  ＰΛＳＳＷＯＲＤ ＦＯＲＧΞ  ■□□□□□□□□□□□□□□□□□□■
  ├─[SLIDER CONTROL] 
     ├─RMB: Adjust length (8-64 chars)
     └─LMB: Lock position
  ├─[COPY PROTOCOL] 
     ├─» Double LMB to select line
     └─» RMB → "Copy"
  ├─[CHARACTER SETS v3.1]
     ├─✓ A-Z ✓ a-z ✓ 0-9 ✓ !@#$%^&*
     └─✗ Ambiguous (l1I|0O) ✗ Repeats
  ├─[ENTROPY CORE] 
     ├─Real-time bit strength analysis
     └─» 64-bit = 294 years @10¹⁵ guesses/sec
  ├─[DARKWEB MODE: SIMULATION]
     ├─⚠ WARNING: Theater-mode only
     ├─» Fake TOR routing animation
     └─» Placeholder AES-256 output

[3]  ΛＩ ＩＮＴΞＧＲΛＴＩＯＮ  ◈ DΞΞＰＳΞΞＫ v1.3 ◈
  ├─[API GATEWAY] 
     ├─» Key: *********** [TEST CONNECTION]
     └─» Status: [ONLINE]/[OFFLINE]
  ├─[FEATURES]
     ├─✓ AI-optimized passwords
     ├─✓ Name vulnerability scan
     └─✓ Dynamic backstories
  ├─[OUTPUT TERMINAL]
     ├─» Streaming response
     └─» Right-click copy/paste

[4]  ＶＩＳＵΛＬ ＴＨΞＭΞＳ  ░▒▓█▓▒░
  ├─[NEO-TOKYO] » Electric magenta/cyan
  ├─[MATRIX] » Emerald-on-void + code rain
  └─[CYBERPUNK] » Neon arterial highlights

[5]  ＮＩＮＪΛ ＰＲＯＴＯＣＯＬＳ  ⚔
  ├─[HOTKEYS] 
     ├─CTRL+MWheel: Zoom UI
     └─RMB: Context menus
  ├─[EXPORT] » Encrypted TXT dumps
  └─[OPTIMAL SETTINGS]
     ├─» 16+ chars for DarkWeb
     └─» L5+ leet for milspec

▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
  » SYSTEM ALERT: 128-bit entropy = 10²⁹ years to crack «
        """
        
        tutorial = tk.Text(content_frame, wrap=tk.WORD, bg=COLOR_SCHEME["panel"],
                         fg=COLOR_SCHEME["text"], font=("Courier New", 12),
                         padx=10, pady=10, relief=tk.FLAT)
        tutorial.insert(tk.END, tutorial_text)
        tutorial.config(state=tk.DISABLED)
        tutorial.pack(fill=tk.BOTH, expand=True)
        
    def create_stats_content(self):
        content_frame = tk.Frame(self.stats_frame, bg=COLOR_SCHEME["background"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.stats_text = tk.Text(content_frame, wrap=tk.WORD, bg=COLOR_SCHEME["panel"],
                                fg=COLOR_SCHEME["text"], font=("Courier New", 12),
                                padx=10, pady=10, relief=tk.FLAT)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        self.update_stats()
        
    def update_stats(self):
        if not hasattr(self, 'stats_text'):
            return
            
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        # Hacker ID stats
        total_hacker = len(self.generator.history)
        unique_hacker = len(set(self.generator.history)) if total_hacker > 0 else 0
        uniqueness_hacker = (unique_hacker / total_hacker * 100) if total_hacker > 0 else 0
        
        # Password stats
        total_pwd = len(self.password_gen.history)
        unique_pwd = len(set(self.password_gen.history)) if total_pwd > 0 else 0
        uniqueness_pwd = (unique_pwd / total_pwd * 100) if total_pwd > 0 else 0
        
        stats_content = f"""
        === GENERATION STATISTICS ===
        
        HACKER IDS:
        Total Generated: {total_hacker}
        Unique Names: {unique_hacker} ({uniqueness_hacker:.1f}% uniqueness)
        
        PASSWORDS:
        Total Generated: {total_pwd}
        Unique Passwords: {unique_pwd} ({uniqueness_pwd:.1f}% uniqueness)
        
        === RECENTLY GENERATED ===
        """
        
        if total_hacker > 0 or total_pwd > 0:
            stats_content += "\n\nHACKER IDS:\n"
            stats_content += "\n".join(f"{i+1}. {name}" for i, name in enumerate(self.generator.history[-5:][::-1]))
            
            stats_content += "\n\nPASSWORDS:\n"
            stats_content += "\n".join(f"{i+1}. {pwd}" for i, pwd in enumerate(self.password_gen.history[-5:][::-1]))
        else:
            stats_content += "\nNo names or passwords generated yet!"
            
        self.stats_text.insert(tk.END, stats_content)
        self.stats_text.config(state=tk.DISABLED)
        
    def update_leet(self):
        self.generator.settings["leet_level"] = self.leet_scale.get()
        
    def update_separator(self, value):
        self.generator.settings["separator"] = value
        
    def change_theme(self, theme_name):
        global COLOR_SCHEME
        COLOR_SCHEME = THEMES[theme_name]
        self.refresh_ui()
        
    def refresh_ui(self):
        def update_widget(widget):
            widget_type = widget.winfo_class()
            
            if isinstance(widget, tk.Frame):
                widget.config(bg=COLOR_SCHEME["panel"])
            elif isinstance(widget, tk.Label):
                widget.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"])
            elif isinstance(widget, tk.Entry):
                widget.config(bg=COLOR_SCHEME["input_bg"], fg=COLOR_SCHEME["text"],
                            insertbackground=COLOR_SCHEME["primary"],
                            highlightbackground=COLOR_SCHEME["border"],
                            highlightcolor=COLOR_SCHEME["highlight"])
            elif isinstance(widget, tk.Text):
                widget.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["terminal"],
                            insertbackground=COLOR_SCHEME["primary"])
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=COLOR_SCHEME["background"])
            elif widget_type == "TCheckbutton":
                widget.config(bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                            selectcolor=COLOR_SCHEME["panel"])
            elif widget_type == "TButton":
                widget.config(background=COLOR_SCHEME["panel"])
            
            for child in widget.winfo_children():
                update_widget(child)
        
        self.configure(bg=COLOR_SCHEME["background"])
        update_widget(self)
        
    def setup_cyber_effects(self):
        self.binary_chars = ["0", "1", "░", "▒", "▓", "█"]
        self.binary_streams = []
        
        for i in range(20):  # More streams for better effect
            x = random.randint(0, 1000)
            speed = random.uniform(1, 4)  # Faster animation
            length = random.randint(8, 15)  # Longer streams
            self.binary_streams.append({
                "x": x,
                "speed": speed,
                "length": length,
                "chars": [random.choice(self.binary_chars) for _ in range(length)],
                "positions": [random.randint(-100, 0) for _ in range(length)]
            })
        
        self.animate_binary_rain()
        
    def animate_binary_rain(self):
        self.header.delete("binary")
        
        for stream in self.binary_streams:
            for i in range(stream["length"]):
                char = stream["chars"][i]
                y = stream["positions"][i]
                
                if 0 <= y < 80:
                    alpha = min(255, max(0, int(255 * (1 - i/stream["length"]))))
                    color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                    self.header.create_text(stream["x"], y, text=char, 
                                          fill=color, font=("Courier New", 10), 
                                          tags="binary")
                
                stream["positions"][i] += stream["speed"]
                
                if stream["positions"][i] > 80:
                    stream["positions"][i] = random.randint(-100, -20)
                    if random.random() < 0.2:
                        stream["chars"][i] = random.choice(self.binary_chars)
        
        self.after(30, self.animate_binary_rain)  # Faster animation
        
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.output.config(insertbackground=COLOR_SCHEME["primary"] if self.cursor_visible else COLOR_SCHEME["panel"])
        self.after(500, self.blink_cursor)
        
    def clear_placeholder(self, event):
        if self.entry.get() == "Enter your name":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLOR_SCHEME["text"])
            
    def add_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Enter your name")
            self.entry.config(fg=COLOR_SCHEME["placeholder"])
            
    def generate_name(self):
        input_text = self.entry.get().strip()
        if not input_text or input_text == "Enter your name":
            self.show_error()
            return
            
        self.generator.settings.update({
            "use_prefix": self.prefix_var.get(),
            "use_suffix": self.suffix_var.get(),
            "add_numbers": self.number_var.get(),
            "random_case": self.random_case_var.get(),
            "double_transform": self.double_transform_var.get(),
            "add_special_chars": self.special_chars_var.get(),
            "military_style": self.military_var.get()
        })
        
        self.output.delete(1.0, tk.END)
        name = self.generator.generate(input_text)
        self.animate_output(name)
        
        if self.ai_backstory_var.get():
            backstory = self.generate_hacker_backstory(input_text, name)
            self.output.insert(tk.END, f"\n\n>> BACKSTORY <<\n{backstory}")
        
        self.update_stats()
        
    def animate_output(self, text):
        self.output.insert(tk.END, "> Initializing generator...\n")
        self.output.see(tk.END)
        self.after(200, lambda: self.type_effect(text, 0))
        
    def type_effect(self, text, index):
        if index < len(text):
            self.output.insert(tk.END, text[index])
            self.output.see(tk.END)
            self.after(random.randint(20, 50), lambda: self.type_effect(text, index+1))
        else:
            self.output.insert(tk.END, "\n\n> Identity generation complete!")
            self.output.see(tk.END)
            
    def generate_password(self):
        self.password_gen.settings.update({
            "length": self.pwd_length.get(),
            "use_uppercase": self.pwd_upper.get(),
            "use_lowercase": self.pwd_lower.get(),
            "use_digits": self.pwd_digits.get(),
            "use_special": self.pwd_special.get(),
            "avoid_ambiguous": self.pwd_no_ambiguous.get(),
            "no_repeating": self.pwd_no_repeat.get()
        })
        
        password = self.password_gen.generate()
        
        if self.darkweb_var.get():
            password = self.darkweb_transform(password)
        
        self.update_strength_display(password)
        
        self.pwd_output.insert(tk.END, f"> Generated password: {password}\n")
        self.pwd_output.see(tk.END)
        self.update_stats()
        
    def bulk_generate_passwords(self):
        count = 5
        
        self.pwd_output.insert(tk.END, f"> Generating {count} passwords...\n\n")
        
        for i in range(count):
            password = self.password_gen.generate()
            
            if self.darkweb_var.get():
                password = self.darkweb_transform(password)
            
            self.pwd_output.insert(tk.END, f"{i+1}. {password}\n")
            self.pwd_output.see(tk.END)
            self.update()
            
        self.update_strength_display(password)
            
        self.pwd_output.insert(tk.END, f"\n> Bulk generation of {count} passwords complete!")
        self.update_stats()
            
    def show_error(self):
        for i in range(3):
            self.after(i*100, lambda: self.entry.config(bg="#FF2C55"))
            self.after(i*100+50, lambda: self.entry.config(bg=COLOR_SCHEME["input_bg"]))
    
    def show_tutorial(self):
        if self.first_run:
            self.notebook.select(self.tutorial_frame)
            self.first_run = False
    
    def create_footer(self):
        footer = tk.Frame(self, bg=COLOR_SCHEME["panel"], height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM, pady=(5,0))
        
        left_frame = tk.Frame(footer, bg=COLOR_SCHEME["panel"])
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        tk.Label(left_frame, text="© 2025 CYBERFORGE NINJA | MIT License",
                bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
                font=("Courier New", 8)).pack(anchor="w")
        
        link_frame = tk.Frame(left_frame, bg=COLOR_SCHEME["panel"])
        link_frame.pack(anchor="w", pady=(2,0))
        
        links = [
            ("Email", "mailto:contact@rocybersolutions.com"),
            ("GitHub", "https://github.com/rocybersolutions"),
            ("LinkedIn", "https://linkedin.com/company/rocyber-solutions"),
            ("Web", "https://rocybersolutions.com")
        ]
        
        for i, (text, url) in enumerate(links):
            if i > 0:
                tk.Label(link_frame, text="|", bg=COLOR_SCHEME["panel"], 
                        fg=COLOR_SCHEME["text"], font=("Courier New", 8)).pack(side=tk.LEFT)
            
            link = tk.Label(link_frame, text=text, bg=COLOR_SCHEME["panel"], 
                          fg=COLOR_SCHEME["primary"], font=("Courier New", 8), 
                          cursor="hand2")
            link.pack(side=tk.LEFT)
            link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        
        self.time_label = tk.Label(footer, text="", 
                                 bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["primary"],
                                 font=("Courier New", 8))
        self.time_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()
        
        bulk_frame = tk.Frame(footer, bg=COLOR_SCHEME["panel"])
        bulk_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Label(bulk_frame, text="Count:", bg=COLOR_SCHEME["panel"],
               fg=COLOR_SCHEME["text"], font=("Courier New", 8)).pack(side=tk.LEFT)
        
        self.bulk_count = tk.IntVar(value=DEFAULT_BULK_COUNT)
        tk.Entry(bulk_frame, textvariable=self.bulk_count, width=3,
               bg=COLOR_SCHEME["panel"], fg=COLOR_SCHEME["text"],
               relief=tk.FLAT).pack(side=tk.LEFT, padx=2)
        
        bulk_btn = CyberButton(bulk_frame, "BULK GEN", self.bulk_generate, width=80, height=25)
        bulk_btn.pack(side=tk.LEFT, padx=2)
        
        export_btn = CyberButton(footer, "EXPORT ALL", self.export_names, width=90, height=25)
        export_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"SYSTEM TIME: {now}")
        self.after(1000, self.update_clock)
    
    def bulk_generate(self):
        input_text = self.entry.get().strip()
        if not input_text or input_text == "Enter your name":
            self.show_error()
            return
            
        count = max(1, min(100, self.bulk_count.get()))
        
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"> Generating {count} hacker identities...\n\n")
        
        for i in range(count):
            name = self.generator.generate(input_text)
            self.output.insert(tk.END, f"{i+1}. {name}\n")
            self.output.see(tk.END)
            self.update()
            
            if i == count-1 and self.ai_backstory_var.get():
                backstory = self.generate_hacker_backstory(input_text, name)
                self.output.insert(tk.END, f"\n\n>> BACKSTORY <<\n{backstory}")
            
        self.output.insert(tk.END, f"\n> Bulk generation of {count} names complete!")
        self.update_stats()
    
    def export_names(self):
        if not self.generator.history and not self.password_gen.history:
            self.output.insert(tk.END, "\n\n> ERROR: No names or passwords generated to export!")
            return
            
        if not os.path.exists(EXPORT_FOLDER):
            os.makedirs(EXPORT_FOLDER)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{EXPORT_FOLDER}/CyberForge_Export_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            initialdir=os.path.abspath(EXPORT_FOLDER),
            initialfile=os.path.basename(default_filename),
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not filename:
            return
            
        content = f"=== CYBERFORGE EXPORT ===\n"
        content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if self.generator.history:
            content += f"=== HACKER ID SETTINGS ===\n"
            content += f"Original Name: {self.entry.get().strip()}\n"
            content += f"Leet Level: {self.generator.settings['leet_level']}\n"
            content += f"Prefixes: {'ON' if self.generator.settings['use_prefix'] else 'OFF'}\n"
            content += f"Suffixes: {'ON' if self.generator.settings['use_suffix'] else 'OFF'}\n"
            content += f"Numbers: {'ON' if self.generator.settings['add_numbers'] else 'OFF'}\n"
            content += f"Random Case: {'ON' if self.generator.settings['random_case'] else 'OFF'}\n"
            content += f"Double Transform: {'ON' if self.generator.settings['double_transform'] else 'OFF'}\n"
            content += f"Special Chars: {'ON' if self.generator.settings['add_special_chars'] else 'OFF'}\n"
            content += f"Military Style: {'ON' if self.generator.settings['military_style'] else 'OFF'}\n"
            content += f"Separator: '{self.generator.settings['separator']}'\n\n"
            content += f"=== GENERATED IDENTITIES ===\n\n"
            content += "\n".join(f"{i+1}. {name}" for i, name in enumerate(self.generator.history)) + "\n\n"
        
        if self.password_gen.history:
            content += f"=== PASSWORD SETTINGS ===\n"
            content += f"Length: {self.password_gen.settings['length']}\n"
            content += f"Uppercase: {'ON' if self.password_gen.settings['use_uppercase'] else 'OFF'}\n"
            content += f"Lowercase: {'ON' if self.password_gen.settings['use_lowercase'] else 'OFF'}\n"
            content += f"Digits: {'ON' if self.password_gen.settings['use_digits'] else 'OFF'}\n"
            content += f"Special: {'ON' if self.password_gen.settings['use_special'] else 'OFF'}\n"
            content += f"Avoid Ambiguous: {'ON' if self.password_gen.settings['avoid_ambiguous'] else 'OFF'}\n"
            content += f"No Repeating: {'ON' if self.password_gen.settings['no_repeating'] else 'OFF'}\n"
            content += f"Dark Web Mode: {'ON' if self.darkweb_var.get() else 'OFF'}\n\n"
            content += f"=== GENERATED PASSWORDS ===\n\n"
            content += "\n".join(f"{i+1}. {pwd}" for i, pwd in enumerate(self.password_gen.history)) + "\n"
        
        try:
            with open(filename, "w") as f:
                f.write(content)
                
            self.output.insert(tk.END, f"\n\n> Successfully exported to:\n{filename}")
            
            if os.name == 'nt':
                os.startfile(os.path.dirname(filename))
            elif os.name == 'posix':
                os.system(f'open "{os.path.dirname(filename)}"' if sys.platform == 'darwin' else f'xdg-open "{os.path.dirname(filename)}"')
        except Exception as e:
            self.output.insert(tk.END, f"\n\n> EXPORT ERROR: {str(e)}")
    
    def zoom(self, event):
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
            
        self.zoom_level = max(0.5, min(2.0, self.zoom_level))
        self.update_font_sizes()
    
    def update_font_sizes(self):
        def update_widget_font(widget):
            if hasattr(widget, 'config'):
                current_font = widget.cget('font')
                if isinstance(current_font, (tuple, list)):
                    if len(current_font) >= 2 and isinstance(current_font[1], (int, float)):
                        new_size = int(current_font[1] * self.zoom_level)
                        new_font = (current_font[0], new_size) + current_font[2:]
                        widget.config(font=new_font)
            
            for child in widget.winfo_children():
                update_widget_font(child)
        
        update_widget_font(self)
    
    def show_output_menu(self, event, menu=None):
        if menu is None:
            menu = self.output_menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def copy_output(self, widget=None):
        if widget is None:
            widget = self.output
        try:
            selected = widget.get("sel.first", "sel.last")
            pyperclip.copy(selected)
        except tk.TclError:
            content = widget.get("1.0", tk.END)
            pyperclip.copy(content)
    
    def clear_output(self, widget=None):
        if widget is None:
            widget = self.output
        widget.delete("1.0", tk.END)
    
    def edit_last_output(self):
        if not self.generator.history:
            return
            
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Last Generated")
        edit_win.geometry("500x200")
        
        last_name = self.generator.history[-1]
        entry = tk.Entry(edit_win, font=("Courier New", 12), width=50)
        entry.pack(pady=20)
        entry.insert(0, last_name)
        
        def save_edit():
            new_name = entry.get()
            self.generator.history[-1] = new_name
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"> Edited identity: {new_name}")
            edit_win.destroy()
            self.update_stats()
        
        save_btn = tk.Button(edit_win, text="Save", command=save_edit)
        save_btn.pack()

if __name__ == "__main__":
    app = CyberForge()
    app.mainloop()