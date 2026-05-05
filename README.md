# ION Scripts

A complete automation toolkit for developing, deploying, and managing **Infor ION Python scripts** without using the Infor UI. Designed for teams using VS Code, GitHub, and GitHub Actions.

---

## Overview

ION Scripts is a CLI-driven solution that implements a **fully automated, API-driven workflow** for Infor ION script development and deployment. Write scripts locally, version them in Git, deploy automatically to ION, approve via API, and execute in CI/CD pipelines.

---

## Features

### Core Capabilities

- **Interactive CLI Menu** - User-friendly interface for all script operations
- **Script Management** - Create, deploy, update, approve, and run scripts via API
- **Format Control** - Set input/output formats (Text, JSON, XML, CSV, Base64)
- **Status Monitoring** - Check script deployment and execution status
- **Authentication** - OAuth password credentials grant with secure token management
- **Template Generation** - Quickly bootstrap new scripts with standard structure
- **No UI Dependency** - Full automation without accessing the Infor interface

### Developer Experience

- Local development with VS Code
- Git version control for all scripts
- GitHub Actions CI/CD integration
- Consistent tooling between local and CI environments
- Automatic script validation

### Security & Best Practices

- OAuth 2.0 authentication
- No secrets committed to source control
- Token-based API access
- Environment variable configuration
- Idempotent deployments (create or update)

---

## Installation

### Prerequisites

- **Python 3.8+** (3.14+ recommended)
- **macOS/Linux** (tested on macOS, requires Homebrew Python on macOS due to LibreSSL issues)
- **pip** and **virtual environment** support

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ion-scripts.git
cd ion-scripts
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On macOS/Linux
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

This installs:
- `requests` - HTTP library for API calls
- `questionary` - Interactive CLI prompts
- `rich` - Rich terminal output formatting

---

## Setup

### Authentication Configuration

Before using ION Scripts, you need to set up authentication credentials.

#### Method 1: Interactive Setup (Recommended)

```bash
ion set-auth
```

This will guide you through providing your ION credentials interactively and create a `.ionapi` configuration file.

#### Method 2: Environment Variables

Create a `.env` file in the project root with your Infor ION credentials:

```env
ION_AUTH_URL=https://your-auth-endpoint/oauth/token
ION_API_URL=https://your-api-endpoint
ION_CLIENT_ID=your_client_id
ION_CLIENT_SECRET=your_client_secret
ION_USERNAME=your_username
ION_PASSWORD=your_password
```

** Important:** Never commit `.env` or `.ionapi` files to version control. Add them to `.gitignore`.

#### Authentication Model

ION uses two distinct endpoints:
- **OAuth/SSO Endpoint** - For authentication (returns access token)
- **ION API Endpoint** - For script deployment, approval, and execution

---

## Usage

### Interactive Menu (Recommended for Beginners)

Start the interactive menu:

```bash
ion menu
```

This presents an easy-to-use interface for all operations:
- New script
- Deploy script
- Approve script
- Run script
- Check script status
- Update script
- Set input/output formats
- Configure authentication

### Command-Line Interface

If you prefer direct commands:

#### Create a New Script

```bash
ion new
```

Creates a new script template with the following structure:

```
scripts/YourScript/
├── script.py       # Your Python script logic
├── model.json      # ION script model configuration
├── meta.json       # Script metadata
└── test-input.txt  # Sample test input
```

#### Deploy a Script

```bash
ion deploy YourScript
```

Deploys your script to ION. If the script doesn't exist, it creates a new version. If it already exists, it updates the current version.

#### Approve a Script

```bash
ion approve YourScript
```

Approves the deployed script for production use.

#### Run a Script

```bash
ion run YourScript
```

Executes your script in ION and displays results.

#### Check Script Status

```bash
ion check YourScript
```

Displays the current deployment status and metadata of the script.

#### Update a Script

```bash
ion update YourScript
```

Updates an existing deployed script with new code.

#### Set Input/Output Formats

```bash
ion set-format YourScript --input JSON
ion set-format YourScript --output CSV
```

Supported formats: **Text**, **JSON**, **XML**, **CSV**, **Base64**

#### Configure Authentication

```bash
ion set-auth
```

Set up or update your ION API credentials.

---

## Project Structure

```
ion-scripts/
├── ioncli/                 # CLI application code
│   ├── __init__.py
│   └── cli.py             # Main CLI entry point
├── security/               # Authentication & token management
│   ├── auth.py            # OAuth authentication
│   ├── iontoken.py        # Token handling
│   └── setauth.py         # Credential setup
├── tools/                  # Core functionality
│   ├── approve.py         # Script approval
│   ├── check.py           # Status checking
│   ├── deploy.py          # Script deployment
│   ├── menu.py            # Interactive menu
│   ├── newscript.py       # Script generation
│   ├── run.py             # Script execution
│   ├── setformat.py       # Format configuration
│   └── update.py          # Script updates
├── scripts/                # Your ION scripts
│   ├── Script1/
│   ├── Script2/
│   └── ...
├── tests/                  # Testing outputs
├── env/                    # Python virtual environment
├── pyproject.toml          # Project metadata
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## Design Principles

- ✅ **No UI Dependency** - Fully API-driven, no need for Infor UI
- ✅ **One Repository, Many Scripts** - Organize multiple scripts in one place
- ✅ **One Folder = One Script** - Clear, intuitive structure
- ✅ **Idempotent Deployments** - Deploy safely; scripts are created or updated as needed
- ✅ **No Secrets in Source Control** - Credentials stored separately
- ✅ **Consistent Tooling** - Same workflow locally and in CI/CD

---

## Troubleshooting

### Authentication Fails

**Issue**: "Missing one or more required environment variables"

**Solution**: Ensure all required environment variables are set or run `ion set-auth` to configure credentials interactively.

### Python Hangs on macOS

**Issue**: Commands freeze or hang on macOS

**Solution**: macOS system Python uses LibreSSL and can hang on ION API calls. Use Homebrew Python instead:
```bash
brew install python@3.14
/usr/local/bin/python3.14 -m venv env
```

### Script Not Found

**Issue**: "Script not found" error when running commands

**Solution**: Ensure your script folder exists in the `scripts/` directory with the correct name, matching the name you use in commands.

---

## Contributing

To contribute to ION Scripts:

1. Create a new branch for your feature
2. Make your changes
3. Test locally using the CLI
4. Submit a pull request

---

## Requirements

See [requirements.txt](requirements.txt) for the complete list of dependencies:

- `requests` - HTTP operations for API calls
- `questionary` - Interactive prompt library
- `rich` - Terminal formatting and UI

---

## Support & Documentation

For issues or questions:
- Check the troubleshooting section above
- Review the authentication configuration steps
- Ensure your Python environment is properly configured

---
