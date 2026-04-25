import time
from rich.console import Console
from rich import print
from agent.agent import app
import json
from pathlib import Path

console = Console()




def fetch_data():
    # The spinner will run as long as the code inside the 'with' block is running
    with console.status("[bold cyan]Figuring aldready present message context...", spinner="bouncingBar"):
        if Path("./messages.json").exists():
            time.sleep(1)
            pass
        else:
            time.sleep(1)
            print("\n[bold red] DID NOT FIND PREVIOUS MESSAGES[/bold red]")
        # Simulate a task taking 3 seconds
        
        
    

if __name__ == "__main__":
    fetch_data()