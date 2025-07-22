
# ⚡ xneon hydra – GUI Brute-Force Attack Platform

> **Modern Python3 GUI for running [Hydra](https://github.com/vanhauser-thc/thc-hydra) password attacks – now with enterprise cyberpunk vibes and built-in music!**

---

## 🚀 Features

- **Point-and-click Hydra GUI** (PyQt5)
- **All attack protocols** supported (SSH, RDP, HTTP-POST, SMB, etc.)
- **HTTP Form custom input**
- **Custom Hydra parameter field**
- **Real-time output viewer**
- **Animated RGB volume slider** for built-in background music
- **Persistent modern dark theme** (Cyberpunk 2077 inspired)

---

## 🛠️ Installation

**1. Clone & Install dependencies:**
```
git clone https://github.com/neo-hydra/neo-hydra.git
cd neo-hydra
python3 -m venv venv
source venv/bin/activate
````
pip install PyQt5 pygame

For PyQt5

On most modern systems, pip install PyQt5 is enough.
If you get errors, install Qt system libs:
````
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine
````
(If you use pip only, you usually don’t need this, but it can help with missing plugins or system-level integration.)

For Pygame
Install SDL libraries and audio codecs if pip install fails:
````
sudo apt install libsdl2-dev libsdl2-mixer-dev libasound2-dev
````
For ALSA (Audio)
Most Linux systems already have alsa-utils and libasound2, but if not:
````
sudo apt install alsa-utils libasound2
````
3. External dependencies

Hydra (for brute-forcing):
Your tool expects the command-line tool hydra to be installed and in your PATH.

sudo apt install hydra

(Or install from source: https://github.com/vanhauser-thc/thc-hydra)

music.mp3 file

You must have a file named music.mp3 in the same directory as your script (or change the path in the code)


**2. Prerequisites:**

* [Hydra](https://github.com/vanhauser-thc/thc-hydra) installed & in your `$PATH`
* Python 3.7+ recommended (works on 3.13)
* Linux, macOS, or WSL

**3. Optional: Place `music.mp3` in the script directory for custom theme music!**

---

## ⚡ Usage

```
python3 neo-xhydra.py
```

* Enter your **target**, **user/pass files**, select protocol.
* Click **"Execute Attack"** to run Hydra with your settings.
* See attack output live in the console box.
* Adjust background music volume with the RGB slider.

---

## 🎛️ Supported Protocols

```python
["afp","asterisk","cisco","cisco-enable","cisco-ise","cisco-ssh","cisco-telnet","cvs","firebird","ftp","ftps",
"http-form-get","http-form-post","http-form-auth","http-get","http-get-auth","http-head","http-head-auth","http-proxy",
"http-proxy-urlenum","http-put","https-form-get","https-form-post","https-get","https-get-auth","https-head","https-head-auth",
"https-proxy","https-proxy-urlenum","https-put","icq","imap","imaps","informix","ldap2","ldap3","mssql","mysql","ncp",
"nntp","oracle","oracle-listener","pcanywhere","pcnfs","pop3","pop3s","postgres","rdp","redis","rexec","rlogin","rsh",
"rtsp","s7-300","sftp","sip","smb","smtp","smtp-enum","smtps","snmp","socks5","ssh","teamspeak","telnet","vmauthd","vnc",
"xmpp","xmpp-auth","xymon","mongodb"]
```

---

## ⚠️ Warnings & Troubleshooting

* **AVX2 Warning with pygame:**
  If you see

  ```
  RuntimeWarning: Your system is avx2 capable but pygame was not built with support for it.
  ```

  You can ignore it – or run:

  ```
  export PYGAME_DETECT_AVX2=1
  ```

* **`XDG_RUNTIME_DIR not set`:**
  Set the environment variable to silence this warning (optional):

  ```
  export XDG_RUNTIME_DIR="/tmp/runtime-$USER"
  mkdir -p "$XDG_RUNTIME_DIR"
  chmod 700 "$XDG_RUNTIME_DIR"
  ```

* **No attack output?**
  Make sure `hydra` is installed and in your PATH, and your wordlists exist.

---

## ✨ Screenshots

to do
---

## ⚡ Credits & License

* Inspired by [THC-Hydra](https://github.com/vanhauser-thc/thc-hydra)
* GUI and enhancements by [ethical hacker teddy](https://github.com/s-b-repo/)
* MIT License

---

> **For educational and authorized testing only! Always respect legal boundaries and target owner permission.**

```

--
