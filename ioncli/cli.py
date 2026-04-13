import sys
import subprocess

def usage():
    print("""
ION CLI

Usage:
  ion menu - Interactive menu for script management
  ion set-auth - Set up authentication by providing a .ionapi file      
  ion new - Create a new script template
  ion deploy <ScriptName> - Deploy a script to ION (creates new version)
  ion approve <ScriptName> - Approve a script
  ion check <ScriptName> - Check the status of a script
  ion update <ScriptName> - Update a script
  ion run <ScriptName> - Run a script
  ion set-format <ScriptName> --input FORMAT
  ion set-format <ScriptName> --output FORMAT
""")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        usage()

    command = sys.argv[1]

    if command == "new":
        subprocess.run([sys.executable, "-m", "tools.newscript"])

    elif command == "deploy":
        if len(sys.argv) < 3:
            usage()
        subprocess.run([sys.executable, "-m", "tools.deploy", sys.argv[2]])

    elif command == "approve":
        if len(sys.argv) < 3:
            usage()
        subprocess.run([sys.executable, "-m", "tools.approve", sys.argv[2]])    

    elif command == "check":
        if len(sys.argv) < 3:
            usage()
        subprocess.run([sys.executable, "-m", "tools.check", sys.argv[2]])     

    elif command == "update":
        if len(sys.argv) < 3:
            usage()
        subprocess.run([sys.executable, "-m", "tools.update", sys.argv[2]])                  

    elif command == "run":
        if len(sys.argv) < 3:
            usage()
        subprocess.run([sys.executable, "-m", "tools.run", sys.argv[2]])

    elif command == "set-format":
        if len(sys.argv) < 5:
            usage()
        subprocess.run([sys.executable, "-m", "tools.setformat", sys.argv[2], sys.argv[3], sys.argv[4]])

    elif command == "set-auth":
        subprocess.run([sys.executable, "-m", "security.setauth"])

    elif command == "menu":
        subprocess.run([sys.executable, "-m", "tools.menu"])

    else:
        usage()

if __name__ == "__main__":
    main()