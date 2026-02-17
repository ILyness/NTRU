import threading
import time
import sys
import itertools
import re

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
    UNDERLINE = '\033[4m'
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
        for c in itertools.cycle(self.steps):
            if self.done:
                break
            # Print the character and move cursor back
            sys.stdout.write(f"\r{self.desc} {c}")
            sys.stdout.flush()
            time.sleep(self.timeout)

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