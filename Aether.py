#!/etc/venv/bin/python3


# --------------- IMPORTS --------------- #


import datetime
import ipaddress
import os
import platform
import random
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import psutil
import psutils
import pywifi
import rich
import scapy
import tabulate

os.system("clear")

# Optional Scapy for ARP Scan (needs sudo) #

try:
    from scapy.all import ARP, Ether, conf, get_if_addr, srp
except ImportError:
    conf = None


# --------------- COLORS --------------- #

ICE = "\033[97m"
PINK = "\033[95m"
RED = "\033[31m"
GREEN = "\033[92m"
BLUE = "\033[34m"
YELLOW = "\033[93m"
ORANGE = "\033[38;5;214m"
RESET = "\033[0m"
BOLD = "\033[1m"


# --------------- GLOBAL SETTINGS --------------- #

SILENT_MODE = False
FATAL_ERROR = False
ERROR = False
WARNING = False
ENERGY_SAVER = False


# --------------- VISUAL UTILITIES --------------- #


def wt(text, d=0.02, color=ICE, bp=True):
    global ENERGY_SAVER, SILENT_MODE
    # Adjust delay based on SILENT_MODE and ENERGY_SAVER
    delay = (d * 3 if SILENT_MODE else d) if not ENERGY_SAVER else 2.05

    for c in text:
        sys.stdout.write(color + c + RESET)
        sys.stdout.flush()
        if bp:
            sys.stdout.write("\a")
        time.sleep(delay)
    print()


def detect_energy_saver():
    global ENERGY_SAVER
    try:
        if platform.system() == "Linux":
            with open("/sys/class/power_supply/AC/online") as f:
                status = f.read().strip()
                ENERGY_SAVER = status == "0"
        elif platform.system() == "Windows":
            import ctypes

            SYSTEM_POWER_STATUS = ctypes.Structure

            class SYSTEM_POWER_STATUS(ctypes.Structure):
                _fields_ = [
                    ("ACLineStatus", ctypes.c_byte),
                    ("BatteryFlag", ctypes.c_byte),
                    ("BatteryLifePercent", ctypes.c_byte),
                    ("Reserved1", ctypes.c_byte),
                    ("BatteryLifeTime", ctypes.c_ulong),
                    ("BatteryFullLifeTime", ctypes.c_ulong),
                ]

            status = SYSTEM_POWER_STATUS()
            ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status))
            ENERGY_SAVER = status.ACLineStatus == 0
        else:
            ENERGY_SAVER = False
    except Exception:
        ENERGY_SAVER = False

    # Only print the message if not in SILENT_MODE
    if ENERGY_SAVER:
        if platform.system() == "Windows" or platform.system() == "macOS":
            message = f"{YELLOW}[!] Energy Saver mode detected. Operations will be slower to conserve battery.{RESET}\n"
            if not SILENT_MODE:
                print(message)
            logging.warning(message)  # Log this to file if needed


def fatal_error(text):
    global FATAL_ERROR
    FATAL_ERROR = True
    wt(f"\n{RED}[FATAL ERROR]{RESET} {text}\n", color=RED)
    logging.error(f"[FATAL ERROR] {text}")  # Log the error to a file
    sys.exit(1)


def detect_scapy():
    try:
        from scapy.all import conf

        if conf is None:
            raise ImportError
    except ImportError:
        wt(
            "\n[!] Scapy library not found. ARP Scan module will be disabled.\n",
            color=YELLOW,
        )
        logging.warning(
            "[!] Scapy library not found. ARP Scan module will be disabled."
        )


def step_loading(label, size=26, speed=0.02):
    global SILENT_MODE
    speed = speed * 3 if SILENT_MODE else speed
    label = label.strip()
    for i in range(size + 1):
        filled = "#" * i
        empty = "-" * (size - i)
        pct = int((i / size) * 100)

        # Ensure the progress bar reaches 100% even if there are small rounding errors
        if i == size:
            pct = 100

        if pct == 100:
            sys.stdout.write(
                f"\r{ORANGE}[LOADING]{RESET} {label:<32} "
                f"{ORANGE}[{filled}{empty}] {pct:3d}% {GREEN}[OK]{RESET}"
            )
        else:
            sys.stdout.write(
                f"\r{ORANGE}[LOADING]{RESET} {label:<32} "
                f"{ORANGE}[{filled}{empty}] {pct:3d}%{RESET}"
            )

        sys.stdout.flush()
        time.sleep(speed)
    print()


# --------------- INTRO --------------- #


def intro():
    wt("BOOTING MODULE...", bp=True)
    time.sleep(2)

    steps = [
        "Loading core systems",
        "Syncing network interfaces",
        "Initializing hardware scanners",
        "Deploying software signatures",
        "Calibrating detection algorithms",
        "Establishing secure channels",
        "Activating firewall bypass",
        "Finalizing system checks",
    ]

    for s in steps:
        step_loading(s)

    wt(f"\n{BOLD}SYSTEM CORE ONLINE{RESET}\n")

    # Ask to activate Silent Mode
    global SILENT_MODE
    print(f"{YELLOW}Activate Silent Mode? (y/n): {RESET}", end="")
    choice = input().strip().lower()
    SILENT_MODE = True if choice == "y" else False
    if SILENT_MODE:
        print(
            f"{GREEN}\n[!] Silent Mode activated. Operations will be slower to avoid detection.\n"
        )
    else:
        print(f"{RED}\n[!] Silent Mode not activated. Running normally. \n")


# --------------- LOCAL OS DETECTION --------------- #


def detect_linux():
    try:
        data = {}
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    data[k] = v.strip('"')

        if "PRETTY_NAME" in data:
            return data["PRETTY_NAME"]
        if "NAME" in data:
            return data["NAME"]

        did = data.get("ID", "").lower()

        known = {
            "arch": "Arch Linux",
            "manjaro": "Manjaro",
            "endeavouros": "EndeavourOS",
            "artix": "Artix Linux",
            "garuda": "Garuda Linux",
            "arcolinux": "ArcoLinux",
            "blackarch": "BlackArch",
            "archlabs": "ArchLabs",
            "cachyos": "CachyOS",
            "mabox": "Mabox Linux",
            "rebornos": "RebornOS",
            "archcraft": "Archcraft",
            "blendos": "blendOS",
            "crystal": "Crystal Linux",
            "archman": "Archman",
            "archbang": "ArchBang",
            "anarchy": "Anarchy Linux",
            "chakra": "Chakra Linux",
            "stormos": "StormOS",
            "biglinux": "BigLinux",
            "axyl": "Axyl",
            "debian": "Debian",
            "ubuntu": "Ubuntu",
            "linuxmint": "Linux Mint",
            "pop": "Pop!_OS",
            "kali": "Kali Linux",
            "parrot": "Parrot OS",
            "elementary": "elementary OS",
            "zorin": "Zorin OS",
            "mx": "MX Linux",
            "antix": "antiX",
            "deepin": "Deepin",
            "devuan": "Devuan",
            "pureos": "PureOS",
            "bodhi": "Bodhi Linux",
            "sparky": "SparkyLinux",
            "bunsenlabs": "BunsenLabs",
            "peppermint": "Peppermint OS",
            "siduction": "Siduction",
            "q4os": "Q4OS",
            "voyager": "Voyager Live",
            "feren": "Feren OS",
            "nitrux": "Nitrux",
            "solydxk": "SolydXK",
            "kubuntu": "Kubuntu",
            "lubuntu": "Lubuntu",
            "xubuntu": "Xubuntu",
            "ubuntu-mate": "Ubuntu MATE",
            "ubuntu-budgie": "Ubuntu Budgie",
            "ubuntu-studio": "Ubuntu Studio",
            "ubuntu-unity": "Ubuntu Unity",
            "ubuntu-kylin": "Ubuntu Kylin",
            "fedora": "Fedora",
            "rhel": "Red Hat Enterprise Linux",
            "centos": "CentOS",
            "rocky": "Rocky Linux",
            "almalinux": "AlmaLinux",
            "oracle": "Oracle Linux",
            "opensuse": "openSUSE",
            "opensuse-leap": "openSUSE Leap",
            "opensuse-tumbleweed": "openSUSE Tumbleweed",
            "sles": "SUSE Linux Enterprise",
            "nobara": "Nobara Linux",
            "clear": "Clear Linux",
            "amazonlinux": "Amazon Linux",
            "virtuozzo": "Virtuozzo",
            "eurolinux": "EuroLinux",
            "navy": "Navy Linux",
            "springdale": "Springdale Linux",
            "mageia": "Mageia",
            "openmandriva": "OpenMandriva",
            "pclinuxos": "PCLinuxOS",
            "rosalinux": "ROSA Linux",
            "gentoo": "Gentoo Linux",
            "nixos": "NixOS",
            "void": "Void Linux",
            "slackware": "Slackware Linux",
            "alpine": "Alpine Linux",
            "solus": "Solus",
            "guix": "Guix System",
            "kaos": "KaOS",
            "crux": "CRUX",
            "lfs": "Linux From Scratch",
            "chimera": "Chimera Linux",
            "serpentos": "Serpent OS",
            "steamos": "SteamOS",
            "chimeraos": "ChimeraOS",
            "batocera": "Batocera",
            "recalbox": "Recalbox",
            "lakka": "Lakka",
            "retropie": "RetroPie",
            "tails": "Tails",
            "whonix": "Whonix",
            "qubes": "Qubes OS",
            "kodachi": "Linux Kodachi",
            "septor": "Septor",
            "turing": "TuringOS",
            "raspbian": "Raspbian",
            "raspios": "Raspberry Pi OS",
            "postmarketos": "postmarketOS",
            "sailfish": "Sailfish OS",
            "utouch": "Ubuntu Touch",
            "droidian": "Droidian",
            "mobian": "Mobian",
            "openwrt": "OpenWrt",
            "dietpi": "DietPi",
            "volumio": "Volumio",
            "libreelec": "LibreELEC",
            "osmc": "OSMC",
            "zenwalk": "Zenwalk",
            "salix": "Salix",
            "vector": "VectorLinux",
            "knoppix": "Knoppix",
            "tinycore": "Tiny Core Linux",
            "puppy": "Puppy Linux",
            "slax": "Slax",
            "porteus": "Porteus",
            "fatdog": "Fatdog64",
            "4mlinux": "4MLinux",
            "tcl": "Tiny Core",
            "slitaz": "SliTaz",
            "altlinux": "ALT Linux",
            "astra": "Astra Linux",
            "redflag": "Red Flag Linux",
            "haiku": "Haiku",
            "reactos": "ReactOS",
            "minix": "MINIX",
            "proxmox": "Proxmox VE",
            "truenas": "TrueNAS SCALE",
            "unraid": "unRAID",
            "clearos": "ClearOS",
            "zentyal": "Zentyal",
            "vyos": "VyOS",
            "pfsense": "pfSense",
            "opnsense": "OPNsense",
            "astral": "Astral Linux",
            "backbox": "BackBox",
            "blackpanther": "blackPanther OS",
            "bluefin": "Bluefin",
            "bazzite": "Bazzite",
            "aurora": "Aurora OS",
            "carbon": "CarbonOS",
            "dahlia": "dahliaOS",
            "easyos": "EasyOS",
            "elive": "Elive",
            "empress": "Empress Linux",
            "endeavour": "EndeavourOS",
            "finit": "Finit",
            "foxlinux": "foxlinux",
            "frugalware": "Frugalware",
            "gecko": "GeckoLinux",
            "ghostbsd": "GhostBSD",
            "gnoppix": "Gnoppix",
            "gobo": "GoboLinux",
            "gparted": "GParted Live",
            "hamonikr": "HamoniKR",
            "hello": "helloSystem",
            "hostis": "Hostis",
            "hyperbola": "Hyperbola",
            "immortal": "Immortal OS",
            "instalinux": "Instalinux",
            "jackit": "JackIT",
            "jlinux": "JLinux",
            "jollas": "Jolla",
            "kaisen": "Kaisen Linux",
            "kali-rolling": "Kali Linux Rolling",
            "kdeneon": "KDE neon",
            "kobold": "Kobold",
            "korora": "Korora",
            "kubic": "openSUSE Kubic",
            "lax": "LaxOS",
            "leaf": "Leaf",
            "lemon": "Lemon OS",
            "libre": "Libre Linux",
            "linspire": "Linspire",
            "linux-lite": "Linux Lite",
            "loongnix": "Loongnix",
            "lycoris": "Lycoris",
            "mandriva": "Mandriva",
            "meizu": "Meizu OS",
            "mer": "Mer",
            "microos": "openSUSE MicroOS",
            "milest": "Milestone",
            "modicia": "Modicia OS",
            "mops": "MOPSLinux",
            "morph": "MorphOS",
            "neptune": "Neptune",
            "netbsd": "NetBSD",
            "netrunner": "Netrunner",
            "nexenta": "Nexenta",
            "nova": "Nova",
            "nxos": "NXOS",
            "olpc": "OLPC",
            "openindiana": "OpenIndiana",
            "openos": "OpenOS",
            "openwall": "Openwall",
            "oracle-linux": "Oracle Linux",
            "os-p": "OS/P",
            "overclock": "Overclock",
            "owrt": "OpenWrt",
            "papyros": "Papyros",
            "pardus": "Pardus",
            "parola": "Parola",
            "parrotsec": "Parrot Security OS",
            "pclinux": "PCLinuxOS",
            "pentoo": "Pentoo",
            "peropesis": "Peropesis",
            "phantom": "Phantom OS",
            "pisi": "Pisi GNU/Linux",
            "plasma": "Plasma Mobile",
            "plop": "Plop Linux",
            "pnut": "Pnut",
            "pogolinux": "Pogo Linux",
            "polaris": "Polaris",
            "popos": "Pop!_OS",
            "primeos": "PrimeOS",
            "prism": "Prism",
            "pumalinux": "Puma Linux",
            "qubesos": "Qubes OS",
            "quimo": "Quimo",
            "rax": "Rax",
            "redcore": "Redcore Linux",
            "refracta": "Refracta",
            "regata": "Regata OS",
            "rhino": "Rhino Linux",
            "rocky-linux": "Rocky Linux",
            "sabayon": "Sabayon",
            "salient": "Salient OS",
            "scientific": "Scientific Linux",
            "scout": "Scout",
            "semplice": "Semplice",
            "shark": "Shark Linux",
            "skalinux": "Ska Linux",
            "skiff": "SkiffOS",
            "sky": "SkyOS",
            "slax-linux": "Slax",
            "smoothwall": "Smoothwall",
            "softlayer": "SoftLayer",
            "solaris": "Solaris",
            "sorcerer": "Sorcerer",
            "source-mage": "Source Mage",
            "spectre": "Spectre",
            "spider": "Spider OS",
            "star": "Star Linux",
            "star-linux": "Star Linux",
            "sugar": "Sugar on a Stick",
            "superos": "SuperOS",
            "swagarch": "SwagArch",
            "swift": "Swift Linux",
            "syllable": "Syllable",
            "systemrescue": "SystemRescue",
            "tally": "Tally",
            "tmaxos": "TmaxOS",
            "toaru": "ToaruOS",
            "trisquel": "Trisquel",
            "tumbleweed": "openSUSE Tumbleweed",
            "turbolinux": "TurboLinux",
            "tux": "TuxOS",
            "ubos": "UBOS",
            "ubuntuce": "Ubuntu CE",
            "ubuntustudio": "Ubuntu Studio",
            "uco": "Ubuntu Core",
            "ultramarine": "Ultramarine Linux",
            "unbreakable": "Oracle Unbreakable",
            "unity": "Unity Operating System",
            "univention": "Univention Corporate Server",
            "unknown": "Unknown Linux",
            "venenux": "Venenux",
            "venice": "Venice",
            "venus": "Venus OS",
            "vine": "Vine Linux",
            "viper": "Viper OS",
            "visopsys": "Visopsys",
            "vms": "VMS",
            "vortex": "VortexOS",
            "vyatta": "Vyatta",
            "webos": "webOS",
            "win-linux": "Win-Linux",
            "wired": "Wired",
            "wolf": "Wolf Linux",
            "xange": "xPUD",
            "xerolinux": "XeroLinux",
            "xos": "xOS",
            "yuno": "YunoHost",
            "zevenos": "ZevenOS",
            "zil": "Zil",
            "zorinos": "Zorin OS",
            "adamantix": "Adamantix",
            "adios": "ADIOS",
            "asplinux": "ASPLinux",
            "beolinux": "BeoLinux",
            "blag": "BLAG",
            "caldera": "Caldera",
            "caos": "caOS",
            "connochaetos": "ConnochaetOS",
            "corel": "Corel Linux",
            "devil": "DeLi Linux",
            "dreamlinux": "Dreamlinux",
            "enlightenment": "Enlightenment OS",
            "eos": "EOS",
            "esware": "ESware Linux",
            "etoy": "eToy",
            "evms": "EVMS",
            "exherbo": "Exherbo",
            "finnix": "Finnix",
            "foresight": "Foresight Linux",
            "free-dos": "FreeDOS",
            "freshrpms": "FreshRPMS",
            "frugal": "Frugalware",
            "gentoo-hardened": "Hardened Gentoo",
            "gigalinux": "GigaLinux",
            "gnustep": "GNUstep",
            "guadalinex": "Guadalinex",
            "hannah": "Hannah Montana Linux",
            "im自由": "FreeOS",
            "innominate": "Innominate",
            "itautec": "Itautec",
            "kanotix": "Kanotix",
            "knoppix-std": "Knoppix STD",
            "kurumin": "Kurumin",
            "linare": "Linare",
            "linux-mandrake": "Mandrake Linux",
            "linux-ppc": "LinuxPPC",
            "lunar": "Lunar Linux",
            "mandrake": "Mandrake",
            "mandriva-one": "Mandriva One",
            "mepis": "MEPIS",
            "monkey": "Monkey Linux",
            "nas-linux": "NAS Linux",
            "newos": "NewOS",
            "open-nas": "OpenNAS",
            "openlinux": "OpenLinux",
            "os-390": "OS/390",
            "pax": "PaX Linux",
            "penguin": "PenguinOS",
            "pinguy": "Pinguy OS",
            "progeny": "Progeny",
            "puredyne": "Puredyne",
            "red-hat": "Red Hat",
            "rocks": "Rocks Cluster",
            "rpath": "rPath Linux",
            "rxlinux": "RxLinux",
            "samba": "SambaOS",
            "sgi": "SGI Linux",
            "silveros": "SilverOS",
            "skyos": "SkyOS",
            "smooth": "Smoothwall",
            "softos": "SoftOS",
            "solaris-x86": "Solaris x86",
            "sorcerer-linux": "Sorcerer",
            "stampede": "Stampede",
            "storm": "Storm Linux",
            "sun": "SunOS",
            "super": "SuperOS",
            "tarkus": "Tarkus",
            "thizlinux": "ThizLinux",
            "tomsrtbt": "tomsrtbt",
            "trustix": "Trustix",
            "turbo": "TurboLinux",
            "ultrapenguin": "UltraPenguin",
            "united": "UnitedLinux",
            "ututo": "Ututo",
            "whitebox": "White Box",
            "yellow-dog": "Yellow Dog Linux",
            "yggdrasil": "Yggdrasil",
            "yoper": "Yoper",
            "zeus": "Zeus Linux",
            "zfs": "ZFSonLinux",
            "zorp": "Zorp Linux",
            "abyss": "Abyss OS",
            "agnix": "Agnix",
            "amiga": "Amiga Linux",
            "anonymos": "Anonym.OS",
            "aquantia": "Aquantia",
            "ark": "Ark Linux",
            "asianux": "Asianux",
            "athene": "Athene",
            "atix": "Atix",
            "augustux": "Augustux",
            "auriga": "Auriga",
            "austrumi": "Austrumi",
            "axene": "Axene",
            "bados": "BadOS",
            "beos": "BeOS",
            "berry": "Berry Linux",
            "bioknoppix": "BioKnoppix",
            "bluecat": "BlueCat",
            "bluelinux": "BlueLinux",
            "bonsai": "Bonsai Linux",
            "boxer": "Boxer",
            "bright": "Bright Cluster",
            "busybox": "BusyBox Linux",
            "byzantine": "Byzantine",
            "catix": "Catix",
            "caudium": "Caudium",
            "cclinux": "CCLinux",
            "cdlinux": "CDlinux",
            "celestial": "Celestial",
            "cesar": "Cesar Linux",
            "chaos": "Chaos",
            "clarkconnect": "ClarkConnect",
            "cobalt": "Cobalt",
            "colinux": "coLinux",
            "compaq": "Compaq Linux",
            "condor": "Condor",
            "conectiva": "Conectiva",
            "core": "Core Linux",
            "coyote": "Coyote Linux",
            "darkstar": "Darkstar",
            "dbn": "DBN",
            "demolinux": "DemoLinux",
            "digit": "Digit Linux",
            "dinx": "Dinx",
            "discreete": "Discreete Linux",
            "diy": "DIY Linux",
            "dlx": "DLX",
            "dns": "DNS Linux",
            "dog": "Dog Linux",
            "dragonfly": "DragonFly BSD",
            "dyne": "dyne:bolic",
            "dz": "DZ Linux",
            "eagle": "Eagle Linux",
            "easys": "EasyS",
            "ecc": "ECC Linux",
            "eclite": "ECLite",
            "edubuntu": "Edubuntu",
            "eisfair": "eisfair",
            "elysium": "Elysium",
            "engarde": "EnGarde",
            "eon": "EON",
            "equinox": "Equinox",
            "estrellas": "Estrellas",
            "euronode": "EuroNode",
            "evo": "Evo Linux",
            "extrem": "Extrem Linux",
            "eyun": "Eyun",
            "falcon": "Falcon Linux",
            "fam": "FAM",
            "fast": "Fast Linux",
            "feather": "Feather Linux",
            "fire": "Fire Linux",
            "flex": "FlexOS",
            "floppyfw": "floppyfw",
            "flux": "FluxOS",
            "fly": "Fly Linux",
            "free-linux": "Free Linux",
            "freedeb": "FreeDebian",
            "freeduc": "Freeduc",
            "freerock": "FreeRock",
            "freesbie": "FreeSBIE",
            "frugal-os": "FrugalOS",
            "fujitsu": "Fujitsu Linux",
            "fusion": "Fusion Linux",
            "fuzz": "Fuzz Linux",
            "gamma": "Gamma Linux",
            "geexbox": "GeeXboX",
            "gemini": "Gemini OS",
            "gnadix": "Gnadix",
            "gnat": "Gnat",
            "gnix": "Gnix",
            "gnome-os": "GNOME OS",
            "gnulinux": "GNU/Linux",
            "granite": "Granite",
            "grml": "Grml",
            "guzz": "Guzz OS",
            "hakin9": "Hakin9",
            "hal": "HAL",
            "helix": "Helix",
            "heretix": "Heretix",
            "his": "HIS Linux",
            "hollywood": "Hollywood",
            "hp-ux": "HP-UX",
            "ice": "IceOS",
            "icon": "Icon Linux",
            "ident": "Ident Linux",
            "ig": "IG Linux",
            "ign": "IGN Linux",
            "inaccess": "Inaccess",
            "indy": "Indy",
            "inferno": "Inferno",
            "insigne": "Insigne",
            "interix": "Interix",
            "iron": "Iron Linux",
            "ix": "IX",
            "jamd": "Jamd",
            "java": "JavaOS",
            "jedi": "Jedi Linux",
            "jelly": "Jelly Linux",
            "jode": "Jode",
            "judas": "Judas Linux",
            "jupiter": "Jupiter",
            "just": "Just Linux",
            "k-os": "k-os",
            "kai": "Kai",
            "karma": "Karma Linux",
            "key": "KeyOS",
            "king": "King Linux",
            "kly": "Kly",
            "kore": "Kore Linux",
            "krd": "KRD",
            "ktos": "K-TOS",
            "l-os": "L-OS",
            "lamp": "LAMP Linux",
            "lbe": "LBE",
            "legacy": "Legacy Linux",
            "liberty": "Liberty Linux",
            "light": "Light Linux",
            "lim": "LIM",
            "lin": "Lin",
            "lindows": "Lindows",
            "lineox": "Lineox",
            "linux-one": "LinuxOne",
            "linuxp": "LinuxP",
            "lion": "Lion Linux",
            "live": "Live Linux",
            "local": "Local Linux",
            "loki": "Loki Linux",
            "loop": "Loop Linux",
            "lucid": "Lucid Linux",
            "lycor": "Lycoris",
            "lynx": "LynxOS",
            "mac": "Mac Linux",
            "magic": "Magic Linux",
            "mail": "Mail Linux",
            "matrix": "Matrix Linux",
            "max": "MAX",
            "media": "Media Linux",
            "micro": "Micro Linux",
            "min": "Min Linux",
            "mini": "Mini Linux",
            "miz": "Miz Linux",
            "mono": "Mono Linux",
            "moon": "Moon Linux",
            "mulinux": "muLinux",
            "multi": "Multi Linux",
            "nano": "Nano Linux",
            "native": "Native Linux",
            "net": "Net Linux",
            "nix": "Nix Linux",
            "node": "Node Linux",
            "open": "Open Linux",
            "opt": "Opt Linux",
            "os-x": "OS X Linux",
            "pax-os": "PaxOS",
            "pda": "PDA Linux",
            "pearl": "Pearl Linux",
            "phoenix": "Phoenix Linux",
            "pico": "Pico Linux",
            "pilot": "Pilot Linux",
            "pixel": "PIXEL",
            "plus": "Plus Linux",
            "pocket": "Pocket Linux",
            "power": "Power Linux",
            "prime": "Prime Linux",
            "pro": "Pro Linux",
            "pure": "Pure Linux",
            "quic": "Quic Linux",
            "r-os": "R-OS",
            "radio": "Radio Linux",
            "real": "Real Linux",
            "root": "Root Linux",
            "safe": "Safe Linux",
            "sky-linux": "Sky Linux",
            "smart": "Smart Linux",
            "soft": "Soft Linux",
            "solid": "Solid Linux",
            "sonic": "Sonic Linux",
            "star-os": "StarOS",
            "super-linux": "Super Linux",
            "t-os": "T-OS",
            "top": "Top Linux",
            "ultra": "Ultra Linux",
            "uni": "Uni Linux",
            "v-os": "V-OS",
            "vision": "Vision Linux",
            "web": "Web Linux",
            "x-os": "X-OS",
            "y-os": "Y-OS",
            "z-os": "Z-OS",
        }

        if did in known:
            return known[did]
        return f"Linux ({did or 'Unknown'})"
    except Exception:
        return "Linux (Unknown)"


def detect_device_type():
    m = platform.machine().lower()
    if "arm" in m:
        return "ARM Device"
    if "x86" in m:
        return "PC / Laptop"
    return "Unknown"


def local_os():
    s = platform.system()
    if s == "Linux":
        return detect_linux()
    if s == "Windows":
        return "Windows"
    if s == "Darwin":
        return "macOS"
    return s


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unknown"


def get_gpu_info():
    try:
        # Linux (lspci)
        if platform.system() == "Linux":
            output = subprocess.check_output(
                "lspci | grep -i 'vga\\|3d'", shell=True
            ).decode()
            gpus = [line.split(":")[-1].strip() for line in output.splitlines()]
            return gpus or ["Unknown GPU"]

        # Windows (wmic)
        elif platform.system() == "Windows":
            output = subprocess.check_output(
                "wmic path win32_VideoController get name", shell=True
            ).decode()
            gpus = [
                line.strip()
                for line in output.splitlines()
                if line.strip() and "Name" not in line
            ]
            return gpus or ["Unknown GPU"]

        # macOS
        elif platform.system() == "Darwin":
            output = subprocess.check_output(
                "system_profiler SPDisplaysDataType", shell=True
            ).decode()
            gpus = re.findall(r"Chipset Model: (.+)", output)
            return gpus or ["Unknown GPU"]

        return ["Unknown GPU"]
    except Exception:
        return ["Unknown GPU"]


def get_memory_info():
    try:
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent,
        }
    except Exception:
        return {"total": 0, "available": 0, "used": 0, "percent": 0}


def get_disks_info():
    disks = []
    for part in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(part.device)
        device_name = part.device.split("/")[-1]
        disks.append({"device": device_name, "used_percent": usage.percent})
    summary = {}
    for d in disks:
        main_dev = "".join(filter(str.isalpha, d["device"])) or d["device"]
        if main_dev not in summary:
            summary[main_dev] = d["used_percent"]
        else:
            summary[main_dev] = max(summary[main_dev], d["used_percent"])
    return [f"{dev}: {percent}%" for dev, percent in summary.items()]


def get_uptime():
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return int(uptime_seconds)
    except Exception:
        return 0


def get_mac_address():
    try:
        local_ip = get_local_ip()

        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # IPv4 match
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    # MAC detection
                    for a in addrs:
                        if a.family == psutil.AF_LINK:
                            return a.address

        return "Unknown"

    except Exception:
        return "Unknown"


def get_processor_info():
    try:
        # Prima prova a leggere il modello della CPU
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line.lower():
                    return line.split(":", 1)[1].strip()

        # Fallback al mapping noto
        p = platform.machine().lower()
        known = {
            "x86_64": "64-bit x86",
            "i386": "32-bit x86",
            "armv7l": "ARMv7",
            "aarch64": "ARM64",
            "ppc64le": "PowerPC 64-bit Little Endian",
            "s390x": "IBM Z 64-bit",
        }
        return known.get(p, platform.processor() or p.capitalize())
    except Exception:
        return "Unknown"


def build_details(osname):
    return {
        "OS": osname,
        "Kernel": platform.release(),
        "Machine": platform.machine(),
        "Platform": platform.platform(),
        "User": os.getenv("USER") or os.getenv("USERNAME") or "Unknown",
        "Device Type": detect_device_type(),
        "Local IP": get_local_ip(),
        "MAC Address": get_mac_address(),
        "Version": platform.version(),
        "Processor": get_processor_info(),
        "GPU(s)": ", ".join(get_gpu_info()),
        "Memory": get_memory_info(),
        "Disks": get_disks_info(),
        "Uptime (s)": get_uptime(),
    }


def reveal(osname, details):
    wt("\nLOCKING TARGET...", bp=True)
    step_loading("Analyzing system", size=40)

    wt(f"\n{BOLD}DETECTED OS: {osname}{RESET}")
    wt("\n-- DETAILS --\n")

    for k, v in details.items():
        wt(f"{k}: {v}")
        time.sleep(0.04)
    print()


# --------------- NETWORK MODULE --------------- #


def arp_scan(subnet, iface=None, retries=3, timeout=2):
    if conf is None:
        print("Scapy not installed.")
        return []

    conf.verb = 0

    if iface is None:
        iface = conf.route.route("0.0.0.0")[0]
    print("Using interface:", iface)

    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)

    answered = []
    for _ in range(retries):
        ans, _ = srp(pkt, timeout=timeout, retry=0, iface=iface)
        print("Responses received:", len(ans))  # debug
        answered.extend(ans)

    hosts = {}
    for _, r in answered:
        ip = r.psrc
        mac = r.hwsrc
        hosts[ip] = mac

    results = []
    for ip, mac in hosts.items():
        # Hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            hostname = "Unknown"

        # Ping alive check
        alive = False
        try:
            p = subprocess.run(
                ["ping", "-c", "1", "-W", "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            alive = p.returncode == 0
        except Exception:
            pass

        results.append({"ip": ip, "mac": mac, "hostname": hostname, "alive": alive})

    return results

    conf.verb = 0
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)

    answered = []
    for _ in range(retries):
        ans, _ = srp(pkt, timeout=timeout, retry=0)
        answered.extend(ans)

    hosts = {}
    for _, r in answered:
        ip = r.psrc
        mac = r.hwsrc
        hosts[ip] = mac
    results = []
    for ip, mac in hosts.items():
        # Hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            hostname = "Unknown"

        # Vendor MAC
        oui = mac[:8].upper()
        vendors = {
            "00:1A:2B": "Cisco",
            "3C:52:82": "Intel",
            "FC:FB:FB": "Apple",
            "B8:27:EB": "Raspberry Pi",
            "00:14:22": "Dell",
            "00:1B:63": "Apple",
            "00:0C:29": "VMware",
            "00:50:56": "VMware",
            "00:15:5D": "Microsoft",
            "00:1E:C2": "Hewlett-Packard",
            "00:25:90": "Samsung",
            "00:0F:FE": "Sony",
            "00:16:3E": "XenSource",
            "00:18:8B": "Huawei",
            "00:1D:D8": "Lenovo",
            "00:1F:3C": "Asus",
            "00:21:6A": "TP-Link",
            "00:22:43": "Netgear",
            "00:24:E8": "LG Electronics",
            "00:26:5E": "ZTE",
            "00:30:48": "Motorola",
            "00:50:DA": "Nokia",
            "00:60:2F": "Xiaomi",
            "00:80:48": "Panasonic",
            "00:90:4C": "HTC",
            "00:00:0C": "Cisco",
            "00:04:0D": "Avaya",
            "00:05:5D": "D-Link",
            "00:08:52": "Belkin",
            "00:09:5B": "Netgear",
            "00:11:2F": "Ubiquiti",
            "00:13:20": "Intel",
            "00:17:C8": "Kyocera",
            "00:1A:11": "Google",
            "00:1C:C4": "Brother",
            "00:21:2F": "Epson",
            "00:23:76": "HTC",
            "00:25:00": "Apple",
            "00:26:BB": "Apple",
            "04:18:D6": "Ubiquiti",
            "08:00:27": "Oracle (VirtualBox)",
            "10:05:01": "Amazon",
            "18:B4:30": "Nest",
            "24:5E:BE": "Xiaomi",
            "28:D2:44": "Nintendo",
            "40:B4:CD": "Amazon",
            "44:65:0D": "Amazon",
            "50:C7:BF": "TP-Link",
            "70:EE:50": "Netgear",
            "84:16:F9": "TP-Link",
        }
        vendor = vendors.get(oui, "Unknown")

        # Ping alive check
        alive = False
        try:
            subprocess.run(
                ["ping", "-c", "1", "-W", "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            alive = True
        except Exception:
            pass

        results.append(
            {
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "vendor": vendor,
                "alive": alive,
            }
        )

    return results


def guess_os_ttl(ip):
    try:
        cmd = ["ping", "-c", "1", "-W", "1", ip]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        o = p.stdout.lower()

        if "ttl=" not in o:
            return "Unknown"

        ttl = int(o.split("ttl=")[1].split()[0])
        if ttl == 64:
            return "Linux"
        if ttl == 128:
            return "Windows"
        if ttl == 255:
            return "Network Device"
        return f"Unknown (TTL={ttl})"
    except:
        return "Unknown"


def vpn_breacher(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unable to resolve"


def network_scan(subnet):
    print("\nENGAGING NETWORK MODULE...")
    hosts = arp_scan(subnet)

    if not hosts:
        print("No active hosts.\n")
        return

    print(f"\nFOUND {len(hosts)} HOSTS\n")

    global SILENT_MODE
    for h in hosts:
        ip = h["ip"]
        mac = h["mac"]

        print(f"\nTARGET    : {ip}")
        print(f"MAC       : {mac}")
        print(f"Vendor    : {h['vendor']}")
        print(f"Hostname  : {h['hostname']}")
        print(f"Alive     : {'Yes' if h['alive'] else 'No'}")
        print(f"OS Guess  : {guess_os_ttl(ip)}")
        time.sleep(0.1 * (3 if SILENT_MODE else 1))

    print("\nNetwork scan complete.\n")


def scan_all_networks():
    wt("Scan all Networks? (y/n) ", color=ORANGE, d=0.01)
    if input().strip().lower() != "y":
        wt("Skipping network scan...\n", color=RED)
        return

    wt("\nAnalyzing the Network around you...\n", bp=True)

    networks = []
    try:
        if platform.system() == "Windows":
            import subprocess

            res = subprocess.check_output("netsh wlan show networks", shell=True)
            lines = res.decode(errors="ignore").splitlines()
            for line in lines:
                if "SSID" in line:
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        networks.append(ssid)
        else:  # Linux
            import subprocess

            res = subprocess.check_output("nmcli -t -f SSID dev wifi", shell=True)
            networks = [
                n.strip() for n in res.decode(errors="ignore").splitlines() if n.strip()
            ]
    except Exception:
        pass

    if networks:
        wt(f"{len(networks)} networks found:\n", color=GREEN)
        for n in networks:
            wt(n)
    else:
        wt("No networks found.\n", color=RED)
    print()


# --------------- WI-FI SCAN MODULE --------------- #


def _get_wifi_iface():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()
    if not ifaces:
        return None
    return ifaces[0]


def _parse_security(profile):
    if not profile.akm:
        return "Open"

    akm_map = {
        pywifi.const.AKM_TYPE_NONE: "Open",
        pywifi.const.AKM_TYPE_WPA: "WPA",
        pywifi.const.AKM_TYPE_WPAPSK: "WPA-PSK",
        pywifi.const.AKM_TYPE_WPA2: "WPA2",
        pywifi.const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
        pywifi.const.AKM_TYPE_WPA3: "WPA3",
    }

    return ", ".join(akm_map.get(a, "Unknown") for a in profile.akm)


def scan_wifi_networks(scans=3, delay=1.2):
    iface = _get_wifi_iface()

    if iface is None:
        print(f"{YELLOW}No Wi-Fi interface found.{RESET}")
        return []

    print(f"\n{YELLOW}Using interface: {iface.name()}{RESET}")
    print(f"{YELLOW}Scanning available Wi-Fi networks...{RESET}")

    raw_results = []

    for _ in range(scans):
        iface.scan()
        time.sleep(delay)
        raw_results.extend(iface.scan_results())

    networks = {}
    for r in raw_results:
        key = (r.bssid, r.ssid)

        if key not in networks:
            networks[key] = {
                "ssid": r.ssid or "<hidden>",
                "bssid": r.bssid,
                "signals": [],
                "security": _parse_security(r),
                "freq": r.freq,
            }

        networks[key]["signals"].append(r.signal)

    results = []
    for n in networks.values():
        results.append(
            {
                "ssid": n["ssid"],
                "bssid": n["bssid"],
                "signal": round(sum(n["signals"]) / len(n["signals"]), 1),
                "security": n["security"],
                "freq": n["freq"],
            }
        )

    results.sort(key=lambda x: x["signal"], reverse=True)

    if not results:
        print(f"{YELLOW}No Wi-Fi networks found.{RESET}")
        return []

    print(f"{YELLOW}Found {len(results)} networks:{RESET}\n")
    for i, n in enumerate(results, 1):
        print(
            f"{YELLOW}{i}. SSID: {n['ssid']}\n"
            f"   BSSID: {n['bssid']}\n"
            f"   Signal: {n['signal']} dBm\n"
            f"   Security: {n['security']}\n"
            f"   Frequency: {n['freq']} MHz{RESET}\n"
        )

    return results


def scan_selected_wifi_network(_network):
    ip = get_local_ip()
    if ip == "Unknown":
        print(f"{YELLOW}Unable to determine local IP.{RESET}")
        return

    subnet = ".".join(ip.split(".")[:3]) + ".0/24"
    print(f"{YELLOW}Scanning local network subnet: {subnet}{RESET}")
    network_scan(subnet)


def choose_network_to_scan():
    print("\nChoose the network to scan:")
    print("1. Scan Local Network (LAN)")
    print("2. Show Wi-Fi Networks in range")

    choice = input(f"{YELLOW}Enter choice: {RESET}")

    if choice == "1":
        ip = get_local_ip()
        if ip != "Unknown":
            subnet = ".".join(ip.split(".")[:3]) + ".0/24"
            print(f"{YELLOW}Scanning local network with subnet: {subnet}{RESET}")
            network_scan(subnet)
        else:
            print(f"{YELLOW}No local network found.{RESET}")

    elif choice == "2":
        scan_wifi_networks()

    else:
        print(f"{YELLOW}Invalid choice, please select again.{RESET}")


# --------------- IP / MAC INFO UTILITIES --------------- #


def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except OSError:
        return False


def is_valid_mac(mac):
    mac = mac.lower().replace("-", ":")
    parts = mac.split(":")
    if len(parts) != 6:
        return False
    return all(len(p) == 2 and all(c in "0123456789abcdef" for c in p) for p in parts)


def ip_info(ip):
    print("\n[ IP INFO ]")
    print("IP:", ip)

    if ip.startswith("127."):
        print("Type: Loopback")
    elif ip.startswith(("10.", "192.168.", "172.")):
        print("Type: Private / Local")
    else:
        print("Type: Public")

    try:
        host = socket.gethostbyaddr(ip)[0]
        print("Hostname:", host)
    except Exception:
        print("Hostname: Not resolvable")


def mac_info(mac):
    mac = mac.lower().replace("-", ":")
    print("\n[ MAC INFO ]")
    print("MAC:", mac)

    oui = mac[:8].upper()
    vendors = {
        "00:1A:2B": "Cisco Systems",
        "3C:52:82": "Intel Corporation",
        "FC:FB:FB": "Apple",
        "B8:27:EB": "Raspberry Pi Foundation",
        "00:14:22": "Dell Inc.",
        "00:1B:63": "Apple",
        "00:0C:29": "VMware, Inc.",
        "00:50:56": "VMware, Inc.",
        "00:15:5D": "Microsoft Corporation",
        "00:1E:C2": "Hewlett-Packard",
        "00:25:90": "Samsung Electronics",
        "00:0F:FE": "Sony Interactive Entertainment",
        "00:16:3E": "XenSource",
        "00:18:8B": "Huawei Technologies",
        "00:1D:D8": "Lenovo",
        "00:1F:3C": "Asus",
        "00:21:6A": "TP-Link",
        "00:22:43": "Netgear",
        "00:24:E8": "LG Electronics",
        "00:26:5E": "ZTE Corporation",
        "00:30:48": "Motorola",
        "00:50:DA": "Nokia",
        "00:60:2F": "Xiaomi Communications",
        "00:80:48": "Panasonic",
        "00:90:4C": "HTC Corporation",
        "00:00:0C": "Cisco Systems",
        "00:04:0D": "Avaya",
        "00:05:5D": "D-Link",
        "00:08:52": "Belkin",
        "00:09:5B": "Netgear",
        "00:11:2F": "Ubiquiti Networks",
        "00:13:20": "Intel Corporation",
        "00:17:C8": "Kyocera",
        "00:1A:11": "Google",
        "00:1C:C4": "Brother Industries",
        "00:21:2F": "Epson",
        "00:23:76": "HTC Corporation",
        "00:25:00": "Apple",
        "00:26:BB": "Apple",
        "04:18:D6": "Ubiquiti Networks",
        "08:00:27": "Oracle (VirtualBox)",
        "10:05:01": "Amazon Technologies",
        "18:B4:30": "Nest Labs",
        "24:5E:BE": "Xiaomi Communications",
        "28:D2:44": "Nintendo",
        "40:B4:CD": "Amazon Technologies",
        "44:65:0D": "Amazon Technologies",
        "50:C7:BF": "TP-Link",
        "70:EE:50": "Netgear",
        "84:16:F9": "TP-Link",
    }

    print("Vendor:", vendors.get(oui, "Unknown Vendor"))


def ip_mac_info_module():
    wt("Run IP / MAC Info module? (y/n): ", d=0.01, color=ORANGE)
    if input().strip().lower() != "y":
        return

    print("\nAnalyze:")
    print("[1] IP Address")
    print("[2] MAC Address")

    choice = input("Select option: ").strip()

    if choice == "1":
        ip = input("Enter IP address: ").strip()
        if is_valid_ip(ip):
            ip_info(ip)
        else:
            print("Invalid IP address.")

    elif choice == "2":
        mac = input("Enter MAC address: ").strip()
        if is_valid_mac(mac):
            mac_info(mac)
        else:
            print("Invalid MAC address.")

    else:
        print("Invalid option.")


# --------------- MAIN --------------- #


def main():
    intro()
    osname = local_os()
    details = build_details(osname)
    reveal(osname, details)

    wt("Run network scan module? (y/n): ", d=0.01, color=ORANGE)
    if input().strip().lower() != "y":
        wt("\nShutting down...", color=BLUE)
        return

    print("\nChoose scan mode:")
    print("[1] Local LAN Scan")
    print("[2] Scan All Wi-Fi Networks Around You")

    mode = input("Select option: ").strip()

    if mode == "1":
        ip = get_local_ip()
        if ip != "Unknown":
            subnet = ".".join(ip.split(".")[:3]) + ".0/24"
            network_scan(subnet)
        else:
            print("Unable to determine subnet.")

    elif mode == "2":
        scan_all_networks()

    else:
        print("Invalid option.")

    ip_mac_info_module()
    wt("\nShutting down...", color=BLUE)
    time.sleep(1.5)


if __name__ == "__main__":
    random.seed(int(time.time()))
    main()


# --------------- END OF FILE --------------- #
# AetherProgram - 2025/2026 © SREA Malware Analisys Program
# Version 8.4.5
