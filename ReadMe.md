> **Note:** The repository edition does not contain the latest Stable Release.  
> For the complete supported version, download the newest release from the Releases section.

```text
 █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

**A modern command-line toolkit for system analysis, network diagnostics, and local network scanning.**

---

## Overview

Aether is a comprehensive Python-based command-line application that provides essential system diagnostics, network analysis, and security capabilities. The toolkit is engineered for portability, modularity, and cross-platform operation, supporting Windows, macOS, and Linux environments.

---

## Features

### System Analysis
- System information retrieval and diagnostics
- System integrity verification
- Host configuration analysis

### Network Operations
- Real-time network monitoring
- Local area network (LAN) discovery and enumeration
- Gateway detection and analysis
- Port scanning and service enumeration
- ARP table analysis
- Traceroute functionality
- Device snapshot comparison and change detection

### Security and Forensic Analysis
- YARA signature-based scanning
- MASI forensic scanner integration
- Browser Extension Audit (BEA)
- USB device security auditing
- Malware detection capabilities
- System component integrity assessment

### User Interface
- Interactive command-line interface
- Modular command architecture
- Cross-platform compatibility

---

## Installation

### Prerequisites

- **Python 3.10 or newer**
- Standard library modules (dependencies listed in `requirements.txt` if applicable)

### Recommended Installation (Stable Release)

Download the latest stable release from the [Releases](../../releases) section.

**Stable Release includes:**
- Complete modular architecture
- Current feature set and improvements
- Updated dependencies
- Security analysis components
- Pre-configured environment

After downloading, extract the archive and proceed to [Running Aether](#running-aether).

### Repository Edition Installation

The repository edition is provided for reference, legacy usage, and source inspection. This edition is not actively maintained and may lack latest features and security components.

**Clone the repository:**

```bash
git clone https://github.com/NullNexus14/AetherProgram
cd AetherProgram
```

**Or download the ZIP archive** and extract it. The resulting directory structure should be:

```text
Aether/
├── modules/
├── Aether.py
└── README.md
```

**Install dependencies (if required):**

```bash
pip install -r requirements.txt
```

> **Important:** Execute `Aether.py` from the project root directory. Do not run files in the `modules/` directory directly.

---

## Running Aether

### Linux / macOS

```bash
python3 Aether.py
```

### Windows (PowerShell)

```powershell
python .\Aether.py
```

### Windows (Command Prompt)

```cmd
python Aether.py
```

### Standalone Executable

If using a standalone packaged version:

```bash
./Aether
```

---

## Project Structure

| Component | Purpose |
|-----------|---------|
| `Aether.py` | Main entry point; initializes the interactive interface |
| `modules/` | Modular components providing core functionality |
| `requirements.txt` | Python package dependencies |

---

## Support

For issues, questions, or configuration assistance:

**Contact:** NullNexus14@proton.me

**Please provide:**
- Description of the issue or question
- Operating system and version
- Python version (`python --version`)
- Error message or screenshot (recommended)
- Steps to reproduce (if applicable)

Detailed information enables faster and more effective troubleshooting.

---

## Troubleshooting

**Common Issues**

- **Module import errors:** Verify Python 3.10+ and all dependencies are installed.
- **Permission errors:** Ensure execute permissions are set on `Aether.py` (Linux/macOS).
- **Network scanning limitations:** Some network operations may require elevated privileges.

If issues persist after standard troubleshooting, contact support with detailed system information.

---

## Contributing

Contributions, bug reports, feature requests, and suggestions are encouraged and welcome.

---

## License

Aether is distributed under the **GNU General Public License v3.0**. See `LICENSE` file for terms.

---

## Author

**NullNexus14**  
SREA - Security Research & Engineering Architecture

---

## Disclaimer

Aether is designed for legitimate system administration, network diagnostics, and security research. Users are responsible for ensuring compliance with applicable laws and organizational policies when using this toolkit.
