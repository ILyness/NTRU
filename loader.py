import threading
import time
import sys
import itertools

from ntru_pipeline import slow_print

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