import subprocess
import sys
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    while True:
        console.print(Panel.fit("ION CLI", style="bold cyan"))

        action = questionary.select(
            "Choose an action",
            choices=[
                "New script",
                "Deploy script",
                "Approve script",
                "Run script",
                "Check script",
                "Update script",
                "Set format",
                "Set auth",
                "Exit"
            ]
        ).ask()

        if action == "New script":
            subprocess.run([sys.executable, "-m", "tools.newscript"])

        elif action == "Deploy script":
            script = questionary.text("Script name").ask()
            subprocess.run([sys.executable, "-m", "tools.deploy", script])

        elif action == "Approve script":
            script = questionary.text("Script name").ask()
            subprocess.run([sys.executable, "-m", "tools.approve", script])            

        elif action == "Run script":
            script = questionary.text("Script name").ask()
            subprocess.run([sys.executable, "-m", "tools.run", script])

        elif action == "Check script":
            script = questionary.text("Script name").ask()
            subprocess.run([sys.executable, "-m", "tools.check", script])

        elif action == "Update script":
            script = questionary.text("Script name").ask()
            subprocess.run([sys.executable, "-m", "tools.update", script])

        elif action == "Set format":
            script = questionary.text("Script name").ask()
            direction = questionary.select(
                "Set which format?",
                choices=["input", "output"]
            ).ask()
            fmt = questionary.select(
                "Format",
                choices=["Text", "JSON", "XML", "CSV", "Base64"]
            ).ask()
            subprocess.run([
                sys.executable, "-m", "tools.setformat",
                script, f"--{direction}", fmt
            ])

        elif action == "Set auth":
            subprocess.run([sys.executable, "-m", "security.setauth"])

        elif action == "Exit" or action is None:
            break

if __name__ == "__main__":
    main()