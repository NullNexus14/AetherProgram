```text
 █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

> **A modern command-line toolkit for system analysis, network diagnostics, and local network scanning.**

---

## Overview

Aether is a Python-based command-line toolkit designed to provide system information, network analysis capabilities, and local security utilities through an interactive interface.

The project is designed with modularity, portability, and ease of use in mind, supporting multiple operating systems while maintaining a lightweight and extensible architecture.

---

## Available Versions

Aether is available through the official Stable Release and the legacy repository edition.

For normal usage, always use the Stable Release.

Stable Release Version (Recommended)

The Stable Release Version is the official supported distribution of Aether.

Users are strongly recommended to download the latest stable release from the Releases section.

The stable release provides:

- Complete modular architecture
- Updated dependencies and components
- Additional security analysis features
- Malware detection capabilities
- System integrity verification
- Improved platform compatibility
- Support for troubleshooting and configuration issues

The release package is designed for end users and requires only:

- Python 3.10 or newer
- Extraction of the downloaded archive

For the most complete and supported Aether experience, use the latest stable release.
---

## Features

**Core Capabilities**

- System information and diagnostics
- Network analysis tools
- Local network scanning
- Interactive command-line interface
- Modular architecture
- Cross-platform compatibility (where supported)

**Security and Forensic Analysis**

- YARA signature scanning
- MASI forensic scanner
- Browser Extension Audit (BEA)
- USB device security auditing
- System integrity analysis

**Network Monitoring and Discovery**

- Real-time network monitoring
- Enhanced port scanning
- Gateway discovery and port scanning
- ARP table enumeration
- Traceroute analysis
- Device snapshot comparison

**Release Structure**

- Stable Release Edition — official supported version with complete functionality
- Repository Edition — lightweight legacy edition for reference and experimentation

---

## Repository Edition

The contents of this repository represent the lightweight edition of Aether and related project documentation.

This edition is provided for:

- Reference purposes
- Legacy usage
- Source inspection
- Experimental usage

The repository edition is not the current supported release and may not contain the latest features, improvements, or security components.

For the complete and supported Aether experience, download the latest Stable Release from the Releases section.

---

## Installation

---
### Stable Release Installation (Recommended)

For the complete Aether experience, download the latest Stable Release from the Releases section.

The Stable Release includes:

- Complete modular architecture
- Current features and improvements
- Updated dependencies
- Security analysis components
- Supported configuration

After extraction, run Aether using the instructions below.

---

## Repository Edition Installation

The following instructions apply only to the legacy lightweight repository edition.

This edition is no longer actively maintained and is provided for reference, experimentation, and source inspection.

Clone the repository:

```bash
git clone https://github.com/NullNexus14/AetherProgram
cd AetherProgram
```

### Download the ZIP

Download the latest release and extract the archive.

Your project should have the following structure:

```text
Aether/
├── modules/
├── Aether.py
└── README.md
```

### CoreSync.py

`CoreSync.py` is a discontinued dependency installer and is no longer maintained.

The tool was deprecated 5 months ago and should not be used for new installations.

For the recommended installation method, download the latest Stable Release. The Stable Release includes all required packages within an isolated virtual environment.

Alternatively, users may install required dependencies manually.

> **Important**
>
> Run **`Aether.py`** from the project root. Do **not** execute files inside the `modules/` directory directly.

---

## Running Aether

### Linux / macOS

```bash
python3 Aether.py
```

### Windows (PowerShell)

```powershell
python Aether.py
```

### Windows (Command Prompt)

```cmd
python Aether.py
```

---

## Standalone Version

If you are using the standalone version:

```bash
python3 ./Aether.py
```

or

```powershell
python .\Aether.py
```

---

## Requirements

- Python 3.10 or newer
- Required Python modules (see `requirements.txt`, if provided)

---

## Support

If you encounter an issue or have a question, contact:

**NullNexus14@proton.me**

Please include the following information:

- Name & Surname *(Optional)*
- Greeting
- Description of the problem
- Operating System
- Screenshot of the error *(Recommended)*

Providing detailed information will help diagnose and resolve the issue more efficiently.

---

## Troubleshooting

If the issue persists after applying the suggested solution, an optimized version tailored to your operating system can be prepared if necessary.

---

## Contributing

Contributions, suggestions, bug reports, and feature requests are always welcome.

---

## License

**GNU General Public License v3.0**

---

## Author

Developed by **NullNexus14**.
***SREA - Security Research & Engineering Architecture***
