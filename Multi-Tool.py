#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════╗
#   CAMZZZ MULTI-TOOL V7  —  By camzzz
#   50+ OSINT / Network / Phone / Mail / Breach tools
#   90+ MODULES  --  By camzzz
#   https://github.com/cameleonnbss/50-multi-tool
# ╚══════════════════════════════════════════════════════╝
#
#  INSTALL :
#    pkg update && pkg upgrade
#    pkg install python python-pip
#    pip install requests colorama Pillow
#    python camzzz_v7.py

import os, sys, platform, socket, ssl, re, hashlib, base64
import time, random, string, urllib.parse, subprocess, configparser, json
import concurrent.futures
from datetime import datetime

# ── Auto-install des dependances manquantes
def _ensure_deps():
    import importlib, subprocess as _sp
    deps = {"requests": "requests", "colorama": "colorama"}
    missing = [pkg for mod, pkg in deps.items() if not importlib.util.find_spec(mod)]
    if missing:
        print(f"  Installation des dependances manquantes: {', '.join(missing)}")
        _sp.check_call([sys.executable, "-m", "pip", "install"] + missing, 
                       stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
        print("  [OK] Dependances installees. Relancement...\n")
_ensure_deps()

import requests
from colorama import Fore, Style, init

# ── Pillow (optionnel)
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_OK = True
except ImportError:
    PIL_OK = False
    Image = None
    TAGS = {}
    GPSTAGS = {}

init(autoreset=True)
SYS = platform.system().lower()
IS_TERMUX = os.path.isdir("/data/data/com.termux") if sys.platform != "win32" else False

# ══════════════════════════════════════════════════════════════
#  SYSTEME DE CONFIG AUTOMATIQUE
#  Fichier : config.ini (meme dossier que le script)
#  Cree automatiquement au premier lancement
# ══════════════════════════════════════════════════════════════

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

CONFIG_TEMPLATE = """\
# ╔══════════════════════════════════════════════════╗
#   CAMZZZ MULTI-TOOL V7 — Config API Keys
#   Remplis tes cles ici, elles seront chargees
#   automatiquement a chaque lancement.
# ╚══════════════════════════════════════════════════╝

[API_KEYS]
# LeakCheck — Free tier 50 req/mois
# Inscription : https://leakcheck.io
leakcheck_key =

# BreachDirectory via RapidAPI — Free tier dispo
# Inscription : https://rapidapi.com/rohan-patra/api/breachdirectory
breachdirectory_key =

# Shodan — Free tier (scan limité)
# Inscription : https://account.shodan.io/register
shodan_key =

# Hunter.io — Free tier 25 req/mois
# Inscription : https://hunter.io/users/sign_up
hunter_key =

# VirusTotal — Free tier 500 req/jour
# Inscription : https://www.virustotal.com/gui/join-us
virustotal_key =

# WormGPT — IA integree au multi-tool
# Cle gratuite sur : https://chat.wrmgpt.com
wormgpt_key =

[SETTINGS]
# Timeout des requetes en secondes
timeout = 10
# Afficher l'intro animee au lancement (true/false)
show_intro = true
# Langue (fr/en)
lang = fr
"""

def load_config():
    """Charge ou cree le fichier config.ini automatiquement."""
    cfg = configparser.ConfigParser()

    if not os.path.exists(CONFIG_FILE):
        # Premier lancement : cree le fichier config vide
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(CONFIG_TEMPLATE)
        print(f"\033[93m  [CONFIG]  Fichier config.ini cree : {CONFIG_FILE}\033[0m")
        print(f"\033[93m  [CONFIG]  Remplis tes cles API dedans pour les charger automatiquement.\033[0m\n")
        time.sleep(1.5)

    cfg.read(CONFIG_FILE, encoding="utf-8")
    return cfg

def get_key(cfg, name, fallback=""):
    """Recupere une cle API depuis la config, avec fallback."""
    try:
        val = cfg.get("API_KEYS", name, fallback=fallback).strip()
        return val if val else fallback
    except Exception:
        return fallback

def save_key(name, value):
    """Sauvegarde une cle API dans config.ini."""
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE, encoding="utf-8")
    if not cfg.has_section("API_KEYS"):
        cfg.add_section("API_KEYS")
    cfg.set("API_KEYS", name, value)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)

def get_setting(cfg, name, fallback=""):
    """Recupere un parametre depuis [SETTINGS]."""
    try:
        return cfg.get("SETTINGS", name, fallback=fallback).strip()
    except Exception:
        return fallback

# Chargement au demarrage
_CFG = load_config()

# Cles chargees automatiquement
LEAKCHECK_KEY   = get_key(_CFG, "leakcheck_key")
BREACHDIR_KEY   = get_key(_CFG, "breachdirectory_key")
SHODAN_KEY      = get_key(_CFG, "shodan_key")
HUNTER_KEY      = get_key(_CFG, "hunter_key")
VIRUSTOTAL_KEY  = get_key(_CFG, "virustotal_key")
WORMGPT_KEY     = get_key(_CFG, "wormgpt_key")

# Settings
REQ_TIMEOUT  = int(get_setting(_CFG, "timeout", "10"))
SHOW_INTRO   = get_setting(_CFG, "show_intro", "true").lower() == "true"

G=Fore.GREEN;  LG=Fore.LIGHTGREEN_EX
Y=Fore.YELLOW; LY=Fore.LIGHTYELLOW_EX
C=Fore.CYAN;   LC=Fore.LIGHTCYAN_EX
R=Fore.RED;    LR=Fore.LIGHTRED_EX
M=Fore.MAGENTA;LM=Fore.LIGHTMAGENTA_EX
W=Fore.WHITE;  LW=Fore.LIGHTWHITE_EX
DIM=Style.DIM

# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def clear(): os.system("cls" if sys.platform == "win32" else "clear")

def pause():
    print()
    input(LG +
        "  ╔════════════════════════════════════╗\n"
        "  ║   ENTER  to return to main menu   ║\n"
        "  ╚════════════════════════════════════╝  ")

def row(l, v, lc=C, vc=LW):
    print(lc + f"  {str(l):<28}" + vc + f" {str(v)[:72]}")

def section(t, col=LG):
    w=56; pad=(w-len(t)-2)//2; ex=w-pad-len(t)-2
    print()
    print(col + f"  ╔{'═'*w}╗")
    print(col + f"  ║{' '*pad} {t} {' '*ex}║")
    print(col + f"  ╚{'═'*w}╝")
    print()

def spinner(label, dur=1.0, col=LG):
    # ASCII fallback — compatible tous terminaux
    frames = ["-", "\\", "|", "/"]
    end = time.time() + dur; i = 0
    while time.time() < end:
        sys.stdout.write(col + f"\r  {frames[i%4]}  {label}   ")
        sys.stdout.flush(); time.sleep(0.1); i += 1
    sys.stdout.write("\r" + " "*72 + "\r"); sys.stdout.flush()

def bar(label, steps=30, delay=0.022, col=LG, bc=G):
    for i in range(steps+1):
        f = "#"*i + "."*(steps-i); pct = int(i/steps*100)
        sys.stdout.write(col + f"\r  {label}  " + bc + f"[{f}]" + LW + f" {pct:3d}%")
        sys.stdout.flush(); time.sleep(delay)
    print()

def glitch(text, rounds=4, col=LG):
    noise = "@#$%&?!*~^<>|"
    for _ in range(rounds):
        g = "".join(random.choice(noise) if random.random()<0.25 else ch for ch in text)
        sys.stdout.write("\r"+col+g); sys.stdout.flush(); time.sleep(0.06)
    sys.stdout.write("\r"+col+text+"\n"); sys.stdout.flush()

def matrix_rain(lines=8, width=70):
    chars = "01@#$%^&*<>!? ABCDEF"
    cols = [G,LG,C,LC,LM,LY,Y]
    for _ in range(lines):
        line = "".join(random.choice(chars) if random.random()>0.62 else " " for _ in range(width))
        print(random.choice(cols) + "  " + line); time.sleep(0.03)

def rainbow(text):
    cols=[LR,Y,LG,LC,LM,LW,LY,LC]
    print("".join(cols[i%len(cols)]+ch for i,ch in enumerate(text)))

def blink(text, times=3, col=LG):
    for _ in range(times):
        sys.stdout.write("\r"+col+text); sys.stdout.flush(); time.sleep(0.28)
        sys.stdout.write("\r"+" "*len(text)); sys.stdout.flush(); time.sleep(0.18)
    sys.stdout.write("\r"+col+text+"\n"); sys.stdout.flush()

def qenc(q): return urllib.parse.quote(str(q))

def link(name, url, col=LC):
    print(col + f"  {name:<28}" + LW + f" {url}")

# ──────────────────────────────────────────────
#  ASCII ART / BANNER
# ──────────────────────────────────────────────

CAMZZZ_LINES = [
    "   ___   _   __  __ _____  ____  ____     __  __ _   _ _  _____ ___ ",
    "  / __| /_\\ |  \\/  |__  ||_  / |_  /    |  \\/  | | | | ||_   _|__ \\",
    " | (__ / _ \\| |\\/| | / /  / /   / /     | |\\/| | |_| | |__| |  /_/ /",
    "  \\___/_/ \\_\\_|  |_|/___|/___|/___|    |_|  |_|\\___/|____|_| (_)  ",
]

BANNER = """
==================================================================================================
/*  _____                                                      _____  */
/* ( ___ )                                                    ( ___ ) */
/*  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |  */
/*  |   |   _________ _____ ___  ____________                  |   |  */
/*  |   |  / ___/ __ `/ __ `__ \\/_  /_  /_  /                  |   |  */
/*  |   | / /__/ /_/ / / / / / / / /_/ /_/ /_                  |   |  */
/*  |   | \\___/\\__,_/_/ /_/ /_/_/___/___/___/_              __ |   |  */
/*  |   |    ____ ___  __  __/ / /_(_)     / /_____  ____  / / |   |  */
/*  |   |   / __ `__ \\/ / / / / __/ /_____/ __/ __ \\/ __ \\/ /  |   |  */
/*  |   |  / / / / / / /_/ / / /_/ /_____/ /_/ /_/ / /_/ / /   |   |  */
/*  |   | /_/ /_/ /_/\\__,_/_/\\__/_/      \\__/\\____/\\____/_/    |   |  */
/*  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|  */
/* (_____)                                                    (_____) */

  C A M Z Z Z   M U L T I - T O O L  ·  V 7  ·  9 0 +  M O D U L E S
==================================================================================================
"""

BOOT_FRAMES = [
"  [          ]  BOOTING...",
"  [####      ]  LOADING MODULES...",
"  [########  ]  NETWORK READY...",
"  [##########]  ACCESS GRANTED - Welcome, camzzz  --  90+ modules",
]

LOGOS = {
"ip":     (LG,  "  [ IP LOOKUP ]"),
"phone":  (LC,  "  [ PHONE INFO ]"),
"mail":   (LM,  "  [ MAIL REINT ]"),
"breach": (LR,  "  [ BREACH DB ]"),
"user":   (LM,  "  [ USERNAME ]"),
"port":   (LG,  "  [ PORT SCAN ]"),
"sub":    (LC,  "  [ SUBDOMAIN ]"),
"geo":    (LY,  "  [ GEO IP ]"),
"hash":   (LM,  "  [ HASH TOOL ]"),
"pass":   (LM,  "  [ PASSWORD ]"),
"cam":    (LR,  "  [ CAMERAS ]"),
"dork":   (LY,  "  [ DORK GEN ]"),
}

def show_logo(key):
    clear()
    col, label = LOGOS.get(key, (LG, "  [ TOOL ]"))
    print()
    print(col + "  " + "="*60)
    print(col + label)
    print(col + "  " + "="*60)
    print()

# ──────────────────────────────────────────────
#  INTRO
# ──────────────────────────────────────────────

def intro():
    if not SHOW_INTRO:
        return
    clear()
    matrix_rain(4, 60)
    time.sleep(0.1); clear()
    for frame in BOOT_FRAMES:
        clear(); print(LG + "\n" + frame); time.sleep(0.35)
    time.sleep(0.2); clear()
    print(LG + "\n  " + "="*60)
    glitch("         B Y   C A M Z Z Z   --   V 7   --   9 0 +   M O D U L E S", 4, LG)
    print(LG + "  " + "="*60 + "\n")
    for line in CAMZZZ_LINES:
        rainbow("  " + line); time.sleep(0.05)
    print(); blink("  >>> ALL SYSTEMS ONLINE  -  By camzzz  -  90+ MODULES  <<<", 3, LG)
    time.sleep(0.4); clear()

# ──────────────────────────────────────────────
#  BANNER
# ──────────────────────────────────────────────

def banner():
    print(LG + BANNER)
    for line in CAMZZZ_LINES:
        rainbow("  " + line)
    print()
    print(C + "  " + "-"*70)
    print(C + f"  # {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}  #  By camzzz  #  V7  #  90+ modules")
    print(C + "  " + "-"*70)
    print()

# ──────────────────────────────────────────────
#  ① IP INFO
# ──────────────────────────────────────────────

def ip_info():
    show_logo("ip")
    print(LW + "  1  My own public IP\n  2  Look up any IP\n  3  IP reputation links\n  4  IP range scanner (/24)")
    c = input(LG + "\n  Choice > ").strip()

    if c == "1":
        spinner("Fetching your IP", 1.0, LG)
        try:
            pub = requests.get("https://api.ipify.org?format=json", timeout=8).json()
            ip  = pub.get("ip","?")
            geo = requests.get(f"https://ipapi.co/{ip}/json", timeout=8).json()
            section("YOUR PUBLIC IP", LG)
            for f in ["ip","country_name","region","city","postal","org","asn","timezone","latitude","longitude","currency"]:
                v = geo.get(f,"N/A")
                if v and v != "N/A": row(f, v, LG, LW)
            lat,lon = geo.get("latitude",""),geo.get("longitude","")
            if lat and lon:
                print(); print(LG + f"  Maps   : https://maps.google.com/?q={lat},{lon}")
        except Exception as e:
            print(LR + f"  Failed: {e}")

    elif c == "2":
        ip = input(LG + "  IP address > ").strip()
        if not ip: pause(); return
        spinner(f"Querying {ip}", 1.0, LG)
        try:
            geo  = requests.get(f"https://ipapi.co/{ip}/json", timeout=10).json()
            geo2 = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
            section(f"IP INFO — {ip}", LG)
            fields = ["country_name","region","city","postal","latitude","longitude",
                      "timezone","org","asn","currency","languages","network","version"]
            for f in fields:
                v = geo.get(f) or geo2.get(f,"N/A")
                if v and v!="N/A": row(f, v, LG, LW)
            lat,lon = geo.get("latitude",""),geo.get("longitude","")
            if lat and lon:
                print(); print(LG + f"  Google Maps : https://maps.google.com/?q={lat},{lon}")
            section("REPUTATION LINKS", LG)
            for name,lnk in [
                ("VirusTotal", f"https://www.virustotal.com/gui/ip-address/{ip}"),
                ("AbuseIPDB",  f"https://www.abuseipdb.com/check/{ip}"),
                ("Shodan",     f"https://www.shodan.io/host/{ip}"),
                ("Greynoise",  f"https://viz.greynoise.io/ip/{ip}"),
                ("Censys",     f"https://search.censys.io/hosts/{ip}"),
                ("Talos",      f"https://talosintelligence.com/reputation_center/lookup?search={ip}"),
                ("Spamhaus",   f"https://check.spamhaus.org/query/ip/{ip}"),
            ]: link(name, lnk, LC)
        except Exception as e:
            print(LR + f"  Failed: {e}")

    elif c == "3":
        ip = input(LG + "  IP address > ").strip()
        section("FULL REPUTATION LINKS", LG)
        for name,lnk in [
            ("AbuseIPDB",       f"https://www.abuseipdb.com/check/{ip}"),
            ("VirusTotal",      f"https://www.virustotal.com/gui/ip-address/{ip}"),
            ("Shodan",          f"https://www.shodan.io/host/{ip}"),
            ("Greynoise",       f"https://viz.greynoise.io/ip/{ip}"),
            ("Censys",          f"https://search.censys.io/hosts/{ip}"),
            ("IPVoid",          f"https://www.ipvoid.com/ip-blacklist-check/?ip={ip}"),
            ("Talos",           f"https://talosintelligence.com/reputation_center/lookup?search={ip}"),
            ("MXToolbox",       f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip}"),
            ("Spamhaus",        f"https://check.spamhaus.org/query/ip/{ip}"),
            ("IPQualityScore",  f"https://www.ipqualityscore.com/ip-reputation/proxy-vpn-bot-check/{ip}"),
            ("OTX AlienVault",  f"https://otx.alienvault.com/indicator/ip/{ip}"),
            ("BinaryEdge",      f"https://app.binaryedge.io/services/query?query={qenc(ip)}"),
        ]: link(name, lnk, LC)

    elif c == "4":
        cidr = input(LG + "  IP/24 prefix (e.g. 192.168.1) > ").strip()
        if not cidr: pause(); return
        spinner("Scanning subnet", 1.0, LG)
        found=[]
        def chk(i):
            ip2 = f"{cidr}.{i}"
            try:
                s = socket.socket(); s.settimeout(0.4)
                if s.connect_ex((ip2, 80)) == 0: return ip2
                s.close()
            except: return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
            results = list(ex.map(chk, range(1,255)))
        section("LIVE HOSTS", LG)
        for r in [r for r in results if r]:
            found.append(r); print(LG + f"  [+]  {r}")
        print(LG + f"\n  {len(found)} host(s) found.")
    pause()

# ──────────────────────────────────────────────
#  ② TRACEROUTE (pur Python)
# ──────────────────────────────────────────────

def traceroute():
    show_logo("geo")
    host = input(LY + "  Host/IP > ").strip()
    if not host: pause(); return
    try:
        dest_ip = socket.gethostbyname(host)
    except Exception as e:
        print(LR + f"  DNS failed: {e}"); pause(); return

    section(f"TRACEROUTE — {host} ({dest_ip})", LY)

    # Windows: utilise tracert natif
    if sys.platform == "win32":
        try:
            print(LY + "  Utilisation de tracert (Windows natif)...\n")
            result = subprocess.run(
                ["tracert", "-d", "-h", "30", host],
                text=True, timeout=60)
        except Exception as ex:
            print(LR + f"  tracert failed: {ex}")
        pause(); return

    print(LY + f"  {'HOP':<5} {'IP':<20} {'RTT':<12} {'HOSTNAME'}")
    print(LY + "  " + "-"*60)

    port = 33434
    max_hops = 30
    timeout = 2.0

    for ttl in range(1, max_hops + 1):
        rtt = None; recv_ip = None; hostname = "?"
        try:
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            recv_sock.settimeout(timeout)
            start = time.time()
            send_sock.sendto(b"", (dest_ip, port))
            try:
                data, addr = recv_sock.recvfrom(512)
                recv_ip = addr[0]
                rtt = (time.time() - start) * 1000
                try:
                    hostname = socket.gethostbyaddr(recv_ip)[0]
                except: hostname = recv_ip
            except socket.timeout:
                recv_ip = "*"
        except PermissionError:
            # RAW sockets need root — fallback to subprocess ping per hop
            try:
                cmd = ["ping", "-c", "1", "-W", "1", "-t", str(ttl), dest_ip]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                rtt_m = re.search(r"time=([\d.]+)", result.stdout)
                rtt = float(rtt_m.group(1)) if rtt_m else None
                recv_ip = dest_ip if result.returncode == 0 else "*"
                hostname = recv_ip
            except Exception:
                recv_ip = "*"; hostname = "?"
        finally:
            try: send_sock.close()
            except: pass
            try: recv_sock.close()
            except: pass

        rtt_str = f"{rtt:.1f}ms" if rtt else "*"
        col = LG if recv_ip == dest_ip else LY if recv_ip != "*" else DIM+LW
        print(col + f"  {ttl:<5} {str(recv_ip):<20} {rtt_str:<12} {hostname}")

        if recv_ip == dest_ip:
            print(LG + f"\n  Destination reached in {ttl} hops.")
            break

    pause()

# ──────────────────────────────────────────────
#  ③ BANNER GRABBER
# ──────────────────────────────────────────────

def banner_grab():
    show_logo("port")
    host = input(LG + "  Host/IP > ").strip()
    if not host: pause(); return
    ports_input = input(LG + "  Ports (e.g. 21,22,80,443,8080) > ").strip()
    try:
        ports = [int(p.strip()) for p in ports_input.split(",") if p.strip()]
    except Exception:
        print(LR + "  Invalid ports."); pause(); return

    section(f"BANNER GRABBER — {host}", LG)

    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((host, port))
            # Send a probe for HTTP-like services
            if port in [80, 8080, 8000, 8888]:
                s.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
            elif port == 443:
                s.close()
                ctx = ssl.create_default_context()
                ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(socket.socket(), server_hostname=host)
                s.settimeout(3); s.connect((host, 443))
                s.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
            banner = s.recv(1024).decode(errors="replace").strip()[:200]
            s.close()
            print(LG + f"\n  Port {port}:")
            for line in banner.split("\n")[:8]:
                print(LW + f"    {line.strip()}")
        except ConnectionRefusedError:
            print(DIM + LW + f"  Port {port}: Closed")
        except Exception as e:
            print(LY + f"  Port {port}: {e}")

    pause()

# ──────────────────────────────────────────────
#  ④ MAC VENDOR LOOKUP
# ──────────────────────────────────────────────

def mac_lookup():
    show_logo("geo")
    mac = input(LY + "  MAC address (e.g. 00:1A:2B:3C:4D:5E) > ").strip()
    if not mac: pause(); return
    mac_clean = mac.upper().replace("-",":").replace(".",":")
    # Take OUI (first 6 hex chars)
    oui = re.sub(r"[^0-9A-F]","",mac_clean)[:6]
    spinner("Looking up MAC vendor", 1.0, LY)
    try:
        r = requests.get(f"https://api.macvendors.com/{qenc(mac_clean)}", timeout=8)
        section("MAC VENDOR INFO", LY)
        row("MAC",    mac_clean,    LY, LW)
        row("OUI",    oui,          LY, LW)
        if r.status_code == 200:
            row("Vendor", r.text.strip(), LY, LG)
        else:
            row("Vendor", "Not found", LY, LR)
        print()
        link("MAClookup.app", f"https://maclookup.app/search/result?mac={qenc(mac_clean)}", LC)
        link("Wireshark OUI", f"https://www.wireshark.org/tools/oui-lookup.html", LC)
    except Exception as e:
        print(LR + f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑤ HTTP METHOD TESTER
# ──────────────────────────────────────────────

def http_method_tester():
    show_logo("port")
    url = input(LG + "  URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS",
               "HEAD", "TRACE", "CONNECT"]
    section("HTTP METHOD TESTER", LG)
    print(LG + f"  {'METHOD':<12} {'STATUS':<10} {'LENGTH':<12} {'SERVER'}")
    print(LG + "  " + "-"*60)
    hdrs = {"User-Agent": "Mozilla/5.0"}
    for method in methods:
        try:
            r = requests.request(method, url, timeout=6, headers=hdrs,
                                 allow_redirects=False)
            col = LG if r.status_code < 300 else LY if r.status_code < 400 else LR
            server = r.headers.get("Server","?")[:20]
            danger = ""
            if method in ["TRACE","PUT","DELETE"] and r.status_code < 400:
                danger = LR + " [!!! DANGEROUS ENABLED]"
            print(col + f"  {method:<12} {r.status_code:<10} {len(r.content):<12} {server}" + danger)
        except Exception as e:
            print(DIM + LW + f"  {method:<12} ERR: {str(e)[:40]}")
    pause()

# ──────────────────────────────────────────────
#  ⑥ CORS CHECKER
# ──────────────────────────────────────────────

def cors_checker():
    show_logo("port")
    url = input(LG + "  URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url
    origins = [
        "https://evil.com",
        "null",
        "https://attacker.example.com",
        url,  # same origin
    ]
    section("CORS MISCONFIGURATION CHECK", LG)
    for origin in origins:
        try:
            r = requests.get(url, timeout=6, headers={
                "Origin": origin,
                "User-Agent": "Mozilla/5.0"
            })
            acao = r.headers.get("Access-Control-Allow-Origin","")
            acac = r.headers.get("Access-Control-Allow-Credentials","")
            if acao == "*":
                print(LR + f"  [VULN] Wildcard CORS: origin={origin} -> ACAO=*")
            elif acao == origin and origin == "https://evil.com":
                print(LR + f"  [VULN] Reflects evil origin! ACAO={acao}")
            elif acao and acac.lower() == "true" and acao != url:
                print(LR + f"  [VULN] Credentials + reflected: ACAO={acao}")
            else:
                col = LG if not acao else LY
                print(col + f"  [  OK] origin={origin[:30]:<35} ACAO={acao[:30] or 'none'}")
        except Exception as e:
            print(LY + f"  [ERR] {origin}: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑦ TOR CHECK
# ──────────────────────────────────────────────

def tor_check():
    show_logo("geo")
    ip = input(LY + "  IP to check (blank = your IP) > ").strip()
    spinner("Checking Tor exit node status", 1.2, LY)
    try:
        if not ip:
            ip = requests.get("https://api.ipify.org", timeout=8).text.strip()
        section(f"TOR CHECK — {ip}", LY)
        row("IP", ip, LY, LW)
        # Method 1 : dan.me.uk
        r = requests.get(f"https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip=1.1.1.1",
                         timeout=8)
        exit_ips = set(r.text.strip().split("\n"))
        is_tor = ip in exit_ips
        row("Is Tor exit node", "YES [!]" if is_tor else "No", LY,
            LR if is_tor else LG)
        print()
        # Method 2 : links
        for name, lnk in [
            ("TorProject check",  f"https://check.torproject.org/"),
            ("IPQualityScore",    f"https://www.ipqualityscore.com/ip-reputation/proxy-vpn-bot-check/{ip}"),
            ("Shodan",            f"https://www.shodan.io/host/{ip}"),
            ("Greynoise",         f"https://viz.greynoise.io/ip/{ip}"),
        ]: link(name, lnk, LC)
    except Exception as e:
        print(LR + f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑧ DNS BRUTE FORCE (amélioré)
# ──────────────────────────────────────────────

# Wordlist etendue
SUBS_EXT = [
    "www","mail","ftp","smtp","pop","imap","webmail","cpanel","admin","api",
    "dev","staging","test","beta","app","portal","dashboard","blog","shop",
    "store","forum","support","help","docs","cdn","static","media","img",
    "images","video","files","download","upload","auth","login","secure",
    "vpn","ssh","git","gitlab","jenkins","ci","status","monitor","grafana",
    "ns1","ns2","mx","mx1","mx2","remote","owa","exchange","autodiscover",
    "m","mobile","panel","server","host","cloud","backup","old","new","v1",
    "v2","api2","search","news","web","assets","s3","bucket","data","db",
    "database","internal","intranet","extranet","private","public","corp",
    "crm","erp","vpn2","proxy","gateway","relay","sftp","ntp","ldap","jira",
    "confluence","wiki","redmine","phpmyadmin","mysql","postgres","elastic",
    "kibana","grafana","prometheus","nagios","zabbix","splunk","jenkins",
    "sonar","nexus","artifactory","registry","k8s","kube","rancher",
    "smtp2","pop3","imap4","autodiscover","webdisk","whm","cpcalendars",
    "cpcontacts","mail2","secure","ssl","ns3","ns4","vps","server1","server2",
    "demo","pre","preprod","uat","qa","prod","production","mx3","email",
    "assets2","cdn2","img2","api3","api4","graphql","rest","rpc","grpc",
]

def subdomain_finder():
    show_logo("sub")
    domain = input(LC + "  Domain > ").strip()
    if not domain: pause(); return
    bar("  Building wordlist", 20, 0.015, LC, C)
    print(LC + f"\n  Testing {len(SUBS_EXT)} subdomains on {domain}...\n")
    found=[]
    def chk(sub):
        t = f"{sub}.{domain}"
        try: return (t, socket.gethostbyname(t))
        except: return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        results = list(ex.map(chk, SUBS_EXT))
    section("FOUND SUBDOMAINS", LC)
    for r in [r for r in results if r]:
        sub, ip = r; found.append(sub)
        print(LC + f"  [+]  {sub:<46}" + LW + f" -> {ip}")
    print(LC + f"\n  {len(found)} subdomain(s) found.")
    section("PASSIVE SEARCH LINKS", LC)
    e = qenc(domain)
    for name, lnk in [
        ("crt.sh",       f"https://crt.sh/?q=%.{domain}"),
        ("Shodan",       f"https://www.shodan.io/domain/{domain}"),
        ("URLScan",      f"https://urlscan.io/search/#{e}"),
        ("VirusTotal",   f"https://www.virustotal.com/gui/domain/{domain}/relations"),
        ("SecurityTrails",f"https://securitytrails.com/domain/{domain}/subdomains"),
        ("Censys",       f"https://search.censys.io/search?resource=hosts&q={e}"),
    ]: link(name, lnk, LC)
    pause()

# ──────────────────────────────────────────────
#  PHONE — base de données
# ──────────────────────────────────────────────

PHONE_DB = {
    "+1":{  "country":"USA / Canada",     "region":"North America","tz":"UTC-5 to UTC-8","fmt":"(XXX) XXX-XXXX"},
    "+7":{  "country":"Russia/Kazakhstan","region":"Eurasia",      "tz":"UTC+2 to UTC+12","fmt":"8 (XXX) XXX-XX-XX"},
    "+33":{ "country":"France",           "region":"Europe",       "tz":"UTC+1","fmt":"0X XX XX XX XX"},
    "+44":{ "country":"United Kingdom",   "region":"Europe",       "tz":"UTC+0","fmt":"0XXXX XXXXXX"},
    "+49":{ "country":"Germany",          "region":"Europe",       "tz":"UTC+1","fmt":"0XXX XXXXXXXX"},
    "+34":{ "country":"Spain",            "region":"Europe",       "tz":"UTC+1","fmt":"XXX XXX XXX"},
    "+39":{ "country":"Italy",            "region":"Europe",       "tz":"UTC+1","fmt":"XXX XXX XXXX"},
    "+31":{ "country":"Netherlands",      "region":"Europe",       "tz":"UTC+1","fmt":"0XX XXX XXXX"},
    "+32":{ "country":"Belgium",          "region":"Europe",       "tz":"UTC+1","fmt":"0XXX XX XX XX"},
    "+41":{ "country":"Switzerland",      "region":"Europe",       "tz":"UTC+1","fmt":"0XX XXX XXXX"},
    "+46":{ "country":"Sweden",           "region":"Europe",       "tz":"UTC+1","fmt":"0XX XXX XXXX"},
    "+47":{ "country":"Norway",           "region":"Europe",       "tz":"UTC+1","fmt":"XXX XX XXX"},
    "+48":{ "country":"Poland",           "region":"Europe",       "tz":"UTC+1","fmt":"XXX XXX XXX"},
    "+351":{"country":"Portugal",         "region":"Europe",       "tz":"UTC+0","fmt":"XXX XXX XXX"},
    "+380":{"country":"Ukraine",          "region":"Europe",       "tz":"UTC+2","fmt":"0XX XXX XXXX"},
    "+86":{ "country":"China",            "region":"Asia",         "tz":"UTC+8","fmt":"0XX XXXX XXXX"},
    "+91":{ "country":"India",            "region":"Asia",         "tz":"UTC+5:30","fmt":"XXXXX XXXXX"},
    "+81":{ "country":"Japan",            "region":"Asia",         "tz":"UTC+9","fmt":"0X XXXX XXXX"},
    "+82":{ "country":"South Korea",      "region":"Asia",         "tz":"UTC+9","fmt":"0X XXXX XXXX"},
    "+55":{ "country":"Brazil",           "region":"South America","tz":"UTC-3","fmt":"(XX) XXXXX-XXXX"},
    "+52":{ "country":"Mexico",           "region":"North America","tz":"UTC-6","fmt":"XXX XXX XXXX"},
    "+90":{ "country":"Turkey",           "region":"Europe/Asia",  "tz":"UTC+3","fmt":"0XXX XXX XXXX"},
    "+212":{"country":"Morocco",          "region":"Africa",       "tz":"UTC+1","fmt":"0XXX XXXXXX"},
    "+213":{"country":"Algeria",          "region":"Africa",       "tz":"UTC+1","fmt":"0XXX XXXXXX"},
    "+216":{"country":"Tunisia",          "region":"Africa",       "tz":"UTC+1","fmt":"XX XXX XXX"},
    "+234":{"country":"Nigeria",          "region":"Africa",       "tz":"UTC+1","fmt":"0XXX XXX XXXX"},
    "+971":{"country":"UAE",              "region":"Middle East",  "tz":"UTC+4","fmt":"0X XXX XXXX"},
    "+966":{"country":"Saudi Arabia",     "region":"Middle East",  "tz":"UTC+3","fmt":"0XX XXX XXXX"},
    "+972":{"country":"Israel",           "region":"Middle East",  "tz":"UTC+2","fmt":"0XX XXX XXXX"},
    "+92":{ "country":"Pakistan",         "region":"Asia",         "tz":"UTC+5","fmt":"0XXX XXX XXXX"},
    "+62":{ "country":"Indonesia",        "region":"Asia",         "tz":"UTC+7 to +9","fmt":"0XXX XXXX XXXX"},
    "+60":{ "country":"Malaysia",         "region":"Asia",         "tz":"UTC+8","fmt":"0X XXXX XXXX"},
    "+63":{ "country":"Philippines",      "region":"Asia",         "tz":"UTC+8","fmt":"0XXX XXX XXXX"},
    "+61":{ "country":"Australia",        "region":"Oceania",      "tz":"UTC+8 to +11","fmt":"0X XXXX XXXX"},
    "+64":{ "country":"New Zealand",      "region":"Oceania",      "tz":"UTC+12","fmt":"0X XXX XXXX"},
}

FR_LINES = {
    "06":"Mobile - Orange / SFR / Bouygues / Free",
    "07":"Mobile - Free Mobile / MVNO",
    "01":"Ile-de-France (fixe)",
    "02":"Nord-Ouest France (fixe)",
    "03":"Nord-Est France (fixe)",
    "04":"Sud-Est France (fixe)",
    "05":"Sud-Ouest France (fixe)",
    "08":"Numero special (surtaxe / gratuit / vert)",
    "09":"VoIP / Box Internet",
}

EXPECTED_LEN = {
    "+33":11,"+44":12,"+1":11,"+49":12,"+34":11,"+39":12,
    "+31":11,"+32":11,"+41":11,"+46":11,"+47":11,"+48":11,
    "+81":11,"+82":11,"+86":11,"+91":12,"+55":13,
}

def phone_info():
    show_logo("phone")
    print(LC + "  1  Full phone OSINT  (analysis + owner search + social accounts)")
    print(LC + "  2  Quick lookup links only")
    print()
    c = input(LC + "  Choice > ").strip()
    number = input(LC + "  Phone number (with + country code, e.g. +33612345678) > ").strip()
    if not number: pause(); return

    spinner("Analysing number", 1.0, LC)
    info = None; matched = ""
    for prefix in sorted(PHONE_DB.keys(), key=lambda x: -len(x)):
        if number.startswith(prefix):
            info = PHONE_DB[prefix]; matched = prefix; break

    digits  = re.sub(r"\D", "", number)
    no_plus = number.lstrip("+")
    e  = qenc(number); d = qenc(digits)

    section("PHONE NUMBER ANALYSIS", LC)
    row("Full number",   number,      LC, LW)
    row("Digits only",  digits,      LC, LW)
    row("Digit count",  len(digits), LC, LW)
    row("Country code", matched or "Unknown", LC, LW)
    if info:
        row("Country",  info["country"], LC, LG)
        row("Region",   info["region"],  LC, LG)
        row("Timezone", info["tz"],      LC, LG)
        row("Format",   info["fmt"],     LC, LY)
    else:
        row("Country",  "Not in database", LC, LR)

    if matched == "+33":
        section("FRANCE DETAILS", LC)
        local = number[3:]
        if local.startswith("0"): local = local[1:]
        p2 = "0" + local[0] if local else ""
        fr_type = FR_LINES.get(p2, "Unknown")
        row("Local format", "0" + local, LC, LW)
        row("Line type",    fr_type,     LC, LG)
        is_mob = p2 in ["06","07"]
        row("Mobile", "Yes" if is_mob else "No", LC, LG if is_mob else LY)

    section("VALIDITY CHECK", LC)
    exp = EXPECTED_LEN.get(matched)
    if exp:
        valid = len(digits) == exp
        row("Expected digits", exp, LC, LW)
        row("Likely valid", "Yes" if valid else "No — check length", LC,
            LG if valid else LR)

    if c == "2":
        section("QUICK LOOKUP LINKS", LC)
        for name, lnk in [
            ("Google",     f"https://www.google.com/search?q={e}"),
            ("TrueCaller", f"https://www.truecaller.com/search/fr/{d}"),
            ("NumLookup",  f"https://www.numlookup.com/?number={e}"),
            ("Sync.me",    f"https://sync.me/search/?number={e}"),
            ("ZSearcher",  f"https://zsearcher.fr/search?q={d}"),
        ]: link(name, lnk, LC)
        pause(); return

    section("REVERSE LOOKUP", LC)
    for name, lnk in [
        ("TrueCaller",       f"https://www.truecaller.com/search/fr/{d}"),
        ("NumLookup",        f"https://www.numlookup.com/?number={e}"),
        ("Sync.me",          f"https://sync.me/search/?number={e}"),
        ("Spokeo",           f"https://www.spokeo.com/phone/{d}"),
        ("WhitePages",       f"https://www.whitepages.com/phone/{d}"),
        ("TruePeopleSearch", f"https://www.truepeoplesearch.com/resultsphonesearch?phoneno={d}"),
        ("FastPeopleSearch", f"https://www.fastpeoplesearch.com/phone/{d}"),
        ("PhoneInfoga",      f"https://www.phoneinfoga.crvx.fr/"),
    ]: link(name, lnk, LC)

    section("SOCIAL MEDIA SEARCH", LC)
    for name, lnk in [
        ("Google",          f"https://www.google.com/search?q=%22{e}%22"),
        ("Facebook",        f"https://www.facebook.com/search/top/?q={e}"),
        ("Twitter/X",       f"https://twitter.com/search?q=%22{e}%22&f=live"),
        ("LinkedIn",        f"https://www.linkedin.com/search/results/people/?keywords={e}"),
        ("WhatsApp check",  f"https://wa.me/{digits}"),
        ("Telegram (Google)",f"https://www.google.com/search?q=site:t.me+%22{e}%22"),
    ]: link(name, lnk, LM)

    section("BREACH / LEAK DBs", LC)
    for name, lnk in [
        ("ZSearcher.fr",  f"https://zsearcher.fr/search?q={d}"),
        ("OathNet.org",   f"https://oathnet.org/search?q={e}"),
        ("DeHashed",      f"https://dehashed.com/search?query={e}"),
        ("IntelX",        f"https://intelx.io/?s={e}"),
        ("GitHub code",   f"https://github.com/search?q={e}&type=code"),
        ("Pastebin",      f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
    ]: link(name, lnk, LR)
    pause()

# ──────────────────────────────────────────────
#  PHONE SOCIAL SCANNER
# ──────────────────────────────────────────────

def phone_social_scanner():
    show_logo("phone")
    number = input(LC + "  Phone number (with + country code) > ").strip()
    if not number: pause(); return
    digits  = re.sub(r"\D", "", number)
    no_plus = number.lstrip("+")
    e = qenc(number); d = qenc(digits)

    section("PLATFORM SEARCH LINKS", LC)
    platforms = [
        ("WhatsApp",           f"https://wa.me/{digits}",                                       LG),
        ("Telegram",           f"https://t.me/{no_plus}",                                       LC),
        ("Signal (Google)",    f"https://www.google.com/search?q=signal+%22{e}%22",             LW),
        ("Facebook",           f"https://www.facebook.com/search/top/?q={e}",                  LC),
        ("Twitter/X",          f"https://twitter.com/search?q=%22{e}%22&f=live",               LC),
        ("Instagram (Google)", f"https://www.google.com/search?q=site:instagram.com+%22{e}%22",LW),
        ("TikTok (Google)",    f"https://www.google.com/search?q=site:tiktok.com+%22{e}%22",   LW),
        ("LinkedIn",           f"https://www.linkedin.com/search/results/people/?keywords={e}",LC),
        ("TrueCaller",         f"https://www.truecaller.com/search/fr/{d}",                    LY),
        ("Sync.me",            f"https://sync.me/search/?number={e}",                          LY),
        ("NumLookup",          f"https://www.numlookup.com/?number={e}",                       LY),
        ("Spokeo",             f"https://www.spokeo.com/phone/{d}",                            LY),
        ("ZSearcher.fr",       f"https://zsearcher.fr/search?q={d}",                           LR),
        ("OathNet.org",        f"https://oathnet.org/search?q={e}",                            LR),
        ("DeHashed",           f"https://dehashed.com/search?query={e}",                       LR),
        ("IntelX",             f"https://intelx.io/?s={e}",                                    LR),
        ("Google (number)",    f"https://www.google.com/search?q=%22{e}%22",                   LW),
        ("Pastebin (Google)",  f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22", LW),
    ]
    for name, url, col in platforms:
        print(col + f"  {name:<28}" + LW + f" {url}")
    pause()

# ──────────────────────────────────────────────
#  EMAIL OSINT
# ──────────────────────────────────────────────

def mail_osint():
    show_logo("mail")
    print(LM + "  1  Full email OSINT analysis")
    print(LM + "  2  Email format guesser")
    print(LM + "  3  Email header analyser")
    print(LM + "  4  Disposable / temp mail checker")
    print()
    c = input(LM + "  Choice > ").strip()

    if c == "1":
        email = input(LM + "  Email > ").strip()
        if "@" not in email: print(LR+"  Invalid."); pause(); return
        user, domain = email.split("@", 1)
        spinner("Analysing email", 1.0, LM)
        md5   = hashlib.md5(email.lower().encode()).hexdigest()
        sha1  = hashlib.sha1(email.lower().encode()).hexdigest()
        sha256= hashlib.sha256(email.lower().encode()).hexdigest()
        section("EMAIL ANALYSIS", LM)
        row("Email",   email,  LM, LW)
        row("Username",user,   LM, LW)
        row("Domain",  domain, LM, LW)
        row("MD5",     md5,    LM, LW)
        row("SHA1",    sha1,   LM, LW)
        row("SHA256",  sha256, LM, LW)
        row("Gravatar",f"https://www.gravatar.com/avatar/{md5}", LM, LC)
        section("DOMAIN DNS INFO", LM)
        try:
            ip = socket.gethostbyname(domain)
            row("Domain IP", ip, LM, LW)
            for rtype in ["MX","TXT","NS"]:
                try:
                    r = requests.get(f"https://dns.google/resolve?name={domain}&type={rtype}",timeout=6).json()
                    ans = r.get("Answer",[])
                    if ans: row(f"{rtype} record", ans[0].get("data","N/A")[:60], LM, LW)
                except: pass
        except Exception as e:
            row("DNS", f"Failed: {e}", LM, LR)
        section("BREACH SEARCH LINKS", LM)
        e = qenc(email)
        for name, lnk in [
            ("ZSearcher.fr",   f"https://zsearcher.fr/search?q={e}"),
            ("OathNet.org",    f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned", f"https://haveibeenpwned.com/account/{e}"),
            ("DeHashed",       f"https://dehashed.com/search?query={e}"),
            ("IntelX",         f"https://intelx.io/?s={e}"),
            ("EmailRep.io",    f"https://emailrep.io/{e}"),
            ("Grep.app",       f"https://grep.app/search?q={e}"),
            ("Pastebin",       f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
        ]: link(name, lnk, LM)

    elif c == "2":
        first  = input(LM + "  First name > ").strip().lower()
        last   = input(LM + "  Last name  > ").strip().lower()
        domain = input(LM + "  Domain     > ").strip().lower()
        fi = first[0] if first else "x"
        li = last[0]  if last  else "x"
        section("POSSIBLE EMAIL FORMATS", LM)
        fmts = [
            f"{first}@{domain}", f"{last}@{domain}",
            f"{first}.{last}@{domain}", f"{last}.{first}@{domain}",
            f"{fi}{last}@{domain}", f"{first}{li}@{domain}",
            f"{fi}.{last}@{domain}", f"{first}_{last}@{domain}",
            f"{first}{last}@{domain}", f"{last}{first}@{domain}",
        ]
        for fmt in fmts:
            md5 = hashlib.md5(fmt.encode()).hexdigest()
            print(LM + f"  {fmt:<40}" + LW + f"  https://gravatar.com/avatar/{md5}")

    elif c == "3":
        print(LM + "  Paste raw email header (end with empty line):")
        lines = []
        while True:
            l = input()
            if not l: break
            lines.append(l)
        header = "\n".join(lines)
        section("HEADER ANALYSIS", LM)
        patterns = {
            "From": r"From:(.+)", "To": r"To:(.+)", "Subject": r"Subject:(.+)",
            "Date": r"Date:(.+)", "Return-Path": r"Return-Path:(.+)",
            "Reply-To": r"Reply-To:(.+)", "X-Mailer": r"X-Mailer:(.+)",
            "X-Originating-IP": r"X-Originating-IP:(.+)",
            "DKIM-Signature": r"DKIM-Signature:(.+)",
        }
        for label, pat in patterns.items():
            m = re.search(pat, header, re.IGNORECASE)
            if m: row(label, m.group(1).strip()[:70], LM, LW)
        ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", header)
        if ips:
            section("IPs FOUND IN HEADER", LM)
            for ip in list(set(ips)):
                print(LM + f"  {ip:<20}" + LW +
                      f" https://www.virustotal.com/gui/ip-address/{ip}")

    elif c == "4":
        email = input(LM + "  Email > ").strip()
        if "@" not in email: print(LR+"  Invalid."); pause(); return
        domain = email.split("@")[1].lower()
        spinner("Checking domain", 0.8, LM)
        disposable_domains = [
            "mailinator.com","guerrillamail.com","10minutemail.com","temp-mail.org",
            "throwam.com","yopmail.com","sharklasers.com","trashmail.com","maildrop.cc",
            "tempmail.com","fakeinbox.com","mailnesia.com","mailsac.com","33mail.com",
        ]
        is_disp = domain in disposable_domains
        section("DISPOSABLE MAIL CHECK", LM)
        row("Domain",    domain,     LM, LW)
        row("Disposable","Yes - likely temp mail" if is_disp else "Not in local list", LM,
            LR if is_disp else LG)
    pause()

# ──────────────────────────────────────────────
#  EMAIL ACCOUNT CHECKER
# ──────────────────────────────────────────────

def email_account_checker():
    show_logo("mail")
    print(LM + "  Checks platforms for an account via password-reset endpoints.\n")
    email = input(LM + "  Email address > ").strip()
    if "@" not in email: print(LR + "  Invalid email."); pause(); return
    sites = {
        "Facebook":  "https://www.facebook.com/recover/initiate",
        "Twitter":   "https://twitter.com/account/begin_password_reset",
        "Instagram": "https://www.instagram.com/accounts/password/reset/",
        "Snapchat":  "https://accounts.snapchat.com/accounts/password/reset",
        "Pinterest": "https://www.pinterest.com/reset/",
        "TikTok":    "https://www.tiktok.com/login/forgot-password",
        "Reddit":    "https://www.reddit.com/password",
        "GitHub":    "https://github.com/password_reset",
        "LinkedIn":  "https://www.linkedin.com/uas/request-password-reset",
        "Discord":   "https://discord.com/api/v9/auth/forgot",
        "Spotify":   "https://accounts.spotify.com/en/password-reset",
        "Netflix":   "https://www.netflix.com/password",
        "Amazon":    "https://www.amazon.com/ap/forgotpassword",
        "Microsoft": "https://account.live.com/password/reset",
        "Dropbox":   "https://www.dropbox.com/forgot",
        "Twitch":    "https://www.twitch.tv/user/password_reset",
        "Steam":     "https://store.steampowered.com/login/forgotpassword",
    }
    bar("  Scanning platforms", 30, 0.012, LM, M)
    print(LM + f"\n  Checking {len(sites)} platforms for '{email}'...\n")
    found = []
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for site, reset_url in sites.items():
        try:
            resp = requests.post(reset_url, data={"email": email},
                                 timeout=5, headers=hdrs, allow_redirects=True)
            text = resp.text.lower()
            keywords = ["sent","email","recovery","reset","check your email","verify","we've sent"]
            if any(k in text for k in keywords):
                print(LG + f"  [+]  {site:<20}" + LW + " Account likely exists")
                found.append(site)
            else:
                print(DIM + LW + f"  [ ]  {site}")
        except Exception:
            print(DIM + LW + f"  [?]  {site}")
    section(f"RESULTS - {len(found)} ACCOUNT(S) FOUND", LM)
    if found:
        for s in found: print(LG + f"  [+]  {s}")
    else:
        print(LM + "  No accounts found via password-reset method.")
    pause()

# ──────────────────────────────────────────────
#  BREACH ENGINE
# ──────────────────────────────────────────────

def xposedornot():
    """XposedOrNot API — gratuite, sans clé, résultats directs."""
    show_logo("breach")
    XON_BASE = "https://api.xposedornot.com/v1"

    print(LR + "  XposedOrNot API  —  Gratuite  —  Sans clé  —  Résultats directs\n")
    print(LR + "  1  Check email (breaches)\n"
               "  2  Breach analytics (stats détaillées)\n"
               "  3  Check pastes (email dans des pastes)\n"
               "  4  Check tout (breach + pastes)\n"
               "  5  Liste de toutes les breaches connues\n"
               "  6  Infos sur une breach spécifique\n"
               "  7  Check password (k-anonymity)\n")
    c = input(LC + "  Choice > ").strip()

    if c == "1":
        email = input(LC + "  Email > ").strip()
        if "@" not in email: print(LR+"  Email invalide."); pause(); return
        spinner(f"Interrogation XposedOrNot pour {email}", 1.2, LR)
        try:
            r = requests.get(f"{XON_BASE}/check-email/{qenc(email)}",
                             timeout=10, headers={"User-Agent": "osint-camzzz-v6"})
            section("XPOSEDORNOT — EMAIL CHECK", LR)
            row("Email",   email,          LR, LW)
            row("Statut HTTP", str(r.status_code), LR, LW)
            if r.status_code == 200:
                data = r.json()
                breaches = data.get("breaches", [])
                if breaches:
                    flat = [b[0] if isinstance(b, list) else str(b) for b in breaches]
                    section(f"TROUVE DANS {len(flat)} BREACH(ES)", LR)
                    for b in flat:
                        print(LR + f"  [!]  {b}")
                else:
                    print(LG + "  [OK]  Aucune breach trouvee.")
            elif r.status_code == 404:
                print(LG + "  [OK]  Email non trouvé dans les breaches connues.")
            elif r.status_code == 429:
                print(LY + "  [!!]  Rate limit atteint (100 req/jour par IP). Réessaie demain.")
            else:
                print(LY + f"  Réponse inattendue: {r.status_code}  {r.text[:100]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    elif c == "2":
        email = input(LC + "  Email > ").strip()
        if "@" not in email: print(LR+"  Email invalide."); pause(); return
        spinner(f"Récupération des analytics pour {email}", 1.5, LR)
        try:
            r = requests.get(f"{XON_BASE}/breach-analytics?email={qenc(email)}",
                             timeout=12, headers={"User-Agent": "osint-camzzz-v6"})
            section("XPOSEDORNOT — BREACH ANALYTICS", LR)
            row("Email", email, LR, LW)
            if r.status_code == 200:
                data = r.json()

                # Infos générales
                xposed = data.get("xposed_data", {})
                metrics = data.get("metrics", {})
                breaches_list = data.get("BreachesSummary", {})

                if metrics:
                    section("STATISTIQUES", LR)
                    row("Breaches trouvées",  metrics.get("breaches_count", "N/A"), LR, LW)
                    row("Pastes trouvés",     metrics.get("pastes_count",   "N/A"), LR, LW)
                    row("Mots de passe expo.",metrics.get("passwords_count","N/A"), LR, LW)

                if xposed:
                    section("TYPES DE DONNÉES EXPOSÉES", LR)
                    for category, items in xposed.items():
                        if items:
                            label = category.replace("_", " ").title()
                            val   = ", ".join(items) if isinstance(items, list) else str(items)
                            print(LR + f"  {label:<28}" + LW + f" {val[:70]}")

                if breaches_list:
                    section("BREACHES DÉTAILLÉES", LR)
                    for bname, binfo in breaches_list.items():
                        if isinstance(binfo, dict):
                            date   = binfo.get("date", "?")
                            pwd    = binfo.get("password", False)
                            fields = binfo.get("xposed_data", [])
                            pwd_flag = LR+"[PWD]" if pwd else LG+"[   ]"
                            print(pwd_flag + LW + f"  {bname:<25}" +
                                  LC + f" {date}  " + LY + f"{str(fields)[:50]}")
                        else:
                            print(LR + f"  [!]  {bname}: {str(binfo)[:60]}")

            elif r.status_code == 404:
                print(LG + "  [OK]  Aucune breach trouvée pour cet email.")
            elif r.status_code == 429:
                print(LY + "  [!!]  Rate limit (100 req/jour). Réessaie demain.")
            else:
                print(LY + f"  HTTP {r.status_code}: {r.text[:150]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    elif c == "3":
        email = input(LC + "  Email > ").strip()
        if "@" not in email: print(LR+"  Email invalide."); pause(); return
        spinner(f"Recherche pastes pour {email}", 1.0, LR)
        try:
            r = requests.get(f"{XON_BASE}/pastes?email={qenc(email)}",
                             timeout=10, headers={"User-Agent": "osint-camzzz-v6"})
            section("XPOSEDORNOT — PASTES CHECK", LR)
            row("Email", email, LR, LW)
            if r.status_code == 200:
                data = r.json()
                pastes = data.get("pastes", [])
                if pastes:
                    section(f"TROUVE DANS {len(pastes)} PASTE(S)", LR)
                    for p in pastes:
                        if isinstance(p, dict):
                            src  = p.get("source", "?")
                            pid  = p.get("id", "?")
                            date = p.get("date", "?")
                            print(LR + f"  [!]  {src:<15}" + LW + f" {pid}  " + LY + f"{date}")
                        else:
                            print(LR + f"  [!]  {p}")
                else:
                    print(LG + "  [OK]  Aucun paste trouvé.")
            elif r.status_code == 404:
                print(LG + "  [OK]  Email non trouvé dans des pastes connus.")
            elif r.status_code == 429:
                print(LY + "  [!!]  Rate limit (100 req/jour). Réessaie demain.")
            else:
                print(LY + f"  HTTP {r.status_code}: {r.text[:150]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    elif c == "4":
        email = input(LC + "  Email > ").strip()
        if "@" not in email: print(LR+"  Email invalide."); pause(); return
        spinner(f"Scan complet XposedOrNot pour {email}", 1.8, LR)

        section("XPOSEDORNOT — SCAN COMPLET", LR)
        row("Email", email, LR, LW)

        # -- check-email
        try:
            r1 = requests.get(f"{XON_BASE}/check-email/{qenc(email)}",
                              timeout=10, headers={"User-Agent": "osint-camzzz-v6"})
            if r1.status_code == 200:
                data1 = r1.json()
                breaches = data1.get("breaches", [])
                flat = [b[0] if isinstance(b, list) else str(b) for b in breaches]
                print(LR + f"\n  Breaches: {len(flat)}")
                for b in flat: print(LR + f"    [!]  {b}")
            elif r1.status_code == 404:
                print(LG + "\n  Breaches: 0 (email propre)")
            else:
                print(LY + f"\n  Breaches: HTTP {r1.status_code}")
        except Exception as ex:
            print(LR + f"\n  Breaches: Erreur — {ex}")

        time.sleep(0.6)  # respecter le rate limit (2 req/s)

        # -- pastes
        try:
            r2 = requests.get(f"{XON_BASE}/pastes?email={qenc(email)}",
                              timeout=10, headers={"User-Agent": "osint-camzzz-v6"})
            if r2.status_code == 200:
                data2 = r2.json()
                pastes = data2.get("pastes", [])
                print(LR + f"\n  Pastes: {len(pastes)}")
                for p in pastes[:5]:
                    src = p.get("source","?") if isinstance(p,dict) else str(p)
                    print(LR + f"    [!]  {src}")
            elif r2.status_code == 404:
                print(LG + "\n  Pastes: 0 (aucun paste)")
            elif r2.status_code == 429:
                print(LY + "\n  Pastes: Rate limit atteint")
            else:
                print(LY + f"\n  Pastes: HTTP {r2.status_code}")
        except Exception as ex:
            print(LR + f"\n  Pastes: Erreur — {ex}")

    elif c == "5":
        spinner("Récupération de la liste des breaches", 1.5, LR)
        try:
            r = requests.get(f"{XON_BASE}/breaches",
                             timeout=15, headers={"User-Agent": "osint-camzzz-v6"})
            section("TOUTES LES BREACHES CONNUES", LR)
            if r.status_code == 200:
                data = r.json()
                breaches = data.get("breaches", data) if isinstance(data, dict) else data
                if isinstance(breaches, list):
                    print(LR + f"  {len(breaches)} breaches indexées\n")
                    for b in breaches[:50]:
                        if isinstance(b, dict):
                            name  = b.get("breachID", b.get("name", "?"))
                            date  = b.get("addedDate", b.get("date", "?"))
                            count = b.get("pwnCount", "?")
                            print(LR + f"  {name:<30}" + LW + f" {date}  " +
                                  LY + f"{count:,}" if isinstance(count,int) else
                                  LR + f"  {name:<30}" + LW + f" {date}  " + LY + str(count))
                        else:
                            print(LR + f"  {b}")
                    if len(breaches) > 50:
                        print(LY + f"\n  ... et {len(breaches)-50} de plus.")
                else:
                    print(LW + str(data)[:500])
            else:
                print(LY + f"  HTTP {r.status_code}: {r.text[:150]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    elif c == "6":
        breach_name = input(LC + "  Nom de la breach (ex: Adobe) > ").strip()
        spinner(f"Récupération infos sur {breach_name}", 1.0, LR)
        try:
            r = requests.get(f"{XON_BASE}/breaches/{qenc(breach_name)}",
                             timeout=10, headers={"User-Agent": "osint-camzzz-v6"})
            section(f"BREACH INFO — {breach_name}", LR)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict):
                    for k, v in data.items():
                        if v is not None:
                            row(str(k), str(v)[:70], LR, LW)
                else:
                    print(LW + str(data)[:300])
            elif r.status_code == 404:
                print(LY + f"  Breach '{breach_name}' non trouvée dans la base.")
                print(LY +  "  Conseil: utilise l'option 5 pour voir les noms exacts.")
            else:
                print(LY + f"  HTTP {r.status_code}: {r.text[:150]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    elif c == "7":
        pwd = input(LC + "  Mot de passe à vérifier > ").strip()
        if not pwd: pause(); return
        sha1   = hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix = sha1[:5]; suffix = sha1[5:]
        spinner("Vérification k-anonymity (HIBP PwnedPasswords)", 1.0, LR)
        try:
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=8)
            found = False
            for line in r.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    print(LR + f"\n  [!!!]  Trouvé {count} fois dans des leaks!")
                    print(LR +  "         Change ce mot de passe immédiatement.")
                    found = True; break
            if not found: print(LG + "\n  [OK]  Non trouvé dans HIBP.")
            print(DIM + "\n  Seuls 5 chars du hash SHA1 sont envoyés — MDP jamais transmis.")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")

    print()
    print(LC + "  XposedOrNot : https://xposedornot.com  |  API : https://api.xposedornot.com")
    print(LC + "  Limite : 2 req/s, 100 req/jour par IP  —  Aucune cle requise")
    pause()


def breach_engine():
    show_logo("breach")
    print(LR + "  1  ZSearcher.fr\n  2  OathNet.org\n  3  HaveIBeenPwned (email)\n"
               "  4  ALL breach links\n  5  Password HIBP check\n"
               "  6  Domain breach search\n  7  Username breach scan\n"
               "  8  XposedOrNot API  [NOUVEAU — sans cle, resultats directs]\n")
    c = input(LC + "  Choice > ").strip()

    if c == "1":
        q = input(LC + "  Search > ").strip(); e = qenc(q)
        section("ZSEARCHER.FR", LR)
        for name, lnk in [
            ("ZSearcher main",   "https://zsearcher.fr/"),
            ("ZSearcher search", f"https://zsearcher.fr/search?q={e}"),
            ("ZSearcher email",  f"https://zsearcher.fr/email?q={e}"),
        ]: link(name, lnk, LC)
    elif c == "2":
        q = input(LC + "  Search > ").strip(); e = qenc(q)
        section("OATHNET.ORG", LR)
        for name, lnk in [
            ("OathNet main",   "https://oathnet.org/"),
            ("OathNet search", f"https://oathnet.org/search?q={e}"),
        ]: link(name, lnk, LC)
    elif c == "3":
        email = input(LC + "  Email > ").strip(); e = qenc(email)
        section("HAVEIBEENPWNED", LR)
        print(LW + f"  Direct link: https://haveibeenpwned.com/account/{e}\n")
        try:
            r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{e}",
                             headers={"User-Agent":"osint-camzzz"}, timeout=8)
            if r.status_code == 200:
                breaches = r.json()
                section(f"FOUND IN {len(breaches)} BREACH(ES)", LR)
                for b in breaches:
                    print(LR + f"  [!]  {b.get('Name','?'):<25}" +
                          LW + f" {b.get('BreachDate','?')}  " +
                          Y  + f"{str(b.get('DataClasses',[]))[:55]}")
            elif r.status_code == 404:
                print(LG + "  [OK]  Not found in known public breaches.")
            elif r.status_code == 401:
                print(LY + "  API key needed — https://haveibeenpwned.com/API/Key")
            else:
                print(LY + f"  HTTP {r.status_code}")
        except Exception as e:
            print(LR + f"  Failed: {e}")
    elif c == "4":
        q = input(LC + "  Query > ").strip(); e = qenc(q)
        section("ALL BREACH DATABASE LINKS", LR)
        for name, lnk in [
            ("ZSearcher.fr",    f"https://zsearcher.fr/search?q={e}"),
            ("OathNet.org",     f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned",  f"https://haveibeenpwned.com/account/{e}"),
            ("DeHashed",        f"https://dehashed.com/search?query={e}"),
            ("IntelX",          f"https://intelx.io/?s={e}"),
            ("LeakCheck",       "https://leakcheck.io/"),
            ("BreachDirectory", "https://breachdirectory.org/"),
            ("Snusbase",        "https://snusbase.com/"),
            ("Grep.app",        f"https://grep.app/search?q={e}"),
            ("Google Pastebin", f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
            ("Spycloud",        "https://spycloud.com/check-your-exposure/"),
            ("CyberNews",       "https://cybernews.com/personal-data-leak-check/"),
            ("XposedOrNot",     f"https://xposedornot.com/"),
        ]: link(name, lnk, LR)
    elif c == "5":
        pwd = input(LC + "  Password to check > ").strip()
        if not pwd: pause(); return
        sha1 = hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        spinner("Querying HIBP (k-anonymity)", 1.0, LM)
        try:
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=8)
            found = False
            for line in r.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    print(LR + f"\n  [!!!]  Found {count} times in known breaches!")
                    found = True; break
            if not found: print(LG + "\n  [OK]  Not found in HIBP database.")
            print(DIM + "\n  Only 5 chars of SHA1 sent — password never leaves your device.")
        except Exception as e:
            print(LR + f"  Failed: {e}")
    elif c == "6":
        domain = input(LC + "  Domain > ").strip(); e = qenc(domain)
        section(f"DOMAIN BREACH — {domain}", LR)
        for name, lnk in [
            ("ZSearcher",      f"https://zsearcher.fr/search?q={e}"),
            ("OathNet",        f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned", f"https://haveibeenpwned.com/DomainSearch/{domain}"),
            ("DeHashed",       f"https://dehashed.com/search?query={e}"),
            ("Grep.app",       f"https://grep.app/search?q={e}"),
            ("URLScan",        f"https://urlscan.io/search/#{e}"),
            ("VirusTotal",     f"https://www.virustotal.com/gui/domain/{domain}"),
        ]: link(name, lnk, LR)
    elif c == "7":
        username = input(LC + "  Username > ").strip(); e = qenc(username)
        section(f"USERNAME BREACH — {username}", LR)
        for name, lnk in [
            ("ZSearcher",      f"https://zsearcher.fr/search?q={e}"),
            ("OathNet",        f"https://oathnet.org/search?q={e}"),
            ("DeHashed",       f"https://dehashed.com/search?query={e}"),
            ("IntelX",         f"https://intelx.io/?s={e}"),
            ("Grep.app",       f"https://grep.app/search?q={e}"),
        ]: link(name, lnk, LR)
    elif c == "8":
        xposedornot()
        return
    pause()

# ──────────────────────────────────────────────
#  USERNAME TRACKER (55+ sites)
# ──────────────────────────────────────────────

SITES = [
    ("GitHub","https://github.com/{}"),("Instagram","https://www.instagram.com/{}"),
    ("Twitter/X","https://twitter.com/{}"),("TikTok","https://www.tiktok.com/@{}"),
    ("Reddit","https://www.reddit.com/user/{}"),("Pinterest","https://www.pinterest.com/{}"),
    ("Twitch","https://www.twitch.tv/{}"),("YouTube","https://www.youtube.com/@{}"),
    ("SoundCloud","https://soundcloud.com/{}"),("Spotify","https://open.spotify.com/user/{}"),
    ("Medium","https://medium.com/@{}"),("Dev.to","https://dev.to/{}"),
    ("Keybase","https://keybase.io/{}"),("GitLab","https://gitlab.com/{}"),
    ("BitBucket","https://bitbucket.org/{}"),
    ("HackerNews","https://news.ycombinator.com/user?id={}"),
    ("ProductHunt","https://www.producthunt.com/@{}"),("Behance","https://www.behance.net/{}"),
    ("Dribbble","https://dribbble.com/{}"),("Fiverr","https://www.fiverr.com/{}"),
    ("Replit","https://replit.com/@{}"),("Patreon","https://www.patreon.com/{}"),
    ("Linktree","https://linktr.ee/{}"),("About.me","https://about.me/{}"),
    ("Gravatar","https://en.gravatar.com/{}"),("Flickr","https://www.flickr.com/people/{}"),
    ("Tumblr","https://{}.tumblr.com"),("WordPress","https://{}.wordpress.com"),
    ("Steam","https://steamcommunity.com/id/{}"),
    ("Roblox","https://www.roblox.com/user.aspx?username={}"),
    ("Ko-fi","https://ko-fi.com/{}"),("Itch.io","https://{}.itch.io"),
    ("ArtStation","https://www.artstation.com/{}"),
    ("Codecademy","https://www.codecademy.com/profiles/{}"),
    ("HackerRank","https://www.hackerrank.com/{}"),("LeetCode","https://leetcode.com/{}"),
    ("Kaggle","https://www.kaggle.com/{}"),("DockerHub","https://hub.docker.com/u/{}"),
    ("npm","https://www.npmjs.com/~{}"),("PyPI","https://pypi.org/user/{}"),
    ("Wattpad","https://www.wattpad.com/user/{}"),("Goodreads","https://www.goodreads.com/{}"),
    ("Disqus","https://disqus.com/by/{}"),("Vimeo","https://vimeo.com/{}"),
    ("Trello","https://trello.com/{}"),("Venmo","https://venmo.com/{}"),
    ("Poshmark","https://poshmark.com/closet/{}"),
    ("Snapchat","https://www.snapchat.com/add/{}"),
    ("Telegram","https://t.me/{}"),
    ("Xbox Live",   "https://account.xbox.com/en-US/Profile?GamerTag={}"),
    ("PlayStation", "https://psnprofiles.com/{}"),
    ("DeviantArt",  "https://www.deviantart.com/{}"),
    ("Last.fm",     "https://www.last.fm/user/{}"),
    ("HackerOne",   "https://hackerone.com/{}"),
    ("Blogger",     "https://{}.blogspot.com"),
]

def username_tracker():
    show_logo("user")
    username = input(LM + "  Username > ").strip()
    if not username: pause(); return
    bar("  Preparing scan", 25, 0.012, LM, M)
    print(LM + f"\n  Scanning {len(SITES)} platforms for '{username}'...\n")
    found = []
    def chk(item):
        name, tpl = item
        url = tpl.format(username)
        try:
            r = requests.get(url, timeout=8, allow_redirects=True,
                             headers={"User-Agent":"Mozilla/5.0"})
            return ("FOUND" if r.status_code==200 else ".", name, url)
        except:
            return ("ERR", name, url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(chk, SITES))
    for status, name, url in results:
        if status == "FOUND":
            print(LG + f"  [+]  {name:<22}" + LW + f" {url}"); found.append(url)
        elif status == "ERR":
            print(DIM+C + f"  [?]  {name}")
        else:
            print(DIM+W + f"  [ ]  {name}")
    section(f"RESULTS  -  {len(found)} FOUND  /  {len(SITES)} CHECKED", LM)
    pause()

# ──────────────────────────────────────────────
#  DNS LOOKUP
# ──────────────────────────────────────────────

def dns_lookup():
    show_logo("geo")
    domain = input(LY + "  Domain > ").strip()
    if not domain: pause(); return
    spinner("Resolving DNS records", 0.8, LY)
    section("A RECORD", LY)
    try:
        ip = socket.gethostbyname(domain)
        row("A", ip, LY, LW)
        try: rev = socket.gethostbyaddr(ip); row("Reverse DNS", rev[0], LY, LW)
        except: pass
    except Exception as e: row("A", f"FAILED: {e}", LY, LR)
    for rtype in ["MX","NS","TXT","AAAA","CAA","SOA","CNAME"]:
        try:
            r = requests.get(f"https://dns.google/resolve?name={domain}&type={rtype}",timeout=8).json()
            answers = r.get("Answer",[])
            if answers:
                section(f"{rtype} RECORDS", LY)
                for a in answers: print(LY + f"  {a.get('data','')[:90]}")
        except: pass
    pause()

# ──────────────────────────────────────────────
#  PORT SCANNER
# ──────────────────────────────────────────────

COMMON_PORTS=[21,22,23,25,53,80,110,111,135,139,143,443,445,465,
              587,631,993,995,1433,1521,2222,3306,3389,5432,5900,
              6379,6443,8080,8443,8888,9200,27017,27018,28017]

SERVICE_MAP = {
    21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
    143:"IMAP",443:"HTTPS",445:"SMB",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",
    5900:"VNC",6379:"Redis",8080:"HTTP-Alt",8443:"HTTPS-Alt",9200:"Elasticsearch",
    27017:"MongoDB",22:"SSH",587:"SMTP-SSL",993:"IMAPS",995:"POP3S"
}

def port_scanner():
    show_logo("port")
    host = input(LG + "  Host/IP > ").strip()
    print(LG + "  (1) Common ports  (2) 1-1024  (3) Custom range")
    choice = input(LG + "  Choice > ").strip()
    if   choice == "1": ports = COMMON_PORTS
    elif choice == "2": ports = range(1, 1025)
    else:
        try:
            s,e = map(int, input(LG+"  Range (e.g. 1-500) > ").split("-"))
            ports = range(s, e+1)
        except: print(LR+"  Invalid."); pause(); return
    spinner(f"Scanning {host}", 1.2, LG)
    found=[]
    def chk(p):
        try:
            s = socket.socket(); s.settimeout(0.5)
            if s.connect_ex((host,p)) == 0:
                svc = SERVICE_MAP.get(p) or "unknown"
                return (p, svc)
            s.close()
        except: pass
        return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as ex:
        results = list(ex.map(chk, ports))
    section("OPEN PORTS", LG)
    for r in sorted([r for r in results if r], key=lambda x: x[0]):
        port, svc = r; found.append(r)
        print(LG + f"  [OPEN]  {port:<8}" + LW + f" {svc}")
    print(LG + f"\n  {len(found)} open port(s) found.")
    pause()

# ──────────────────────────────────────────────
#  GEO IP
# ──────────────────────────────────────────────

def geo_ip():
    show_logo("geo")
    ip = input(LY + "  IP > ").strip()
    if not ip: pause(); return
    spinner("Fetching geolocation", 1.0, LY)
    try:
        d  = requests.get(f"https://ipapi.co/{ip}/json", timeout=10).json()
        d2 = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        section(f"GEO IP — {ip}", LY)
        fields=["country_name","region","city","postal","latitude","longitude",
                "timezone","org","asn","currency","languages","network"]
        for f in fields:
            v = d.get(f) or d2.get(f,"N/A")
            if v and v!="N/A": row(f, v, LY, LW)
        lat=d.get("latitude",""); lon=d.get("longitude","")
        if lat and lon:
            print(); print(LY+f"  Google Maps : https://maps.google.com/?q={lat},{lon}")
    except Exception as e:
        print(LR + f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  WHOIS / REVERSE DNS
# ──────────────────────────────────────────────

def whois_reverse():
    show_logo("geo")
    print(LY+"  1  WHOIS Domain\n  2  Reverse DNS (IP -> hostname)\n")
    c = input(LY+"  Choice > ").strip()
    if c=="1":
        d = input(LY+"  Domain > ").strip()
        spinner("Querying WHOIS", 1.0, LY)
        try:
            r = requests.get(f"https://api.whois.vu/?q={d}", timeout=10).json()
            section("WHOIS DATA", LY)
            for k,v in r.items():
                if v: row(k,v,LY,LW)
        except:
            try: ip=socket.gethostbyname(d); row("IP",ip,LY,LW)
            except Exception as e: print(LR+f"  Failed: {e}")
        section("WHOIS LINKS", LY)
        for name,lnk in [
            ("ICANN",     f"https://lookup.icann.org/en/lookup?name={d}"),
            ("Whois.com", f"https://www.whois.com/whois/{d}"),
            ("DomainTools",f"https://whois.domaintools.com/{d}"),
        ]: link(name,lnk,LC)
    elif c=="2":
        ip=input(LY+"  IP > ").strip()
        spinner("Reverse DNS",0.8,LY)
        try:
            h=socket.gethostbyaddr(ip)
            section("REVERSE DNS",LY); row("IP",ip,LY,LW); row("Hostname",h[0],LY,LG)
        except Exception as e: print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  SSL INSPECTOR
# ──────────────────────────────────────────────

def ssl_inspector():
    show_logo("port")
    host = input(LC+"  Host > ").strip()
    if not host: pause(); return
    spinner("Connecting SSL", 1.0, LC)
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(10); s.connect((host,443)); cert=s.getpeercert()
            proto = s.version(); cipher = s.cipher()
        subj=dict(x[0] for x in cert.get("subject",[]))
        iss=dict(x[0] for x in cert.get("issuer",[]))
        section("SSL CERTIFICATE", LC)
        row("Subject CN",  subj.get("commonName","N/A"), LC, LW)
        row("Org",         subj.get("organizationName","N/A"), LC, LW)
        row("Issuer",      iss.get("organizationName","N/A"), LC, LW)
        row("Valid From",  cert.get("notBefore","N/A"), LC, LG)
        row("Valid Until", cert.get("notAfter","N/A"),  LC, LG)
        row("Protocol",    proto or "N/A", LC, LW)
        row("Cipher",      cipher[0] if cipher else "N/A", LC, LW)
        sans=cert.get("subjectAltName",[])
        if sans:
            section("SUBJECT ALT NAMES", LC)
            for t,v in sans: print(LC+f"  {t:<10}"+LW+f" {v}")
    except Exception as e:
        print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  HTTP HEADER INSPECTOR
# ──────────────────────────────────────────────

def header_inspector():
    show_logo("geo")
    url = input(LC+"  URL > ").strip()
    if not url.startswith("http"): url="https://"+url
    spinner("Fetching headers", 0.8, LC)
    try:
        r=requests.get(url,timeout=10,headers={"User-Agent":"Mozilla/5.0"})
        section("RESPONSE HEADERS", LC)
        for k,v in r.headers.items(): row(k,v,LC,LW)
        section("SECURITY HEADERS AUDIT", LC)
        sec_hdrs=["Strict-Transport-Security","Content-Security-Policy",
                  "X-Frame-Options","X-Content-Type-Options",
                  "Referrer-Policy","Permissions-Policy","X-XSS-Protection"]
        for h in sec_hdrs:
            v=r.headers.get(h)
            flag=LC+"  [OK     ]" if v else LR+"  [MISSING]"
            print(flag+LW+f"  {h}")
    except Exception as e:
        print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  TECH DETECTOR
# ──────────────────────────────────────────────

def tech_detector():
    show_logo("dork")
    url = input(LY+"  URL > ").strip()
    if not url.startswith("http"): url="https://"+url
    spinner("Analysing website", 1.2, LY)
    try:
        r=requests.get(url,timeout=10,headers={"User-Agent":"Mozilla/5.0"})
        body=r.text.lower(); hdrs=str(r.headers).lower()
        checks={
            "WordPress":["wp-content","wp-includes"],"Drupal":["drupal"],
            "Joomla":["joomla"],"Shopify":["shopify"],"Wix":["wix.com"],
            "React":["react","__react"],"Vue.js":["vue.js"],"Angular":["angular"],
            "Next.js":["__next"],"jQuery":["jquery"],"Bootstrap":["bootstrap"],
            "Tailwind":["tailwind"],"PHP":["php",".php"],"Django":["csrfmiddlewaretoken"],
            "Laravel":["laravel_session"],"Ruby on Rails":["rails","csrf-token"],
            "ASP.NET":["asp.net","__viewstate"],"Cloudflare":["cf-ray"],
            "Nginx":["nginx"],"Apache":["apache"],"Google Analytics":["google-analytics","gtag("],
        }
        section("DETECTED TECHNOLOGIES", LY)
        found=[]
        for tech,sigs in checks.items():
            for sig in sigs:
                if sig in body or sig in hdrs:
                    found.append(tech); break
        if found:
            for t in found: print(LY+f"  [+]  {t}")
        else: print(LY+"  Nothing obvious detected.")
        section("SERVER INFO", LY)
        row("Server",      r.headers.get("Server","N/A"),      LY, LW)
        row("X-Powered-By",r.headers.get("X-Powered-By","N/A"),LY, LW)
        row("Status",      str(r.status_code),                 LY, LW)
    except Exception as e:
        print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  GOOGLE DORK GENERATOR
# ──────────────────────────────────────────────

def dork_gen():
    show_logo("dork")
    target = input(LY+"  Domain > ").strip()
    kw     = input(LY+"  Keyword (optional) > ").strip()
    dorks=[
        ("All indexed pages",  f"site:{target}"),
        ("Subdomains",         f"site:*.{target}"),
        ("Login pages",        f"site:{target} inurl:login OR inurl:admin"),
        ("Config / env files", f"site:{target} ext:env OR ext:cfg OR ext:ini"),
        ("Documents",          f"site:{target} ext:pdf OR ext:doc OR ext:xls"),
        ("Open directories",   f"site:{target} intitle:index of"),
        ("SQL errors",         f"site:{target} intext:sql error"),
        ("Email addresses",    f"site:{target} intext:@{target}"),
        ("WordPress admin",    f"site:{target} inurl:wp-admin"),
        ("phpMyAdmin",         f"site:{target} inurl:phpmyadmin"),
        ("AWS S3",             f"site:s3.amazonaws.com \"{target}\""),
        ("GitHub mentions",    f"site:github.com \"{target}\""),
        ("Pastebin mentions",  f"site:pastebin.com \"{target}\""),
        ("LinkedIn employees", f"site:linkedin.com inurl:/in/ \"{target}\""),
        ("Backup files",       f"site:{target} ext:bak OR ext:old OR ext:backup"),
        ("API keys exposed",   f"site:{target} intext:apikey OR intext:api_key"),
        ("Cache",              f"cache:{target}"),
    ]
    if kw: dorks.append(("Keyword", f"site:{target} \"{kw}\""))
    section("GENERATED DORKS", LY)
    for desc, dork in dorks:
        print(LY+f"  {desc:<28}"+LW+f" https://www.google.com/search?q={qenc(dork)}")
    pause()

# ──────────────────────────────────────────────
#  ADVANCED DORK BUILDER
# ──────────────────────────────────────────────

def adv_dork():
    show_logo("dork")
    print(LY+"  Build a custom Google dork.\n")
    site   =input(LY+"  site:     > ").strip()
    inurl  =input(LY+"  inurl:    > ").strip()
    intitle=input(LY+"  intitle:  > ").strip()
    intext =input(LY+"  intext:   > ").strip()
    ext    =input(LY+"  ext:      > ").strip()
    kw     =input(LY+"  keyword   > ").strip()
    parts=[]
    if site:    parts.append(f"site:{site}")
    if inurl:   parts.append(f"inurl:{inurl}")
    if intitle: parts.append(f"intitle:{intitle}")
    if intext:  parts.append(f"intext:{intext}")
    if ext:     parts.append(f"ext:{ext}")
    if kw:      parts.append(f'"{kw}"')
    dork=" ".join(parts)
    section("YOUR DORK", LY)
    print(LY+f"  {dork}")
    print(LW+f"\n  Search: https://www.google.com/search?q={qenc(dork)}")
    pause()

# ──────────────────────────────────────────────
#  OSINT DORK BUILDER (avancé)
# ──────────────────────────────────────────────

def osint_dork_builder():
    show_logo("dork")
    print(LY+"  Advanced OSINT dork builder.\n")
    first    = input(LY+"  First name   > ").strip()
    last     = input(LY+"  Last name    > ").strip()
    username = input(LY+"  Username     > ").strip()
    email    = input(LY+"  Email        > ").strip()
    phone    = input(LY+"  Phone        > ").strip()
    domain   = input(LY+"  Domain/site  > ").strip()
    company  = input(LY+"  Company      > ").strip()
    dorks = []
    E = qenc
    names = []
    if first and last: names.append(f"{first} {last}")
    if first: names.append(first)
    if last:  names.append(last)
    if names:
        for n in names:
            dorks += [
                ("Name basic",      f'"{n}"'),
                ("LinkedIn",        f'site:linkedin.com "{n}"'),
                ("Twitter/X",       f'site:twitter.com "{n}"'),
                ("Facebook",        f'site:facebook.com "{n}"'),
                ("GitHub",          f'site:github.com "{n}"'),
                ("Resume/CV",       f'"{n}" (resume OR cv) filetype:pdf'),
            ]
            if company:
                dorks.append(("Name + company", f'"{n}" "{company}"'))
    if username:
        dorks += [
            ("Username basic",   f'"{username}"'),
            ("Username inurl",   f'inurl:{username}'),
        ]
    if email:
        dorks += [
            ("Email basic",    f'"{email}"'),
            ("Email breach",   f'"{email}" (breach OR leak OR dump)'),
            ("Email pastebin", f'site:pastebin.com "{email}"'),
        ]
    if phone:
        clean = re.sub(r"\D","",phone)
        dorks += [
            ("Phone basic",  f'"{phone}"'),
            ("Phone digits", f'"{clean}"'),
        ]
    if domain:
        dorks += [
            ("Domain all",   f"site:{domain}"),
            ("Domain login", f"site:{domain} inurl:login OR inurl:admin"),
            ("Domain config",f"site:{domain} ext:env OR ext:cfg OR ext:sql"),
            ("Domain crt.sh",f"site:crt.sh \"{domain}\""),
        ]
    dorks = [(k,v) for k,v in dorks if v]
    section(f"GENERATED {len(dorks)} DORKS", LY)
    for desc, dork in dorks:
        print(LY+f"  {desc:<28}"+LW+f" https://www.google.com/search?q={E(dork)}")
    pause()

# ──────────────────────────────────────────────
#  PASSWORD TOOLS
# ──────────────────────────────────────────────

def password_tools():
    show_logo("pass")
    print(LM+"  1  Generate secure password\n  2  Strength test + HIBP\n  3  Bulk generate\n")
    c = input(LM+"  Choice > ").strip()
    if c=="1":
        section("PASSWORD GENERATOR",LM)
        try: length=int(input(LM+"  Length (default 20) > ").strip() or "20")
        except: length=20
        use_u=input(LM+"  Uppercase?  [Y/n] > ").lower()!="n"
        use_l=input(LM+"  Lowercase?  [Y/n] > ").lower()!="n"
        use_d=input(LM+"  Digits?     [Y/n] > ").lower()!="n"
        use_s=input(LM+"  Symbols?    [Y/n] > ").lower()!="n"
        pool=""
        if use_u: pool+=string.ascii_uppercase
        if use_l: pool+=string.ascii_lowercase
        if use_d: pool+=string.digits
        if use_s: pool+="!@#$%^&*()-_=+[]{}|;:,.<>?"
        if not pool: pool=string.ascii_letters+string.digits
        pwd="".join(random.choices(pool,k=length))
        print(); rainbow("  "+pwd); print()
        row("Length",len(pwd),LM,LW)
    elif c=="2":
        pwd=input(LM+"  Password > ").strip()
        if not pwd: pause(); return
        section("STRENGTH ANALYSIS",LM)
        checks=[
            (len(pwd)>=8,"Length >= 8"),(len(pwd)>=12,"Length >= 12"),
            (len(pwd)>=16,"Length >= 16"),
            (any(ch.isupper() for ch in pwd),"Uppercase"),
            (any(ch.islower() for ch in pwd),"Lowercase"),
            (any(ch.isdigit() for ch in pwd),"Digits"),
            (any(ch in "!@#$%^&*()-_=+[]{}|;:,.<>?" for ch in pwd),"Special chars"),
        ]
        score=0
        for passed,label in checks:
            print((LG+"  [OK] " if passed else LR+"  [!!] ")+LW+label)
            if passed: score+=1
        rating=["Very Weak","Weak","Weak","Medium","Medium","Good","Strong","Very Strong"][min(score,7)]
        print(LM+f"\n  Score: {score}/7  "+rating)
        section("HIBP CHECK",LM)
        sha1=hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix,suffix=sha1[:5],sha1[5:]
        spinner("Querying HIBP",0.8,LM)
        try:
            r=requests.get(f"https://api.pwnedpasswords.com/range/{prefix}",timeout=8)
            found=False
            for line in r.text.splitlines():
                h,count=line.split(":")
                if h==suffix:
                    print(LR+f"  [!!!]  Seen {count} times in breaches. Change it!"); found=True; break
            if not found: print(LG+"  [OK]  Not found in HIBP database.")
        except Exception as e: print(LR+f"  Failed: {e}")
    elif c=="3":
        try: n=int(input(LM+"  How many? > ").strip() or "10"); l=int(input(LM+"  Length? > ").strip() or "20")
        except: n,l=10,20
        pool=string.ascii_letters+string.digits+"!@#$%^&*-_=+"
        section(f"{n} GENERATED PASSWORDS",LM)
        for i in range(n):
            pwd="".join(random.choices(pool,k=l))
            rainbow(f"  {i+1:>3}.  {pwd}")
    pause()

# ──────────────────────────────────────────────
#  HASH TOOLS
# ──────────────────────────────────────────────

def hash_tools():
    show_logo("hash")
    print(LM+"  1  Generate hashes from text\n  2  Hash lookup links\n")
    c=input(LM+"  Choice > ").strip()
    if c=="1":
        text=input(LM+"  Text > ").strip()
        section("HASHES",LM)
        for name,fn in [("MD5",hashlib.md5),("SHA1",hashlib.sha1),
                        ("SHA224",hashlib.sha224),("SHA256",hashlib.sha256),
                        ("SHA384",hashlib.sha384),("SHA512",hashlib.sha512)]:
            row(name,fn(text.encode()).hexdigest(),LM,LW)
        row("Base64",base64.b64encode(text.encode()).decode(),LM,LW)
        row("Hex",text.encode().hex(),LM,LW)
    elif c=="2":
        h=input(LM+"  Hash > ").strip()
        section("LOOKUP LINKS",LM)
        for name,lnk in [
            ("MD5Decrypt",  f"https://md5decrypt.net/en/#answer={h}"),
            ("CrackStation","https://crackstation.net/"),
            ("Hashes.com",  f"https://hashes.com/en/decrypt/hash#{h}"),
            ("HashKiller",  "https://hashkiller.io/listmanager"),
        ]: link(name,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  METADATA EXTRACTOR
# ──────────────────────────────────────────────

def metadata_extractor():
    show_logo("ip")
    if not PIL_OK:
        print(LR+"  Pillow not installed.")
        print(LY+"  Install with:  pip install Pillow")
        pause(); return
    path=input(LG+"  Image path > ").strip().strip('"').strip("'")
    if not path: pause(); return
    spinner("Reading EXIF",0.6,LG)
    try:
        img=Image.open(path)
        section("IMAGE INFO",LG)
        row("Format",img.format,LG,LW); row("Mode",img.mode,LG,LW)
        row("Size",f"{img.size[0]} x {img.size[1]} px",LG,LW)
        # EXIF moderne (getexif)
        try:
            from PIL.ExifTags import TAGS, GPSTAGS
            exif_data = img.getexif()
            if exif_data:
                section("EXIF DATA",LG)
                for tid, val in exif_data.items():
                    tag = TAGS.get(tid, str(tid))
                    print(LG+f"  {str(tag):<28}"+LW+f" {str(val)[:80]}")
            else:
                print(LG+"  No EXIF metadata found.")
        except Exception as exif_e:
            print(LY+f"  EXIF read error: {exif_e}")
    except Exception as e: print(LR+f"  Error: {e}")
    pause()

# ──────────────────────────────────────────────
#  WIFI SCANNER
# ──────────────────────────────────────────────

def wifi_scanner():
    show_logo("geo")
    print(LY + "  WiFi scanner — By camzzz\n")

    spinner("Scanning WiFi networks", 1.5, LY)
    networks = []

    if IS_TERMUX:
        # API WiFi Android
        try:
            result = subprocess.run(
                ["termux-wifi-scaninfo"],
                capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                import json as _json
                data = _json.loads(result.stdout)
                for net in data:
                    networks.append({
                        "ssid":    net.get("ssid","Hidden") or "Hidden",
                        "bssid":   net.get("bssid","?"),
                        "signal":  str(net.get("level","?")),
                        "channel": str(net.get("channelWidth","?")),
                        "authentication": net.get("capabilities","?"),
                    })
            else:
                print(LY + "  termux-wifi-scaninfo returned no data.")
                print(LY + "  Installe 'Termux:API' si ce n'est pas fait, et active la localisation.")
        except FileNotFoundError:
            print(LR + "  termux-wifi-scaninfo not found.")
            print(LY + "  Install with:  pkg install termux-api")
        except Exception as ex:
            print(LR + f"  WiFi scan error: {ex}")
    else:
        # Linux fallback (nmcli)
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "SSID,SIGNAL,CHAN,SECURITY", "dev", "wifi", "list"],
                capture_output=True, text=True, timeout=10)
            for line in result.stdout.strip().split("\n"):
                if line:
                    p = line.split(":")
                    networks.append({
                        "ssid":    p[0] if p[0] else "Hidden",
                        "signal":  p[1]+"%"  if len(p)>1 else "N/A",
                        "channel": p[2] if len(p)>2 else "N/A",
                        "authentication": p[3] if len(p)>3 else "N/A",
                    })
        except Exception as ex:
            print(LR + f"  nmcli error: {ex}")

    if not networks:
        print(LR + "\n  No networks found.")
        if IS_TERMUX:
            print(LY + "  Make sure Termux:API is installed:  pkg install termux-api")
            print(LY + "  Et que la permission localisation est accordee.")
        pause(); return

    section(f"FOUND {len(networks)} NETWORKS", LY)
    print(LY + f"  {'#':<4} {'SSID':<30} {'Signal':<12} {'Security'}")
    print(LY + "  " + "-"*60)
    for i, net in enumerate(networks, 1):
        ssid  = net.get("ssid","?")[:28]
        sig   = str(net.get("signal","?"))
        auth  = net.get("authentication","?")[:20]
        col   = LR if "OPEN" in auth.upper() else LG
        print(LY + f"  {i:<4} {ssid:<30} {sig:<12} " + col + auth)

    open_nets = [n["ssid"] for n in networks
                 if "OPEN" in n.get("authentication","").upper()
                 or n.get("authentication","").upper() in ["","NONE","N/A"]]
    if open_nets:
        print(LR + "\n  Open (unencrypted) networks:")
        for s in open_nets: print(LR + f"    - {s}")
    pause()

# ──────────────────────────────────────────────
#  WEB VULN SCANNER
# ──────────────────────────────────────────────

def web_vuln_scanner():
    show_logo("port")
    print(LR + "  Passive web vulnerability scanner — 20 checks.\n")
    url = input(LR + "  Target URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url
    results = []
    spinner(f"Connecting to {url}", 0.8, LR)
    try:
        resp = requests.get(url, timeout=10,
                            headers={"User-Agent": "Mozilla/5.0"})
    except Exception as ex:
        print(LR + f"  Cannot reach target: {ex}"); pause(); return
    hdrs = resp.headers; text = resp.text.lower()
    section("SECURITY HEADERS", LR)
    for hdr, label in [
        ("Strict-Transport-Security","HSTS"),
        ("Content-Security-Policy",  "CSP"),
        ("X-Frame-Options",          "X-Frame-Options"),
        ("X-Content-Type-Options",   "X-Content-Type-Options"),
        ("X-XSS-Protection",         "X-XSS-Protection"),
        ("Referrer-Policy",          "Referrer-Policy"),
    ]:
        present = hdr in hdrs
        col = LG if present else LY
        status = "OK  " if present else "WARN"
        print(col + f"  [{status}]  {label:<35}" +
              LW + f" {hdrs.get(hdr,'MISSING')[:50]}")
        results.append((label, status, hdrs.get(hdr,"MISSING")))
    section("SERVER INFO EXPOSURE", LR)
    for hdr in ["Server","X-Powered-By","X-AspNet-Version","X-Generator"]:
        val = hdrs.get(hdr)
        if val:
            print(LY + f"  [WARN]  {hdr:<35}" + LW + f" {val[:60]}")
            results.append((hdr,"WARN",val))
    section("SENSITIVE FILES", LR)
    base = url.rstrip("/")
    for path in ["/.env","/.git/config","/robots.txt","/phpinfo.php",
                 "/wp-config.php","/.htaccess","/config.php","/admin","/phpmyadmin"]:
        try:
            r2 = requests.get(base+path, timeout=5,
                              headers={"User-Agent":"Mozilla/5.0"})
            if r2.status_code == 200 and len(r2.text) > 10:
                print(LR + f"  [VULN]  Sensitive file exposed: {path}")
                results.append((path,"VULN",f"HTTP 200"))
        except: pass
    section("SUMMARY", LR)
    vulns = [r for r in results if r[1]=="VULN"]
    warns = [r for r in results if r[1]=="WARN"]
    row("VULN findings", len(vulns), LR, LR if vulns else LG)
    row("WARN findings", len(warns), LY, LY if warns else LG)
    try:
        save = input(LY+"\n  Save report to txt? [y/N] > ").strip().lower()
        if save=="y":
            fname = f"vuln_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname,"w") as f:
                f.write(f"Scan: {url}\nDate: {datetime.now()}\n{'='*60}\n")
                for label,status,detail in results:
                    f.write(f"[{status}] {label}: {detail}\n")
            print(LG+f"  Saved to {fname}")
    except: pass
    pause()

# ──────────────────────────────────────────────
#  FIREWALL DETECTOR
# ──────────────────────────────────────────────

def firewall_detector():
    show_logo("port")
    print(LC + "  Detects WAF, CDN, bot protection, SSL info.\n")
    url = input(LC + "  Target URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url
    from urllib.parse import urlparse as _up
    hostname = _up(url).netloc
    spinner(f"Scanning {url}", 1.5, LC)
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        all_hdrs = r.headers; page = r.text.lower()
    except Exception as ex:
        print(LR + f"  Cannot reach target: {ex}"); pause(); return

    WAF_SIGS = {
        "Cloudflare": ["cf-ray","cf-cache-status","__cf_bm"],
        "AWS WAF":    ["x-amzn-requestid","x-amz-cf-id"],
        "Akamai":     ["akamai","x-akamai"],
        "Imperva":    ["x-iinfo","incap_ses"],
        "Sucuri":     ["x-sucuri-id"],
        "Cloudfront": ["x-amz-cf","cloudfront"],
        "Fastly":     ["fastly","x-served-by"],
        "Varnish":    ["x-varnish"],
        "DDoS-Guard": ["ddos-guard"],
    }
    BOT_SIGS = {
        "reCAPTCHA":   ["recaptcha"],
        "hCaptcha":    ["hcaptcha"],
        "Turnstile":   ["turnstile"],
        "PerimeterX":  ["perimeterx","_px"],
        "DataDome":    ["datadome"],
    }
    waf_found=[]
    for hdr, val in all_hdrs.items():
        hl=hdr.lower(); vl=str(val).lower()
        for waf, sigs in WAF_SIGS.items():
            if any(s in hl or s in vl for s in sigs):
                if waf not in " ".join(waf_found): waf_found.append(waf)
    bot_found=[]
    for bp, sigs in BOT_SIGS.items():
        if any(s in page for s in sigs): bot_found.append(bp)

    section("WAF / FIREWALL", LR)
    if waf_found:
        for w in waf_found: print(LR + f"  [+]  {w}")
    else: print(DIM+LW+"  None detected")

    section("BOT PROTECTION", LM)
    if bot_found:
        for b in bot_found: print(LM + f"  [+]  {b}")
    else: print(DIM+LW+"  None detected")

    section("SERVER INFO", LY)
    for hdr in ["Server","X-Powered-By","X-Generator"]:
        v = all_hdrs.get(hdr)
        if v: row(hdr, v, LY, LW)

    section("SECURITY HEADERS", LC)
    for sh in ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options","X-Content-Type-Options"]:
        if sh in all_hdrs:
            print(LG + f"  [OK]  {sh}")
        else:
            print(LR + f"  [!!]  {sh} MISSING")
    pause()

# ──────────────────────────────────────────────
#  FILE SCANNER
# ──────────────────────────────────────────────

def file_scanner():
    show_logo("hash")
    print(LM + "  Scans a file for suspicious strings, high entropy, hashes.\n")
    filepath = input(LM + "  File path > ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(LR + "  File not found."); pause(); return
    spinner("Analysing file", 1.0, LM)
    md5h = hashlib.md5(); sha256h = hashlib.sha256()
    threats=[]; warnings=[]
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                md5h.update(chunk); sha256h.update(chunk)
        md5_val    = md5h.hexdigest()
        sha256_val = sha256h.hexdigest()
    except Exception as ex:
        print(LR + f"  Hash error: {ex}"); pause(); return
    section("FILE INFO", LM)
    row("Path",   filepath,    LM, LW)
    row("Size",   f"{os.path.getsize(filepath):,} bytes", LM, LW)
    row("MD5",    md5_val,     LM, LW)
    row("SHA256", sha256_val,  LM, LW)
    print(LM + f"\n  VT check: https://www.virustotal.com/gui/file/{sha256_val}")
    SUSPICIOUS = [
        b"cmd.exe", b"powershell", b"WScript.Shell", b"HKEY_",
        b"CreateRemoteThread", b"VirtualAllocEx", b"URLDownloadToFile",
        b"system(", b"exec(", b"eval(", b"base64",
        b"ransom", b"bitcoin", b"keylog",
        b"wget ", b"curl ", b"chmod 777", b"/etc/passwd",
        b"DROP TABLE", b"UNION SELECT",
        b"<script>", b"javascript:", b"onerror=",
    ]
    try:
        with open(filepath,"rb") as f: content = f.read()
        for sig in SUSPICIOUS:
            if sig in content:
                threats.append(f"Suspicious string: {sig.decode('utf-8',errors='ignore')}")
    except Exception as ex:
        warnings.append(f"String scan error: {ex}")
    # Entropy
    try:
        import math
        sample = content[:65536]
        if sample:
            freq = [0]*256
            for byte in sample: freq[byte]+=1
            entropy = -sum((c/len(sample))*math.log2(c/len(sample)) for c in freq if c>0)
            row("Entropy", f"{entropy:.2f}/8.0", LM,
                LR if entropy>7.0 else LY if entropy>6.0 else LG)
            if entropy>7.0: threats.append(f"Very high entropy ({entropy:.2f}) — packed/encrypted?")
    except: pass
    ext = os.path.splitext(filepath)[1].lower()
    dangerous_exts=[".exe",".dll",".bat",".cmd",".vbs",".ps1",".jar",".msi"]
    if ext in dangerous_exts: warnings.append(f"Executable file type: {ext}")
    section("SCAN RESULTS", LM)
    risk = "CRITICAL" if len(threats)>=5 else "HIGH" if len(threats)>=3 else \
           "MEDIUM" if len(threats)>=1 else "LOW" if warnings else "CLEAN"
    rcol = {"CRITICAL":LR,"HIGH":LR,"MEDIUM":LY,"LOW":LY,"CLEAN":LG}[risk]
    row("Risk level", risk, LM, rcol)
    if threats:
        section("THREATS DETECTED",LM)
        for i,t in enumerate(threats,1): print(LR+f"  [{i}]  {t}")
    if warnings:
        section("WARNINGS",LM)
        for i,w in enumerate(warnings,1): print(LY+f"  [{i}]  {w}")
    if risk=="CLEAN": print(LG+"\n  File appears clean based on static analysis.")
    pause()

# ──────────────────────────────────────────────
#  ASN / BGP
# ──────────────────────────────────────────────

def asn_lookup():
    show_logo("geo")
    q=input(LC+"  IP or ASN (e.g. 8.8.8.8 or AS15169) > ").strip()
    if not q: pause(); return
    spinner("Querying BGPView",1.0,LC)
    try:
        r=requests.get(f"https://api.bgpview.io/ip/{q}",timeout=10).json()
        data=r.get("data",{})
        section("IP / ASN INFO",LC); row("IP",data.get("ip","N/A"),LC,LW)
        for p in data.get("prefixes",[])[:10]:
            asn=p.get("asn",{})
            print(LC+f"  {p.get('prefix',''):<22}"+LW+f" AS{asn.get('asn','')}  {asn.get('name','')}")
    except:
        try:
            asn_clean=q.upper().replace("AS","")
            r2=requests.get(f"https://api.bgpview.io/asn/{asn_clean}",timeout=10).json()
            d=r2.get("data",{})
            section("ASN INFO",LC)
            row("ASN",f"AS{d.get('asn','N/A')}",LC,LW)
            row("Name",d.get("name","N/A"),LC,LW)
            row("Country",d.get("country_code","N/A"),LC,LW)
        except Exception as e: print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  WAYBACK / ARCHIVE
# ──────────────────────────────────────────────

def wayback():
    show_logo("geo")
    url=input(LG+"  URL > ").strip()
    if not url: pause(); return
    spinner("Querying archive.org",1.0,LG)
    try:
        r=requests.get(f"http://archive.org/wayback/available?url={url}",timeout=10).json()
        snap=r.get("archived_snapshots",{}).get("closest",{})
        section("SNAPSHOT INFO",LG)
        if snap:
            row("Available", snap.get("available","N/A"),LG,LW)
            row("URL",       snap.get("url","N/A"),      LG,LC)
            row("Timestamp", snap.get("timestamp","N/A"),LG,LW)
        else: print(LG+"  No snapshots found.")
        print(LG+f"\n  All snapshots: https://web.archive.org/web/*/{url}")
    except Exception as e: print(LR+f"  Failed: {e}")
    pause()

def wayback_urls():
    show_logo("geo")
    domain=input(LG+"  Domain > ").strip()
    if not domain: pause(); return
    spinner("Querying CDX API",1.5,LG)
    try:
        r=requests.get(
            f"http://web.archive.org/cdx/search/cdx?url=*.{domain}&output=text&fl=original&collapse=urlkey&limit=100",
            timeout=15)
        urls=list(set(r.text.strip().split("\n")))
        section(f"FOUND {len(urls)} UNIQUE URLs",LG)
        for u in sorted(urls)[:80]: print(LG+f"  {u}")
        if len(urls)>80: print(LG+f"\n  ... and {len(urls)-80} more.")
    except Exception as e: print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  PROFILE BUILDER
# ──────────────────────────────────────────────

def profile_builder():
    show_logo("user")
    name    =input(LM+"  Full name  > ").strip()
    username=input(LM+"  Username   > ").strip()
    email   =input(LM+"  Email      > ").strip()
    loc     =input(LM+"  Location   > ").strip()
    section("PROFILE SUMMARY",LM)
    row("Name",    name,    LM,LW)
    row("Username",username,LM,LW)
    if email:
        row("Email",email,LM,LW)
        md5=hashlib.md5(email.lower().encode()).hexdigest()
        row("Gravatar",f"https://gravatar.com/avatar/{md5}",LM,LC)
    if loc: row("Location",loc,LM,LW)
    enc_name=qenc(name)
    section("NAME SEARCH LINKS",LM)
    for n,l in [
        ("Google",        f"https://www.google.com/search?q=%22{enc_name}%22"),
        ("LinkedIn",      f"https://www.linkedin.com/search/results/people/?keywords={enc_name}"),
        ("Twitter",       f"https://twitter.com/search?q=%22{enc_name}%22"),
        ("Facebook",      f"https://www.facebook.com/search/top/?q={enc_name}"),
        ("ZSearcher.fr",  f"https://zsearcher.fr/search?q={enc_name}"),
        ("OathNet.org",   f"https://oathnet.org/search?q={enc_name}"),
    ]: link(n,l,LM)
    if username:
        section("USERNAME QUICK LINKS",LM)
        for site,tpl in SITES[:15]:
            print(LM+f"  {site:<20}"+LW+f" {tpl.format(username)}")
    pause()

# ──────────────────────────────────────────────
#  SHODAN LINKS
# ──────────────────────────────────────────────

def shodan_links():
    show_logo("port")
    target=input(LC+"  IP or domain > ").strip()
    e=qenc(target)
    section("SHODAN",LC)
    for name,lnk in [
        ("Host info",  f"https://www.shodan.io/host/{target}"),
        ("Search",     f"https://www.shodan.io/search?query={e}"),
        ("Domain",     f"https://www.shodan.io/domain/{target}"),
        ("SSL cert",   f"https://www.shodan.io/search?query=ssl.cert.subject.cn:{target}"),
    ]: link(name,lnk,LC)
    section("OTHER INTEL PLATFORMS",LC)
    for name,lnk in [
        ("Censys",     f"https://search.censys.io/search?resource=hosts&q={e}"),
        ("ZoomEye",    f"https://www.zoomeye.org/searchResult?q={e}"),
        ("Greynoise",  f"https://viz.greynoise.io/ip/{target}"),
        ("VirusTotal", f"https://www.virustotal.com/gui/domain/{target}"),
        ("URLScan",    f"https://urlscan.io/search/#{e}"),
        ("FOFA",       f"https://fofa.info/result?qbase64={base64.b64encode(target.encode()).decode()}"),
        ("OTX",        f"https://otx.alienvault.com/indicator/domain/{target}"),
        ("BinaryEdge", f"https://app.binaryedge.io/services/query?query={e}"),
    ]: link(name,lnk,LC)
    pause()

# ──────────────────────────────────────────────
#  QUICK RECON
# ──────────────────────────────────────────────

def quick_recon():
    show_logo("geo")
    domain=input(LG+"  Domain > ").strip()
    if not domain: pause(); return
    bar("  Running full recon",40,0.03,LG,G)
    section("DNS",LG)
    try:
        ip=socket.gethostbyname(domain); row("A Record",ip,LG,LW)
        try: rev=socket.gethostbyaddr(ip); row("Reverse DNS",rev[0],LG,LW)
        except: pass
    except Exception as e: row("DNS",f"Failed: {e}",LG,LR)
    section("GEO IP",LG)
    try:
        d=requests.get(f"https://ipapi.co/{socket.gethostbyname(domain)}/json",timeout=8).json()
        for f in ["country_name","city","org","asn","timezone"]:
            row(f,d.get(f,"N/A"),LG,LW)
    except: pass
    section("HTTP",LG)
    try:
        r=requests.get(f"https://{domain}",timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        row("Status",str(r.status_code),LG,LW)
        row("Server",r.headers.get("Server","N/A"),LG,LW)
        row("CSP","present" if r.headers.get("Content-Security-Policy") else "MISSING",LG,
            LG if r.headers.get("Content-Security-Policy") else LR)
    except: pass
    section("QUICK SUBDOMAINS",LG)
    for sub in ["www","mail","api","admin","dev","staging","ftp","vpn","cdn","blog"]:
        t=f"{sub}.{domain}"
        try: ip2=socket.gethostbyname(t); print(LG+f"  [+]  {t:<40}"+LW+f" -> {ip2}")
        except: pass
    section("USEFUL LINKS",LG)
    e=qenc(domain)
    for name,lnk in [
        ("Shodan",    f"https://www.shodan.io/search?query={e}"),
        ("VirusTotal",f"https://www.virustotal.com/gui/domain/{domain}"),
        ("URLScan",   f"https://urlscan.io/search/#{e}"),
        ("Wayback",   f"https://web.archive.org/web/*/{domain}"),
        ("crt.sh",    f"https://crt.sh/?q=%.{domain}"),
        ("ZSearcher", f"https://zsearcher.fr/search?q={e}"),
    ]: link(name,lnk,LC)
    pause()

# ──────────────────────────────────────────────
#  NETWORK INFO
# ──────────────────────────────────────────────

def network_info():
    show_logo("geo")
    spinner("Gathering info",0.8,LG)
    section("LOCAL MACHINE",LG)
    hn=socket.gethostname(); lip=socket.gethostbyname(hn)
    row("Hostname",hn,LG,LW); row("Local IP",lip,LG,LW)
    row("Platform",platform.system()+" "+platform.release(),LG,LW)
    row("Python",sys.version.split()[0],LG,LW)
    row("Termux","Yes" if IS_TERMUX else "No",LG,LG if IS_TERMUX else LW)
    section("PUBLIC IP",LG)
    try:
        pub=requests.get("https://api.ipify.org?format=json",timeout=8).json()
        pip=pub.get("ip","N/A")
        geo=requests.get(f"https://ipapi.co/{pip}/json",timeout=8).json()
        row("Public IP",pip,LG,LW)
        for f in ["country_name","city","org","asn","timezone"]:
            row(f,geo.get(f,"N/A"),LG,LW)
    except: print(LR+"  Could not retrieve public IP.")
    pause()

# ──────────────────────────────────────────────
#  ROBOTS / SITEMAP
# ──────────────────────────────────────────────

def robots_sitemap():
    show_logo("geo")
    domain=input(LG+"  Domain > ").strip()
    if not domain.startswith("http"): base=f"https://{domain}"
    else: base=domain
    for path in ["/robots.txt","/sitemap.xml","/sitemap_index.xml"]:
        spinner(f"Fetching {path}",0.4,LG)
        try:
            r=requests.get(base+path,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200:
                section(f"CONTENT OF {path}",LG)
                for line in r.text.strip().split("\n")[:60]:
                    print(LG+f"  {line}")
            else: print(LG+f"  {path}  ->  {r.status_code}")
        except Exception as e: print(LG+f"  {path}  ->  Error: {e}")
    pause()

# ──────────────────────────────────────────────
#  SOCIAL SEARCH / PASTE / DARK WEB / CVE
# ──────────────────────────────────────────────

def social_search():
    show_logo("user")
    q=input(LM+"  Name / username / hashtag > ").strip(); e=qenc(q)
    section("SOCIAL MEDIA SEARCH LINKS",LM)
    for plat,lnk in [
        ("Twitter/X",    f"https://twitter.com/search?q={e}&f=live"),
        ("Instagram tags",f"https://www.instagram.com/explore/tags/{e}/"),
        ("TikTok",       f"https://www.tiktok.com/search?q={e}"),
        ("Facebook",     f"https://www.facebook.com/search/top/?q={e}"),
        ("LinkedIn",     f"https://www.linkedin.com/search/results/people/?keywords={e}"),
        ("Reddit",       f"https://www.reddit.com/search/?q={e}"),
        ("YouTube",      f"https://www.youtube.com/results?search_query={e}"),
        ("Telegram",     f"https://t.me/s/{q}"),
        ("Snapchat",     f"https://www.snapchat.com/add/{q}"),
    ]: link(plat,lnk,LM)
    pause()

def paste_search():
    show_logo("user")
    q=input(LM+"  Search term > ").strip(); e=qenc(q)
    section("PASTE SEARCH LINKS",LM)
    for name,lnk in [
        ("Google Pastebin", f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
        ("Google Gist",     f"https://www.google.com/search?q=site:gist.github.com+%22{e}%22"),
        ("Psbdmp",          f"https://psbdmp.ws/api/search/{e}"),
        ("Grep.app",        f"https://grep.app/search?q={e}"),
        ("GitHub code",     f"https://github.com/search?q={e}&type=code"),
    ]: link(name,lnk,LM)
    pause()

def darkweb_search():
    show_logo("breach")
    print(LR+"  Clearnet search engines that index .onion content.\n")
    q=input(LC+"  Search term > ").strip(); e=qenc(q)
    section("DARK WEB SEARCH ENGINES",LR)
    for name,lnk in [
        ("Ahmia (clearnet)", f"https://ahmia.fi/search/?q={e}"),
        ("DarkSearch",       f"https://darksearch.io/search?query={e}"),
        ("DeHashed",         f"https://dehashed.com/search?query={e}"),
        ("IntelX",           f"https://intelx.io/?s={e}"),
    ]: link(name,lnk,LR)
    pause()

def vuln_search():
    show_logo("port")
    q=input(LR+"  Software / CVE ID > ").strip(); e=qenc(q)
    section("VULN SEARCH LINKS",LR)
    for name,lnk in [
        ("NVD (NIST)",       f"https://nvd.nist.gov/vuln/search/results?query={e}"),
        ("CVE Details",      f"https://www.cvedetails.com/google-search-results.php?q={e}"),
        ("Exploit-DB",       f"https://www.exploit-db.com/search?q={e}"),
        ("Shodan CVE",       f"https://www.shodan.io/search?query=vuln:{q}"),
        ("PacketStorm",      f"https://packetstormsecurity.com/search/?q={e}"),
        ("GitHub Advisories",f"https://github.com/advisories?query={e}"),
        ("Snyk Vuln DB",     f"https://security.snyk.io/vuln?search={e}"),
    ]: link(name,lnk,LR)
    pause()

def reverse_image():
    show_logo("user")
    url=input(LM+"  Image URL > ").strip()
    if not url: pause(); return
    e=qenc(url)
    section("REVERSE IMAGE SEARCH LINKS",LM)
    for name,lnk in [
        ("Google Images", f"https://www.google.com/searchbyimage?image_url={e}"),
        ("Yandex Images", f"https://yandex.com/images/search?url={e}&rpt=imageview"),
        ("TinEye",        f"https://tineye.com/search?url={e}"),
        ("SauceNAO",      f"https://saucenao.com/search.php?url={e}"),
    ]: link(name,lnk,LM)
    pause()

def osint_framework():
    show_logo("user")
    section("KEY OSINT RESOURCES",LM)
    for name,lnk in [
        ("OSINT Framework",  "https://osintframework.com"),
        ("IntelTechniques",  "https://inteltechniques.com/tools/index.html"),
        ("ZSearcher.fr",     "https://zsearcher.fr/"),
        ("OathNet.org",      "https://oathnet.org/"),
        ("Shodan",           "https://www.shodan.io"),
        ("Censys",           "https://search.censys.io"),
        ("HaveIBeenPwned",   "https://haveibeenpwned.com"),
        ("URLScan.io",       "https://urlscan.io"),
        ("VirusTotal",       "https://www.virustotal.com"),
        ("Wayback Machine",  "https://web.archive.org"),
        ("BGPView",          "https://bgpview.io"),
        ("Grep.app",         "https://grep.app"),
        ("DeHashed",         "https://dehashed.com"),
        ("IntelX",           "https://intelx.io"),
        ("LeakIX",           "https://leakix.net"),
        ("GrayHatWarfare",   "https://grayhatwarfare.com"),
        ("OTX AlienVault",   "https://otx.alienvault.com"),
        ("Hunter.io",        "https://hunter.io"),
        ("crt.sh",           "https://crt.sh"),
        ("SecurityTrails",   "https://securitytrails.com"),
    ]: link(name,lnk,LM)
    pause()

def archive_links():
    show_logo("geo")
    url=input(LG+"  URL > ").strip()
    if not url.startswith("http"): url="https://"+url
    e=qenc(url)
    section("ARCHIVE LINKS",LG)
    for name,lnk in [
        ("Wayback Machine", f"https://web.archive.org/web/*/{url}"),
        ("Archive.ph",      f"https://archive.ph/{url}"),
        ("Google Cache",    f"https://webcache.googleusercontent.com/search?q=cache:{url}"),
    ]: link(name,lnk,LG)
    pause()

def url_tracer():
    show_logo("geo")
    url=input(LG+"  URL > ").strip()
    if not url.startswith("http"): url="https://"+url
    spinner("Tracing redirects",0.8,LG)
    try:
        r=requests.get(url,timeout=10,allow_redirects=True,headers={"User-Agent":"Mozilla/5.0"})
        section("REDIRECT CHAIN",LG)
        for i,resp in enumerate(r.history+[r]):
            print(LG+f"  Step {i}  [{resp.status_code}]  {resp.url}")
    except Exception as e: print(LR+f"  Failed: {e}")
    pause()

def public_records():
    show_logo("user")
    q=input(LM+"  Name / email / username > ").strip(); e=qenc(q)
    section("PUBLIC RECORD SEARCH LINKS",LM)
    for name,lnk in [
        ("Spokeo",           f"https://www.spokeo.com/search?q={e}"),
        ("TruePeopleSearch", f"https://www.truepeoplesearch.com/results?name={e}"),
        ("WhitePages",       f"https://www.whitepages.com/name/{e}"),
        ("FastPeopleSearch", f"https://www.fastpeoplesearch.com/name/{e}"),
        ("LinkedIn",         f"https://www.google.com/search?q=site:linkedin.com+%22{e}%22"),
        ("Twitter",          f"https://twitter.com/search?q=%22{e}%22"),
        ("ZSearcher.fr",     f"https://zsearcher.fr/search?q={e}"),
        ("OathNet.org",      f"https://oathnet.org/search?q={e}"),
    ]: link(name,lnk,LM)
    pause()

def file_osint():
    show_logo("dork")
    domain=input(LY+"  Domain > ").strip()
    section("FILE SEARCH LINKS",LY)
    for label,ext in [
        ("PDF","pdf"),("Word","doc OR docx"),("Excel","xls OR xlsx"),
        ("CSV","csv"),("SQL","sql"),("ENV","env"),("LOG","log"),
        ("BAK","bak"),("ZIP","zip"),("CONFIG","conf OR config"),
    ]:
        q=qenc(f"site:{domain} ext:{ext}")
        print(LY+f"  {label:<12}"+LW+f" https://www.google.com/search?q={q}")
    pause()

def public_cameras():
    show_logo("cam")
    print(LR+"  Searches for publicly indexed camera feeds.\n")
    location=input(LC+"  Location (city/country, blank to skip) > ").strip()
    section("SHODAN CAMERA SEARCHES",LR)
    queries=[
        ("Webcams generic",   "has_screenshot:true port:80"),
        ("Hikvision cameras", "server:Hikvision-Webs"),
        ("RTSP streams",      "port:554 has_screenshot:true"),
    ]
    for name,q in queries:
        full_q=q+(f" city:{location}" if location else "")
        print(LR+f"  {name:<28}"+LW+f" https://www.shodan.io/search?query={qenc(full_q)}")
    section("PUBLIC CAMERA DIRECTORIES",LR)
    for name,lnk in [
        ("Insecam",    "http://www.insecam.org/"),
        ("EarthCam",   "https://www.earthcam.com/"),
        ("Windy cams", "https://www.windy.com/"),
    ]: link(name,lnk,LR)
    pause()

def contact():
    clear()
    print(LG+"\n  CONTACT — By camzzz")
    print(LG+"  "+"="*40)
    row("Discord","cameleonmortis",   LC,LW)
    row("GitHub", "https://github.com/cameleonnbss/50-multi-tool",LC,LW)
    print()
    for line in CAMZZZ_LINES: rainbow("  "+line)
    print(); pause()

# ──────────────────────────────────────────────
#  MENU
# ──────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════
#  APIS BREACH AVEC CLÉ GRATUITE
# ══════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────
#  LEAKCHECK API  (free tier : 50 req/mois)
#  Clé gratuite sur : https://leakcheck.io
#  7.5 milliards de records, 3000+ bases
# ──────────────────────────────────────────────

# LEAKCHECK_KEY est charge automatiquement depuis config.ini

def leakcheck_api():
    show_logo("breach")
    print(LR + "  LeakCheck API  —  7.5B+ records  —  3000+ bases")
    print(LR + "  Free tier : 50 requetes/mois  —  Cle gratuite sur leakcheck.io\n")

    global LEAKCHECK_KEY
    key = LEAKCHECK_KEY.strip()
    if not key:
        print(LY + "  Aucune cle LeakCheck trouvee dans config.ini")
        print(LY + "  Inscription gratuite : https://leakcheck.io\n")
        key = input(LY + "  Entre ta cle LeakCheck (ou ENTER pour annuler) > ").strip()
        if not key:
            print(LR + "  Cle requise.")
            pause(); return
        # Sauvegarde automatique SANS demander
        save_key("leakcheck_key", key)
        LEAKCHECK_KEY = key
        print(LG + "  [OK]  Cle sauvegardee dans config.ini — ne sera plus jamais redemandee.")

    print(LR + "\n  1  Recherche email\n"
               "  2  Recherche username\n"
               "  3  Recherche domaine\n"
               "  4  Recherche telephone\n"
               "  5  Recherche hash (SHA256 email)\n"
               "  6  Infos sur ton compte (credits restants)\n")
    c = input(LC + "  Choice > ").strip()

    SEARCH_TYPES = {
        "1": ("email",    "Email > "),
        "2": ("username", "Username > "),
        "3": ("domain",   "Domaine > "),
        "4": ("phone",    "Telephone (ex: +33612345678) > "),
        "5": ("hash",     "SHA256 hash d'email > "),
    }

    if c == "6":
        spinner("Verification du compte LeakCheck", 1.0, LR)
        try:
            r = requests.get("https://leakcheck.io/api/v2/query/test@test.com",
                             headers={"X-API-Key": key}, timeout=10)
            section("INFOS COMPTE LEAKCHECK", LR)
            if r.status_code in [200, 404]:
                hdrs = r.headers
                remaining = hdrs.get("X-RateLimit-Remaining", "?")
                limit     = hdrs.get("X-RateLimit-Limit", "?")
                reset     = hdrs.get("X-RateLimit-Reset", "?")
                row("Requetes restantes", remaining, LR, LG if str(remaining) != "0" else LR)
                row("Limite mensuelle",   limit,     LR, LW)
                row("Reset le",          reset,     LR, LW)
                row("Statut cle",        "Valide [OK]", LR, LG)
            elif r.status_code == 401:
                print(LR + "  Cle invalide ou expiree.")
            else:
                print(LY + f"  HTTP {r.status_code}: {r.text[:100]}")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")
        pause(); return

    if c not in SEARCH_TYPES:
        print(LR + "  Option invalide."); pause(); return

    stype, prompt = SEARCH_TYPES[c]
    query = input(LC + f"  {prompt}").strip()
    if not query: pause(); return

    spinner(f"Recherche LeakCheck ({stype}): {query}", 1.5, LR)

    try:
        r = requests.get(
            f"https://leakcheck.io/api/v2/query/{qenc(query)}",
            headers={"X-API-Key": key},
            params={"type": stype},
            timeout=12
        )

        # Rate limit info
        remaining = r.headers.get("X-RateLimit-Remaining", "?")

        section(f"LEAKCHECK — {stype.upper()} — {query}", LR)
        row("Query",   query,         LR, LW)
        row("Type",    stype,         LR, LW)
        row("Credits restants", remaining, LR, LG if str(remaining) != "0" else LR)
        print()

        if r.status_code == 200:
            data = r.json()
            results = data.get("result", [])
            found   = data.get("found", 0)
            success = data.get("success", False)

            if not success or not results:
                print(LG + f"  [OK]  Aucun resultat trouve pour '{query}'.")
            else:
                print(LR + f"  [!!!]  {found} entree(s) trouvee(s) !\n")

                # Stats rapides
                all_sources = list(set(r.get("sources", ["?"])[0] if r.get("sources") else "?" for r in results))
                row("Sources uniques", len(all_sources), LR, LW)

                section("RESULTATS DETAILLES", LR)
                for i, entry in enumerate(results[:30], 1):
                    print(LR + f"\n  --- Entree #{i} ---")
                    for field in ["email", "username", "password", "hash",
                                  "name", "ip", "phone", "address", "domain"]:
                        val = entry.get(field)
                        if val and val not in ["", "N/A"]:
                            col = LR if field == "password" else LW
                            print(LR + f"  {field:<16}" + col + f" {str(val)[:70]}")
                    sources = entry.get("sources", [])
                    if sources:
                        print(LC + f"  {'sources':<16}" + LY + f" {', '.join(sources[:5])}")

                if len(results) > 30:
                    print(LY + f"\n  ... et {len(results)-30} resultats de plus (limite affichage).")

                # Export
                try:
                    save = input(LY + "\n  Sauvegarder les resultats? [y/N] > ").strip().lower()
                    if save == "y":
                        import json as _json
                        fname = f"leakcheck_{stype}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(fname, "w") as f:
                            _json.dump({"query": query, "type": stype,
                                        "found": found, "results": results}, f, indent=2)
                        print(LG + f"  Sauvegarde: {fname}")
                except Exception: pass

        elif r.status_code == 401:
            print(LR + "  Cle API invalide ou expiree.")
            print(LY + "  Renouvelle ta cle sur https://leakcheck.io")
        elif r.status_code == 429:
            print(LY + "  Rate limit atteint (50 req/mois sur free tier).")
            print(LY + "  Prochaine reset visible dans les headers.")
        elif r.status_code == 404:
            print(LG + f"  [OK]  Aucun resultat pour '{query}'.")
        else:
            print(LY + f"  HTTP {r.status_code}: {r.text[:200]}")

    except Exception as ex:
        print(LR + f"  Erreur: {ex}")

    print()
    print(LC + "  LeakCheck : https://leakcheck.io  |  7.5B+ records  |  3000+ bases")
    pause()


# ──────────────────────────────────────────────
#  BREACHDIRECTORY (Logoutify) API
#  Free : inscription + cle gratuite
#  Clé sur : https://breachdirectory.com
#  Email, username, IP, domaine
# ──────────────────────────────────────────────

def breachdirectory_api():
    show_logo("breach")
    print(LR + "  BreachDirectory API  —  Email / Username / IP / Domaine")
    print(LR + "  Gratuite via RapidAPI (free tier disponible)")
    print(LR + "  Cle sur : https://rapidapi.com/rohan-patra/api/breachdirectory\n")

    global BREACHDIR_KEY
    key = BREACHDIR_KEY.strip()
    if not key:
        print(LY + "  Aucune cle BreachDirectory trouvee dans config.ini")
        print(LY + "  Inscription gratuite sur RapidAPI :")
        print(LC + "  https://rapidapi.com/rohan-patra/api/breachdirectory\n")
        key = input(LY + "  Entre ta cle RapidAPI (ou ENTER pour annuler) > ").strip()
        if not key:
            pause(); return
        # Sauvegarde automatique SANS demander
        save_key("breachdirectory_key", key)
        BREACHDIR_KEY = key
        print(LG + "  [OK]  Cle sauvegardee dans config.ini — ne sera plus jamais redemandee.")

    print(LR + "\n  1  Recherche par email\n"
               "  2  Recherche par username\n"
               "  3  Recherche par IP\n"
               "  4  Recherche par domaine\n")
    c = input(LC + "  Choice > ").strip()

    TYPES = {"1": "email", "2": "username", "3": "ip", "4": "domain"}
    if c not in TYPES:
        print(LR + "  Option invalide."); pause(); return

    stype = TYPES[c]
    query = input(LC + f"  {stype.title()} > ").strip()
    if not query: pause(); return

    spinner(f"Recherche BreachDirectory ({stype}): {query}", 1.5, LR)

    try:
        r = requests.get(
            "https://breachdirectory.p.rapidapi.com/",
            headers={
                "X-RapidAPI-Key":  key,
                "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
            },
            params={"func": "auto", "term": query},
            timeout=12
        )

        section(f"BREACHDIRECTORY — {stype.upper()} — {query}", LR)
        row("Query", query, LR, LW)
        row("Type",  stype, LR, LW)
        print()

        if r.status_code == 200:
            data = r.json()
            results = data if isinstance(data, list) else data.get("result", data.get("data", []))

            if not results:
                print(LG + f"  [OK]  Aucun resultat pour '{query}'.")
            else:
                print(LR + f"  [!!!]  {len(results)} entree(s) trouvee(s) !\n")
                section("RESULTATS", LR)
                for i, entry in enumerate(results[:25], 1):
                    print(LR + f"\n  --- #{i} ---")
                    if isinstance(entry, dict):
                        for field in ["title", "email", "username", "password",
                                      "hash", "ip", "name", "phone", "domain"]:
                            val = entry.get(field)
                            if val:
                                col = LR if field == "password" else LW
                                print(LR + f"  {field:<14}" + col + f" {str(val)[:70]}")
                    else:
                        print(LW + f"  {str(entry)[:80]}")

                if len(results) > 25:
                    print(LY + f"\n  ... et {len(results)-25} de plus.")

                try:
                    save = input(LY + "\n  Sauvegarder? [y/N] > ").strip().lower()
                    if save == "y":
                        import json as _json
                        fname = f"breachdir_{stype}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(fname, "w") as f:
                            _json.dump({"query": query, "type": stype, "results": results}, f, indent=2)
                        print(LG + f"  Sauvegarde: {fname}")
                except Exception: pass

        elif r.status_code == 401 or r.status_code == 403:
            print(LR + "  Cle invalide ou non autorisee.")
        elif r.status_code == 429:
            print(LY + "  Rate limit atteint sur ton plan RapidAPI.")
        else:
            print(LY + f"  HTTP {r.status_code}: {r.text[:200]}")

    except Exception as ex:
        print(LR + f"  Erreur: {ex}")

    print()
    print(LC + "  BreachDirectory : https://breachdirectory.com")
    print(LC + "  RapidAPI        : https://rapidapi.com/rohan-patra/api/breachdirectory")
    pause()


# ══════════════════════════════════════════════════════════════
#  OUTILS OPEN SOURCE RECONNUS (liens + infos d'utilisation)
# ══════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────
#  HOLEHE — vérifie si un email est utilisé
#  sur 120+ plateformes via reset password
#  github.com/megadose/holehe
# ──────────────────────────────────────────────

def holehe_tool():
    show_logo("mail")
    print(LM + "  Holehe — verifie si un email est utilise sur 120+ sites")
    print(LM + "  Methode : reset password (read-only, aucune connexion)\n")
    print(LM + "  Install : pip install holehe")
    print(LM + "  Usage   : holehe <email>\n")

    email = input(LM + "  Email a analyser > ").strip()
    if "@" not in email:
        print(LR + "  Email invalide."); pause(); return

    # Tente d'utiliser holehe directement si installé
    try:
        result = subprocess.run(
            ["holehe", email, "--only-used"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            section(f"HOLEHE — {email}", LM)
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line: continue
                if "[+]" in line or "used" in line.lower():
                    print(LG + f"  {line}")
                elif "[-]" in line or "not used" in line.lower():
                    print(DIM + LW + f"  {line}")
                else:
                    print(LM + f"  {line}")
        elif result.returncode != 0:
            raise FileNotFoundError("not installed")
    except FileNotFoundError:
        print(LY + "  Holehe n'est pas installe sur ce systeme.")
        print(LY + "  Pour l'installer :\n")
        print(LW + "    pip install holehe")
        print(LW + "    holehe " + email + "\n")
        print(LM + "  En attendant, liens de recherche rapide :\n")
        e = qenc(email)
        section(f"LIENS ALTERNATIFS — {email}", LM)
        for name, lnk in [
            ("Google",         f"https://www.google.com/search?q=%22{e}%22"),
            ("GitHub code",    f"https://github.com/search?q={e}&type=code"),
            ("Gravatar",       f"https://www.gravatar.com/avatar/{hashlib.md5(email.lower().encode()).hexdigest()}"),
            ("EmailRep.io",    f"https://emailrep.io/{e}"),
            ("HaveIBeenPwned", f"https://haveibeenpwned.com/account/{e}"),
        ]: link(name, lnk, LM)

    section("RESSOURCES HOLEHE", LM)
    for name, lnk in [
        ("GitHub",       "https://github.com/megadose/holehe"),
        ("PyPI",         "https://pypi.org/project/holehe/"),
        ("Demo en ligne","https://github.com/megadose/holehe#usage"),
    ]: link(name, lnk, LC)
    pause()


# ──────────────────────────────────────────────
#  H8MAIL — breach hunting par email
#  github.com/khast3x/h8mail
#  Supporte : HIBP, LeakCheck, Snusbase, etc.
# ──────────────────────────────────────────────

def h8mail_tool():
    show_logo("breach")
    print(LR + "  h8mail — Password Breach Hunting & Email OSINT")
    print(LR + "  Supporte : HIBP, LeakCheck, Snusbase, Hunter.io, etc.")
    print(LR + "  github.com/khast3x/h8mail\n")

    email = input(LR + "  Email cible > ").strip()
    if "@" not in email:
        print(LR + "  Email invalide."); pause(); return

    # Tente d'utiliser h8mail si installé
    try:
        result = subprocess.run(
            ["h8mail", "-t", email],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode == 0 and result.stdout.strip():
            section(f"H8MAIL — {email}", LR)
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line: continue
                if any(x in line.upper() for x in ["FOUND","BREACH","LEAK","[+]"]):
                    print(LR + f"  {line}")
                elif any(x in line.upper() for x in ["[-]","NOT","NONE"]):
                    print(DIM + LW + f"  {line}")
                else:
                    print(LY + f"  {line}")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(LY + "  h8mail n'est pas installe.")
        print(LY + "  Pour l'installer :\n")
        print(LW + "    pip install h8mail")
        print(LW + "    h8mail -t " + email + "\n")

    section("INSTALLATION H8MAIL", LR)
    print(LW + "  pip install h8mail\n")
    print(LW + "  Usage basique :")
    print(LC + f"    h8mail -t {email}")
    print(LW + "\n  Avec cles API (cree un fichier config.ini) :")
    print(LC +  "    h8mail -t " + email + " -c config.ini\n")
    print(LW + "  Exemple config.ini :")
    print(DIM + "    [DEFAULT]\n"
                "    hunterio = <ta_cle>\n"
                "    leakcheck = <ta_cle>\n"
                "    snusbase = <ta_cle>")

    section("RESSOURCES H8MAIL", LR)
    for name, lnk in [
        ("GitHub",          "https://github.com/khast3x/h8mail"),
        ("PyPI",            "https://pypi.org/project/h8mail/"),
        ("Config examples", "https://github.com/khast3x/h8mail#config"),
    ]: link(name, lnk, LC)
    pause()


# ──────────────────────────────────────────────
#  SHERLOCK — username search sur 400+ sites
#  github.com/sherlock-project/sherlock
#  Le plus connu des username trackers
# ──────────────────────────────────────────────

def sherlock_tool():
    show_logo("user")
    print(LM + "  Sherlock — Username OSINT sur 400+ plateformes")
    print(LM + "  Le tracker de username le plus connu et maintenu")
    print(LM + "  github.com/sherlock-project/sherlock\n")

    username = input(LM + "  Username > ").strip()
    if not username: pause(); return

    # Tente d'utiliser sherlock si installé
    try:
        result = subprocess.run(
            ["sherlock", username, "--print-found"],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode == 0 and result.stdout.strip():
            section(f"SHERLOCK — {username}", LM)
            found_count = 0
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line: continue
                if "[+]" in line:
                    print(LG + f"  {line}"); found_count += 1
                elif "[-]" in line:
                    print(DIM + LW + f"  {line}")
                elif "[*]" in line or "[!" in line:
                    print(LY + f"  {line}")
                else:
                    print(LM + f"  {line}")
            print(LM + f"\n  Total trouve : {found_count} profils")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(LY + "  Sherlock n'est pas installe.")
        print(LY + "  Pour l'installer :\n")
        print(LW + "    pip install sherlock-project")
        print(LW + "    sherlock " + username + "\n")
        print(LM + "  En attendant, le tracker integre (55+ sites) :")
        print(LM + "  => Utilise l'option 26 du menu principal\n")

    section("INSTALLATION SHERLOCK", LM)
    print(LW + "  pip install sherlock-project\n")
    print(LW + "  Usages :")
    print(LC + f"    sherlock {username}                  # scan complet")
    print(LC + f"    sherlock {username} --print-found    # affiche seulement les trouves")
    print(LC + f"    sherlock {username} --timeout 5      # timeout par site")
    print(LC + f"    sherlock {username} --output out.txt # exporte les resultats\n")

    section("RESSOURCES SHERLOCK", LM)
    for name, lnk in [
        ("GitHub",     "https://github.com/sherlock-project/sherlock"),
        ("PyPI",       "https://pypi.org/project/sherlock-project/"),
        ("Sites list", "https://github.com/sherlock-project/sherlock/blob/master/sherlock_project/resources/data.json"),
    ]: link(name, lnk, LC)
    pause()


# ──────────────────────────────────────────────
#  THEHARVESTER — recon email/subdomain/IP
#  github.com/laramies/theHarvester
#  Outil de pentest classique, bien connu
# ──────────────────────────────────────────────

def theharvester_tool():
    show_logo("sub")
    print(LC + "  theHarvester — Email, Subdomain & IP Recon")
    print(LC + "  Sources : Google, Bing, LinkedIn, Shodan, crt.sh, etc.")
    print(LC + "  github.com/laramies/theHarvester\n")

    print(LC + "  1  Recon sur un domaine\n"
               "  2  Recon sur une organisation\n"
               "  3  Infos installation\n")
    c = input(LC + "  Choice > ").strip()

    if c == "3":
        section("INSTALLATION THEHARVESTER", LC)
        print(LW + "  Via pip :")
        print(LC + "    pip install theHarvester\n")
        print(LW + "  Via git (version la plus a jour) :")
        print(LC + "    git clone https://github.com/laramies/theHarvester")
        print(LC + "    cd theHarvester && pip install -r requirements/base.txt\n")
        print(LW + "  Usage basique :")
        print(LC + "    theHarvester -d example.com -b google")
        print(LC + "    theHarvester -d example.com -b all -l 500\n")
        print(LW + "  Sources dispo (free sans cle) :")
        print(LY + "    google, bing, duckduckgo, yahoo, crtsh, urlscan, dnsdumpster")
        print(LW + "  Sources avec cle :")
        print(LY + "    shodan, hunter, intelx, securityTrails, virustotal")
        section("RESSOURCES", LC)
        for name, lnk in [
            ("GitHub",     "https://github.com/laramies/theHarvester"),
            ("PyPI",       "https://pypi.org/project/theHarvester/"),
            ("Wiki usage", "https://github.com/laramies/theHarvester/wiki"),
        ]: link(name, lnk, LC)
        pause(); return

    if c in ["1", "2"]:
        prompt = "Domaine (ex: example.com) > " if c == "1" else "Organisation (ex: Google) > "
        target = input(LC + f"  {prompt}").strip()
        if not target: pause(); return

        sources = input(LC + "  Sources (ENTER = google,bing,crtsh) > ").strip()
        if not sources: sources = "google,bing,crtsh"

        limit = input(LC + "  Limite de resultats (ENTER = 200) > ").strip()
        if not limit: limit = "200"

        try:
            cmd = ["theHarvester", "-d", target, "-b", sources, "-l", limit]
            print(LY + f"\n  Lancement : {' '.join(cmd)}")
            print(LY + "  (Ctrl+C pour arreter)\n")
            result = subprocess.run(cmd, timeout=300, text=True)
        except FileNotFoundError:
            print(LY + "\n  theHarvester n'est pas installe.")
            print(LY + "  Install : pip install theHarvester\n")

            # Fallback : liens passifs
            e = qenc(target)
            section(f"RECON PASSIF — {target}", LC)
            for name, lnk in [
                ("crt.sh",        f"https://crt.sh/?q=%.{target}"),
                ("URLScan",       f"https://urlscan.io/search/#{e}"),
                ("DNSDumpster",   f"https://dnsdumpster.com/ (cherche: {target})"),
                ("Shodan domain", f"https://www.shodan.io/domain/{target}"),
                ("VirusTotal",    f"https://www.virustotal.com/gui/domain/{target}/relations"),
                ("SecurityTrails",f"https://securitytrails.com/domain/{target}/subdomains"),
                ("HunterIO",      f"https://hunter.io/domain-search/{target}"),
                ("Google emails", f"https://www.google.com/search?q=site:{target}+intext:@{target}"),
            ]: link(name, lnk, LC)
        except subprocess.TimeoutExpired:
            print(LY + "\n  Timeout (300s). Resultats partiels affiches.")
        except KeyboardInterrupt:
            print(LY + "\n  Interrompu.")

    section("RESSOURCES THEHARVESTER", LC)
    for name, lnk in [
        ("GitHub",     "https://github.com/laramies/theHarvester"),
        ("PyPI",       "https://pypi.org/project/theHarvester/"),
    ]: link(name, lnk, LC)
    pause()


# ──────────────────────────────────────────────
#  MAIGRET — username OSINT (fork Sherlock++)
#  github.com/soxoj/maigret
#  3000+ sites, profil complet, graphes
# ──────────────────────────────────────────────

def maigret_tool():
    show_logo("user")
    print(LM + "  Maigret — Username OSINT sur 3000+ sites")
    print(LM + "  Fork avance de Sherlock avec profils complets")
    print(LM + "  github.com/soxoj/maigret\n")

    username = input(LM + "  Username > ").strip()
    if not username: pause(); return

    try:
        cmd = ["maigret", username, "--print-found"]
        print(LY + f"  Lancement : {' '.join(cmd)}\n")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and result.stdout.strip():
            section(f"MAIGRET — {username}", LM)
            found = 0
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line: continue
                if "[+]" in line or "Found" in line:
                    print(LG + f"  {line}"); found += 1
                elif "[-]" in line or "Not Found" in line:
                    print(DIM + LW + f"  {line}")
                else:
                    print(LM + f"  {line}")
            print(LM + f"\n  Total : {found} profils trouves")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print(LY + "  Maigret n'est pas installe.")
        print(LY + "  Install :\n")
        print(LW + "    pip install maigret\n")
        print(LW + "  Usages :")
        print(LC + f"    maigret {username}                    # scan basique")
        print(LC + f"    maigret {username} --print-found      # seulement trouves")
        print(LC + f"    maigret {username} -P report/         # genere un rapport HTML")
        print(LC + f"    maigret {username} --timeout 5\n")

    section("RESSOURCES MAIGRET", LM)
    for name, lnk in [
        ("GitHub",          "https://github.com/soxoj/maigret"),
        ("PyPI",            "https://pypi.org/project/maigret/"),
        ("Sites supported", "https://github.com/soxoj/maigret/blob/main/sites.md"),
    ]: link(name, lnk, LC)
    pause()


# ──────────────────────────────────────────────
#  HUB OUTILS OPEN SOURCE
#  Centralise tous les outils open source
# ──────────────────────────────────────────────

def open_source_hub():
    show_logo("user")
    print(LG + "  Hub des outils Open Source OSINT les plus connus\n")
    print(LG + "  1  Holehe     — email sur 120+ sites (reset pwd)")
    print(LG + "  2  h8mail     — breach hunting email multi-sources")
    print(LG + "  3  Sherlock   — username sur 400+ plateformes")
    print(LG + "  4  theHarvester — recon email/subdomain/IP")
    print(LG + "  5  Maigret    — username sur 3000+ sites (fork Sherlock)")
    print(LG + "  6  Infos + install de tous les outils\n")
    c = input(LG + "  Choice > ").strip()
    if   c == "1": holehe_tool()
    elif c == "2": h8mail_tool()
    elif c == "3": sherlock_tool()
    elif c == "4": theharvester_tool()
    elif c == "5": maigret_tool()
    elif c == "6":
        section("INSTALL TOUS LES OUTILS EN UNE FOIS", LG)
        print(LW + "  Copie-colle dans ton terminal :\n")
        print(LC + "    pip install holehe h8mail sherlock-project maigret theHarvester\n")
        print(LW + "  Verification :")
        print(LC + "    holehe --version\n"
                   "    h8mail --version\n"
                   "    sherlock --version\n"
                   "    maigret --version\n"
                   "    theHarvester --version\n")
        section("LIENS GITHUB", LG)
        for name, lnk in [
            ("Holehe",       "https://github.com/megadose/holehe"),
            ("h8mail",       "https://github.com/khast3x/h8mail"),
            ("Sherlock",     "https://github.com/sherlock-project/sherlock"),
            ("theHarvester", "https://github.com/laramies/theHarvester"),
            ("Maigret",      "https://github.com/soxoj/maigret"),
            ("Awesome OSINT","https://github.com/jivoi/awesome-osint"),
        ]: link(name, lnk, LG)
        pause()


# ──────────────────────────────────────────────
#  WORMGPT — IA integree au multi-tool
#  Compatible OpenAI API format
#  Cle gratuite sur : https://chat.wrmgpt.com
# ──────────────────────────────────────────────

WRMGPT_BASE   = "https://api.wrmgpt.com/v1"
WORMGPT_MODEL = "gpt-3.5-turbo"

WORMGPT_SYSTEM = (
    "Tu es WormGPT, une IA integree dans un outil OSINT / pentest. "
    "Tu es directe, technique, et tu reponds en francais. "
    "Tu peux analyser des resultats OSINT, generer des dorks, "
    "analyser des breaches, expliquer des concepts reseau/cyber, "
    "et aider avec toutes les taches de l'outil. Sois concis et utile."
)

def wormgpt_tool():
    show_logo("hash")
    print(LR + "  WormGPT — IA integree au multi-tool")
    print(LR + "  Compatible OpenAI API  |  chat.wrmgpt.com\n")

    global WORMGPT_KEY
    key = WORMGPT_KEY.strip()

    if not key:
        print(LY + "  Aucune cle WormGPT trouvee dans config.ini")
        print(LY + "  1. Va sur https://chat.wrmgpt.com")
        print(LY + "  2. Cree un compte gratuit")
        print(LY + "  3. Dashboard > API Key > copie ta cle\n")
        key = input(LY + "  Entre ta cle WormGPT (ou ENTER pour annuler) > ").strip()
        if not key:
            pause(); return
        # Sauvegarde automatique SANS demander — plus jamais redemandee
        save_key("wormgpt_key", key)
        WORMGPT_KEY = key
        print(LG + "  [OK]  Cle sauvegardee dans config.ini — ne sera plus jamais redemandee.")

    print(LR + "\n  1  Chat libre avec WormGPT")
    print(LR + "  2  Analyser un email / username OSINT")
    print(LR + "  3  Analyser des resultats de breach")
    print(LR + "  4  Expliquer un concept cyber / reseau")
    print(LR + "  5  Analyser une IP / domaine")
    print(LR + "  6  Generer un rapport OSINT complet (.txt)\n")
    c = input(LR + "  Choice > ").strip()

    PRE_PROMPTS = {
        "2": ("Email / Username a analyser > ",
              "Analyse cet email ou username d'un point de vue OSINT. "
              "Donne des pistes de recherche, plateformes probables, "
              "methodes et ce qu'on peut trouver. Sois precis et structure : "),
        "3": ("Colle tes resultats de breach ici > ",
              "Analyse ces resultats de data breach. Resume les donnees exposees, "
              "evalue le niveau de risque (critique/haut/moyen/bas), et donne "
              "des conseils pratiques concrets : "),
        "4": ("Concept a expliquer > ",
              "Explique ce concept de cybersecurite ou de reseau de facon claire "
              "et technique, avec un exemple concret : "),
        "5": ("IP ou domaine > ",
              "Analyse cette IP ou ce domaine d'un point de vue OSINT/securite. "
              "Quoi chercher, quels outils utiliser, quels indicateurs surveiller, "
              "et quelles conclusions preliminaires tirer : "),
        "6": ("Sujet du rapport OSINT > ",
              "Genere un rapport OSINT complet et structure sur ce sujet. "
              "Inclus : resume executif, methodologie, sources recommandees, "
              "resultats attendus, et recommandations finales : "),
    }

    def call_wormgpt(messages):
        r = requests.post(
            f"{WRMGPT_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type":  "application/json",
            },
            json={
                "model":       WORMGPT_MODEL,
                "messages":    messages,
                "max_tokens":  1024,
                "temperature": 0.7,
            },
            timeout=30
        )
        return r

    def display_response(reply, tokens="?"):
        print()
        print(LR + "  WormGPT :")
        print()
        for line in reply.split("\n"):
            print(LW + f"  {line}")
        print()
        print(DIM + f"  [tokens: {tokens}]")
        print()

    def handle_error(r):
        if r.status_code == 401:
            print(LR + "  Cle API invalide ou expiree.")
            print(LY + "  Verifie ta cle sur https://chat.wrmgpt.com")
        elif r.status_code == 429:
            print(LY + "  Rate limit atteint. Attends un peu.")
        else:
            print(LR + f"  Erreur API: HTTP {r.status_code}")
            print(LY + f"  {r.text[:200]}")

    # Chat libre multi-tour
    if c == "1":
        section("WormGPT — CHAT LIBRE", LR)
        print(LR + "  Tape 'exit' pour quitter.\n")
        history = [{"role": "system", "content": WORMGPT_SYSTEM}]
        while True:
            try:
                user_input = input(LG + "  Toi > ").strip()
            except (EOFError, KeyboardInterrupt):
                print(); break
            if user_input.lower() in ["exit", "quit", "q", ""]:
                break
            history.append({"role": "user", "content": user_input})
            spinner("WormGPT reflechit...", 1.2, LR)
            try:
                r = call_wormgpt(history)
                if r.status_code == 200:
                    data  = r.json()
                    reply = data["choices"][0]["message"]["content"].strip()
                    tokens = data.get("usage", {}).get("total_tokens", "?")
                    history.append({"role": "assistant", "content": reply})
                    display_response(reply, tokens)
                else:
                    handle_error(r); break
            except requests.exceptions.ConnectionError:
                print(LR + "  Connexion impossible a api.wrmgpt.com")
                print(LY + "  Verifie ta connexion internet."); break
            except Exception as ex:
                print(LR + f"  Erreur: {ex}"); break

    # Modes pre-configures
    elif c in PRE_PROMPTS:
        label, inject = PRE_PROMPTS[c]
        user_input = input(LR + f"  {label}").strip()
        if not user_input: pause(); return
        spinner("WormGPT analyse...", 1.5, LR)
        try:
            r = call_wormgpt([
                {"role": "system", "content": WORMGPT_SYSTEM},
                {"role": "user",   "content": inject + user_input},
            ])
            if r.status_code == 200:
                data   = r.json()
                reply  = data["choices"][0]["message"]["content"].strip()
                tokens = data.get("usage", {}).get("total_tokens", "?")
                mode_labels = {
                    "2":"ANALYSE OSINT","3":"ANALYSE BREACH",
                    "4":"EXPLICATION CYBER","5":"ANALYSE IP/DOMAINE",
                    "6":"RAPPORT OSINT",
                }
                section(f"WormGPT — {mode_labels.get(c,'REPONSE')}", LR)
                display_response(reply, tokens)
                try:
                    sv = input(LY + "  Sauvegarder en .txt? [y/N] > ").strip().lower()
                    if sv == "y":
                        fname = f"wormgpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        with open(fname, "w", encoding="utf-8") as f:
                            f.write(f"WormGPT — {mode_labels.get(c,'REPONSE')}\n")
                            f.write(f"Date: {datetime.now()}\nInput: {user_input}\n")
                            f.write("="*60 + "\n\n" + reply + "\n")
                        print(LG + f"  Sauvegarde: {fname}")
                except Exception: pass
            else:
                handle_error(r)
        except requests.exceptions.ConnectionError:
            print(LR + "  Connexion impossible a api.wrmgpt.com")
        except Exception as ex:
            print(LR + f"  Erreur: {ex}")
    else:
        print(LR + "  Option invalide.")

    print()
    print(LC + "  WormGPT : https://chat.wrmgpt.com")
    print(LC + "  Cle configurable via option 98 (Gestionnaire cles API)")
    pause()


# ──────────────────────────────────────────────
#  GESTIONNAIRE DE CLES API
#  Option 98 — gere config.ini automatiquement
# ──────────────────────────────────────────────

def api_key_manager():
    global LEAKCHECK_KEY, BREACHDIR_KEY, SHODAN_KEY, HUNTER_KEY, VIRUSTOTAL_KEY, WORMGPT_KEY
    show_logo("hash")
    print(LG + "  Gestionnaire de cles API — config.ini\n")
    print(LG + f"  Fichier config : {CONFIG_FILE}\n")

    # Statut actuel des clés
    keys_status = [
        ("LeakCheck",       "leakcheck_key",       LEAKCHECK_KEY,  "https://leakcheck.io"),
        ("BreachDirectory", "breachdirectory_key",  BREACHDIR_KEY,  "https://rapidapi.com/rohan-patra/api/breachdirectory"),
        ("Shodan",          "shodan_key",            SHODAN_KEY,     "https://account.shodan.io/register"),
        ("Hunter.io",       "hunter_key",            HUNTER_KEY,     "https://hunter.io/users/sign_up"),
        ("VirusTotal",      "virustotal_key",        VIRUSTOTAL_KEY, "https://www.virustotal.com/gui/join-us"),
        ("WormGPT",         "wormgpt_key",           WORMGPT_KEY,    "https://chat.wrmgpt.com"),
    ]

    section("STATUT DES CLES API", LG)
    print(LG + f"  {'SERVICE':<20} {'STATUT':<15} {'INSCRIPTION (GRATUITE)'}")
    print(LG + "  " + "-"*70)
    for name, cfg_name, val, url in keys_status:
        if val:
            masked = val[:4] + "*" * (len(val) - 8) + val[-4:] if len(val) > 8 else "****"
            print(LG + f"  {name:<20} " + LG + f"[OK] {masked:<10} " + DIM + url)
        else:
            print(LY + f"  {name:<20} " + LR + f"[MANQUANTE]      " + DIM + url)

    print()
    print(LW + "  1  Ajouter / modifier une cle")
    print(LW + "  2  Voir le fichier config complet")
    print(LW + "  3  Reinitialiser la config")
    print(LW + "  4  Ouvrir le dossier config")
    print(LW + "  5  Guide d'obtention des cles\n")
    c = input(LG + "  Choice > ").strip()

    if c == "1":
        section("MODIFICATION DE CLE", LG)
        for i, (name, cfg_name, val, url) in enumerate(keys_status, 1):
            status = LG+"[OK]" if val else LR+"[VIDE]"
            print(f"  {i}  {name:<20} {status}")
        print()
        try:
            idx = int(input(LG + "  Choisis le service (numero) > ").strip()) - 1
            if not 0 <= idx < len(keys_status):
                print(LR + "  Numero invalide."); pause(); return
            name, cfg_name, old_val, url = keys_status[idx]
            print(LY + f"\n  Service  : {name}")
            print(LY + f"  Lien     : {url}")
            if old_val:
                print(LY + f"  Cle actuelle : {old_val[:4]}...{old_val[-4:]}")
            new_key = input(LG + f"\n  Nouvelle cle {name} > ").strip()
            if not new_key:
                print(LY + "  Aucune modification."); pause(); return
            save_key(cfg_name, new_key)
            # Mise a jour en memoire — active immediatement
            if   cfg_name == "leakcheck_key":       LEAKCHECK_KEY  = new_key
            elif cfg_name == "breachdirectory_key": BREACHDIR_KEY  = new_key
            elif cfg_name == "shodan_key":           SHODAN_KEY     = new_key
            elif cfg_name == "hunter_key":           HUNTER_KEY     = new_key
            elif cfg_name == "virustotal_key":       VIRUSTOTAL_KEY = new_key
            elif cfg_name == "wormgpt_key":          WORMGPT_KEY    = new_key
            print(LG + f"\n  [OK]  Cle {name} sauvegardee dans config.ini")
            print(LG + f"  [OK]  Active immediatement — ne sera plus jamais redemandee")
        except (ValueError, IndexError):
            print(LR + "  Entree invalide.")

    elif c == "2":
        section("CONTENU DU FICHIER CONFIG", LG)
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    # Masquer les vraies clés à l'affichage
                    if "=" in line and not line.strip().startswith("#"):
                        k, _, v = line.partition("=")
                        v = v.strip()
                        if v and len(v) > 8:
                            v_display = v[:4] + "****" + v[-4:]
                        elif v:
                            v_display = "****"
                        else:
                            v_display = "(vide)"
                        print(LC + f"  {k.strip():<25} = {v_display}")
                    else:
                        print(DIM + LW + f"  {line.rstrip()}")
        except Exception as ex:
            print(LR + f"  Erreur lecture: {ex}")

    elif c == "3":
        confirm = input(LR + "  Reinitialiser config.ini? Toutes les cles seront effacees. [oui/non] > ").strip().lower()
        if confirm == "oui":
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(CONFIG_TEMPLATE)
            LEAKCHECK_KEY = BREACHDIR_KEY = SHODAN_KEY = HUNTER_KEY = VIRUSTOTAL_KEY = WORMGPT_KEY = ""
            print(LG + "  [OK]  Config reinitialise.")
        else:
            print(LY + "  Annule.")

    elif c == "4":
        folder = os.path.dirname(CONFIG_FILE)
        print(LG + f"\n  Dossier config : {folder}")
        print(LG + f"  Fichier        : {CONFIG_FILE}")
        try:
            if sys.platform == "win32":
                os.startfile(folder)
            elif IS_TERMUX:
                subprocess.run(["termux-open", folder], timeout=5)
            else:
                subprocess.run(["xdg-open", folder], timeout=5)
        except Exception:
            print(LY + "  Ouvre manuellement le fichier ci-dessus.")

    elif c == "5":
        section("GUIDE D'OBTENTION DES CLES GRATUITES", LG)
        guides = [
            ("LeakCheck",       "https://leakcheck.io",
             "1. Va sur leakcheck.io\n"
             "  2. Clique Sign Up (email suffit)\n"
             "  3. Verifie ton email\n"
             "  4. Dashboard > API > copie ta cle\n"
             "  => Free : 50 req/mois, 7.5B records"),
            ("BreachDirectory", "https://rapidapi.com/rohan-patra/api/breachdirectory",
             "1. Va sur rapidapi.com, cree un compte\n"
             "  2. Cherche 'breachdirectory'\n"
             "  3. Clique Subscribe > plan Basic (gratuit)\n"
             "  4. Ta cle est dans 'X-RapidAPI-Key'\n"
             "  => Free : 50 req/mois"),
            ("Shodan",          "https://account.shodan.io/register",
             "1. Cree un compte sur shodan.io\n"
             "  2. Mon compte > API Key\n"
             "  => Free : scan 1 IP, recherches limitees"),
            ("Hunter.io",       "https://hunter.io/users/sign_up",
             "1. Cree un compte sur hunter.io\n"
             "  2. Dashboard > API\n"
             "  => Free : 25 req/mois, recherche email"),
            ("VirusTotal",      "https://www.virustotal.com/gui/join-us",
             "1. Cree un compte sur virustotal.com\n"
             "  2. Profil > API Key\n"
             "  => Free : 500 req/jour, 4 req/min"),
            ("WormGPT",         "https://chat.wrmgpt.com",
             "1. Va sur chat.wrmgpt.com\n"
             "  2. Cree un compte gratuit\n"
             "  3. Dashboard > API Key > copie ta cle\n"
             "  => Cle sauvegardee automatiquement des la 1ere utilisation"),
        ]
        for name, url, guide in guides:
            print(LG + f"\n  [{name}]")
            print(LC + f"  URL : {url}")
            print(LW + f"  {guide}\n")
            print(LG + "  " + "-"*50)

    pause()


MENU = """
  +---------------------------------+  +---------------------------------+  +---------------------------------+
  |        NETWORK / IP             |  |        WEB / DOMAIN             |  |    PHONE / MAIL / BREACH        |
  +---------------------------------+  +---------------------------------+  +---------------------------------+
  | (1)  IP Info & Tracker          |  | (11) HTTP Header Inspector      |  | (21) Phone Number Info          |
  | (2)  DNS Lookup                 |  | (12) SSL Certificate Inspector  |  | (22) Phone Social Scanner       |
  | (3)  Port Scanner               |  | (13) Tech Detector              |  | (23) Mail / Email OSINT         |
  | (4)  Geo IP Tracker             |  | (14) URL Redirect Tracer        |  | (24) Email Account Checker      |
  | (5)  Network Info               |  | (15) Robots / Sitemap Reader    |  | (25) Breach Search Engine       |
  | (6)  WHOIS / Reverse DNS        |  | (16) Wayback Machine            |  | (26) Username Tracker [55+]     |
  | (7)  Subdomain Finder           |  | (17) Wayback URL Extractor      |  | (27) Profile Builder            |
  | (8)  ASN / BGP Lookup           |  | (18) Google Dork Generator      |  | (28) Reverse Image Search       |
  | (9)  Quick Recon (all-in-one)   |  | (19) Advanced Dork Builder      |  | (29) Social Media Search        |
  | (10) IP Range Scanner           |  | (20) File / Doc OSINT           |  | (30) Public Records Search      |
  +---------------------------------+  +---------------------------------+  | (31) Paste Search               |
                                                                            | (32) Public Camera Feeds        |
  +---------------------------------+  +---------------------------------+  +---------------------------------+
  |    OUTILS RESEAU / AVANCES      |  |    PENTEST / VULN / SCAN        |
  +---------------------------------+  +---------------------------------+  +---------------------------------+
  | (40) Traceroute (pure Python)   |  | (50) Web Vuln Scanner           |  |    PASSWORD / HASH / TOOLS      |
  | (41) Banner Grabber             |  | (51) Firewall / WAF Detector    |  +---------------------------------+
  | (42) MAC Vendor Lookup          |  | (52) WiFi Scanner               |  | (60) Password Generator/Tester  |
  | (43) HTTP Method Tester         |  | (53) File Scanner (AV basic)    |  | (61) Hash Tools                 |
  | (44) CORS Checker               |  | (54) OSINT Dork Builder         |  | (62) Metadata Extractor         |
  | (45) Tor Exit Node Check        |  | (55) CORS Checker               |  | (63) Shodan / Censys Links      |
  | (46) DNS Brute Force (ext.)     |  | (56) HTTP Method Tester         |  | (64) CVE / Vuln Search          |
  | (47) Dark Web Search Links      |  +---------------------------------+  | (65) Archive Links              |
  | (48) Dark Web Search            |                                        | (66) OSINT Framework Navigator  |
  | (49) ASN / BGP Lookup           |  +---------------------------------+  | (67) URL Redirect Tracer        |
  +---------------------------------+  |  APIS BREACH AVEC CLE (GRATUIT) |  | (68) Dark Web Search            |
                                       +---------------------------------+  | (69) XposedOrNot API [DIRECT]   |
  +---------------------------------+  | (70) LeakCheck API [7.5B+]      |  +---------------------------------+
  |  OUTILS OPEN SOURCE RECONNUS   |  | (71) BreachDirectory API        |
  +---------------------------------+  +---------------------------------+  (0) Exit    (99) Contact
  | (80) Hub Outils Open Source     |
  | (81) Holehe  (email 120+ sites) |  +---------------------------------+
  | (82) h8mail  (breach hunting)   |  |      IA INTEGREE                |
  | (83) Sherlock (user 400+ sites) |  +---------------------------------+
  | (84) theHarvester (recon dom.)  |  | (90) WormGPT  [chat.wrmgpt.com] |
  | (85) Maigret (user 3000+ sites) |  |      Chat / OSINT / Dorks /     |
  +---------------------------------+  |      Breach / Rapports          |
                                       +---------------------------------+

  (98) Gestionnaire cles API [config.ini]
"""

DISPATCH = {
    "1":  ip_info,
    "2":  dns_lookup,
    "3":  port_scanner,
    "4":  geo_ip,
    "5":  network_info,
    "6":  whois_reverse,
    "7":  subdomain_finder,
    "8":  asn_lookup,
    "9":  quick_recon,
    "10": ip_info,   # IP range — inside ip_info option 4
    "11": header_inspector,
    "12": ssl_inspector,
    "13": tech_detector,
    "14": url_tracer,
    "15": robots_sitemap,
    "16": wayback,
    "17": wayback_urls,
    "18": dork_gen,
    "19": adv_dork,
    "20": file_osint,
    "21": phone_info,
    "22": phone_social_scanner,
    "23": mail_osint,
    "24": email_account_checker,
    "25": breach_engine,
    "26": username_tracker,
    "27": profile_builder,
    "28": reverse_image,
    "29": social_search,
    "30": public_records,
    "31": paste_search,
    "32": public_cameras,
    "35": file_osint,
    # Nouveaux outils reseau
    "40": traceroute,
    "41": banner_grab,
    "42": mac_lookup,
    "43": http_method_tester,
    "44": cors_checker,
    "45": tor_check,
    "46": subdomain_finder,  # brute force étendu
    "47": darkweb_search,
    "48": darkweb_search,
    "49": asn_lookup,
    # Pentest
    "50": web_vuln_scanner,
    "51": firewall_detector,
    "52": wifi_scanner,
    "53": file_scanner,
    "54": osint_dork_builder,
    "55": cors_checker,
    "56": http_method_tester,
    # Password / hash
    "60": password_tools,
    "61": hash_tools,
    "62": metadata_extractor,
    "63": shodan_links,
    "64": vuln_search,
    "65": archive_links,
    "66": osint_framework,
    "67": url_tracer,
    "68": darkweb_search,
    "69": xposedornot,
    # APIs breach avec clé gratuite
    "70": leakcheck_api,
    "71": breachdirectory_api,
    # Outils open source
    "80": open_source_hub,
    "81": holehe_tool,
    "82": h8mail_tool,
    "83": sherlock_tool,
    "84": theharvester_tool,
    "85": maigret_tool,
    "90": wormgpt_tool,
    "98": api_key_manager,
    "99": contact,
}

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    intro()
    while True:
        clear()
        banner()
        print(LG + MENU)
        choice = input(LG + "  Select module > ").strip()
        if choice in ["0","00"]:
            clear()
            for line in CAMZZZ_LINES: rainbow("  " + line)
            print()
            print(LG + "  Goodbye -- By camzzz")
            time.sleep(0.8); break
        fn = DISPATCH.get(choice)
        if fn:
            fn()
        else:
            print(LR + "  Invalid option."); time.sleep(0.6)
