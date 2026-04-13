import json
from pathlib import Path
import questionary
from rich.console import Console
from rich.panel import Panel
from rich import print

console = Console()

ION_TYPES = ["STRING", "INTEGER", "FLOAT", "BOOLEAN"]
STRING_FORMATS = ["Plain Text", "JSON", "XML", "CSV", "Base64"]

def ask_variable(var_kind):
    name = questionary.text(f"{var_kind} variable name").ask()

    ion_type = questionary.select(
        f"{var_kind} ION variable type",
        choices=ION_TYPES
    ).ask()

    string_format = None
    if ion_type == "STRING":
        string_format = questionary.select(
            f"{var_kind} STRING content format (for test template)",
            choices=STRING_FORMATS
        ).ask()

    description = questionary.text(
        f"{var_kind} variable description",
        default="Variable description"
    ).ask()

    return {
        "name": name,
        "type": ion_type,
        "description": description
    }

def main():
    console.print(Panel.fit("ION Script Wizard", style="bold cyan"))

    script_name = questionary.text("Script name").ask()

    base_path = Path("scripts") / script_name
    if base_path.exists():
        console.print(f"[red]❌ Script folder '{script_name}' already exists.[/red]")
        return

    description = questionary.text("Description").ask()
    documentation = questionary.text("Documentation").ask()

    # INPUT VARIABLES
    console.print("\n[bold yellow]Input Variables[/bold yellow]")
    input_vars = []
    while True:
        input_vars.append(ask_variable("Input"))
        more = questionary.confirm("Add another input variable?", default=False).ask()
        if not more:
            break

    # OUTPUT VARIABLES
    console.print("\n[bold yellow]Output Variables[/bold yellow]")
    output_vars = []
    while True:
        output_vars.append(ask_variable("Output"))
        more = questionary.confirm("Add another output variable?", default=False).ask()
        if not more:
            break

    # LIBRARIES
    console.print("\n[bold yellow]Used Libraries[/bold yellow]")
    used_libraries = []
    while questionary.confirm("Add a library?", default=False).ask():
        lib_name = questionary.text("Library name").ask()
        lib_version = questionary.text("Library version").ask()
        used_libraries.append({
            "name": lib_name,
            "version": lib_version
        })

    # Create folder
    base_path.mkdir(parents=True)

    # Build model.json
    model = {
        "name": script_name,
        "description": description,
        "documentation": documentation,
        "scriptCode": "",
        "inputVariables": input_vars,
        "outputVariables": output_vars,
        "usedLibraries": used_libraries
    }

    with open(base_path / "model.json", "w") as f:
        json.dump(model, f, indent=2)


    # Build meta.json (local development metadata)
    meta = {
        "input_format": input_vars[0].get("string_format"),
        "output_format": None  # can be set later manually if desired
    }
    with open(base_path / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


    # Build script template
    first_input = input_vars[0]["name"]
    first_output = output_vars[0]["name"]

    script_template = f"""def main({first_input}):
    # TODO: implement your logic here
    result = {first_input}
    return result

{first_output} = main({first_input})
"""

    with open(base_path / "script.py", "w") as f:
        f.write(script_template)

    # Blank test input
    input_type = input_vars[0]["type"]
    string_format = input_vars[0].get("string_format")

    if input_type == "STRING":
        if string_format == "JSON":
            default_input = json.dumps({
                "message": f"Hello from {script_name}"
            }, indent=2)
        elif string_format == "XML":
            default_input = f"""<root>
    <message>Hello from {script_name}</message>
    </root>"""
        elif string_format == "CSV":
            default_input = "id,name\n1,Sample"
        elif string_format == "Base64":
            default_input = "SGVsbG8gV29ybGQ="  # Hello World
        else:
            default_input = f"Hello from {script_name}"
    elif input_type == "INTEGER":
        default_input = "1"
    elif input_type == "FLOAT":
        default_input = "1.0"
    elif input_type == "BOOLEAN":
        default_input = "true"
    else:
        default_input = f"Sample input for {script_name}"

    with open(base_path / "test-input.txt", "w") as f:
        f.write(default_input)    

    console.print(f"\n[green] Script {script_name} created at scripts/{script_name}[/green]")

if __name__ == "__main__":
    main()