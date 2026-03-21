# 🔍 Multi Tool V5 — By camzzz

> https://github.com/cameleonnbss
> 
<img width="1101" height="1322" alt="image" src="https://github.com/user-attachments/assets/978675ca-b948-4fdc-acb8-98602a37604a" />


# camzzz multi-tool V5

```
==================================================================================================
/*  _____                                                      _____  */
/* ( ___ )                                                    ( ___ ) */
/*  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |  */
/*  |   |   _________ _____ ___  ____________                  |   |  */
/*  |   |  / ___/ __ `/ __ `__ \/_  /_  /_  /                  |   |  */
/*  |   | / /__/ /_/ / / / / / / / /_/ /_/ /_                  |   |  */
/*  |   | \___/\__,_/_/ /_/ /_/_/___/___/___/_              __ |   |  */
/*  |   |    ____ ___  __  __/ / /_(_)     / /_____  ____  / / |   |  */
/*  |   |   / __ `__ \/ / / / / __/ /_____/ __/ __ \/ __ \/ /  |   |  */
/*  |   |  / / / / / / /_/ / / /_/ /_____/ /_/ /_/ / /_/ / /   |   |  */
/*  |   | /_/ /_/ /_/\__,_/_/\__/_/      \__/\____/\____/_/    |   |  */
/*  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|  */
/* (_____)                                                    (_____) */

  C A M Z Z Z   M U L T I - T O O L  ·  V 5  ·  5 0 +  M O D U L E S
==================================================================================================
```

> **OSINT / Network / Phone / Mail / Breach / Pentest — 53 modules**
> By camzzz — Discord: `cameleonmortis` — GitHub: https://github.com/cameleonnbss/50-multi-tool

---

## 🇬🇧 English

### What is this?
camzzz multi-tool is a terminal-based OSINT and network reconnaissance toolkit written in Python.
It includes 53 modules covering IP analysis, phone number intelligence, email OSINT,
data breach search, username tracking, web vulnerability scanning, WiFi scanning, and much more.

**For educational and authorized security research purposes only.**
**Do NOT use on systems or people without explicit authorization.**
**The author is not responsible for any misuse.**

### 🪟 Install on Windows

**1 — Install Python (if not already installed)**
Download Python 3.10+ from https://www.python.org/downloads/windows/
Make sure to check **"Add Python to PATH"** during installation.

**2 — Download the tool**
```bat
git clone https://github.com/cameleonnbss/50-multi-tool
cd 50-multi-tool
```
Or download the ZIP directly from GitHub and extract it.

**3 — Install dependencies**
Open **Command Prompt** or **PowerShell** and run:
```bat
pip install -r requirements.txt
```

**4 — Run**
```bat
python3 multi-tool+osint-osint_tools_v5.py
```

> **Tip for Windows:** Run CMD or PowerShell as Administrator if you have permission issues.
> If `python` is not recognized, try `py multitool_v5.py` instead.

---

### 🐧 Install on Linux

**1 — Install Python and pip (if not already installed)**
```bash
# Debian / Ubuntu / Kali
sudo apt update && sudo apt install python3 python3-pip git -y

# Arch / Manjaro
sudo pacman -S python python-pip git

# Fedora / CentOS
sudo dnf install python3 python3-pip git -y
```

**2 — Clone the repository**
```bash
git clone https://github.com/cameleonnbss/50-multi-tool
cd 50-multi-tool
```

**3 — Install dependencies**
```bash
pip install -r requirements.txt
# or if pip is not in PATH:
pip3 install -r requirements.txt
```

**4 — Run**
```bash
python3 multitool_v5.py
```

> **Optional:** Install extra dependencies for more features:
> ```bash
> pip3 install beautifulsoup4 pefile python-magic
> ```

---

---

## 🇫🇷 Français

### C'est quoi ?
camzzz multi-tool est un outil OSINT et reconnaissance réseau en terminal, écrit en Python.
Il contient 53 modules : analyse IP, intelligence téléphonique, OSINT email,
recherche dans les fuites de données, tracking de usernames, scan de vulnérabilités web, WiFi, et plus.

**Uniquement pour des usages éducatifs et de recherche en sécurité autorisée.**
**N'utilise pas cet outil sur des systèmes ou des personnes sans autorisation explicite.**
**L'auteur décline toute responsabilité en cas de mauvaise utilisation.**

### 🪟 Installation sur Windows

**1 — Installer Python (si pas déjà installé)**
Télécharge Python 3.10+ sur https://www.python.org/downloads/windows/
Coche bien **"Add Python to PATH"** pendant l'installation.

**2 — Télécharger l'outil**
```bat
git clone https://github.com/cameleonnbss/50-multi-tool
cd 50-multi-tool
```
Ou télécharge le ZIP directement depuis GitHub et extrais-le.

**3 — Installer les dépendances**
Ouvre **l'Invite de commandes** ou **PowerShell** et tape :
```bat
pip install -r requirements.txt
```

**4 — Lancer**
```bat
python multitool_v5.py
```

> **Conseil Windows :** Lance CMD ou PowerShell en tant qu'Administrateur si tu as des erreurs de permission.
> Si `python` n'est pas reconnu, essaie `py multitool_v5.py`.

---

### 🐧 Installation sur Linux

**1 — Installer Python et pip (si pas déjà installé)**
```bash
# Debian / Ubuntu / Kali
sudo apt update && sudo apt install python3 python3-pip git -y

# Arch / Manjaro
sudo pacman -S python python-pip git

# Fedora / CentOS
sudo dnf install python3 python3-pip git -y
```

**2 — Cloner le dépôt**
```bash
git clone https://github.com/cameleonnbss/50-multi-tool
cd 50-multi-tool
```

**3 — Installer les dépendances**
```bash
pip install -r requirements.txt
# ou si pip n'est pas dans le PATH :
pip3 install -r requirements.txt
```

**4 — Lancer**
```bash
python3 multitool_v5.py
```

> **Optionnel :** Installe les dépendances supplémentaires pour plus de fonctionnalités :
> ```bash
> pip3 install beautifulsoup4 pefile python-magic
> ```

---

---

## 🗂️ Modules (53 total)

### 🌐 Network / IP (1–10)
| # | Module | Description |
|---|--------|-------------|
| 1 | IP Info & Tracker | Own IP / any IP / reputation / /24 range scanner |
| 2 | DNS Lookup | A, MX, NS, TXT, AAAA, CAA, SOA, CNAME |
| 3 | Port Scanner | Common / 1-1024 / custom range, multithreaded |
| 4 | Geo IP Tracker | Country, city, ISP, ASN, Google Maps |
| 5 | Network Info | Local machine + public IP + ISP |
| 6 | WHOIS / Reverse DNS | Domain WHOIS + IP reverse lookup |
| 7 | Subdomain Finder | 80+ wordlist, multithreaded |
| 8 | ASN / BGP Lookup | Prefix info via BGPView |
| 9 | Quick Recon | All-in-one domain scan |
| 10 | IP Range Scanner | Full /24 subnet for live hosts |

### 🌍 Web / Domain (11–20)
| # | Module | Description |
|---|--------|-------------|
| 11 | HTTP Header Inspector | Full headers + security audit |
| 12 | SSL Certificate Inspector | Subject, issuer, SANs, expiry |
| 13 | Tech Detector | 30+ CMS / framework detection |
| 14 | URL Redirect Tracer | Full redirect chain |
| 15 | Robots / Sitemap Reader | robots.txt + sitemap.xml |
| 16 | Wayback Machine | Latest snapshot info |
| 17 | Wayback URL Extractor | 100 historical URLs via CDX API |
| 18 | Google Dork Generator | 18 pre-built dorks for a domain |
| 19 | OSINT Dork Builder | Custom dorks by name/email/phone/domain/company |
| 20 | File / Doc OSINT | PDF, DOC, XLS, ENV, SQL, BAK, ZIP… |

### 📱 Phone / Mail / Breach (21–32)
| # | Module | Description |
|---|--------|-------------|
| 21 | Phone Number Info | 70+ countries, FR line type, validity, 14 OSINT links |
| 22 | Phone Social Scanner | 30+ links — WhatsApp, Telegram, TrueCaller, social, leaks |
| 23 | Mail / Email OSINT | Analysis, DNS, format guesser, header analyser, disposable |
| 24 | Email Account Checker | Tests 20 platforms for existing account |
| 25 | Breach Search Engine | ZSearcher.fr / OathNet.org / HIBP / 20 breach DBs |
| 26 | Username Tracker | 55 platforms, multithreaded |
| 27 | ID / Username Tracker Ext | 65+ platforms incl. Xbox, PlayStation, Fortnite |
| 28 | Profile Builder | Name + username + email search links |
| 29 | Reverse Image Search | Google, Bing, Yandex, TinEye, SauceNAO |
| 30 | Social Media Search | 12 platforms |
| 31 | Public Records Search | 10 people-finder services |
| 32 | Paste Search | Pastebin, Gist, Grep.app, Psbdmp, GitHub |

### 🔬 Intel / Advanced (33–42)
| # | Module | Description |
|---|--------|-------------|
| 33 | Shodan / Censys Links | Shodan, Censys, ZoomEye, Greynoise, OTX, FOFA |
| 34 | CVE / Vuln Search | NVD, Exploit-DB, Snyk, GitHub Advisories |
| 35 | Archive & Screenshot Links | Wayback, Archive.ph, screenshot services |
| 36 | OSINT Framework Navigator | 20 key OSINT resources |
| 37 | Dark Web Search Links | Ahmia, DarkSearch, clearnet indexes |
| 38 | Public Camera Feeds | Shodan dorks + Google dorks + directories |

### 🛡️ Pentest / Vuln / Scan (43–47)
| # | Module | Description |
|---|--------|-------------|
| 43 | Web Vuln Scanner | 20 passive checks: headers, sensitive files, tech, dirs |
| 44 | Firewall / WAF Detector | 14 WAFs, CDN, bot protection, SSL, score /100 |
| 45 | WiFi Scanner | Nearby networks, security analysis (Win/Linux/macOS) |
| 46 | File Scanner | Static AV: hashes, suspicious strings, entropy, VT link |
| 47 | HTTP Stress Tester | Load test for YOUR OWN servers only |

### 🔐 Password / Hash (50–53)
| # | Module | Description |
|---|--------|-------------|
| 50 | Password Generator / Tester | Generate + strength test + HIBP k-anonymity |
| 51 | Hash Tools | MD5/SHA1/SHA256/SHA512/Base64/Hex + crack links |
| 52 | Metadata Extractor | EXIF + GPS from images |
| 53 | File Scanner | (alias 46) |

### 🎭 Extra
| # | Module |
|---|--------|
| 48 | Contact (camzzz) |
| 49 | fsociety logo + matrix rain |

---

## 🔑 Breach Search Engines

| Service | URL | Scope |
|---------|-----|-------|
| **ZSearcher.fr** | https://zsearcher.fr/ | French specialised |
| **OathNet.org** | https://oathnet.org/ | International |
| **HaveIBeenPwned** | https://haveibeenpwned.com/ | Email / k-anonymity |
| DeHashed | https://dehashed.com/ | International |
| IntelX | https://intelx.io/ | International |
| LeakCheck | https://leakcheck.io/ | International |
| BreachDirectory | https://breachdirectory.org/ | International |
| Snusbase | https://snusbase.com/ | International |
| + 12 more | — | See module 25 |

> HIBP password check uses **k-anonymity** — only 5 chars of SHA1 sent. Password never leaves your machine.
>
> soon gonna add an uncensored ai 

---

## 👨‍💻 Author / Auteur

**camzzz**
- Discord: `cameleonmortis`
- GitHub: https://github.com/cameleonnbss/50-multi-tool
