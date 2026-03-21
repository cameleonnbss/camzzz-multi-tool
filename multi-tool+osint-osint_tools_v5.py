#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════╗
#   CAMZZZ MULTI-TOOL V5  —  By camzzz
#   50+ OSINT / Network / Phone / Mail / Breach tools
#   https://github.com/cameleonnbss/50-multi-tool
# ╚══════════════════════════════════════════════════════╝

import os, sys, platform, socket, requests, concurrent.futures
import ssl, re, hashlib, base64, time, random, string, urllib.parse
from datetime import datetime
from colorama import Fore, Style, init

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    PIL_OK = True
except ImportError:
    PIL_OK = False

init(autoreset=True)
SYS = platform.system().lower()

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

def clear(): os.system("cls" if SYS=="windows" else "clear")

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
    frames=["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    end=time.time()+dur; i=0
    while time.time()<end:
        sys.stdout.write(col+f"\r  {frames[i%8]}  {label}   ")
        sys.stdout.flush(); time.sleep(0.07); i+=1
    sys.stdout.write("\r"+" "*72+"\r"); sys.stdout.flush()

def bar(label, steps=30, delay=0.022, col=LG, bc=G):
    for i in range(steps+1):
        f="█"*i+"░"*(steps-i); pct=int(i/steps*100)
        sys.stdout.write(col+f"\r  {label}  "+bc+f"[{f}]"+LW+f" {pct:3d}%")
        sys.stdout.flush(); time.sleep(delay)
    print()

def glitch(text, rounds=4, col=LG):
    noise="@#$%&?!*~^<>|"
    for _ in range(rounds):
        g="".join(random.choice(noise) if random.random()<0.25 else ch for ch in text)
        sys.stdout.write("\r"+col+g); sys.stdout.flush(); time.sleep(0.06)
    sys.stdout.write("\r"+col+text+"\n"); sys.stdout.flush()

def matrix_rain(lines=8, width=70):
    jp="アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ"
    chars=jp+"01@#$%^&*<>!?"
    cols=[G,LG,C,LC,LM,LY,Y]
    for _ in range(lines):
        line="".join(random.choice(chars) if random.random()>0.62 else " " for _ in range(width))
        print(random.choice(cols)+"  "+line); time.sleep(0.03)

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
#  ASCII ART
# ──────────────────────────────────────────────

CAMZZZ_LINES = [
    "                                                                                             l)L    t)   ##      t)                   l)L  ",
    "                                                                                   l)  t)tTTT       t)tTTT                  l)  ",
    "  c)CCCC a)AAAA   m)MM MMM  z)ZZZZZ z)ZZZZZ     m)MM MMM  u)   UU  l)    t)   i)      t)    o)OOO   o)OOO   l)  ",
    " c)       a)AAA  m)  MM  MM     z)      z)     m)  MM  MM u)   UU  l)    t)   i)      t)   o)   OO o)   OO  l)  ",
    " c)      a)   A  m)  MM  MM   z)      z)       m)  MM  MM u)   UU  l)    t)   i)      t)   o)   OO o)   OO  l)  ",
    "  c)CCCC  a)AAAA m)      MM z)ZZZZZ z)ZZZZZ    m)      MM  u)UUU  l)LL   t)T  i)      t)T   o)OOO   o)OOO  l)LL ",
]

BANNER = r"""
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
==================================================================================================

      C A M Z Z Z   M U L T I - T O O L  ·  V 5  ·  5 0 +  M O D U L E S
      github.com/cameleonnbss/50-multi-tool  ·  By camzzz"""

SKULL = r"""
  __________________________________________________________________________

                           __xxxxxxxxxxxxxxxx___.
                      _gxXXXXXXXXXXXXXXXXXXXXXXXX!x_
                 __x!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!x_
              ,gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx_
            ,gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!_
          _!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!.
        gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXs
      ,!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!.
     g!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
    iXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
   ,XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
   !XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
   XXXXXXXXXXXXXXXXXXXf~~~VXXXXXXXXXXXXXXXXXXXXXXXXXvvvvvvvvXXXXXXXXXXXXXX!
   !XXXXXXXXXXXXXXXf         XXXXXXXXXXXXXXXXXXXXXf            XXXXXXXXXXP
    vXXXXXXXXXXXX!            !XXXXXXXXXXXXXXXXXX!              !XXXXXXXXX
     XXXXXXXXXXv               VXXXXXXXXXXXXXXX                !XXXXXXXX!
     !XXXXXXXXX.                YXXXXXXXXXXXXX!                XXXXXXXXX
      XXXXXXXXX!               ,XXXXXXXXXXXXXX                VXXXXXXX!
      XXXXXXXX!               ,!XXXX  XXXXXXX               iXXXXXX~
       XXXXXXXX               XXXXXX   XXXXXXXX!             xXXXXXX!
        !XXXXXXX!xxxxxxs_____xXXXXXXX   YXXXXXX!          ,xXXXXXXXX
         YXXXXXXXXXXXXXXXXXXXXXXXXXXX    VXXXXXXX!s. __gxx!XXXXXXXXXP
          XXXXXXXXXXXXXXXXXXXXXXXXXX!    XXXXXXXXXXXXXXXXXXXXXXXXX!
          XXXXXXXXXXXXXXXXXXXXXXXXXP      YXXXXXXXXXXXXXXXXXXXXXXX!
          XXXXXXXXXXXXXXXXXXXXXXXX!   i    XXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXX!   XX   XXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXXx_ iXX_,_dXXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXP
          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
           ~vXvvvvXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                    VXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXvvvvvv~
                      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~
                  _    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXv
                 -XX!  XXXXXXX~XXXXXXXXXXXXXXXXXXXXXX~   Xxi
                  YXX    XXXXX XXXXXXXXXXXXXXXXXXXX       iXX
                  !XX!   !XXX  XXXXXXXXXXXXXXXXXXXX      !XX
                  !XXX    ~Vf  YXXXXXXXXXXXXXP YXXX     !XXX
                  !XXX         !XXP YXXXfXXXX!  XXX     XXXV
                  !XXX !XX           XXP  YXX!       ,.!XXX!
                  !XXXi!XP  XX.                  ,_  !XXXXXX!
                  iXXXx X!  XX! !Xx.  ,.     xs.,XXi !XXXXXXf
                   XXXXXXXXXXXXXXXXX! _!XXx  dXXXXXXX.iXXXXXX
                   VXXXXXXXXXXXXXXXXXXXXXXXxxXXXXXXXXXXXXXXX!
                   YXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXV
                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                       VXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                         VXXXXXXXXXXXXXXXXXXXXXXXXXXXXv
                          ~vXXXXXXXXXXXXXXXXXXXXXXXf
                              ~vXXXXXXXXXXXXXXXXv~
                                 ~VvXXXXXXXV~~"""

BOOT_FRAMES = [
"  ╔══════════════════════════════════════╗\n  ║  [          ]  BOOTING...           ║\n  ╚══════════════════════════════════════╝",
"  ╔══════════════════════════════════════╗\n  ║  [████      ]  LOADING MODULES...   ║\n  ╚══════════════════════════════════════╝",
"  ╔══════════════════════════════════════╗\n  ║  [████████  ]  NETWORK READY...     ║\n  ╚══════════════════════════════════════╝",
"  ╔══════════════════════════════════════╗\n  ║  [██████████]  ACCESS GRANTED ✓     ║\n  ║               Welcome, camzzz       ║\n  ╚══════════════════════════════════════╝",
]

# per-module logos (colour, art)
LOGOS = {
"ip": (LG, r"""
  ██╗██████╗     ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗
  ██║██╔══██╗    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
  ██║██████╔╝    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
  ██║██╔═══╝     ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝
  ██║██║         ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║
  ╚═╝╚═╝         ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  By camzzz"""),

"phone": (LC, r"""
  ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗    ██╗███╗   ██╗███████╗ ██████╗
  ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝    ██║████╗  ██║██╔════╝██╔═══██╗
  ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗      ██║██╔██╗ ██║█████╗  ██║   ██║
  ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝      ██║██║╚██╗██║██╔══╝  ██║   ██║
  ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗    ██║██║ ╚████║██║     ╚██████╔╝
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝  By camzzz"""),

"mail": (LM, r"""
  ███╗   ███╗ █████╗ ██╗██╗         ██████╗ ███████╗██╗███╗   ██╗████████╗
  ████╗ ████║██╔══██╗██║██║         ██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝
  ██╔████╔██║███████║██║██║         ██████╔╝█████╗  ██║██╔██╗ ██║   ██║
  ██║╚██╔╝██║██╔══██║██║██║         ██╔══██╗██╔══╝  ██║██║╚██╗██║   ██║
  ██║ ╚═╝ ██║██║  ██║██║███████╗    ██║  ██║███████╗██║██║ ╚████║   ██║
  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝  By camzzz"""),

"breach": (LR, r"""
  ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗    ██████╗ ██████╗
  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║    ██╔══██╗██╔══██╗
  ██████╔╝██████╔╝█████╗  ███████║██║     ███████║    ██║  ██║██████╔╝
  ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║    ██║  ██║██╔══██╗
  ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║    ██████╔╝██████╔╝
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═════╝ ╚═════╝  By camzzz"""),

"user": (LM, r"""
  ██╗   ██╗███████╗███████╗██████╗ ███╗   ██╗ █████╗ ███╗   ███╗███████╗
  ██║   ██║██╔════╝██╔════╝██╔══██╗████╗  ██║██╔══██╗████╗ ████║██╔════╝
  ██║   ██║███████╗█████╗  ██████╔╝██╔██╗ ██║███████║██╔████╔██║█████╗
  ██║   ██║╚════██║██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝
  ╚██████╔╝███████║███████╗██║  ██║██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗
   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝  By camzzz"""),

"port": (LG, r"""
  ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
  ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║
  ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║
  ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  By camzzz"""),

"sub": (LC, r"""
  ███████╗██╗   ██╗██████╗ ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗
  ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║
  ███████╗██║   ██║██████╔╝██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║
  ╚════██║██║   ██║██╔══██╗██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║
  ███████║╚██████╔╝██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
  ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝  By camzzz"""),

"geo": (LY, r"""
   ██████╗ ███████╗ ██████╗     ██╗██████╗
  ██╔════╝ ██╔════╝██╔═══██╗    ██║██╔══██╗
  ██║  ███╗█████╗  ██║   ██║    ██║██████╔╝
  ██║   ██║██╔══╝  ██║   ██║    ██║██╔═══╝
  ╚██████╔╝███████╗╚██████╔╝    ██║██║
   ╚═════╝ ╚══════╝ ╚═════╝     ╚═╝╚═╝    By camzzz"""),

"hash": (LM, r"""
  ██╗  ██╗ █████╗ ███████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗
  ██║  ██║██╔══██╗██╔════╝██║  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ███████║███████║███████╗███████║       ██║   ██║   ██║██║   ██║██║
  ██╔══██║██╔══██║╚════██║██╔══██║       ██║   ██║   ██║██║   ██║██║
  ██║  ██║██║  ██║███████║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝  By camzzz"""),

"pass": (LM, r"""
  ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗
  ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
  ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
  ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
  ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  By camzzz"""),

"cam": (LR, r"""
  ██████╗██╗   ██╗██████╗ ██╗     ██╗ ██████╗     ██████╗  █████╗  ██████╗
  ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝    ██╔════╝██╔══██╗██╔═══██╗
  ██████╔╝██║   ██║██████╔╝██║     ██║██║         ██║     ███████║██║   ██║
  ██╔═══╝ ██║   ██║██╔══██╗██║     ██║██║         ██║     ██╔══██║██║   ██║
  ██║     ╚██████╔╝██████╔╝███████╗██║╚██████╗    ╚██████╗██║  ██║╚██████╔╝
  ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝ ╚═════╝  By camzzz"""),

"dork": (LY, r"""
  ██████╗  ██████╗ ██████╗ ██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗
  ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ██║  ██║██║   ██║██████╔╝█████╔╝        ██║   ██║   ██║██║   ██║██║
  ██║  ██║██║   ██║██╔══██╗██╔═██╗        ██║   ██║   ██║██║   ██║██║
  ██████╔╝╚██████╔╝██║  ██║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝  By camzzz"""),
}

def show_logo(key):
    clear()
    col, art = LOGOS.get(key, (LG, ""))
    for line in art.strip().split("\n"):
        rainbow("  " + line.strip())
    print()
    print(col + "  " + "─"*70)
    print()

# ──────────────────────────────────────────────
#  INTRO ANIMATION
# ──────────────────────────────────────────────

def intro():
    clear()
    matrix_rain(7, 72)
    time.sleep(0.1); clear()

    skull_cols = [LG, G, LC, LM, LY, LR, LG]
    for col in skull_cols:
        clear(); print(col + SKULL); time.sleep(0.14)

    clear()
    for frame in BOOT_FRAMES:
        clear(); matrix_rain(3, 72); print(LG + frame); time.sleep(0.4)

    time.sleep(0.2); clear()
    matrix_rain(2, 72); print()
    print(LG + "  " + "─"*68)
    for _ in range(6):
        noise = "@#$%camzzz&?!OSINT*~tool^<>V5"
        line = "  " + "".join(random.choice(noise) for _ in range(52))
        sys.stdout.write(random.choice([G,LG,C,LC,M,LM,Y]) + line + "\r")
        sys.stdout.flush(); time.sleep(0.07)
    glitch("         B Y   C A M Z Z Z   —   M U L T I   T O O L   V 5", 5, LG)
    print(LG + "  " + "─"*68)
    time.sleep(0.2); print()

    for line in CAMZZZ_LINES:
        rainbow(line); time.sleep(0.05)
    time.sleep(0.3); print()

    modules = [
        ("  [ IP / GEO MODULE     ]", LG,  G),
        ("  [ PHONE MODULE        ]", LC,  C),
        ("  [ MAIL / EMAIL MODULE ]", LM,  M),
        ("  [ BREACH MODULE       ]", LR,  R),
        ("  [ OSINT MODULE        ]", LY,  Y),
        ("  [ NETWORK MODULE      ]", LG,  G),
        ("  [ PASSWORD MODULE     ]", LM,  M),
        ("  [ CAMERA MODULE       ]", LR,  R),
        ("  [ INTEL MODULE        ]", LC,  C),
        ("  [ ALL 50+ TOOLS READY ]", LG,  G),
    ]
    for label, col, bc in modules:
        bar(label, 28, 0.012, col, bc)

    print(); blink("  ◈◈◈  ALL SYSTEMS ONLINE  ·  By camzzz  ·  V5  ◈◈◈", 3, LG)
    time.sleep(0.3); clear(); matrix_rain(4, 72); time.sleep(0.2); clear()

# ──────────────────────────────────────────────
#  BANNER
# ──────────────────────────────────────────────

def banner():
    print(LG + BANNER)
    for line in CAMZZZ_LINES:
        rainbow(line)
    print()
    print(C + "  " + "─"*70)
    print(C + f"  ◈  {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}  ◈  By camzzz  ◈  github.com/cameleonnbss/50-multi-tool")
    print(C + "  " + "─"*70)
    print()

# ──────────────────────────────────────────────
#  ① IP INFO  (own + target + reputation)
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
                print(LG + f"  Street : https://www.openstreetmap.org/?mlat={lat}&mlon={lon}")
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
            fields=["country_name","region","city","postal","latitude","longitude",
                    "timezone","org","asn","currency","languages","country_capital",
                    "country_calling_code","network","version"]
            for f in fields:
                v = geo.get(f) or geo2.get(f,"N/A")
                if v and v!="N/A": row(f, v, LG, LW)
            lat,lon=geo.get("latitude",""),geo.get("longitude","")
            if lat and lon:
                print(); print(LG+f"  Google Maps : https://maps.google.com/?q={lat},{lon}")
                print(LG+f"  OpenStreet  : https://www.openstreetmap.org/?mlat={lat}&mlon={lon}")
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
            ("ThreatCrowd",     f"https://www.threatcrowd.org/ip.php?ip={ip}"),
            ("OTX AlienVault",  f"https://otx.alienvault.com/indicator/ip/{ip}"),
            ("BinaryEdge",      f"https://app.binaryedge.io/services/query?query={qenc(ip)}"),
        ]: link(name, lnk, LC)

    elif c == "4":
        cidr = input(LG + "  IP/24 prefix (e.g. 192.168.1) > ").strip()
        if not cidr: pause(); return
        spinner("Scanning subnet", 1.0, LG)
        found=[]
        def chk(i):
            ip2=f"{cidr}.{i}"
            try: socket.setdefaulttimeout(0.4); socket.gethostbyname(ip2); return ip2
            except: return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
            results=list(ex.map(chk,range(1,255)))
        section("LIVE HOSTS", LG)
        for r in [r for r in results if r]:
            found.append(r); print(LG+f"  [+]  {r}")
        print(LG+f"\n  {len(found)} host(s) found.")
    pause()

# ──────────────────────────────────────────────
#  ② PHONE NUMBER INFO
# ──────────────────────────────────────────────

PHONE_DB = {
    "+1":  {"country":"USA / Canada",       "region":"North America",  "tz":"UTC-5 to UTC-8",   "fmt":"(XXX) XXX-XXXX"},
    "+7":  {"country":"Russia/Kazakhstan",  "region":"Eurasia",        "tz":"UTC+2 to UTC+12",  "fmt":"8 (XXX) XXX-XX-XX"},
    "+20": {"country":"Egypt",              "region":"Africa",         "tz":"UTC+2",             "fmt":"0XX XXXX XXXX"},
    "+27": {"country":"South Africa",       "region":"Africa",         "tz":"UTC+2",             "fmt":"0XX XXX XXXX"},
    "+30": {"country":"Greece",             "region":"Europe",         "tz":"UTC+2",             "fmt":"XXX XXX XXXX"},
    "+31": {"country":"Netherlands",        "region":"Europe",         "tz":"UTC+1",             "fmt":"0XX XXX XXXX"},
    "+32": {"country":"Belgium",            "region":"Europe",         "tz":"UTC+1",             "fmt":"0XXX XX XX XX"},
    "+33": {"country":"France",             "region":"Europe",         "tz":"UTC+1",             "fmt":"0X XX XX XX XX"},
    "+34": {"country":"Spain",              "region":"Europe",         "tz":"UTC+1",             "fmt":"XXX XXX XXX"},
    "+36": {"country":"Hungary",            "region":"Europe",         "tz":"UTC+1",             "fmt":"06X XXX XXXX"},
    "+39": {"country":"Italy",              "region":"Europe",         "tz":"UTC+1",             "fmt":"XXX XXX XXXX"},
    "+40": {"country":"Romania",            "region":"Europe",         "tz":"UTC+2",             "fmt":"0XXX XXX XXX"},
    "+41": {"country":"Switzerland",        "region":"Europe",         "tz":"UTC+1",             "fmt":"0XX XXX XXXX"},
    "+43": {"country":"Austria",            "region":"Europe",         "tz":"UTC+1",             "fmt":"0XXX XXXXXX"},
    "+44": {"country":"United Kingdom",     "region":"Europe",         "tz":"UTC+0",             "fmt":"0XXXX XXXXXX"},
    "+45": {"country":"Denmark",            "region":"Europe",         "tz":"UTC+1",             "fmt":"XX XX XX XX"},
    "+46": {"country":"Sweden",             "region":"Europe",         "tz":"UTC+1",             "fmt":"0XX XXX XXXX"},
    "+47": {"country":"Norway",             "region":"Europe",         "tz":"UTC+1",             "fmt":"XXX XX XXX"},
    "+48": {"country":"Poland",             "region":"Europe",         "tz":"UTC+1",             "fmt":"XXX XXX XXX"},
    "+49": {"country":"Germany",            "region":"Europe",         "tz":"UTC+1",             "fmt":"0XXX XXXXXXXX"},
    "+51": {"country":"Peru",               "region":"South America",  "tz":"UTC-5",             "fmt":"XXX XXX XXX"},
    "+52": {"country":"Mexico",             "region":"North America",  "tz":"UTC-6",             "fmt":"XXX XXX XXXX"},
    "+54": {"country":"Argentina",          "region":"South America",  "tz":"UTC-3",             "fmt":"0XX XXXX-XXXX"},
    "+55": {"country":"Brazil",             "region":"South America",  "tz":"UTC-3",             "fmt":"(XX) XXXXX-XXXX"},
    "+56": {"country":"Chile",              "region":"South America",  "tz":"UTC-4",             "fmt":"X XXXX XXXX"},
    "+57": {"country":"Colombia",           "region":"South America",  "tz":"UTC-5",             "fmt":"XXX XXX XXXX"},
    "+60": {"country":"Malaysia",           "region":"Asia",           "tz":"UTC+8",             "fmt":"0X XXXX XXXX"},
    "+61": {"country":"Australia",          "region":"Oceania",        "tz":"UTC+8 to +11",      "fmt":"0X XXXX XXXX"},
    "+62": {"country":"Indonesia",          "region":"Asia",           "tz":"UTC+7 to +9",       "fmt":"0XXX XXXX XXXX"},
    "+63": {"country":"Philippines",        "region":"Asia",           "tz":"UTC+8",             "fmt":"0XXX XXX XXXX"},
    "+64": {"country":"New Zealand",        "region":"Oceania",        "tz":"UTC+12",            "fmt":"0X XXX XXXX"},
    "+65": {"country":"Singapore",          "region":"Asia",           "tz":"UTC+8",             "fmt":"XXXX XXXX"},
    "+66": {"country":"Thailand",           "region":"Asia",           "tz":"UTC+7",             "fmt":"0X XXXX XXXX"},
    "+81": {"country":"Japan",              "region":"Asia",           "tz":"UTC+9",             "fmt":"0X XXXX XXXX"},
    "+82": {"country":"South Korea",        "region":"Asia",           "tz":"UTC+9",             "fmt":"0X XXXX XXXX"},
    "+84": {"country":"Vietnam",            "region":"Asia",           "tz":"UTC+7",             "fmt":"0XX XXXX XXXX"},
    "+86": {"country":"China",              "region":"Asia",           "tz":"UTC+8",             "fmt":"0XX XXXX XXXX"},
    "+90": {"country":"Turkey",             "region":"Europe/Asia",    "tz":"UTC+3",             "fmt":"0XXX XXX XXXX"},
    "+91": {"country":"India",              "region":"Asia",           "tz":"UTC+5:30",          "fmt":"XXXXX XXXXX"},
    "+92": {"country":"Pakistan",           "region":"Asia",           "tz":"UTC+5",             "fmt":"0XXX XXX XXXX"},
    "+94": {"country":"Sri Lanka",          "region":"Asia",           "tz":"UTC+5:30",          "fmt":"0XX XXX XXXX"},
    "+98": {"country":"Iran",               "region":"Asia",           "tz":"UTC+3:30",          "fmt":"0XXX XXX XXXX"},
    "+212":{"country":"Morocco",            "region":"Africa",         "tz":"UTC+1",             "fmt":"0XXX XXXXXX"},
    "+213":{"country":"Algeria",            "region":"Africa",         "tz":"UTC+1",             "fmt":"0XXX XXXXXX"},
    "+216":{"country":"Tunisia",            "region":"Africa",         "tz":"UTC+1",             "fmt":"XX XXX XXX"},
    "+221":{"country":"Senegal",            "region":"Africa",         "tz":"UTC+0",             "fmt":"XX XXX XX XX"},
    "+225":{"country":"Ivory Coast",        "region":"Africa",         "tz":"UTC+0",             "fmt":"XX XX XX XX XX"},
    "+234":{"country":"Nigeria",            "region":"Africa",         "tz":"UTC+1",             "fmt":"0XXX XXX XXXX"},
    "+237":{"country":"Cameroon",           "region":"Africa",         "tz":"UTC+1",             "fmt":"XXXX XXXX"},
    "+254":{"country":"Kenya",              "region":"Africa",         "tz":"UTC+3",             "fmt":"0XXX XXX XXX"},
    "+255":{"country":"Tanzania",           "region":"Africa",         "tz":"UTC+3",             "fmt":"0XXX XXX XXX"},
    "+256":{"country":"Uganda",             "region":"Africa",         "tz":"UTC+3",             "fmt":"0XXX XXXXXX"},
    "+351":{"country":"Portugal",           "region":"Europe",         "tz":"UTC+0",             "fmt":"XXX XXX XXX"},
    "+353":{"country":"Ireland",            "region":"Europe",         "tz":"UTC+0",             "fmt":"0XX XXX XXXX"},
    "+358":{"country":"Finland",            "region":"Europe",         "tz":"UTC+2",             "fmt":"0XX XXX XXXX"},
    "+380":{"country":"Ukraine",            "region":"Europe",         "tz":"UTC+2",             "fmt":"0XX XXX XXXX"},
    "+381":{"country":"Serbia",             "region":"Europe",         "tz":"UTC+1",             "fmt":"0XX XXXXXXX"},
    "+385":{"country":"Croatia",            "region":"Europe",         "tz":"UTC+1",             "fmt":"0XX XXX XXXX"},
    "+420":{"country":"Czech Republic",     "region":"Europe",         "tz":"UTC+1",             "fmt":"XXX XXX XXX"},
    "+421":{"country":"Slovakia",           "region":"Europe",         "tz":"UTC+1",             "fmt":"0XXX XXX XXX"},
    "+972":{"country":"Israel",             "region":"Middle East",    "tz":"UTC+2",             "fmt":"0XX XXX XXXX"},
    "+974":{"country":"Qatar",              "region":"Middle East",    "tz":"UTC+3",             "fmt":"XXXX XXXX"},
    "+971":{"country":"UAE",                "region":"Middle East",    "tz":"UTC+4",             "fmt":"0X XXX XXXX"},
    "+966":{"country":"Saudi Arabia",       "region":"Middle East",    "tz":"UTC+3",             "fmt":"0XX XXX XXXX"},
    "+962":{"country":"Jordan",             "region":"Middle East",    "tz":"UTC+2",             "fmt":"0X XXXX XXXX"},
    "+961":{"country":"Lebanon",            "region":"Middle East",    "tz":"UTC+2",             "fmt":"0X XXX XXX"},
    "+880":{"country":"Bangladesh",         "region":"Asia",           "tz":"UTC+6",             "fmt":"0XXXX XXXXXX"},
    "+852":{"country":"Hong Kong",          "region":"Asia",           "tz":"UTC+8",             "fmt":"XXXX XXXX"},
    "+886":{"country":"Taiwan",             "region":"Asia",           "tz":"UTC+8",             "fmt":"0X XXXX XXXX"},
    "+58": {"country":"Venezuela",          "region":"South America",  "tz":"UTC-4",             "fmt":"0XXX XXX XXXX"},
    "+593":{"country":"Ecuador",            "region":"South America",  "tz":"UTC-5",             "fmt":"0XX XXX XXXX"},
    "+595":{"country":"Paraguay",           "region":"South America",  "tz":"UTC-4",             "fmt":"0XXX XXX XXX"},
    "+598":{"country":"Uruguay",            "region":"South America",  "tz":"UTC-3",             "fmt":"0X XXX XXXX"},
}

FR_LINES = {
    "06":"Mobile — Orange / SFR / Bouygues / Free",
    "07":"Mobile — Free Mobile / MVNO",
    "01":"Île-de-France (fixe)",
    "02":"Nord-Ouest France (fixe)",
    "03":"Nord-Est France (fixe)",
    "04":"Sud-Est France (fixe)",
    "05":"Sud-Ouest France (fixe)",
    "08":"Numéro spécial (surtaxé / gratuit / vert)",
    "09":"VoIP / Box Internet",
}

EXPECTED_LEN = {
    "+33":11,"+44":12,"+1":11,"+49":12,"+34":11,"+39":12,
    "+31":11,"+32":11,"+41":11,"+43":11,"+46":11,"+47":11,
    "+48":11,"+45":11,"+30":11,"+353":11,"+358":11,
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
    e       = qenc(number)
    d       = qenc(digits)
    e_np    = qenc(no_plus)

    # ── BASE ANALYSIS ──────────────────────────────
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
        if is_mob:
            print(LC + "\n  Possible operators: Orange, SFR, Bouygues Telecom, Free Mobile, MVNO")

    section("VALIDITY CHECK", LC)
    exp = EXPECTED_LEN.get(matched)
    if exp:
        valid = len(digits) == exp
        row("Expected digits", exp, LC, LW)
        row("Actual digits",   len(digits), LC, LW)
        row("Likely valid", "Yes ✓" if valid else "No — check length", LC,
            LG if valid else LR)
    else:
        row("Length check", "No rule for this country code", LC, LY)

    if c == "2":
        section("QUICK LOOKUP LINKS", LC)
        for name, lnk in [
            ("Google",     f"https://www.google.com/search?q={e}"),
            ("TrueCaller", f"https://www.truecaller.com/search/fr/{d}"),
            ("NumLookup",  f"https://www.numlookup.com/?number={e}"),
            ("Sync.me",    f"https://sync.me/search/?number={e}"),
            ("ZSearcher",  f"https://zsearcher.fr/search?q={d}"),
            ("OathNet",    f"https://oathnet.org/search?q={e}"),
        ]: link(name, lnk, LC)
        pause(); return

    # ── FULL OSINT MODE ────────────────────────────

    section("POTENTIAL OWNER SEARCH", LC)
    print(LC + "  Reverse lookup services — may show name / address linked to number:")
    print()
    for name, lnk in [
        ("TrueCaller",          f"https://www.truecaller.com/search/fr/{d}"),
        ("NumLookup",           f"https://www.numlookup.com/?number={e}"),
        ("Sync.me",             f"https://sync.me/search/?number={e}"),
        ("Spokeo",              f"https://www.spokeo.com/phone/{d}"),
        ("WhitePages",          f"https://www.whitepages.com/phone/{d}"),
        ("TruePeopleSearch",    f"https://www.truepeoplesearch.com/resultsphonesearch?phoneno={d}"),
        ("FastPeopleSearch",    f"https://www.fastpeoplesearch.com/phone/{d}"),
        ("CallerIDTest",        f"https://www.calleridtest.com/phone-lookup/{d}"),
        ("PhoneInfoga",         f"https://www.phoneinfoga.crvx.fr/"),
        ("AnyWho",              f"https://www.anywho.com/reverse-phone-lookup/{d}"),
        ("NumVerify (check)",   f"https://numverify.com/"),
        ("InternationalSkipTrace","https://www.skipease.com/"),
    ]: link(name, lnk, LC)

    section("SOCIAL MEDIA — ACCOUNT SEARCH", LC)
    print(LC + "  Search for social accounts linked to this phone number:")
    print()
    for name, lnk in [
        ("Google full",         f"https://www.google.com/search?q=%22{e}%22"),
        ("Google no plus",      f"https://www.google.com/search?q=%22{e_np}%22"),
        ("Google digits",       f"https://www.google.com/search?q=%22{d}%22"),
        ("Facebook search",     f"https://www.facebook.com/search/top/?q={e}"),
        ("Twitter/X search",    f"https://twitter.com/search?q=%22{e}%22&f=live"),
        ("LinkedIn search",     f"https://www.linkedin.com/search/results/people/?keywords={e}"),
        ("Instagram (Google)",  f"https://www.google.com/search?q=site:instagram.com+%22{e}%22"),
        ("TikTok (Google)",     f"https://www.google.com/search?q=site:tiktok.com+%22{e}%22"),
        ("Telegram (Google)",   f"https://www.google.com/search?q=site:t.me+%22{e}%22"),
        ("WhatsApp check",      f"https://wa.me/{d}"),
        ("Viber check",         f"https://www.google.com/search?q=viber+%22{e}%22"),
        ("Signal (Google)",     f"https://www.google.com/search?q=signal+%22{e}%22"),
        ("Snapchat (Google)",   f"https://www.google.com/search?q=site:snapchat.com+%22{e}%22"),
        ("Discord (Google)",    f"https://www.google.com/search?q=site:discord.com+%22{e}%22"),
        ("Reddit (Google)",     f"https://www.google.com/search?q=site:reddit.com+%22{e}%22"),
    ]: link(name, lnk, LM)

    section("DATING / CLASSIFIEDS SEARCH", LC)
    print(LC + "  Platforms where phone numbers are sometimes publicly posted:")
    print()
    for name, lnk in [
        ("Google Craigslist",   f"https://www.google.com/search?q=site:craigslist.org+%22{e}%22"),
        ("Google Leboncoin",    f"https://www.google.com/search?q=site:leboncoin.fr+%22{e}%22"),
        ("Google OLX",          f"https://www.google.com/search?q=site:olx.com+%22{e}%22"),
        ("Google Badoo",        f"https://www.google.com/search?q=site:badoo.com+%22{e}%22"),
        ("Google Tinder",       f"https://www.google.com/search?q=site:tinder.com+%22{e}%22"),
        ("Google forums",       f"https://www.google.com/search?q=%22{e}%22+forum"),
        ("Google comments",     f"https://www.google.com/search?q=%22{e}%22+contact"),
    ]: link(name, lnk, LY)

    section("BREACH / LEAK DATABASES", LC)
    print(LC + "  Check if this number appeared in data leaks:")
    print()
    for name, lnk in [
        ("ZSearcher.fr",        f"https://zsearcher.fr/search?q={d}"),
        ("OathNet.org",         f"https://oathnet.org/search?q={e}"),
        ("DeHashed",            f"https://dehashed.com/search?query={e}"),
        ("IntelX",              f"https://intelx.io/?s={e}"),
        ("Snusbase",            "https://snusbase.com/"),
        ("LeakCheck",           "https://leakcheck.io/"),
        ("HaveIBeenPwned",      "https://haveibeenpwned.com/"),
        ("Grep.app",            f"https://grep.app/search?q={e}"),
        ("Pastebin (Google)",   f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
        ("GitHub code search",  f"https://github.com/search?q={e}&type=code"),
    ]: link(name, lnk, LR)

    section("OSINT TOOLS FOR PHONE", LC)
    print(LC + "  Dedicated phone OSINT tools:")
    print()
    for name, lnk in [
        ("PhoneInfoga (tool)",  "https://github.com/sundowndev/phoneinfoga"),
        ("Ignorant (tool)",     "https://github.com/megadose/ignorant"),
        ("Moriarty-Project",    "https://github.com/AzizKpln/Moriarty-Project"),
    ]: link(name, lnk, LG)
    print()
    print(LY + "  Tip: PhoneInfoga and Ignorant are open-source Python tools")
    print(LY + "  you can run locally for deeper phone OSINT automation.")

    pause()

# ──────────────────────────────────────────────
#  ③ EMAIL / MAIL OSINT
# ──────────────────────────────────────────────

def mail_osint():
    show_logo("mail")
    print(LM + "  1  Full email OSINT analysis")
    print(LM + "  2  Email format guesser")
    print(LM + "  3  Email header analyser (paste raw header)")
    print(LM + "  4  Disposable / temp mail checker")
    print()
    c = input(LM + "  Choice > ").strip()

    if c == "1":
        email = input(LM + "  Email > ").strip()
        if "@" not in email: print(LR+"  Invalid."); pause(); return
        user, domain = email.split("@", 1)
        spinner("Analysing email", 1.0, LM)

        md5  = hashlib.md5(email.lower().encode()).hexdigest()
        sha1 = hashlib.sha1(email.lower().encode()).hexdigest()
        sha256 = hashlib.sha256(email.lower().encode()).hexdigest()

        section("EMAIL ANALYSIS", LM)
        row("Email",    email,  LM, LW)
        row("Username", user,   LM, LW)
        row("Domain",   domain, LM, LW)
        row("MD5",      md5,    LM, LW)
        row("SHA1",     sha1,   LM, LW)
        row("SHA256",   sha256, LM, LW)
        row("Gravatar", f"https://www.gravatar.com/avatar/{md5}", LM, LC)

        section("DOMAIN DNS INFO", LM)
        try:
            ip = socket.gethostbyname(domain)
            row("Domain IP", ip, LM, LW)
            try:
                rev = socket.gethostbyaddr(ip)
                row("Reverse DNS", rev[0], LM, LW)
            except: pass
            for rtype in ["MX","TXT","NS"]:
                try:
                    r = requests.get(f"https://dns.google/resolve?name={domain}&type={rtype}",
                                     timeout=6).json()
                    ans = r.get("Answer",[])
                    if ans:
                        row(f"{rtype} record", ans[0].get("data","N/A")[:60], LM, LW)
                except: pass
        except Exception as e:
            row("DNS", f"Failed: {e}", LM, LR)

        section("WEB PRESENCE", LM)
        try:
            r = requests.get(f"https://{domain}", timeout=8,
                             headers={"User-Agent":"Mozilla/5.0"})
            row("HTTP Status", str(r.status_code), LM, LW)
            row("Server",      r.headers.get("Server","N/A"), LM, LW)
            row("X-Powered-By",r.headers.get("X-Powered-By","N/A"), LM, LW)
        except: row("Website", "Unreachable", LM, LY)

        section("BREACH SEARCH LINKS", LM)
        e = qenc(email)
        for name, lnk in [
            ("ZSearcher.fr",    f"https://zsearcher.fr/search?q={e}"),
            ("OathNet.org",     f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned",  f"https://haveibeenpwned.com/account/{e}"),
            ("DeHashed",        f"https://dehashed.com/search?query={e}"),
            ("IntelX",          f"https://intelx.io/?s={e}"),
            ("LeakCheck",       "https://leakcheck.io/"),
            ("BreachDirectory", "https://breachdirectory.org/"),
            ("EmailRep.io",     f"https://emailrep.io/{e}"),
            ("Grep.app",        f"https://grep.app/search?q={e}"),
            ("GitHub search",   f"https://github.com/search?q={e}&type=code"),
            ("Pastebin",        f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
            ("Snusbase",        "https://snusbase.com/"),
            ("Spycloud",        "https://spycloud.com/check-your-exposure/"),
            ("Firefox Monitor", "https://monitor.firefox.com/"),
        ]: link(name, lnk, LM)

        section("SOCIAL / ACCOUNT LINKS", LM)
        for name, lnk in [
            ("Gravatar profile", f"https://www.gravatar.com/{md5}"),
            ("Twitter search",   f"https://twitter.com/search?q={e}"),
            ("LinkedIn",         f"https://www.linkedin.com/search/results/people/?keywords={qenc(user)}"),
            ("GitHub search",    f"https://github.com/search?q={e}&type=users"),
        ]: link(name, lnk, LM)

    elif c == "2":
        first  = input(LM + "  First name > ").strip().lower()
        last   = input(LM + "  Last name  > ").strip().lower()
        domain = input(LM + "  Domain     > ").strip().lower()
        fi = first[0] if first else "x"
        li = last[0]  if last  else "x"
        section("POSSIBLE EMAIL FORMATS", LM)
        fmts = [
            f"{first}@{domain}",
            f"{last}@{domain}",
            f"{first}.{last}@{domain}",
            f"{last}.{first}@{domain}",
            f"{fi}{last}@{domain}",
            f"{first}{li}@{domain}",
            f"{fi}.{last}@{domain}",
            f"{first}_{last}@{domain}",
            f"{last}_{first}@{domain}",
            f"{first}{last}@{domain}",
            f"{last}{first}@{domain}",
            f"{fi}{li}@{domain}",
            f"{first[0:2]}{last}@{domain}",
            f"{first}.{last[0]}@{domain}",
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
            "From":         r"From:(.+)",
            "To":           r"To:(.+)",
            "Subject":      r"Subject:(.+)",
            "Date":         r"Date:(.+)",
            "Message-ID":   r"Message-ID:(.+)",
            "Return-Path":  r"Return-Path:(.+)",
            "Reply-To":     r"Reply-To:(.+)",
            "X-Mailer":     r"X-Mailer:(.+)",
            "X-Originating-IP": r"X-Originating-IP:(.+)",
            "DKIM-Signature":r"DKIM-Signature:(.+)",
            "Received-SPF": r"Received-SPF:(.+)",
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
        section("DISPOSABLE MAIL CHECK", LM)
        disposable_domains = [
            "mailinator.com","guerrillamail.com","10minutemail.com","temp-mail.org",
            "throwam.com","yopmail.com","sharklasers.com","guerrillamailblock.com",
            "grr.la","guerrillamail.info","guerrillamail.biz","guerrillamail.de",
            "guerrillamail.net","guerrillamail.org","spam4.me","trashmail.com",
            "trashmail.at","trashmail.io","trashmail.me","trashmail.net",
            "dispostable.com","discard.email","maildrop.cc","mailnull.com",
            "spamgourmet.com","spamgourmet.net","spamgourmet.org","spamex.com",
            "spamfree24.org","spamfree24.de","spamfree24.info","spamfree24.biz",
            "tempail.com","tempmail.com","tempmail.de","tempr.email",
            "fakeinbox.com","fakeinbox.net","fakeinbox.org","mailnesia.com",
            "mailnull.com","mailsac.com","33mail.com","mintemail.com",
        ]
        is_disp = domain in disposable_domains
        row("Domain",    domain,     LM, LW)
        row("Disposable","Yes — likely a temp mail provider" if is_disp
            else "Not in local list (may still be temp)", LM,
            LR if is_disp else LG)
        print()
        print(LM + "  Online checkers:")
        for name, lnk in [
            ("DisposableMailCheck", f"https://www.dispostable.com/"),
            ("MailChecker API",     f"https://api.mailchecker.io/v4/check/{qenc(email)}"),
            ("Kickbox",            f"https://kickbox.com/"),
        ]: link(name, lnk, LM)
    pause()

# ──────────────────────────────────────────────
#  ④ DATA BREACH SEARCH ENGINE
# ──────────────────────────────────────────────

def breach_engine():
    show_logo("breach")
    print(LW + "  All services below are legal publicly accessible breach databases.")
    print()
    print(LR + "  1  ZSearcher.fr          French specialised breach engine")
    print(LR + "  2  OathNet.org           International breach engine")
    print(LR + "  3  HaveIBeenPwned        International — email check via API")
    print(LR + "  4  ALL breach links      Generate all links for any query")
    print(LR + "  5  Password HIBP check   k-anonymity — nothing sent to server")
    print(LR + "  6  Domain breach search  All breaches linked to a domain")
    print(LR + "  7  Username breach scan  Check username across breach DBs")
    print()
    c = input(LC + "  Choice > ").strip()

    if c == "1":
        q = input(LC + "  Search (email / phone / username) > ").strip()
        e = qenc(q)
        section("ZSEARCHER.FR", LR)
        print(LW + "  ZSearcher.fr is a French specialised breach search engine.")
        print(LW + "  Indexes French and international leak databases.\n")
        for name, lnk in [
            ("ZSearcher main",   "https://zsearcher.fr/"),
            ("ZSearcher search", f"https://zsearcher.fr/search?q={e}"),
            ("ZSearcher email",  f"https://zsearcher.fr/email?q={e}"),
            ("ZSearcher phone",  f"https://zsearcher.fr/search?q={qenc(re.sub(chr(92)+'D','',q))}"),
        ]: link(name, lnk, LC)

    elif c == "2":
        q = input(LC + "  Search (email / phone / username / domain) > ").strip()
        e = qenc(q)
        section("OATHNET.ORG", LR)
        print(LW + "  OathNet.org — international breach and OSINT aggregator.\n")
        for name, lnk in [
            ("OathNet main",   "https://oathnet.org/"),
            ("OathNet search", f"https://oathnet.org/search?q={e}"),
            ("OathNet email",  f"https://oathnet.org/email?q={e}"),
        ]: link(name, lnk, LC)

    elif c == "3":
        email = input(LC + "  Email > ").strip()
        e = qenc(email)
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
                print(LY + "  API key needed — get free key at haveibeenpwned.com/API/Key")
                print(LW + "  Or use the direct link above.")
            else:
                print(LY + f"  HTTP {r.status_code} — use the direct link.")
        except Exception as e:
            print(LR + f"  Failed: {e}")

    elif c == "4":
        q = input(LC + "  Email / username / phone / domain > ").strip()
        e = qenc(q)
        section("ALL BREACH DATABASE LINKS", LR)
        for name, lnk in [
            ("ZSearcher.fr",       f"https://zsearcher.fr/search?q={e}"),
            ("OathNet.org",        f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned",     f"https://haveibeenpwned.com/account/{e}"),
            ("DeHashed",           f"https://dehashed.com/search?query={e}"),
            ("IntelX",             f"https://intelx.io/?s={e}"),
            ("LeakCheck",          "https://leakcheck.io/"),
            ("BreachDirectory",    "https://breachdirectory.org/"),
            ("Snusbase",           "https://snusbase.com/"),
            ("Leak-Lookup",        "https://leak-lookup.com/search"),
            ("ScatteredSecrets",   "https://scatteredsecrets.com/"),
            ("EmailRep.io",        f"https://emailrep.io/{e}"),
            ("Firefox Monitor",    "https://monitor.firefox.com/"),
            ("CyberNews Checker",  "https://cybernews.com/personal-data-leak-check/"),
            ("Spycloud",           "https://spycloud.com/check-your-exposure/"),
            ("Psbdmp pastes",      f"https://psbdmp.ws/api/search/{e}"),
            ("Grep.app",           f"https://grep.app/search?q={e}"),
            ("Google Pastebin",    f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
            ("Google Gist",        f"https://www.google.com/search?q=site:gist.github.com+%22{e}%22"),
            ("PublicWWW",          f"https://publicwww.com/websites/{e}/"),
            ("Ahmia dark web",     f"https://ahmia.fi/search/?q={e}"),
            ("GhostProject",       "https://ghostproject.fr/"),
        ]: link(name, lnk, LR)

    elif c == "5":
        pwd = input(LC + "  Password to check > ").strip()
        if not pwd: pause(); return
        sha1 = hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        spinner("Querying HIBP Pwned Passwords (k-anonymity)", 1.0, LM)
        try:
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=8)
            found = False
            for line in r.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    print(LR + f"\n  [!!!]  Found {count} times in known breaches!")
                    print(LR +  "         Change this password immediately.")
                    found = True; break
            if not found:
                print(LG + "\n  [OK]  Not found in known breaches.")
            print(DIM + "\n  Only 5 chars of SHA1 hash sent — password never leaves your device.")
        except Exception as e:
            print(LR + f"  Failed: {e}")

    elif c == "6":
        domain = input(LC + "  Domain > ").strip()
        e = qenc(domain)
        section(f"DOMAIN BREACH SEARCH — {domain}", LR)
        for name, lnk in [
            ("ZSearcher",       f"https://zsearcher.fr/search?q={e}"),
            ("OathNet",         f"https://oathnet.org/search?q={e}"),
            ("HaveIBeenPwned",  f"https://haveibeenpwned.com/DomainSearch/{domain}"),
            ("DeHashed",        f"https://dehashed.com/search?query={e}"),
            ("IntelX",          f"https://intelx.io/?s={e}"),
            ("Shodan",          f"https://www.shodan.io/domain/{domain}"),
            ("Grep.app",        f"https://grep.app/search?q={e}"),
            ("PublicWWW",       f"https://publicwww.com/websites/{e}/"),
            ("URLScan",         f"https://urlscan.io/search/#{e}"),
            ("VirusTotal",      f"https://www.virustotal.com/gui/domain/{domain}"),
        ]: link(name, lnk, LR)

    elif c == "7":
        username = input(LC + "  Username > ").strip()
        e = qenc(username)
        section(f"USERNAME BREACH SEARCH — {username}", LR)
        for name, lnk in [
            ("ZSearcher",       f"https://zsearcher.fr/search?q={e}"),
            ("OathNet",         f"https://oathnet.org/search?q={e}"),
            ("DeHashed",        f"https://dehashed.com/search?query={e}"),
            ("IntelX",          f"https://intelx.io/?s={e}"),
            ("Grep.app",        f"https://grep.app/search?q={e}"),
            ("Snusbase",        "https://snusbase.com/"),
            ("Google Pastebin", f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
        ]: link(name, lnk, LR)
    pause()

# ──────────────────────────────────────────────
#  ⑤ USERNAME TRACKER  (50+ sites)
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
    ("Crates.io","https://crates.io/users/{}"),("Wattpad","https://www.wattpad.com/user/{}"),
    ("Goodreads","https://www.goodreads.com/{}"),("Disqus","https://disqus.com/by/{}"),
    ("Vimeo","https://vimeo.com/{}"),("Mix","https://mix.com/{}"),
    ("Trello","https://trello.com/{}"),("Venmo","https://venmo.com/{}"),
    ("Instructables","https://www.instructables.com/member/{}"),
    ("Poshmark","https://poshmark.com/closet/{}"),
    ("Snapchat","https://www.snapchat.com/add/{}"),
    ("Telegram","https://t.me/{}"),
    ("Discord","https://discord.com/users/{}"),
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
            return ("FOUND" if r.status_code==200 else "·", name, url)
        except:
            return ("ERR", name, url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(chk, SITES))
    for status, name, url in results:
        if status == "FOUND":
            print(LG + f"  [+]  {name:<22}" + LW + f" {url}")
            found.append(url)
        elif status == "ERR":
            print(DIM+C + f"  [?]  {name}")
        else:
            print(DIM+W + f"  [ ]  {name}")
    section(f"RESULTS  —  {len(found)} FOUND  /  {len(SITES)} CHECKED", LM)
    pause()

# ──────────────────────────────────────────────
#  ⑥ DNS LOOKUP
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
        try:
            rev = socket.gethostbyaddr(ip)
            row("Reverse DNS", rev[0], LY, LW)
        except: pass
    except Exception as e:
        row("A", f"FAILED: {e}", LY, LR)
    for rtype in ["MX","NS","TXT","AAAA","CAA","SOA","CNAME"]:
        try:
            r = requests.get(f"https://dns.google/resolve?name={domain}&type={rtype}",
                             timeout=8).json()
            answers = r.get("Answer",[])
            if answers:
                section(f"{rtype} RECORDS", LY)
                for a in answers:
                    print(LY + f"  {a.get('data','')[:90]}")
        except: pass
    pause()

# ──────────────────────────────────────────────
#  ⑦ PORT SCANNER
# ──────────────────────────────────────────────

COMMON_PORTS=[21,22,23,25,53,80,110,111,135,139,143,443,445,465,
              587,631,993,995,1433,1521,2222,3306,3389,5432,5900,
              6379,6443,8080,8443,8888,9200,27017,27018,28017]

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
        except:
            print(LR+"  Invalid."); pause(); return
    spinner(f"Scanning {host}", 1.2, LG)
    found=[]
    def chk(p):
        try:
            s = socket.socket(); s.settimeout(0.4)
            if s.connect_ex((host,p)) == 0:
                try: svc = socket.getservbyport(p)
                except: svc = "unknown"
                return (p, svc)
            s.close()
        except: pass
        return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
        results = list(ex.map(chk, ports))
    section("OPEN PORTS", LG)
    for r in sorted([r for r in results if r], key=lambda x: x[0]):
        port, svc = r; found.append(r)
        print(LG + f"  [OPEN]  {port:<8}" + LW + f" {svc}")
    print(LG + f"\n  {len(found)} open port(s) found.")
    pause()

# ──────────────────────────────────────────────
#  ⑧ GEO IP
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
                "timezone","org","asn","currency","languages","country_capital",
                "country_calling_code","network","version","country_area",
                "country_population"]
        for f in fields:
            v = d.get(f) or d2.get(f,"N/A")
            if v and v!="N/A": row(f, v, LY, LW)
        lat=d.get("latitude",""); lon=d.get("longitude","")
        if lat and lon:
            print(); print(LY+f"  Google Maps : https://maps.google.com/?q={lat},{lon}")
            print(LY+f"  OpenStreet  : https://www.openstreetmap.org/?mlat={lat}&mlon={lon}")
    except Exception as e:
        print(LR + f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑨ SUBDOMAIN FINDER
# ──────────────────────────────────────────────

SUBS=["www","mail","ftp","smtp","pop","imap","webmail","cpanel","admin","api",
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
      "sonar","nexus","artifactory","registry","k8s","kube","rancher"]

def subdomain_finder():
    show_logo("sub")
    domain = input(LC + "  Domain > ").strip()
    if not domain: pause(); return
    bar("  Building wordlist", 20, 0.015, LC, C)
    print(LC + f"\n  Testing {len(SUBS)} subdomains on {domain}...\n")
    found=[]
    def chk(sub):
        t=f"{sub}.{domain}"
        try: return (t, socket.gethostbyname(t))
        except: return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        results = list(ex.map(chk, SUBS))
    section("FOUND SUBDOMAINS", LC)
    for r in [r for r in results if r]:
        sub,ip=r; found.append(sub)
        print(LC+f"  [+]  {sub:<46}"+LW+f" -> {ip}")
    print(LC+f"\n  {len(found)} subdomain(s) found.")
    pause()

# ──────────────────────────────────────────────
#  ⑩ WHOIS / REVERSE DNS
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
    elif c=="2":
        ip=input(LY+"  IP > ").strip()
        spinner("Reverse DNS",0.8,LY)
        try:
            h=socket.gethostbyaddr(ip)
            section("REVERSE DNS",LY); row("IP",ip,LY,LW); row("Hostname",h[0],LY,LG)
            if h[1]: row("Aliases",", ".join(h[1]),LY,LW)
        except Exception as e: print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑪ SSL INSPECTOR
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
        subj=dict(x[0] for x in cert.get("subject",[]))
        iss=dict(x[0] for x in cert.get("issuer",[]))
        section("SSL CERTIFICATE", LC)
        row("Subject CN",  subj.get("commonName","N/A"), LC, LW)
        row("Org",         subj.get("organizationName","N/A"), LC, LW)
        row("Issuer",      iss.get("organizationName","N/A"), LC, LW)
        row("Valid From",  cert.get("notBefore","N/A"), LC, LG)
        row("Valid Until", cert.get("notAfter","N/A"),  LC, LG)
        sans=cert.get("subjectAltName",[])
        if sans:
            section("SUBJECT ALT NAMES", LC)
            for t,v in sans: print(LC+f"  {t:<10}"+LW+f" {v}")
    except Exception as e:
        print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑫ HTTP HEADER INSPECTOR
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
#  ⑬ TECH DETECTOR
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
            "Squarespace":["squarespace"],"Webflow":["webflow"],
            "React":["react","__react"],"Vue.js":["vue.js"],"Angular":["angular"],
            "Next.js":["__next"],"Gatsby":["gatsby"],"jQuery":["jquery"],
            "Bootstrap":["bootstrap"],"Tailwind":["tailwind"],
            "PHP":["php",".php"],"Django":["csrfmiddlewaretoken"],
            "Laravel":["laravel_session"],"Ruby on Rails":["rails","csrf-token"],
            "ASP.NET":["asp.net","__viewstate"],"Cloudflare":["cf-ray"],
            "Nginx":["nginx"],"Apache":["apache"],"IIS":["iis"],
            "Google Analytics":["google-analytics","gtag("],
            "HubSpot":["hubspot"],"Intercom":["intercom"],"Zendesk":["zendesk"],
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
#  ⑭ GOOGLE DORK GENERATOR
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
        ("Cache",              f"cache:{target}"),
        ("Related sites",      f"related:{target}"),
        ("Backup files",       f"site:{target} ext:bak OR ext:old OR ext:backup"),
        ("API keys exposed",   f"site:{target} intext:apikey OR intext:api_key"),
    ]
    if kw: dorks.append(("Keyword", f"site:{target} \"{kw}\""))
    section("GENERATED DORKS", LY)
    for desc, dork in dorks:
        print(LY+f"  {desc:<28}"+LW+f" https://www.google.com/search?q={qenc(dork)}")
    pause()

# ──────────────────────────────────────────────
#  ⑮ PASSWORD TOOLS
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
            (not any(pwd.lower().startswith(w) for w in
                     ["password","pass","123","qwerty","admin","letme","abc"]),"Not common prefix"),
        ]
        score=0
        for passed,label in checks:
            print((LG+"  [OK] " if passed else LR+"  [!!] ")+LW+label)
            if passed: score+=1
        rating=["Very Weak","Weak","Weak","Medium","Medium","Good","Good","Strong","Very Strong"]
        rcol=[LR,LR,LR,LY,LY,LG,LG,LG,LG][min(score,8)]
        print()
        print(LM+f"  Score: "+LG+"█"*score+DIM+"░"*(8-score)+LM+f"  {score}/8  "+rcol+rating[min(score,8)])
        section("HIBP CHECK (k-anonymity)",LM)
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
#  ⑯ HASH TOOLS
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
#  ⑰ METADATA EXTRACTOR
# ──────────────────────────────────────────────

def metadata_extractor():
    show_logo("ip")
    if not PIL_OK: print(LR+"  Pillow not installed. Run: pip install Pillow"); pause(); return
    path=input(LG+"  Image path > ").strip()
    if not path: pause(); return
    spinner("Reading EXIF",0.6,LG)
    try:
        img=Image.open(path)
        section("IMAGE INFO",LG)
        row("Format",img.format,LG,LW); row("Mode",img.mode,LG,LW)
        row("Size",f"{img.size[0]} x {img.size[1]} px",LG,LW)
        exif=img._getexif()
        if exif:
            section("EXIF DATA",LG)
            for tid,val in exif.items():
                tag=TAGS.get(tid,tid)
                if tag=="GPSInfo" and isinstance(val,dict):
                    section("GPS DATA",LY)
                    for gt,gv in val.items():
                        print(LY+f"  {str(GPSTAGS.get(gt,gt)):<28}"+LW+f" {gv}")
                else:
                    print(LG+f"  {str(tag):<28}"+LW+f" {str(val)[:80]}")
        else: print(LG+"  No EXIF metadata found.")
    except Exception as e: print(LR+f"  Error: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑱ PUBLIC CAMERA FEEDS
# ──────────────────────────────────────────────

def public_cameras():
    show_logo("cam")
    print(LR+"  Searches for publicly indexed / accessible camera feeds.\n")
    location=input(LC+"  Location (city/country, leave blank to skip) > ").strip()
    section("SHODAN CAMERA SEARCHES",LR)
    queries=[
        ("Webcams generic",   "has_screenshot:true port:80"),
        ("Axis cameras",      "Axis title:Live"),
        ("Hikvision cameras", "server:Hikvision-Webs"),
        ("RTSP streams",      "port:554 has_screenshot:true"),
        ("Port 8080 cams",    "port:8080 has_screenshot:true"),
    ]
    for name,q in queries:
        full_q=q+(f" city:{location}" if location else "")
        print(LR+f"  {name:<28}"+LW+f" https://www.shodan.io/search?query={qenc(full_q)}")
    section("GOOGLE DORKS",LR)
    dorks=[
        ("Axis live view",  'intitle:"Live View / - AXIS"'),
        ("Network camera",  'intitle:"Network Camera" inurl:main.cgi'),
        ("Webcam index",    'intitle:"webcam" inurl:"view/index.shtml"'),
        ("Traffic cams",    'intitle:"traffic camera" inurl:"cam"'),
    ]
    for name,dork in dorks:
        full=dork+(f' "{location}"' if location else "")
        print(LR+f"  {name:<28}"+LW+f" https://www.google.com/search?q={qenc(full)}")
    section("PUBLIC CAMERA DIRECTORIES",LR)
    for name,lnk in [
        ("Insecam",         "http://www.insecam.org/"),
        ("EarthCam",        "https://www.earthcam.com/"),
        ("Windy cams",      "https://www.windy.com/"),
        ("Camstreamer",     "https://app.camstreamer.com/"),
        ("Opentopia",       "http://www.opentopia.com/webcam/"),
    ]: link(name,lnk,LR)
    pause()

# ──────────────────────────────────────────────
#  ⑲ ASN / BGP
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
            row("RIR",d.get("rir_allocation",{}).get("rir_name","N/A"),LC,LW)
        except Exception as e: print(LR+f"  Failed: {e}")
    pause()

# ──────────────────────────────────────────────
#  ⑳ WAYBACK MACHINE
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

# ──────────────────────────────────────────────
#  ㉑ WAYBACK URL EXTRACTOR
# ──────────────────────────────────────────────

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
#  ㉒ PROFILE BUILDER
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
        ("Spokeo",        f"https://www.spokeo.com/search?q={enc_name}"),
        ("WhitePages",    f"https://www.whitepages.com/name/{enc_name}"),
        ("ZSearcher.fr",  f"https://zsearcher.fr/search?q={enc_name}"),
        ("OathNet.org",   f"https://oathnet.org/search?q={enc_name}"),
    ]: link(n,l,LM)
    if username:
        section("USERNAME QUICK LINKS",LM)
        for site,tpl in SITES[:15]:
            print(LM+f"  {site:<20}"+LW+f" {tpl.format(username)}")
    pause()

# ──────────────────────────────────────────────
#  ㉓ SHODAN LINKS
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
        ("BinaryEdge", f"https://app.binaryedge.io/services/query?query={e}"),
        ("FOFA",       f"https://fofa.info/result?qbase64={base64.b64encode(target.encode()).decode()}"),
        ("OTX",        f"https://otx.alienvault.com/indicator/domain/{target}"),
    ]: link(name,lnk,LC)
    pause()

# ──────────────────────────────────────────────
#  ㉔ QUICK RECON
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
        row("HSTS","present" if r.headers.get("Strict-Transport-Security") else "MISSING",LG,
            LG if r.headers.get("Strict-Transport-Security") else LR)
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
        ("Dork",      f"https://www.google.com/search?q=site:{domain}"),
        ("ZSearcher", f"https://zsearcher.fr/search?q={e}"),
        ("OathNet",   f"https://oathnet.org/search?q={e}"),
    ]: link(name,lnk,LC)
    pause()

# ──────────────────────────────────────────────
#  ㉕ NETWORK INFO
# ──────────────────────────────────────────────

def network_info():
    show_logo("geo")
    spinner("Gathering info",0.8,LG)
    section("LOCAL MACHINE",LG)
    hn=socket.gethostname(); lip=socket.gethostbyname(hn)
    row("Hostname",hn,LG,LW); row("Local IP",lip,LG,LW)
    row("Platform",platform.system()+" "+platform.release(),LG,LW)
    row("Python",sys.version.split()[0],LG,LW)
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
#  ㉖ ROBOTS / SITEMAP
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
#  ㉗ PASTE SEARCH
# ──────────────────────────────────────────────

def paste_search():
    show_logo("user")
    q=input(LM+"  Search term > ").strip()
    e=qenc(q)
    section("PASTE SEARCH LINKS",LM)
    for name,lnk in [
        ("Google Pastebin", f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22"),
        ("Google Gist",     f"https://www.google.com/search?q=site:gist.github.com+%22{e}%22"),
        ("Psbdmp",          f"https://psbdmp.ws/api/search/{e}"),
        ("Grep.app",        f"https://grep.app/search?q={e}"),
        ("GitHub code",     f"https://github.com/search?q={e}&type=code"),
        ("Rentry",          f"https://www.google.com/search?q=site:rentry.co+%22{e}%22"),
    ]: link(name,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  ㉘ FILE / DOC OSINT
# ──────────────────────────────────────────────

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

# ──────────────────────────────────────────────
#  ㉙ SOCIAL MEDIA SEARCH
# ──────────────────────────────────────────────

def social_search():
    show_logo("user")
    q=input(LM+"  Name / username / hashtag > ").strip()
    e=qenc(q)
    section("SOCIAL MEDIA SEARCH LINKS",LM)
    for plat,lnk in [
        ("Twitter/X search",    f"https://twitter.com/search?q={e}&f=live"),
        ("Instagram tags",      f"https://www.instagram.com/explore/tags/{e}/"),
        ("TikTok",              f"https://www.tiktok.com/search?q={e}"),
        ("Facebook",            f"https://www.facebook.com/search/top/?q={e}"),
        ("LinkedIn people",     f"https://www.linkedin.com/search/results/people/?keywords={e}"),
        ("Reddit",              f"https://www.reddit.com/search/?q={e}"),
        ("YouTube",             f"https://www.youtube.com/results?search_query={e}"),
        ("Pinterest",           f"https://www.pinterest.com/search/pins/?q={e}"),
        ("Twitch",              f"https://www.twitch.tv/search?term={e}"),
        ("Telegram",            f"https://t.me/s/{q}"),
        ("Discord (Google)",    f"https://www.google.com/search?q=site:discord.com+%22{e}%22"),
        ("Snapchat",            f"https://www.snapchat.com/add/{q}"),
    ]: link(plat,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  ㉚ DARK WEB SEARCH LINKS
# ──────────────────────────────────────────────

def darkweb_search():
    show_logo("breach")
    print(LR+"  Clearnet search engines that index .onion content.\n")
    q=input(LC+"  Search term > ").strip()
    e=qenc(q)
    section("DARK WEB SEARCH ENGINES",LR)
    for name,lnk in [
        ("Ahmia (clearnet)", f"https://ahmia.fi/search/?q={e}"),
        ("DarkSearch",       f"https://darksearch.io/search?query={e}"),
        ("Onion Search",     f"https://onionsearchengine.com/search.php?q={e}"),
        ("DeHashed",         f"https://dehashed.com/search?query={e}"),
        ("IntelX",           f"https://intelx.io/?s={e}"),
        ("Psbdmp",           f"https://psbdmp.ws/api/search/{e}"),
    ]: link(name,lnk,LR)
    pause()

# ──────────────────────────────────────────────
#  ㉛ CVE / VULN SEARCH
# ──────────────────────────────────────────────

def vuln_search():
    show_logo("port")
    q=input(LR+"  Software / CVE ID > ").strip()
    e=qenc(q)
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

# ──────────────────────────────────────────────
#  ㉜ OSINT FRAMEWORK NAVIGATOR
# ──────────────────────────────────────────────

def osint_framework():
    show_logo("user")
    section("KEY OSINT RESOURCES",LM)
    for name,lnk in [
        ("OSINT Framework",   "https://osintframework.com"),
        ("IntelTechniques",   "https://inteltechniques.com/tools/index.html"),
        ("ZSearcher.fr",      "https://zsearcher.fr/"),
        ("OathNet.org",       "https://oathnet.org/"),
        ("Shodan",            "https://www.shodan.io"),
        ("Censys",            "https://search.censys.io"),
        ("HaveIBeenPwned",    "https://haveibeenpwned.com"),
        ("URLScan.io",        "https://urlscan.io"),
        ("VirusTotal",        "https://www.virustotal.com"),
        ("Wayback Machine",   "https://web.archive.org"),
        ("BGPView",           "https://bgpview.io"),
        ("Grep.app",          "https://grep.app"),
        ("DeHashed",          "https://dehashed.com"),
        ("IntelX",            "https://intelx.io"),
        ("LeakIX",            "https://leakix.net"),
        ("GrayHatWarfare",    "https://grayhatwarfare.com"),
        ("Maltego",           "https://www.maltego.com"),
        ("Spiderfoot",        "https://www.spiderfoot.net"),
        ("OTX AlienVault",    "https://otx.alienvault.com"),
        ("Hunter.io",         "https://hunter.io"),
    ]: link(name,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  ㉝ ARCHIVE / SCREENSHOT LINKS
# ──────────────────────────────────────────────

def archive_links():
    show_logo("geo")
    url=input(LG+"  URL > ").strip()
    if not url.startswith("http"): url="https://"+url
    e=qenc(url)
    section("ARCHIVE LINKS",LG)
    for name,lnk in [
        ("Wayback Machine", f"https://web.archive.org/web/*/{url}"),
        ("Google Cache",    f"https://webcache.googleusercontent.com/search?q=cache:{url}"),
        ("Archive.ph",      f"https://archive.ph/{url}"),
        ("TimeTravel",      f"http://timetravel.mementoweb.org/timemap/link/{url}"),
    ]: link(name,lnk,LG)
    section("SCREENSHOT SERVICES",LG)
    for name,lnk in [
        ("ScreenshotMachine",f"https://www.screenshotmachine.com/?url={e}"),
        ("PagePeeker",       f"https://pagepeeker.com/v2/thumbs.php?size=x&url={e}"),
        ("Thumbnail.ws",     f"https://thumbnail.ws/api/thumbnail.png?url={e}&width=1280"),
    ]: link(name,lnk,LG)
    pause()

# ──────────────────────────────────────────────
#  ㉞ ADVANCED DORK BUILDER
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
    section("YOUR DORK",LY)
    print(LY+f"  {dork}")
    print(LW+f"\n  Search: https://www.google.com/search?q={qenc(dork)}")
    pause()

# ──────────────────────────────────────────────
#  ㉟ URL REDIRECT TRACER
# ──────────────────────────────────────────────

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

# ──────────────────────────────────────────────
#  ㊱ PUBLIC RECORDS SEARCH
# ──────────────────────────────────────────────

def public_records():
    show_logo("user")
    q=input(LM+"  Name / email / username > ").strip()
    e=qenc(q)
    section("PUBLIC RECORD SEARCH LINKS",LM)
    for name,lnk in [
        ("Spokeo",           f"https://www.spokeo.com/search?q={e}"),
        ("PeopleFinder",     f"https://www.peoplefinder.com/people?q={e}"),
        ("TruePeopleSearch", f"https://www.truepeoplesearch.com/results?name={e}"),
        ("WhitePages",       f"https://www.whitepages.com/name/{e}"),
        ("FastPeopleSearch", f"https://www.fastpeoplesearch.com/name/{e}"),
        ("LinkedIn",         f"https://www.google.com/search?q=site:linkedin.com+%22{e}%22"),
        ("Twitter",          f"https://twitter.com/search?q=%22{e}%22"),
        ("Facebook",         f"https://www.facebook.com/search/top/?q={e}"),
        ("ZSearcher.fr",     f"https://zsearcher.fr/search?q={e}"),
        ("OathNet.org",      f"https://oathnet.org/search?q={e}"),
    ]: link(name,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  ㊲ REVERSE IMAGE SEARCH
# ──────────────────────────────────────────────

def reverse_image():
    show_logo("user")
    url=input(LM+"  Image URL > ").strip()
    if not url: pause(); return
    e=qenc(url)
    section("REVERSE IMAGE SEARCH LINKS",LM)
    for name,lnk in [
        ("Google Images",  f"https://www.google.com/searchbyimage?image_url={e}"),
        ("Bing Visual",    f"https://www.bing.com/images/search?q=imgurl:{e}&iss=sbi"),
        ("Yandex Images",  f"https://yandex.com/images/search?url={e}&rpt=imageview"),
        ("TinEye",         f"https://tineye.com/search?url={e}"),
        ("SauceNAO",       f"https://saucenao.com/search.php?url={e}"),
        ("IQDB",           f"https://iqdb.org/?url={e}"),
    ]: link(name,lnk,LM)
    pause()

# ──────────────────────────────────────────────
#  CONTACT
# ──────────────────────────────────────────────

def contact():
    clear()
    print(LG+r"""
   ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗  ██████╗████████╗
  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝
  ██║     ██║   ██║██╔██╗ ██║   ██║   ███████║██║        ██║
  ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║        ██║
  ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╗   ██║
   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝
                                                  By camzzz""")
    print(); print(LG+"  "+"─"*68); print()
    row("Discord","cameleonmortis",   LC,LW)
    row("GitHub", "https://github.com/cameleonnbss/50-multi-tool",LC,LW)
    print()
    for line in CAMZZZ_LINES: rainbow(line)
    print(); pause()

# ──────────────────────────────────────────────
#  FSOCIETY
# ──────────────────────────────────────────────

def fsociety():
    clear(); matrix_rain(4,72)
    print(LG+r"""
fsociety                                             By camzzz
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                `XER0'""")
    print()
    for line in CAMZZZ_LINES: rainbow(line)
    pause()

# ──────────────────────────────────────────────
#  MENU
# ──────────────────────────────────────────────


# ──────────────────────────────────────────────
#  PHONE SOCIAL SCANNER  (from AltTool menu 12)
# ──────────────────────────────────────────────

def phone_social_scanner():
    show_logo("phone")
    print(LC + "  Scans 20+ platforms for accounts linked to a phone number.")
    print(LC + "  Uses public search — no API keys needed.\n")

    number = input(LC + "  Phone number (with + country code) > ").strip()
    if not number: pause(); return

    digits  = re.sub(r"\D", "", number)
    no_plus = number.lstrip("+")
    e       = qenc(number)
    d       = qenc(digits)

    # detect country
    info = None; matched = ""
    for prefix in sorted(PHONE_DB.keys(), key=lambda x: -len(x)):
        if number.startswith(prefix):
            info = PHONE_DB[prefix]; matched = prefix; break

    section("NUMBER INFO", LC)
    row("Number",      number,                    LC, LW)
    row("Country code",matched or "Unknown",       LC, LW)
    if info:
        row("Country", info["country"],            LC, LG)
        row("Region",  info["region"],             LC, LG)
        row("Timezone",info["tz"],                 LC, LW)

    section("PLATFORM SEARCH LINKS", LC)
    print(LC + "  Open these links to check if the number is linked to an account:\n")

    platforms = [
        # Messaging
        ("WhatsApp",          f"https://wa.me/{digits}",                           LG),
        ("Telegram",          f"https://t.me/{no_plus}",                           LC),
        ("Signal (Google)",   f"https://www.google.com/search?q=signal+%22{e}%22", LW),
        ("Viber (Google)",    f"https://www.google.com/search?q=viber+%22{e}%22",  LW),
        # Social
        ("Facebook",          f"https://www.facebook.com/search/top/?q={e}",       LC),
        ("Twitter/X",         f"https://twitter.com/search?q=%22{e}%22&f=live",    LC),
        ("Instagram (Google)",f"https://www.google.com/search?q=site:instagram.com+%22{e}%22", LW),
        ("TikTok (Google)",   f"https://www.google.com/search?q=site:tiktok.com+%22{e}%22",    LW),
        ("Snapchat (Google)", f"https://www.google.com/search?q=site:snapchat.com+%22{e}%22",  LW),
        ("LinkedIn",          f"https://www.linkedin.com/search/results/people/?keywords={e}", LC),
        ("Reddit (Google)",   f"https://www.google.com/search?q=site:reddit.com+%22{e}%22",    LW),
        ("Discord (Google)",  f"https://www.google.com/search?q=site:discord.com+%22{e}%22",   LW),
        ("Telegram (Google)", f"https://www.google.com/search?q=site:t.me+%22{e}%22",          LW),
        # Reverse lookup
        ("TrueCaller",        f"https://www.truecaller.com/search/fr/{d}",          LY),
        ("Sync.me",           f"https://sync.me/search/?number={e}",                LY),
        ("NumLookup",         f"https://www.numlookup.com/?number={e}",             LY),
        ("Spokeo",            f"https://www.spokeo.com/phone/{d}",                  LY),
        ("WhitePages",        f"https://www.whitepages.com/phone/{d}",              LY),
        ("FastPeopleSearch",  f"https://www.fastpeoplesearch.com/phone/{d}",        LY),
        ("TruePeopleSearch",  f"https://www.truepeoplesearch.com/resultsphonesearch?phoneno={d}", LY),
        # Dating / classifieds
        ("Craigslist (Google)",f"https://www.google.com/search?q=site:craigslist.org+%22{e}%22", LM),
        ("Leboncoin (Google)", f"https://www.google.com/search?q=site:leboncoin.fr+%22{e}%22",   LM),
        ("Badoo (Google)",     f"https://www.google.com/search?q=site:badoo.com+%22{e}%22",      LM),
        # Leaks
        ("ZSearcher.fr",       f"https://zsearcher.fr/search?q={d}",               LR),
        ("OathNet.org",        f"https://oathnet.org/search?q={e}",                LR),
        ("DeHashed",           f"https://dehashed.com/search?query={e}",           LR),
        ("IntelX",             f"https://intelx.io/?s={e}",                        LR),
        ("Google (number)",    f"https://www.google.com/search?q=%22{e}%22",       LW),
        ("Google (digits)",    f"https://www.google.com/search?q=%22{d}%22",       LW),
        ("Pastebin (Google)",  f"https://www.google.com/search?q=site:pastebin.com+%22{e}%22", LW),
        ("GitHub code",        f"https://github.com/search?q={e}&type=code",       LW),
    ]

    cats = {
        "MESSAGING": platforms[:4],
        "SOCIAL MEDIA": platforms[4:13],
        "REVERSE LOOKUP": platforms[13:20],
        "DATING / CLASSIFIEDS": platforms[20:23],
        "BREACH / LEAK DBs": platforms[23:],
    }
    for cat, items in cats.items():
        print(col_cat := LC, end="")
        print(f"\n  ── {cat} {'─'*(52-len(cat))}")
        for name, url, col in items:
            print(col + f"  {name:<28}" + LW + f" {url}")

    section("OSINT TOOLS FOR PHONE", LC)
    for name, lnk in [
        ("PhoneInfoga (local tool)", "https://github.com/sundowndev/phoneinfoga"),
        ("Ignorant (local tool)",    "https://github.com/megadose/ignorant"),
        ("Moriarty-Project",         "https://github.com/AzizKpln/Moriarty-Project"),
    ]: link(name, lnk, LG)
    pause()


# ──────────────────────────────────────────────
#  EMAIL ACCOUNT CHECKER  (AltTool menu 13)
# ──────────────────────────────────────────────

def email_account_checker():
    show_logo("mail")
    print(LM + "  Checks which platforms have an account for this email.")
    print(LM + "  Uses password-reset endpoints — read-only, no login.\n")

    email = input(LM + "  Email address > ").strip()
    if "@" not in email: print(LR + "  Invalid email."); pause(); return

    sites = {
        "Facebook":   "https://www.facebook.com/recover/initiate",
        "Twitter":    "https://twitter.com/account/begin_password_reset",
        "Instagram":  "https://www.instagram.com/accounts/password/reset/",
        "Snapchat":   "https://accounts.snapchat.com/accounts/password/reset",
        "Pinterest":  "https://www.pinterest.com/reset/",
        "TikTok":     "https://www.tiktok.com/login/forgot-password",
        "Reddit":     "https://www.reddit.com/password",
        "Tumblr":     "https://www.tumblr.com/login/forgot",
        "YouTube":    "https://www.youtube.com/account_recovery",
        "GitHub":     "https://github.com/password_reset",
        "LinkedIn":   "https://www.linkedin.com/uas/request-password-reset",
        "Discord":    "https://discord.com/api/v9/auth/forgot",
        "Spotify":    "https://accounts.spotify.com/en/password-reset",
        "Netflix":    "https://www.netflix.com/password",
        "Amazon":     "https://www.amazon.com/ap/forgotpassword",
        "Microsoft":  "https://account.live.com/password/reset",
        "Apple":      "https://iforgot.apple.com/password/verify/appleid",
        "Dropbox":    "https://www.dropbox.com/forgot",
        "Twitch":     "https://www.twitch.tv/user/password_reset",
        "Steam":      "https://store.steampowered.com/login/forgotpassword",
    }

    bar("  Scanning platforms", 30, 0.012, LM, M)
    print(LM + f"\n  Checking {len(sites)} platforms for '{email}'...\n")

    found = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for site, reset_url in sites.items():
        try:
            resp = requests.post(reset_url, data={"email": email},
                                 timeout=5, headers=headers,
                                 allow_redirects=True)
            text = resp.text.lower()
            keywords = ["sent", "email", "recovery", "reset",
                        "check your email", "verify", "we've sent"]
            if any(k in text for k in keywords):
                print(LG + f"  [+]  {site:<20}" + LW + " Account likely exists")
                found.append(site)
            else:
                print(DIM + LW + f"  [ ]  {site}")
        except Exception:
            print(DIM + LW + f"  [?]  {site}")

    section(f"RESULTS — {len(found)} ACCOUNT(S) FOUND", LM)
    if found:
        for s in found:
            print(LG + f"  ✓  {s}")
    else:
        print(LM + "  No accounts found via password-reset method.")

    section("BREACH SEARCH LINKS", LM)
    e = qenc(email)
    for name, lnk in [
        ("ZSearcher.fr",    f"https://zsearcher.fr/search?q={e}"),
        ("OathNet.org",     f"https://oathnet.org/search?q={e}"),
        ("HaveIBeenPwned",  f"https://haveibeenpwned.com/account/{e}"),
        ("DeHashed",        f"https://dehashed.com/search?query={e}"),
        ("IntelX",          f"https://intelx.io/?s={e}"),
    ]: link(name, lnk, LM)
    pause()


# ──────────────────────────────────────────────
#  WIFI SCANNER  (AltTool menu 26)
# ──────────────────────────────────────────────

def wifi_scanner():
    show_logo("geo")
    print(LY + "  Scans nearby WiFi networks and analyses security.\n")

    import platform as _plat, subprocess as _sub

    os_type = _plat.system()
    networks = []

    spinner("Scanning WiFi networks", 1.5, LY)

    try:
        if os_type == "Windows":
            result = _sub.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True, text=True, timeout=12)
            lines = result.stdout.split("\n")
            current = None
            for line in lines:
                line = line.strip()
                if line.startswith("SSID") and ":" in line and "BSSID" not in line:
                    if current and current.get("ssid"):
                        networks.append(current)
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        current = {"ssid": ssid, "bssid": "N/A",
                                   "signal": "N/A", "channel": "N/A",
                                   "authentication": "N/A"}
                elif current:
                    for key, prefix in [("authentication","Authentication"),
                                        ("signal","Signal"),
                                        ("channel","Channel"),
                                        ("bssid","BSSID")]:
                        if prefix in line and ":" in line:
                            current[key] = line.split(":", 1)[1].strip()
            if current and current.get("ssid"):
                networks.append(current)

        elif os_type == "Linux":
            result = _sub.run(
                ["nmcli", "-t", "-f", "SSID,SIGNAL,CHAN,SECURITY",
                 "dev", "wifi", "list"],
                capture_output=True, text=True, timeout=10)
            for line in result.stdout.strip().split("\n"):
                if line:
                    p = line.split(":")
                    networks.append({
                        "ssid":           p[0] if p[0] else "Hidden",
                        "signal":         p[1] + "%" if len(p) > 1 else "N/A",
                        "channel":        p[2] if len(p) > 2 else "N/A",
                        "authentication": p[3] if len(p) > 3 else "N/A",
                    })

        elif os_type == "Darwin":
            airport = ("/System/Library/PrivateFrameworks/"
                       "Apple80211.framework/Versions/Current/Resources/airport")
            result = _sub.run([airport, "-s"],
                              capture_output=True, text=True, timeout=10)
            for line in result.stdout.split("\n")[1:]:
                if line.strip():
                    p = line.split()
                    if len(p) >= 3:
                        networks.append({
                            "ssid":           p[0],
                            "signal":         p[2],
                            "channel":        p[3] if len(p) > 3 else "N/A",
                            "authentication": " ".join(p[6:]) if len(p) > 6 else "N/A",
                        })
    except Exception as ex:
        print(LR + f"  Scan error: {ex}")

    if not networks:
        print(LR + "  No networks found. Make sure WiFi is enabled.")
        pause(); return

    section(f"FOUND {len(networks)} NETWORKS", LY)
    print(LY + f"  {'#':<4} {'SSID':<30} {'Signal':<12} {'Channel':<10} {'Security'}")
    print(LY + "  " + "─"*68)
    for i, net in enumerate(networks, 1):
        ssid  = net.get("ssid","?")[:28]
        sig   = net.get("signal","?")
        chan  = str(net.get("channel","?"))
        auth  = net.get("authentication","?")[:20]
        col   = LR if "OPEN" in auth.upper() or auth.upper() in ["","NONE"] else LG
        print(LY + f"  {i:<4} {ssid:<30} {sig:<12} {chan:<10} " + col + auth)

    section("SECURITY ANALYSIS", LY)
    open_nets  = [n["ssid"] for n in networks if
                  "OPEN" in n.get("authentication","").upper() or
                  n.get("authentication","").upper() in ["","NONE","N/A"]]
    wep_nets   = [n["ssid"] for n in networks if "WEP"  in n.get("authentication","").upper()]
    wpa3_nets  = [n["ssid"] for n in networks if "WPA3" in n.get("authentication","").upper()]
    wpa2_nets  = [n["ssid"] for n in networks if "WPA2" in n.get("authentication","").upper()]

    row("Total networks",    len(networks),   LY, LW)
    row("Open (dangerous)",  len(open_nets),  LY, LR if open_nets  else LG)
    row("WEP (weak)",        len(wep_nets),   LY, LR if wep_nets   else LG)
    row("WPA2",              len(wpa2_nets),  LY, LG)
    row("WPA3",              len(wpa3_nets),  LY, LG)

    if open_nets:
        print(LR + "\n  Open networks:")
        for s in open_nets[:5]: print(LR + f"    - {s}")

    secure = len(wpa2_nets) + len(wpa3_nets)
    score  = int(secure / len(networks) * 100) if networks else 0
    print(LY + f"\n  Security score: {score}/100  " +
          (LG + "Good" if score >= 70 else LY + "Medium" if score >= 40 else LR + "Poor"))
    pause()


# ──────────────────────────────────────────────
#  WEB VULNERABILITY SCANNER  (AltTool menu 25)
#  Subset of the 40-scan AltScan — no active attacks
# ──────────────────────────────────────────────

def web_vuln_scanner():
    show_logo("port")
    print(LR + "  Passive web vulnerability scanner — 20 checks.\n")

    url = input(LR + "  Target URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url

    results = []

    def chk(label, fn):
        try:
            r = fn()
            status, detail = r if isinstance(r, tuple) else ("INFO", r)
        except Exception as ex:
            status, detail = "ERR", str(ex)[:60]
        col = LR if status == "VULN" else LY if status == "WARN" else LG
        print(col + f"  [{status:<4}]  {label:<35}" + LW + f" {str(detail)[:60]}")
        results.append((label, status, detail))

    spinner(f"Connecting to {url}", 0.8, LR)

    try:
        resp = requests.get(url, timeout=10, verify=False,
                            headers={"User-Agent": "Mozilla/5.0"})
    except Exception as ex:
        print(LR + f"  Cannot reach target: {ex}"); pause(); return

    hdrs = resp.headers
    text = resp.text.lower()

    section("SECURITY HEADERS", LR)
    for hdr, label in [
        ("Strict-Transport-Security",   "HSTS"),
        ("Content-Security-Policy",     "CSP"),
        ("X-Frame-Options",             "X-Frame-Options"),
        ("X-Content-Type-Options",      "X-Content-Type-Options"),
        ("X-XSS-Protection",            "X-XSS-Protection"),
        ("Referrer-Policy",             "Referrer-Policy"),
        ("Permissions-Policy",          "Permissions-Policy"),
    ]:
        present = hdr in hdrs
        status = "OK  " if present else "WARN"
        col    = LG if present else LY
        print(col + f"  [{status}]  {label:<35}" +
              LW + f" {hdrs.get(hdr, 'MISSING')[:60]}")
        results.append((label, status, hdrs.get(hdr, "MISSING")))

    section("SERVER INFO EXPOSURE", LR)
    for hdr in ["Server", "X-Powered-By", "X-AspNet-Version", "X-Generator"]:
        val = hdrs.get(hdr)
        if val:
            print(LY + f"  [WARN]  {hdr:<35}" + LW + f" {val[:60]}")
            results.append((hdr, "WARN", val))

    section("SENSITIVE FILES", LR)
    base = url.rstrip("/")
    for path in ["/.env", "/.git/config", "/robots.txt", "/phpinfo.php",
                 "/wp-config.php", "/.htaccess", "/config.php",
                 "/backup.sql", "/admin", "/phpmyadmin"]:
        try:
            r2 = requests.get(base + path, timeout=5, verify=False,
                              headers={"User-Agent": "Mozilla/5.0"})
            if r2.status_code == 200 and len(r2.text) > 10:
                print(LR + f"  [VULN]  Sensitive file exposed: {path}")
                results.append((path, "VULN", f"HTTP 200 — {len(r2.text)} bytes"))
        except Exception: pass

    section("TECHNOLOGY DETECTION", LR)
    techs = {
        "WordPress": ["wp-content","wp-includes"],
        "Drupal":    ["drupal","sites/default"],
        "Joomla":    ["joomla","com_content"],
        "Shopify":   ["shopify"],
        "React":     ["react","__react"],
        "Vue.js":    ["vue.js","v-"],
        "Angular":   ["ng-","angular"],
        "jQuery":    ["jquery"],
        "Bootstrap": ["bootstrap"],
        "PHP":       [".php","php"],
        "Django":    ["csrfmiddlewaretoken"],
        "Laravel":   ["laravel_session"],
        "Nginx":     ["nginx"],
        "Apache":    ["apache"],
        "Cloudflare":["cf-ray","cloudflare"],
    }
    found_techs = []
    hdrs_str = str(hdrs).lower()
    for tech, sigs in techs.items():
        if any(s in text or s in hdrs_str for s in sigs):
            found_techs.append(tech)
    if found_techs:
        print(LC + "  Detected: " + LW + ", ".join(found_techs))

    section("DIRECTORY LISTING", LR)
    for d in ["/", "/uploads/", "/images/", "/files/", "/backup/"]:
        try:
            r3 = requests.get(base + d, timeout=5, verify=False,
                              headers={"User-Agent": "Mozilla/5.0"})
            if any(ind in r3.text for ind in
                   ["Index of", "Directory listing", "Parent Directory"]):
                print(LR + f"  [VULN]  Directory listing enabled: {d}")
                results.append((d, "VULN", "Directory listing"))
        except Exception: pass

    section("SUMMARY", LR)
    vulns = [r for r in results if r[1] == "VULN"]
    warns = [r for r in results if r[1] == "WARN"]
    row("VULN findings", len(vulns), LR, LR)
    row("WARN findings", len(warns), LY, LY)
    row("Checks run",    len(results), LC, LW)

    # export
    try:
        save = input(LY + "\n  Save report to txt? [y/N] > ").strip().lower()
        if save == "y":
            fname = f"vuln_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname, "w") as f:
                f.write(f"Scan: {url}\nDate: {datetime.now()}\n{'='*60}\n")
                for label, status, detail in results:
                    f.write(f"[{status}] {label}: {detail}\n")
            print(LG + f"  Saved to {fname}")
    except Exception: pass
    pause()


# ──────────────────────────────────────────────
#  ADVANCED SECURITY / FIREWALL DETECTOR  (AltTool menu 27)
# ──────────────────────────────────────────────

def firewall_detector():
    show_logo("port")
    print(LC + "  Detects WAF, CDN, bot protection, SSL info, rate limiting.\n")

    url = input(LC + "  Target URL > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url

    from urllib.parse import urlparse as _urlparse
    hostname = _urlparse(url).netloc

    spinner(f"Scanning {url}", 1.5, LC)

    findings = {
        "waf": [], "cdn": [], "bot": [],
        "security_headers": {}, "server": [],
        "ssl": [], "dns": [], "rate": [],
    }

    # ── Header scan
    try:
        methods = ["GET", "OPTIONS"]
        all_hdrs = {}
        for method in methods:
            try:
                r = requests.request(method, url, timeout=8,
                                     headers={"User-Agent": "Mozilla/5.0"})
                all_hdrs.update(r.headers)
            except Exception: pass

        WAF_SIGS = {
            "Cloudflare":   ["cf-ray","cf-cache-status","__cf_bm"],
            "AWS WAF":      ["x-amzn-requestid","x-amz-cf-id"],
            "Akamai":       ["akamai","x-akamai"],
            "Imperva":      ["x-iinfo","incap_ses","visid_incap"],
            "Sucuri":       ["x-sucuri-id","x-sucuri-cache"],
            "ModSecurity":  ["mod_security"],
            "F5 BIG-IP":    ["f5","bigip","x-wa-info"],
            "Barracuda":    ["barra","bni__"],
            "FortiWeb":     ["fortigate","fortiweb"],
            "Cloudfront":   ["x-amz-cf","cloudfront"],
            "Fastly":       ["fastly","x-served-by"],
            "Varnish":      ["x-varnish"],
            "Wordfence":    ["wordfence"],
            "DDoS-Guard":   ["ddos-guard"],
        }
        CDN_SIGS = {
            "Cloudflare":  ["cloudflare","cf-"],
            "Fastly":      ["fastly"],
            "Akamai":      ["akamai"],
            "CloudFront":  ["cloudfront","x-amz"],
            "MaxCDN":      ["maxcdn"],
            "BunnyCDN":    ["bunnycdn"],
            "Sucuri":      ["sucuri"],
        }
        SEC_HDRS = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy":   "CSP",
            "X-Frame-Options":           "Clickjacking protection",
            "X-Content-Type-Options":    "MIME sniffing protection",
            "X-XSS-Protection":          "XSS filter",
            "Referrer-Policy":           "Referrer policy",
        }

        for hdr, val in all_hdrs.items():
            hl = hdr.lower(); vl = str(val).lower()
            for waf, sigs in WAF_SIGS.items():
                if any(s in hl or s in vl for s in sigs):
                    if waf not in " ".join(findings["waf"]):
                        findings["waf"].append(f"{waf} (header: {hdr})")
            for cdn, sigs in CDN_SIGS.items():
                if any(s in hl or s in vl for s in sigs):
                    if cdn not in " ".join(findings["cdn"]):
                        findings["cdn"].append(f"{cdn} (header: {hdr})")
            for sh, desc in SEC_HDRS.items():
                if hdr.lower() == sh.lower():
                    findings["security_headers"][sh] = {"val": val, "desc": desc}
            if hdr.lower() in ["server","x-powered-by","x-generator"]:
                findings["server"].append(f"{hdr}: {val}")
    except Exception as ex:
        print(LR + f"  Header scan error: {ex}")

    # ── Bot protection
    try:
        r2 = requests.get(url, timeout=8,
                          headers={"User-Agent": "Mozilla/5.0"})
        page = r2.text.lower()
        BOT_SIGS = {
            "reCAPTCHA":    ["recaptcha","google.com/recaptcha"],
            "hCaptcha":     ["hcaptcha"],
            "Cloudflare Turnstile": ["turnstile","challenges.cloudflare.com"],
            "PerimeterX":   ["perimeterx","_px"],
            "DataDome":     ["datadome"],
        }
        for bp, sigs in BOT_SIGS.items():
            if any(s in page for s in sigs):
                findings["bot"].append(bp)
        if any(c in page for c in ["checking your browser","please wait","verifying you are human"]):
            findings["bot"].append("JS Challenge (generic)")
    except Exception: pass

    # ── SSL
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(8); s.connect((hostname, 443))
            cert = s.getpeercert()
        findings["ssl"].append(f"Protocol: {s.version()}")
        findings["ssl"].append(f"Cipher: {s.cipher()[0]}")
        subj = dict(x[0] for x in cert.get("subject",[]))
        if subj.get("commonName"):
            findings["ssl"].append(f"CN: {subj['commonName']}")
        findings["ssl"].append(f"Valid until: {cert.get('notAfter','N/A')}")
    except Exception as ex:
        findings["ssl"].append(f"SSL check failed: {ex}")

    # ── DNS
    try:
        ip = socket.gethostbyname(hostname)
        findings["dns"].append(f"IP: {ip}")
        try:
            rev = socket.gethostbyaddr(ip)
            findings["dns"].append(f"Reverse DNS: {rev[0]}")
        except Exception: pass
    except Exception: pass

    # ── Rate limiting quick test
    try:
        codes = []
        for _ in range(8):
            r3 = requests.get(url, timeout=4,
                              headers={"User-Agent": "Mozilla/5.0"})
            codes.append(r3.status_code)
            time.sleep(0.1)
        if 429 in codes:
            findings["rate"].append("Rate limiting active (429 detected)")
        elif codes.count(503) > 2:
            findings["rate"].append("Possible rate limiting (503 repeated)")
        else:
            findings["rate"].append("No rate limiting detected in quick test")
    except Exception: pass

    # ── Display
    clear()
    show_logo("port")
    print(LC + f"  Target: {url}")
    print(LC + f"  Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for cat, title, col in [
        ("waf",    "WAF / FIREWALL",        LR),
        ("cdn",    "CDN SERVICES",          LC),
        ("bot",    "BOT PROTECTION",        LM),
        ("server", "SERVER INFO",           LY),
        ("ssl",    "SSL / TLS",             LG),
        ("dns",    "DNS",                   LY),
        ("rate",   "RATE LIMITING",         LC),
    ]:
        section(title, col)
        items = findings[cat]
        if items:
            for item in items:
                print(col + f"  [+]  {item}")
        else:
            print(DIM + LW + "  None detected")

    section("SECURITY HEADERS", LC)
    all_sec = ["Strict-Transport-Security","Content-Security-Policy",
               "X-Frame-Options","X-Content-Type-Options",
               "X-XSS-Protection","Referrer-Policy"]
    for sh in all_sec:
        if sh in findings["security_headers"]:
            info = findings["security_headers"][sh]
            print(LG + f"  [OK]  {sh:<40}" + LW + f" {info['val'][:40]}")
        else:
            print(LR + f"  [!!]  {sh:<40}" + LW + " MISSING")

    # Score
    score = 0
    if findings["waf"]:   score += 30
    if findings["cdn"]:   score += 15
    if len(findings["security_headers"]) >= 4: score += 25
    elif len(findings["security_headers"]) > 0: score += 10
    if findings["ssl"]:   score += 15
    if findings["bot"]:   score += 10
    if "active" in str(findings["rate"]).lower(): score += 5
    score = min(score, 100)

    section(f"SECURITY SCORE: {score}/100", LG if score>=70 else LY if score>=40 else LR)
    bar_s = LG+"█"*int(score/5)+DIM+"░"*(20-int(score/5))
    print(f"  {bar_s}  " + (LG+"Excellent" if score>=80 else LY+"Good" if score>=60 else LR+"Needs improvement"))
    pause()


# ──────────────────────────────────────────────
#  FILE SCANNER  (AltTool menu 28)
# ──────────────────────────────────────────────

def file_scanner():
    show_logo("hash")
    print(LM + "  Scans a file for suspicious strings, high entropy,")
    print(LM + "  dangerous patterns, and calculates hashes.\n")

    filepath = input(LM + "  File path > ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(LR + "  File not found."); pause(); return

    spinner("Analysing file", 1.0, LM)

    report = {
        "path":      filepath,
        "size":      os.path.getsize(filepath),
        "md5":       "",
        "sha256":    "",
        "threats":   [],
        "warnings":  [],
    }

    # Hashes
    md5h = hashlib.md5(); sha256h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                md5h.update(chunk); sha256h.update(chunk)
        report["md5"]    = md5h.hexdigest()
        report["sha256"] = sha256h.hexdigest()
    except Exception as ex:
        print(LR + f"  Hash error: {ex}"); pause(); return

    section("FILE INFO", LM)
    row("Path",   filepath,            LM, LW)
    row("Size",   f"{report['size']:,} bytes", LM, LW)
    row("MD5",    report["md5"],       LM, LW)
    row("SHA256", report["sha256"],    LM, LW)

    # VirusTotal link
    print(LM + f"\n  VT check: https://www.virustotal.com/gui/file/{report['sha256']}")

    # String scan
    SUSPICIOUS = [
        b"cmd.exe", b"powershell", b"rundll32", b"regsvr32",
        b"WScript.Shell", b"Shell.Application", b"HKEY_",
        b"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
        b"CreateRemoteThread", b"VirtualAllocEx", b"WriteProcessMemory",
        b"ShellExecute", b"URLDownloadToFile", b"WinExec",
        b"system(", b"exec(", b"eval(", b"base64",
        b"encrypt", b"decrypt", b"ransom", b"bitcoin",
        b"keylog", b"password", b"credentials",
        b"wget ", b"curl ", b"chmod 777", b"/etc/passwd",
        b"DROP TABLE", b"SELECT * FROM", b"UNION SELECT",
        b"<script>", b"javascript:", b"onerror=",
    ]

    try:
        with open(filepath, "rb") as f:
            content = f.read()
        for sig in SUSPICIOUS:
            if sig in content:
                report["threats"].append(
                    f"Suspicious string: {sig.decode('utf-8', errors='ignore')}")
    except Exception as ex:
        report["warnings"].append(f"String scan error: {ex}")

    # Entropy check (high entropy = possibly packed/encrypted)
    try:
        import math
        sample = content[:65536]
        if sample:
            freq = [0] * 256
            for byte in sample: freq[byte] += 1
            entropy = -sum((c/len(sample)) * math.log2(c/len(sample))
                           for c in freq if c > 0)
            row("Entropy", f"{entropy:.2f}/8.0", LM,
                LR if entropy > 7.0 else LY if entropy > 6.0 else LG)
            if entropy > 7.0:
                report["threats"].append(f"Very high entropy ({entropy:.2f}) — possibly packed or encrypted")
            elif entropy > 6.0:
                report["warnings"].append(f"Elevated entropy ({entropy:.2f})")
    except Exception: pass

    # Extension check
    ext = os.path.splitext(filepath)[1].lower()
    dangerous_exts = [".exe",".dll",".sys",".scr",".bat",".cmd",
                      ".vbs",".ps1",".jar",".msi",".com"]
    if ext in dangerous_exts:
        report["warnings"].append(f"Potentially executable file type: {ext}")

    # Results
    section("SCAN RESULTS", LM)
    risk = "CRITICAL" if len(report["threats"]) >= 5 else \
           "HIGH"     if len(report["threats"]) >= 3 else \
           "MEDIUM"   if len(report["threats"]) >= 1 else \
           "LOW"      if report["warnings"] else "CLEAN"

    rcol = {
        "CRITICAL": LR, "HIGH": LR, "MEDIUM": LY,
        "LOW": LY, "CLEAN": LG
    }[risk]

    row("Risk level", risk, LM, rcol)
    row("Threats",    len(report["threats"]),  LM, LR if report["threats"] else LG)
    row("Warnings",   len(report["warnings"]), LM, LY if report["warnings"] else LG)

    if report["threats"]:
        section("THREATS DETECTED", LM)
        for i, t in enumerate(report["threats"], 1):
            print(LR + f"  [{i}]  {t}")

    if report["warnings"]:
        section("WARNINGS", LM)
        for i, w in enumerate(report["warnings"], 1):
            print(LY + f"  [{i}]  {w}")

    if risk == "CLEAN":
        print(LG + "\n  File appears clean based on static analysis.")

    # Save JSON
    try:
        save = input(LY + "\n  Save JSON report? [y/N] > ").strip().lower()
        if save == "y":
            fname = f"file_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            import json as _json
            with open(fname, "w") as f:
                _json.dump(report, f, indent=2)
            print(LG + f"  Saved to {fname}")
    except Exception: pass
    pause()


# ──────────────────────────────────────────────
#  ID / USERNAME TRACKER  (AltTool menu 14)
# ──────────────────────────────────────────────

def id_tracker():
    show_logo("user")
    print(LM + "  Extended username/ID tracker — 40+ platforms.\n")

    user_id = input(LM + "  Username or ID > ").strip()
    if not user_id: pause(); return

    EXTENDED_SITES = SITES + [
        ("Xbox Live",   f"https://account.xbox.com/en-US/Profile?GamerTag={user_id}"),
        ("PlayStation", f"https://psnprofiles.com/{user_id}"),
        ("Fortnite",    f"https://fortnitetracker.com/profile/all/{user_id}"),
        ("DeviantArt",  f"https://www.deviantart.com/{user_id}"),
        ("Last.fm",     f"https://www.last.fm/user/{user_id}"),
        ("Mixcloud",    f"https://www.mixcloud.com/{user_id}"),
        ("Bandcamp",    f"https://{user_id}.bandcamp.com"),
        ("HackerOne",   f"https://hackerone.com/{user_id}"),
        ("Slack",       f"https://{user_id}.slack.com"),
        ("Blogger",     f"https://{user_id}.blogspot.com"),
    ]

    bar("  Preparing scan", 20, 0.012, LM, M)
    print(LM + f"\n  Scanning {len(EXTENDED_SITES)} platforms for '{user_id}'...\n")

    found = []
    def chk(item):
        name, url = item[0], item[1].format(user_id) if "{}" in item[1] else item[1]
        try:
            r = requests.get(url, timeout=7, allow_redirects=True,
                             headers={"User-Agent": "Mozilla/5.0"})
            return ("FOUND" if r.status_code == 200 else "·", name, url)
        except:
            return ("ERR", name, url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(chk, EXTENDED_SITES))

    for status, name, url in results:
        if status == "FOUND":
            print(LG + f"  [+]  {name:<22}" + LW + f" {url}")
            found.append(url)
        elif status == "ERR":
            print(DIM+C + f"  [?]  {name}")
        else:
            print(DIM+W + f"  [ ]  {name}")

    section(f"RESULTS  —  {len(found)} FOUND  /  {len(EXTENDED_SITES)} CHECKED", LM)
    pause()


# ──────────────────────────────────────────────
#  HTTP STRESS TESTER  (legitimate load test only)
# ──────────────────────────────────────────────

def http_stress_test():
    show_logo("port")
    print(LY + "  HTTP load / stress tester for YOUR OWN servers.")
    print(LY + "  Only use on infrastructure you own or have written permission to test.\n")

    url = input(LY + "  Target URL (your own server) > ").strip()
    if not url: pause(); return
    if not url.startswith("http"): url = "https://" + url

    try:
        n_threads = int(input(LY + "  Threads (default 10) > ").strip() or "10")
        n_req     = int(input(LY + "  Total requests (default 100) > ").strip() or "100")
    except Exception:
        n_threads, n_req = 10, 100

    confirm = input(LR + f"\n  Confirm you own {url} and have permission to test [yes/no] > ").strip().lower()
    if confirm != "yes":
        print(LY + "  Cancelled — only test your own servers."); pause(); return

    import threading as _thr
    stats = {"ok": 0, "fail": 0, "times": []}
    lock  = _thr.Lock()

    def worker(count):
        session = requests.Session()
        session.headers["User-Agent"] = "LoadTest/camzzz"
        for _ in range(count):
            t0 = time.perf_counter()
            try:
                r = session.get(url, timeout=5)
                with lock:
                    stats["ok"] += 1
                    stats["times"].append(time.perf_counter() - t0)
            except Exception:
                with lock:
                    stats["fail"] += 1

    per_thread = n_req // n_threads
    remain     = n_req  % n_threads
    start      = time.time()

    bar("  Sending requests", 30, 0.01, LY, Y)

    threads = []
    for i in range(n_threads):
        cnt = per_thread + (1 if i < remain else 0)
        t = _thr.Thread(target=worker, args=(cnt,))
        t.start(); threads.append(t)
    for t in threads: t.join()

    elapsed = time.time() - start
    section("RESULTS", LY)
    row("Total requests", n_req,          LY, LW)
    row("Success",        stats["ok"],    LY, LG)
    row("Failed",         stats["fail"],  LY, LR if stats["fail"] else LG)
    row("Duration",       f"{elapsed:.2f}s", LY, LW)
    row("Req/sec",        f"{n_req/elapsed:.0f}", LY, LW)
    if stats["times"]:
        avg = sum(stats["times"]) / len(stats["times"])
        row("Avg response",  f"{avg*1000:.1f}ms", LY, LW)
        row("Min response",  f"{min(stats['times'])*1000:.1f}ms", LY, LW)
        row("Max response",  f"{max(stats['times'])*1000:.1f}ms", LY, LW)
    pause()


# ──────────────────────────────────────────────
#  OSINT DORK GENERATOR  (AltTool menu 18 — enhanced)
# ──────────────────────────────────────────────

def osint_dork_builder():
    show_logo("dork")
    print(LY + "  Advanced OSINT dork builder — generates targeted Google dorks.\n")

    print(LY + "  Enter target info (leave blank to skip):")
    first    = input(LY + "  First name   > ").strip()
    last     = input(LY + "  Last name    > ").strip()
    username = input(LY + "  Username     > ").strip()
    email    = input(LY + "  Email        > ").strip()
    phone    = input(LY + "  Phone        > ").strip()
    domain   = input(LY + "  Domain/site  > ").strip()
    company  = input(LY + "  Company      > ").strip()
    city     = input(LY + "  City         > ").strip()

    dorks = []
    E = qenc

    names = []
    if first and last: names.append(f"{first} {last}")
    if first:          names.append(first)
    if last:           names.append(last)

    if names:
        for n in names:
            dorks += [
                (f"Name basic",          f'"{n}"'),
                (f"Name + company",      f'"{n}" "{company}"' if company else None),
                (f"Name + city",         f'"{n}" "{city}"'    if city    else None),
                (f"LinkedIn",            f'site:linkedin.com "{n}"'),
                (f"Twitter/X",           f'site:twitter.com "{n}"'),
                (f"Facebook",            f'site:facebook.com "{n}"'),
                (f"Instagram",           f'site:instagram.com "{n}"'),
                (f"GitHub",              f'site:github.com "{n}"'),
                (f"News",                f'"{n}" (news OR article OR press)'),
                (f"Resume/CV",           f'"{n}" (resume OR cv) filetype:pdf'),
            ]

    if username:
        dorks += [
            ("Username basic",       f'"{username}"'),
            ("Username profile",     f'"{username}" (profile OR account)'),
            ("Username inurl",       f'inurl:{username}'),
        ]

    if email:
        ed = email.split("@")[1] if "@" in email else ""
        dorks += [
            ("Email basic",         f'"{email}"'),
            ("Email not domain",    f'"{email}" -site:{ed}' if ed else None),
            ("Email breach",        f'"{email}" (breach OR leak OR dump)'),
            ("Email pastebin",      f'site:pastebin.com "{email}"'),
            ("Email github",        f'site:github.com "{email}"'),
        ]

    if phone:
        clean = re.sub(r"\D", "", phone)
        dorks += [
            ("Phone basic",         f'"{phone}"'),
            ("Phone digits",        f'"{clean}"'),
            ("Phone pastebin",      f'site:pastebin.com "{phone}"'),
        ]

    if domain:
        dorks += [
            ("Domain all pages",    f'site:{domain}'),
            ("Domain subdomains",   f'site:*.{domain}'),
            ("Domain login",        f'site:{domain} inurl:login OR inurl:admin'),
            ("Domain config",       f'site:{domain} ext:env OR ext:cfg OR ext:sql'),
            ("Domain docs",         f'site:{domain} ext:pdf OR ext:doc OR ext:xls'),
            ("Domain open dirs",    f'site:{domain} intitle:"index of"'),
            ("Domain emails",       f'site:{domain} intext:@{domain}'),
            ("Domain github",       f'site:github.com "{domain}"'),
            ("Domain pastebin",     f'site:pastebin.com "{domain}"'),
            ("Domain AWS S3",       f'site:s3.amazonaws.com "{domain}"'),
            ("Domain API keys",     f'site:{domain} (apikey OR api_key OR token)'),
            ("Domain backup files", f'site:{domain} ext:bak OR ext:old OR ext:backup'),
            ("Domain cache",        f'cache:{domain}'),
        ]

    if company:
        dorks += [
            ("Company LinkedIn",    f'site:linkedin.com "{company}"'),
            ("Company employees",   f'"{company}" (employees OR staff OR team)'),
            ("Company documents",   f'"{company}" filetype:pdf'),
        ]

    # filter None
    dorks = [(k, v) for k, v in dorks if v]

    section(f"GENERATED {len(dorks)} DORKS", LY)
    for desc, dork in dorks:
        print(LY + f"  {desc:<28}" + LW +
              f" https://www.google.com/search?q={E(dork)}")

    # export
    try:
        save = input(LY + "\n  Export dorks to txt? [y/N] > ").strip().lower()
        if save == "y":
            fname = f"dorks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname, "w") as f:
                f.write(f"OSINT Dorks — By camzzz\n{'='*60}\n\n")
                for desc, dork in dorks:
                    f.write(f"# {desc}\nhttps://www.google.com/search?q={E(dork)}\n\n")
            print(LG + f"  Saved to {fname}")
    except Exception: pass
    pause()


# ──────────────────────────────────────────────
#  UPDATED MENU
# ──────────────────────────────────────────────

MENU = """
╔══════════════════════════════════╗  ╔══════════════════════════════════╗  ╔══════════════════════════════════╗
║         NETWORK / IP             ║  ║          WEB / DOMAIN            ║  ║       PHONE / MAIL / BREACH      ║
╠══════════════════════════════════╣  ╠══════════════════════════════════╣  ╠══════════════════════════════════╣
║ (1)   IP Info & Tracker          ║  ║ (11)  HTTP Header Inspector      ║  ║ (21)  Phone Number Info          ║
║ (2)   DNS Lookup                 ║  ║ (12)  SSL Certificate Inspector  ║  ║ (22)  Phone Social Scanner       ║
║ (3)   Port Scanner               ║  ║ (13)  Tech Detector              ║  ║ (23)  Mail / Email OSINT         ║
║ (4)   Geo IP Tracker             ║  ║ (14)  URL Redirect Tracer        ║  ║ (24)  Email Account Checker      ║
║ (5)   Network Info               ║  ║ (15)  Robots / Sitemap Reader    ║  ║ (25)  Breach Search Engine       ║
║ (6)   WHOIS / Reverse DNS        ║  ║ (16)  Wayback Machine            ║  ║       ZSearcher / OathNet / HIBP ║
║ (7)   Subdomain Finder           ║  ║ (17)  Wayback URL Extractor      ║  ║ (26)  Username Tracker [55+]     ║
║ (8)   ASN / BGP Lookup           ║  ║ (18)  Google Dork Generator      ║  ║ (27)  ID / Username Tracker Ext  ║
║ (9)   Quick Recon (all-in-one)   ║  ║ (19)  OSINT Dork Builder         ║  ║ (28)  Profile Builder            ║
║ (10)  IP Range Scanner           ║  ║ (20)  File / Doc OSINT           ║  ║ (29)  Reverse Image Search       ║
╚══════════════════════════════════╝  ╚══════════════════════════════════╝  ║ (30)  Social Media Search        ║
                                                                            ║ (31)  Public Records Search      ║
                                                                            ║ (32)  Paste Search               ║
                                                                            ╚══════════════════════════════════╝

╔══════════════════════════════════╗  ╔══════════════════════════════════╗  ╔══════════════════════════════════╗
║       INTEL / ADVANCED           ║  ║     PENTEST / VULN / SCAN        ║  ║        PASSWORD / HASH           ║
╠══════════════════════════════════╣  ╠══════════════════════════════════╣  ╠══════════════════════════════════╣
║ (33)  Shodan / Censys Links      ║  ║ (43)  Web Vuln Scanner (20 chk)  ║  ║ (50)  Password Generator/Tester  ║
║ (34)  CVE / Vuln Search          ║  ║ (44)  Firewall / WAF Detector    ║  ║ (51)  Hash Tools                 ║
║ (35)  Archive & Screenshot Links ║  ║ (45)  WiFi Scanner               ║  ║ (52)  Metadata Extractor         ║
║ (36)  OSINT Framework Navigator  ║  ║ (46)  File Scanner (AV basic)    ║  ║ (53)  File Scanner (AV)          ║
║ (37)  Dark Web Search Links      ║  ║ (47)  HTTP Stress Tester (own)   ║  ╚══════════════════════════════════╝
║ (38)  Public Camera Feeds        ║  ╚══════════════════════════════════╝
║ (39)  Wayback URL Extractor      ║
║ (40)  Quick Recon (domain)       ║      (0) Exit
║ (41)  Reverse Image Search       ║
║ (42)  Social Media Search        ║
╚══════════════════════════════════╝
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
    "10": ip_info,
    "11": header_inspector,
    "12": ssl_inspector,
    "13": tech_detector,
    "14": url_tracer,
    "15": robots_sitemap,
    "16": wayback,
    "17": wayback_urls,
    "18": dork_gen,
    "19": osint_dork_builder,
    "20": file_osint,
    "21": phone_info,
    "22": phone_social_scanner,
    "23": mail_osint,
    "24": email_account_checker,
    "25": breach_engine,
    "26": username_tracker,
    "27": id_tracker,
    "28": profile_builder,
    "29": reverse_image,
    "30": social_search,
    "31": public_records,
    "32": paste_search,
    "33": shodan_links,
    "34": vuln_search,
    "35": archive_links,
    "36": osint_framework,
    "37": darkweb_search,
    "38": public_cameras,
    "39": wayback_urls,
    "40": quick_recon,
    "41": reverse_image,
    "42": social_search,
    "43": web_vuln_scanner,
    "44": firewall_detector,
    "45": wifi_scanner,
    "46": file_scanner,
    "47": http_stress_test,
    "50": password_tools,
    "51": hash_tools,
    "52": metadata_extractor,
    "53": file_scanner,
    "48": contact,
    "49": fsociety,
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
            clear(); matrix_rain(5, 72); print()
            for line in CAMZZZ_LINES: rainbow(line)
            print()
            print(LG + "  Goodbye — By camzzz")
            time.sleep(0.8); break
        fn = DISPATCH.get(choice)
        if fn:
            fn()
        else:
            print(LR + "  Invalid option."); time.sleep(0.6)
