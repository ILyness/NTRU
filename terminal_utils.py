import threading
import time
import sys
import itertools
import re
import random
import string
import shutil
import math

def prettify_polynomial(poly_str):
    superscript_map = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "-": "⁻" 
    }
    coeff_map = {
        "0": "𝟢", "1": "𝟣", "2": "𝟤", "3": "𝟥", "4": "𝟦",
        "5": "𝟧", "6": "𝟨", "7": "𝟩", "8": "𝟪", "9": "𝟫"
    }
    def replace_exponent(match):
        exponent = match.group(1)
        return "".join([superscript_map.get(char, char) for char in exponent])

    res = re.sub(r'\^(-?\d+)', replace_exponent, poly_str).replace('x', '𝑥')
    for (key, val) in coeff_map.items():
        res.replace(key, val)
    return res

def slow_print(text, delay=0.05, final_delay=1, end=None):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    i = 0
    while i < len(text):
        match = ansi_escape.match(text, i)
        if match:
            sys.stdout.write(match.group(0))
            sys.stdout.flush()
            i = match.end(0)
        else:
            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(delay)
            i += 1
    print(end=end) 
    time.sleep(final_delay)

class Colors:
    ALICE = '\033[91;1m'
    BOB = '\033[94;1m'
    EVE = '\033[35;1m'
    MESSAGE = '\033[92;1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

FUN_FACTS = [
    # --- NTRU ---
    "NTRUEncrypt was founded by Hoffstein, Pipher, and Silverman in 1998!",
    "NTRU stands for Narwhals, Turtles, Raccoons, and sea Urchins!",
    "NTRU stands for Nth Degree Truncated polynomial Ring Unit!",
    "NTRU stands for Number Theorists R Us!",
    "NTRU is based on the Shortest Vector Problem in a lattice.",
    "Unlike RSA, NTRU is considered 'Post-Quantum' secure.",
    
    # --- RSA ---
    "RSA is based on the difficulty of factoring large prime numbers.",
    "Clifford Cocks invented RSA at GCHQ years before the public knew.",
    "Shor's Algorithm on a quantum computer could break RSA.",
    
    # --- ECC / ECDH ---
    "A 256-bit ECC key is as strong as a 3072-bit RSA key!",
    "Bitcoin uses the elliptic curve secp256k1.",
    "ECDH lets you agree on a secret key over public channels.",
    
    # --- General ---
    "Eve is always listening...",
    "Mallory is always tampering...",
    "Alice and Bob have been talking since 1978.",
    "The One-Time Pad is the only mathematically unbreakable cipher.",
    "Kerckhoffs's principle: The enemy knows the system!",
    "Rot13 is the best encryption (just kidding)."
]

STYLES = [
    # --- Standard Foreground Colors ---
    '\033[31m', # Red
    '\033[32m', # Green
    '\033[33m', # Yellow
    '\033[34m', # Blue
    '\033[35m', # Magenta
    '\033[36m', # Cyan
    '\033[37m', # White

    # --- Bright / High Intensity Foregrounds ---
    '\033[91m', # Bright Red
    '\033[92m', # Bright Green
    '\033[93m', # Bright Yellow
    '\033[94m', # Bright Blue
    '\033[95m', # Bright Magenta
    '\033[96m', # Bright Cyan
    '\033[97m', # Bright White

    # --- Formatting ---
    '\033[1m',  # Bold
    '\033[2m',  # Dim (Faint)
    '\033[3m',  # Italic
    '\033[4m',  # Underline
    '\033[7m',  # Reverse (Swaps background and foreground)
    '\033[9m',  # Strikethrough

    # --- Background Colors (High Contrast) ---
    '\033[41m', # Red Background
    '\033[42m', # Green Background
    '\033[44m', # Blue Background
    '\033[45m', # Magenta Background

    # --- COMBOS (The "Chaos" Options) ---
    '\033[1;31m',    # Bold Red
    '\033[1;32m',    # Bold Green
    '\033[1;33m',    # Bold Yellow
    '\033[4;36m',    # Underline Cyan
    '\033[1;97;41m', # Bold White on Red Background (Error style)
    '\033[1;30;47m', # Bold Black on White Background
    '\033[3;35m',    # Italic Magenta
]
RESET = '\033[0m'

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager
        
        @param desc: The text to display while loading
        @param end: The text to display when done
        @param timeout: Sleep time between animation frames
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        HEIGHT = 4
        characters = string.ascii_letters + string.digits
        def force_fit(text, width):
            if len(text) > width:
                return text[:width-3] + "..."
            return text

        i = 0
        fact = random.choice(FUN_FACTS)
        current_style = random.choice(STYLES)
        
        # 1. RESERVE SPACE (Crucial Step)
        # We print 4 empty lines to create our "canvas". 
        # This guarantees we never accidentally move up into old history.
        sys.stdout.write("\n" * HEIGHT)

        for c in itertools.cycle(self.steps):
            # --- LOGIC ---
            # Update fact every 15 cycles (slows down fact changing)
            if i % 15 == 0:
                fact = random.choice(FUN_FACTS)
                current_style = random.choice(STYLES)
            i += 1
            
            # Get terminal width (subtract 1 to prevent edge-case wrapping)
            width = shutil.get_terminal_size().columns - 1
            for _ in range(100):
                # --- PREPARE LINES ---
                # We enforce exactly 4 lines. We truncate them to 'width'
                # so they NEVER wrap unexpectedly.
                lines = [
                    force_fit(f"{self.desc} {c}", width),
                    force_fit(''.join(random.choices(characters, k=10)), width), # s1
                    current_style + force_fit(fact, width) + RESET,                                     # Fact
                    force_fit(''.join(random.choices(characters, k=10)), width)  # s2
                ]
                
                # --- RENDER ---
                # 1. Move up 4 lines (to the start of our reserved space)
                sys.stdout.write(f"\033[{HEIGHT}F") 
                if self.done:
                    print((' ' * (width-1) + '\n') * (HEIGHT + 1))
                    sys.stdout.write(f"\033[{HEIGHT}F") 
                    break
                
                # 2. Print the lines (Clear line first with \033[K)
                for line in lines:
                    sys.stdout.write(f"\033[K{line}\n")
                
                sys.stdout.flush()
                time.sleep(self.timeout / 100)
            if self.done:
                break

    def stop(self):
        self.done = True
        # Join ensures the thread finishes before we print the final message
        # preventing race conditions on the stdout
        self._thread.join()
        print("\r" + " " * (len(self.desc) + 2))
        slow_print(f"\r{self.end}")

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

# --- Usage Example ---

if __name__ == "__main__":
    # Example 1: Using it as a context manager (cleanest)
    print("Example 1: Context Manager")
    with Loader(desc="Waiting for user input..."):
        # The main thread blocks here
        user_input = input("") 
    
    print(f"You typed: {user_input}")
    
    # Example 2: Manual start/stop
    print("\nExample 2: Manual Start/Stop")
    loader = Loader(desc="Processing data...", end="Complete!").start()
    time.sleep(3) # Simulating a long task
    loader.stop()