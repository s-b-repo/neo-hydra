import sys
import subprocess
import signal
import os
import ipaddress
import shlex
from datetime import datetime
from typing import List, Tuple, Optional
from PyQt6.QtWidgets import *
from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation,
    QEasingCurve, QSettings, QThread, QUrl, QParallelAnimationGroup,
    QSequentialAnimationGroup, QRect, QSize, pyqtSlot
)
from PyQt6.QtGui import QTextCursor, QFont, QIntValidator, QValidator, QPalette, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# Constants
APPLICATION_NAME = "NEO HYDRA :: MODERN EDITION"
SETTINGS_ORG = "CyberHydra"
SETTINGS_APP = "MainConfig"
MUSIC_FILE = "music.mp3"

# Protocol definitions
PROTOCOLS = {
    "ssh": "Secure Shell", "ftp": "File Transfer Protocol", "smb": "Server Message Block",
    "http-form-post": "HTTP POST forms", "https-form-post": "HTTPS POST forms",
    "telnet": "Telnet protocol", "smtp": "Simple Mail Transfer Protocol",
    "imap": "IMAP email", "pop3": "POP3 email", "rdp": "Remote Desktop Protocol",
    "vnc": "Virtual Network Computing", "mysql": "MySQL database",
    "postgres": "PostgreSQL database", "mssql": "Microsoft SQL Server",
    "oracle": "Oracle database", "mongodb": "MongoDB database", "redis": "Redis database",
    "afp": "Apple Filing Protocol", "cisco-enable": "Cisco enable", "ldap3": "LDAP v3",
    "snmp": "SNMP", "sip": "Session Initiation Protocol", "xmpp": "XMPP",
    "cvs": "CVS", "svn": "Subversion", "imap": "IMAP", "imaps": "IMAP over SSL",
    "pop3s": "POP3 over SSL", "smtps": "SMTP over SSL", "ftps": "FTP over SSL",
    "sftp": "SSH File Transfer Protocol", "http-proxy": "HTTP Proxy",
    "https-proxy": "HTTPS Proxy", "socks5": "SOCKS5 Proxy"
}

class Theme:
    COLORS = {
        'primary': '#bb86fc', 'secondary': '#03dac6', 'error': '#cf6679',
        'warning': '#ff7979', 'success': '#76ff03', 'bg_dark': '#0a0a0a',
        'bg_medium': '#1a1a1a', 'bg_light': '#2a2a2a', 'text_primary': '#e8e8e8',
        'text_secondary': '#b8b8b8', 'border': '#3a3a3a', 'hover': '#4a4a4a',
        'accent': '#9d4edd', 'glow': 'rgba(187, 134, 252, 0.3)'
    }

    @classmethod
    def get_stylesheet(cls) -> str:
        return f"""
            QWidget {{
                background-color: {cls.COLORS['bg_dark']};
                color: {cls.COLORS['text_primary']};
                font-family: 'Segoe UI', 'Roboto', 'Inter', sans-serif;
                font-size: 11px;
                border: none;
            }}
            QLineEdit, QComboBox, QTextEdit {{
                border: 2px solid {cls.COLORS['border']};
                padding: 12px;
                border-radius: 8px;
                background-color: {cls.COLORS['bg_medium']};
                color: {cls.COLORS['text_primary']};
                selection-background-color: {cls.COLORS['primary']};
                selection-color: #000000;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {cls.COLORS['primary']};
                background-color: {cls.COLORS['bg_light']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {cls.COLORS['primary']};
                width: 0;
                height: 0;
            }}
            QComboBox QAbstractItemView {{
                background-color: {cls.COLORS['bg_medium']};
                border: 2px solid {cls.COLORS['primary']};
                border-radius: 6px;
                selection-background-color: {cls.COLORS['primary']};
                selection-color: #000000;
                padding: 4px;
            }}
            QPushButton {{
                border: 2px solid {cls.COLORS['border']};
                padding: 12px 20px;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['bg_light']}, stop:1 {cls.COLORS['bg_medium']});
                color: {cls.COLORS['text_primary']};
                font-weight: 600;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['hover']}, stop:1 {cls.COLORS['bg_light']});
                border: 2px solid {cls.COLORS['primary']};
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['bg_medium']}, stop:1 {cls.COLORS['bg_dark']});
                border: 2px solid {cls.COLORS['secondary']};
                padding: 11px 19px;
            }}
            QPushButton:disabled {{
                background: {cls.COLORS['bg_medium']};
                border: 2px solid {cls.COLORS['border']};
                color: #666666;
            }}
            QSlider::groove:horizontal {{
                height: 8px;
                background: {cls.COLORS['border']};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                width: 20px;
                height: 20px;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['accent']});
                border-radius: 10px;
                margin: -6px 0;
                border: 2px solid {cls.COLORS['bg_light']};
            }}
            QSlider::handle:horizontal:hover {{
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    stop:0 #ffffff, stop:1 {cls.COLORS['primary']});
            }}
            QSlider::sub-page:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['secondary']}, stop:1 {cls.COLORS['primary']});
                border-radius: 4px;
            }}
            QGroupBox {{
                border: 2px solid {cls.COLORS['border']};
                border-radius: 12px;
                margin-top: 18px;
                padding-top: 25px;
                background-color: rgba(26, 26, 26, 0.8);
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 18px;
                padding: 0 12px;
                color: {cls.COLORS['primary']};
                font-weight: 700;
                font-size: 12px;
            }}
            QProgressBar {{
                border: 2px solid {cls.COLORS['border']};
                border-radius: 8px;
                text-align: center;
                background-color: {cls.COLORS['bg_medium']};
                color: {cls.COLORS['text_primary']};
                font-weight: 600;
                height: 24px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['secondary']}, stop:1 {cls.COLORS['primary']});
                border-radius: 6px;
            }}
            QLabel {{
                color: {cls.COLORS['text_primary']};
            }}
        """

class OutputSignal(QObject):
    output = pyqtSignal(str)
    finished = pyqtSignal()
    attempt_count = pyqtSignal(int)
    credential_found = pyqtSignal(str)
    stats_update = pyqtSignal(dict)

class HydraThread(QThread):
    def __init__(self, cmd: List[str]):
        super().__init__()
        self.cmd = cmd
        self.proc = None
        self.attack_running = True
        self.output_signal = OutputSignal()
        self.attempt_count = 0
        self.start_time = None
        self.last_stats_time = None
        self.stats_buffer = []

    def run(self):
        try:
            self.start_time = datetime.now()
            self.last_stats_time = self.start_time
            self.proc = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                errors='replace',
                preexec_fn=os.setsid if os.name != 'nt' else None
            )

            if self.proc.stdout:
                for line in iter(self.proc.stdout.readline, ''):
                    if not self.attack_running:
                        break
                    clean_line = line.rstrip()
                    if clean_line:
                        self.stats_buffer.append(clean_line)
                        if len(self.stats_buffer) >= 10:
                            self._emit_buffered_output()
                        else:
                            self.output_signal.output.emit(clean_line)

                        # Parse attempts and credentials
                        line_lower = clean_line.lower()
                        if any(keyword in line_lower for keyword in ["login:", "host:", "[", "attempt"]):
                            self.attempt_count += 1
                            self.output_signal.attempt_count.emit(self.attempt_count)

                        # Detect successful credentials in various formats
                        if ("login:" in line_lower and "password:" in line_lower) or \
                           ("[host]" in line_lower and "login:" in line_lower) or \
                           ("[ssh]" in line_lower and "login:" in line_lower) or \
                           ("[ftp]" in line_lower and "login:" in line_lower) or \
                           ("[rdp]" in line_lower and "login:" in line_lower) or \
                           ("successfully" in line_lower and "login" in line_lower):
                            self.output_signal.credential_found.emit(clean_line)

                        # Emit stats periodically
                        now = datetime.now()
                        if (now - self.last_stats_time).total_seconds() >= 1.0:
                            self._emit_stats()
                            self.last_stats_time = now

                # Emit remaining buffered output
                if self.stats_buffer:
                    self._emit_buffered_output()

            # Wait for process without timeout (hydra can run for hours)
            return_code = self.proc.wait()
            if return_code != 0 and self.attack_running:
                self.output_signal.output.emit(f"⚠️ Process exited with code: {return_code}")
        except FileNotFoundError:
            self.output_signal.output.emit("❌ HYDRA NOT FOUND: Please install THC-Hydra")
        except Exception as e:
            error_msg = str(e)
            if "No such file or directory" in error_msg or "hydra" in error_msg.lower():
                self.output_signal.output.emit("❌ HYDRA NOT FOUND: Please install THC-Hydra")
            else:
                self.output_signal.output.emit(f"❌ EXECUTION ERROR: {error_msg}")
        finally:
            self.output_signal.finished.emit()
            self.cleanup()

    def _emit_buffered_output(self):
        for line in self.stats_buffer:
            self.output_signal.output.emit(line)
        self.stats_buffer.clear()

    def _emit_stats(self):
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            rate = self.attempt_count / elapsed if elapsed > 0 else 0
            stats = {
                'attempts': self.attempt_count,
                'elapsed': elapsed,
                'rate': rate
            }
            self.output_signal.stats_update.emit(stats)

    def stop(self):
        self.attack_running = False
        if self.proc:
            try:
                if os.name == 'nt':
                    try:
                        self.proc.send_signal(signal.CTRL_C_EVENT)
                    except:
                        self.proc.terminate()
                else:
                    try:
                        pgid = os.getpgid(self.proc.pid)
                        os.killpg(pgid, signal.SIGTERM)
                    except (ProcessLookupError, OSError):
                        try:
                            self.proc.terminate()
                        except:
                            pass
            except (ProcessLookupError, OSError):
                try:
                    self.proc.kill()
                except:
                    pass

    def cleanup(self):
        if self.proc:
            try:
                if self.proc.poll() is None:
                    self.proc.terminate()
                    try:
                        self.proc.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        self.proc.kill()
            except (ProcessLookupError, OSError):
                pass
            finally:
                self.proc = None

class FileValidatorThread(QThread):
    validation_complete = pyqtSignal(str, bool, str)
    
    def __init__(self, file_path: str, field_name: str):
        super().__init__()
        self.file_path = file_path
        self.field_name = field_name
    
    def run(self):
        if not self.file_path:
            self.validation_complete.emit(self.field_name, False, "File path is empty")
            return
        
        expanded_path = os.path.expanduser(self.file_path)
        abs_path = os.path.abspath(expanded_path)
        
        if not os.path.exists(abs_path):
            self.validation_complete.emit(self.field_name, False, f"File not found: {abs_path}")
            return
        
        if not os.path.isfile(abs_path):
            self.validation_complete.emit(self.field_name, False, f"Path is not a file: {abs_path}")
            return
        
        if not os.access(abs_path, os.R_OK):
            self.validation_complete.emit(self.field_name, False, f"File is not readable: {abs_path}")
            return
        
        self.validation_complete.emit(self.field_name, True, abs_path)

class QIPAddressValidator(QValidator):
    def validate(self, input_str: str, pos: int):
        if not input_str:
            return QValidator.State.Acceptable, input_str, pos
        try:
            ipaddress.ip_address(input_str)
            return QValidator.State.Acceptable, input_str, pos
        except ValueError:
            return QValidator.State.Invalid, input_str, pos

class CyberHydra(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self.hydra_thread = None
        self.media_player = None
        self.audio_output = None
        self.attack_running = False
        self.found_credentials = []
        self.attempt_count = 0
        self.start_time = None
        self.pulse_animation = None
        self.attempt_rate = 0.0
        self.progress_bar = None
        self.validation_threads = []

        self.initUI()
        self.initMusic()
        self.initAnimations()
        self.loadSettings()

    def initMusic(self):
        try:
            self.audio_output = QAudioOutput()
            self.media_player = QMediaPlayer()
            self.media_player.setAudioOutput(self.audio_output)
            volume = self.settings.value("volume", 30, int)
            self.audio_output.setVolume(volume / 100.0)

            if os.path.exists(MUSIC_FILE):
                media_path = os.path.abspath(MUSIC_FILE)
                self.media_player.setSource(QUrl.fromLocalFile(media_path))
                self.media_player.play()
                # Loop music
                self.media_player.mediaStatusChanged.connect(self.restartMusic)
            else:
                print(f"Audio: '{MUSIC_FILE}' not found - continuing without music")
                self.settings.setValue("volume", 0)
        except Exception as e:
            print(f"Audio initialization error: {e}")
            self.settings.setValue("volume", 0)

    def restartMusic(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.play()

    def initAnimations(self):
        if self.runBtn:
            self.pulse_animation = QPropertyAnimation(self.runBtn, b"styleSheet")
            self.pulse_animation.setDuration(1000)
            self.pulse_animation.setLoopCount(-1)
            self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def initUI(self):
        self.setWindowTitle(APPLICATION_NAME)
        self.setGeometry(100, 50, 950, 800)
        self.setMinimumSize(900, 750)
        self.setStyleSheet(Theme.get_stylesheet())

        # Create scroll area for main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Theme.COLORS['bg_dark']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {Theme.COLORS['bg_medium']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.COLORS['primary']};
                min-height: 30px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Theme.COLORS['secondary']};
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {Theme.COLORS['bg_medium']};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background: {Theme.COLORS['primary']};
                min-width: 30px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {Theme.COLORS['secondary']};
            }}
        """)

        # Create widget to hold all content
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header with enhanced styling
        header_layout = QHBoxLayout()
        header_container = QWidget()
        header_container.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {Theme.COLORS['bg_medium']}, stop:1 {Theme.COLORS['bg_dark']});
            border-radius: 10px;
            padding: 10px;
        """)
        header_inner = QHBoxLayout(header_container)
        
        title_label = QLabel(APPLICATION_NAME)
        title_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {Theme.COLORS['primary']};
            padding: 5px;
            background: transparent;
        """)
        header_inner.addWidget(title_label)
        header_inner.addStretch()

        self.status_label = QLabel("● SYSTEM READY")
        self.status_label.setStyleSheet(f"""
            color: {Theme.COLORS['secondary']}; 
            font-weight: 700; 
            font-size: 14px;
            background: transparent;
            padding: 8px 15px;
            border-radius: 6px;
            border: 2px solid {Theme.COLORS['secondary']};
        """)
        header_inner.addWidget(self.status_label)
        header_layout.addWidget(header_container)
        main_layout.addLayout(header_layout)

        # Configuration Group
        config_group = QGroupBox("ATTACK CONFIGURATION")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(12)

        # Target section
        target_layout = QHBoxLayout()
        self.target_mode = "single"
        self.target_toggle = QPushButton("SWITCH TO TARGET LIST MODE")
        self.target_toggle.setCheckable(True)
        self.target_toggle.clicked.connect(self.toggleTargetMode)
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target IP/domain or file path")
        target_layout.addWidget(QLabel("🎯 TARGET:"))
        target_layout.addWidget(self.target_toggle)
        target_layout.addWidget(self.target_input)
        config_layout.addLayout(target_layout)

        # Credentials section
        creds_layout = QHBoxLayout()
        self.userlist = QLineEdit()
        self.userlist.setPlaceholderText("Path to username list")
        self.passlist = QLineEdit()
        self.passlist.setPlaceholderText("Path to password list")
        creds_layout.addWidget(QLabel("👤 USER LIST:"))
        creds_layout.addWidget(self.userlist)
        user_browse_btn = QPushButton("📁")
        user_browse_btn.setMaximumWidth(40)
        user_browse_btn.clicked.connect(lambda: self.browseFile(self.userlist, "Select Username File"))
        creds_layout.addWidget(user_browse_btn)
        creds_layout.addWidget(QLabel("🔑 PASS LIST:"))
        creds_layout.addWidget(self.passlist)
        pass_browse_btn = QPushButton("📁")
        pass_browse_btn.setMaximumWidth(40)
        pass_browse_btn.clicked.connect(lambda: self.browseFile(self.passlist, "Select Password File"))
        creds_layout.addWidget(pass_browse_btn)
        config_layout.addLayout(creds_layout)

        # Protocol section
        protocol_layout = QHBoxLayout()
        self.protocol = QComboBox()
        self.protocol.addItems(list(PROTOCOLS.keys()))
        self.protocol.setCurrentText("ssh")
        for i, (proto, desc) in enumerate(PROTOCOLS.items()):
            self.protocol.setItemData(i, desc, Qt.ItemDataRole.ToolTipRole)
        self.customParam = QLineEdit()
        self.customParam.setPlaceholderText("Additional parameters (optional)")
        protocol_layout.addWidget(QLabel("📡 PROTOCOL:"))
        protocol_layout.addWidget(self.protocol)
        protocol_layout.addWidget(QLabel("⚙️ PARAMS:"))
        protocol_layout.addWidget(self.customParam)
        config_layout.addLayout(protocol_layout)

        # HTTP Form section
        http_layout = QHBoxLayout()
        self.httpFormInput = QLineEdit()
        self.httpFormInput.setPlaceholderText("user=^USER^&pass=^PASS^ (for form attacks)")
        http_layout.addWidget(QLabel("🌐 HTTP FORM:"))
        http_layout.addWidget(self.httpFormInput)
        config_layout.addLayout(http_layout)

        # Tasks section
        tasks_layout = QHBoxLayout()
        self.tasksInput = QLineEdit()
        self.tasksInput.setPlaceholderText("Parallel tasks (1-64)")
        self.tasksInput.setText("16")
        self.tasksInput.setValidator(QIntValidator(1, 64, self))
        tasks_layout.addWidget(QLabel("🧵 TASKS:"))
        tasks_layout.addWidget(self.tasksInput)
        config_layout.addLayout(tasks_layout)

        # Proxy section
        proxy_group = self._createProxyGroup()
        config_layout.addWidget(proxy_group)
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # Command preview
        preview_group = QGroupBox("COMMAND PREVIEW")
        preview_layout = QVBoxLayout()
        self.previewBox = QTextEdit()
        self.previewBox.setMaximumHeight(80)
        self.previewBox.setReadOnly(True)
        self.previewBox.setStyleSheet(f"""
            background-color: {Theme.COLORS['bg_medium']};
            border: 1px solid {Theme.COLORS['border']};
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: {Theme.COLORS['text_primary']};
            padding: 8px;
        """)
        preview_layout.addWidget(self.previewBox)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)

        # Control buttons
        button_layout = QHBoxLayout()
        self.runBtn = QPushButton("🔴 LAUNCH ATTACK")
        self.runBtn.clicked.connect(self.runHydra)
        self.stopBtn = QPushButton("⏹️ TERMINATE")
        self.stopBtn.setEnabled(False)
        self.stopBtn.clicked.connect(self.stopAttack)
        button_layout.addWidget(self.runBtn)
        button_layout.addWidget(self.stopBtn)
        main_layout.addLayout(button_layout)
        
        # Initialize animations after runBtn is created
        if not self.pulse_animation:
            self.initAnimations()

        # Output section
        output_group = QGroupBox("ATTACK OUTPUT")
        output_layout = QVBoxLayout()
        
        # Output controls
        output_controls = QHBoxLayout()
        self.auto_scroll = True
        self.auto_scroll_btn = QPushButton("📜 AUTO-SCROLL: ON")
        self.auto_scroll_btn.setCheckable(True)
        self.auto_scroll_btn.setChecked(True)
        self.auto_scroll_btn.setMaximumWidth(150)
        self.auto_scroll_btn.clicked.connect(self.toggleAutoScroll)
        output_controls.addWidget(self.auto_scroll_btn)
        
        clear_btn = QPushButton("🗑️ CLEAR")
        clear_btn.setMaximumWidth(100)
        clear_btn.clicked.connect(self.clearOutput)
        output_controls.addWidget(clear_btn)
        output_controls.addStretch()
        output_layout.addLayout(output_controls)
        
        self.outputBox = QTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputBox.setStyleSheet(f"""
            background-color: {Theme.COLORS['bg_medium']};
            border: 2px solid {Theme.COLORS['border']};
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 11px;
            color: {Theme.COLORS['text_primary']};
            padding: 10px;
            border-radius: 8px;
        """)
        output_layout.addWidget(self.outputBox)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # Progress bar
        progress_group = QGroupBox("ATTACK PROGRESS")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Initializing...")
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

        # Footer with volume and status
        footer_container = QWidget()
        footer_container.setStyleSheet(f"""
            background-color: {Theme.COLORS['bg_medium']};
            border-radius: 8px;
            padding: 10px;
        """)
        footer_layout = QHBoxLayout(footer_container)
        
        footer_layout.addWidget(QLabel("🔊 VOLUME:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.settings.value("volume", 30, int))
        self.slider.valueChanged.connect(self.setVolume)
        self.slider.setMaximumWidth(150)
        footer_layout.addWidget(self.slider)
        
        footer_layout.addStretch()

        self.progress_label = QLabel("ATTEMPTS: 0 | FOUND: 0")
        self.progress_label.setStyleSheet(f"""
            color: {Theme.COLORS['secondary']}; 
            font-weight: 700; 
            font-size: 12px;
            padding: 5px 10px;
            background-color: {Theme.COLORS['bg_light']};
            border-radius: 6px;
        """)
        footer_layout.addWidget(self.progress_label)

        self.rate_label = QLabel("RATE: 0.0/sec")
        self.rate_label.setStyleSheet(f"""
            color: {Theme.COLORS['primary']}; 
            font-weight: 700; 
            font-size: 12px;
            padding: 5px 10px;
            background-color: {Theme.COLORS['bg_light']};
            border-radius: 6px;
        """)
        footer_layout.addWidget(self.rate_label)

        self.timer_label = QLabel("ELAPSED: 00:00:00")
        self.timer_label.setStyleSheet(f"""
            color: {Theme.COLORS['accent']}; 
            font-weight: 700; 
            font-size: 12px;
            padding: 5px 10px;
            background-color: {Theme.COLORS['bg_light']};
            border-radius: 6px;
        """)
        footer_layout.addWidget(self.timer_label)
        main_layout.addWidget(footer_container)

        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Set scroll area as main layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll_area)

        # Connect all input fields
        self._connectSignalUpdates()


    def browseFile(self, line_edit: QLineEdit, title: str):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            line_edit.setText(file_path)

    def _createProxyGroup(self) -> QGroupBox:
        group = QGroupBox("PROXY CONFIGURATION")
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Proxy main settings
        proxy_main_layout = QHBoxLayout()
        self.proxy_ip = QLineEdit()
        self.proxy_ip.setPlaceholderText("Proxy IP (e.g., 127.0.0.1)")
        self.proxy_ip.setValidator(QIPAddressValidator())
        self.proxy_port = QLineEdit()
        self.proxy_port.setPlaceholderText("Port (e.g., 8080)")
        self.proxy_port.setValidator(QIntValidator(1, 65535, self))
        self.proxy_type = QComboBox()
        self.proxy_type.addItems(["HTTP", "SOCKS4", "SOCKS5"])
        proxy_main_layout.addWidget(QLabel("🔌 PROXY IP:"))
        proxy_main_layout.addWidget(self.proxy_ip)
        proxy_main_layout.addWidget(QLabel("PORT:"))
        proxy_main_layout.addWidget(self.proxy_port)
        proxy_main_layout.addWidget(QLabel("TYPE:"))
        proxy_main_layout.addWidget(self.proxy_type)
        layout.addLayout(proxy_main_layout)

        # Proxy authentication fields
        proxy_auth_layout = QHBoxLayout()
        self.proxy_user = QLineEdit()
        self.proxy_user.setPlaceholderText("Username (if required)")
        self.proxy_pass = QLineEdit()
        self.proxy_pass.setPlaceholderText("Password (if required)")
        self.proxy_pass.setEchoMode(QLineEdit.EchoMode.Password)
        proxy_auth_layout.addWidget(QLabel("👤 PROXY USER:"))
        proxy_auth_layout.addWidget(self.proxy_user)
        proxy_auth_layout.addWidget(QLabel("🔑 PROXY PASS:"))
        proxy_auth_layout.addWidget(self.proxy_pass)
        layout.addLayout(proxy_auth_layout)
        group.setLayout(layout)
        return group

    def _connectSignalUpdates(self):
        for widget in [self.target_input, self.userlist, self.passlist, self.customParam,
                      self.httpFormInput, self.proxy_ip, self.proxy_port, self.proxy_user,
                      self.proxy_pass, self.tasksInput]:
            widget.textChanged.connect(self.updatePreview)
        self.protocol.currentIndexChanged.connect(self.updatePreview)
        self.proxy_type.currentIndexChanged.connect(self.updatePreview)
        
        # Async file validation
        self.userlist.textChanged.connect(lambda: self._validateFileAsync(self.userlist, "userlist"))
        self.passlist.textChanged.connect(lambda: self._validateFileAsync(self.passlist, "passlist"))
    
    def _validateFileAsync(self, line_edit: QLineEdit, field_name: str):
        file_path = line_edit.text().strip()
        if not file_path:
            line_edit.setStyleSheet("")
            return
        
        # Start validation in background thread
        validator = FileValidatorThread(file_path, field_name)
        validator.validation_complete.connect(
            lambda name, valid, msg: self._onValidationComplete(line_edit, name, valid, msg)
        )
        validator.finished.connect(validator.deleteLater)
        self.validation_threads.append(validator)
        validator.start()
    
    def _onValidationComplete(self, line_edit: QLineEdit, field_name: str, valid: bool, message: str):
        if valid:
            line_edit.setStyleSheet(f"""
                border: 2px solid {Theme.COLORS['success']};
                background-color: {Theme.COLORS['bg_medium']};
            """)
            line_edit.setToolTip(f"✓ Valid file: {message}")
        else:
            line_edit.setStyleSheet(f"""
                border: 2px solid {Theme.COLORS['error']};
                background-color: {Theme.COLORS['bg_medium']};
            """)
            line_edit.setToolTip(f"✗ {message}")

    def loadSettings(self):
        self.userlist.setText(self.settings.value("userlist", ""))
        self.passlist.setText(self.settings.value("passlist", ""))
        self.proxy_ip.setText(self.settings.value("proxy_ip", ""))
        self.proxy_port.setText(self.settings.value("proxy_port", ""))
        self.proxy_user.setText(self.settings.value("proxy_user", ""))
        self.proxy_type.setCurrentText(self.settings.value("proxy_type", "HTTP"))
        self.tasksInput.setText(self.settings.value("tasks", "16"))
        self.target_input.setText(self.settings.value("last_target", ""))

    def saveSettings(self):
        self.settings.setValue("userlist", self.userlist.text())
        self.settings.setValue("passlist", self.passlist.text())
        self.settings.setValue("proxy_ip", self.proxy_ip.text())
        self.settings.setValue("proxy_port", self.proxy_port.text())
        self.settings.setValue("proxy_user", self.proxy_user.text())
        self.settings.setValue("proxy_type", self.proxy_type.currentText())
        self.settings.setValue("tasks", self.tasksInput.text())
        self.settings.setValue("volume", self.slider.value())
        self.settings.setValue("last_target", self.target_input.text())

    def toggleTargetMode(self):
        if self.target_toggle.isChecked():
            self.target_mode = "list"
            self.target_toggle.setText("SWITCH TO SINGLE TARGET MODE")
            self.target_input.setPlaceholderText("Path to target list file")
        else:
            self.target_mode = "single"
            self.target_toggle.setText("SWITCH TO TARGET LIST MODE")
            self.target_input.setPlaceholderText("Enter target IP/domain")
        self.updatePreview()

    def buildCommand(self) -> Tuple[str, List[str]]:
        cmd = ["hydra"]

        # Add tasks parameter
        if self.tasksInput.text():
            try:
                tasks = int(self.tasksInput.text())
                if 1 <= tasks <= 64:
                    cmd.extend(["-t", str(tasks)])
            except ValueError:
                pass

        # Add credentials (use absolute paths for security)
        if self.userlist.text():
            user_path = os.path.abspath(os.path.expanduser(self.userlist.text()))
            cmd.extend(["-L", user_path])
        if self.passlist.text():
            pass_path = os.path.abspath(os.path.expanduser(self.passlist.text()))
            cmd.extend(["-P", pass_path])

        # Add proxy settings (hydra uses -x for proxy)
        if self.proxy_ip.text() and self.proxy_port.text():
            proxy_type = self.proxy_type.currentText().lower()
            proxy_str = f"{proxy_type}://{self.proxy_ip.text()}:{self.proxy_port.text()}"
            if self.proxy_user.text() and self.proxy_pass.text():
                proxy_str = f"{proxy_type}://{self.proxy_user.text()}:{self.proxy_pass.text()}@{self.proxy_ip.text()}:{self.proxy_port.text()}"
            cmd.extend(["-x", proxy_str])

        # Add target (must come before protocol in hydra syntax)
        if self.target_mode == "list" and self.target_input.text():
            target_path = os.path.abspath(os.path.expanduser(self.target_input.text()))
            cmd.extend(["-M", target_path])
        elif self.target_input.text():
            cmd.append(self.target_input.text().strip())

        # Add protocol
        proto = self.protocol.currentText()
        cmd.append(proto)
        
        # Add HTTP form data (comes after protocol for form attacks)
        if "form" in proto and self.httpFormInput.text():
            cmd.append(self.httpFormInput.text())

        # Add custom parameters (safe parsing)
        if self.customParam.text():
            try:
                parsed_params = shlex.split(self.customParam.text())
                cmd.extend(parsed_params)
            except ValueError as e:
                if hasattr(self, 'outputBox'):
                    self.outputBox.append(f"❌ PARAMETER PARSING ERROR: {e}")

        # Filter empty strings
        cmd = [x for x in cmd if x and x.strip()]

        # Create readable command string with proper escaping
        escaped_cmd = []
        for x in cmd:
            if ' ' in x or any(c in x for c in ['&', '|', ';', '<', '>', '(', ')', '$', '`']):
                escaped_cmd.append(f'"{x}"')
            else:
                escaped_cmd.append(x)
        pretty_cmd = " ".join(escaped_cmd)
        return pretty_cmd, cmd

    def updatePreview(self):
        preview, _ = self.buildCommand()
        self.previewBox.setPlainText(f"$ {preview}")

    def setVolume(self, value: int):
        try:
            if hasattr(self, 'audio_output') and self.audio_output:
                self.audio_output.setVolume(value / 100.0)
                self.settings.setValue("volume", value)
        except Exception:
            pass

    def validateInputs(self) -> bool:
        errors = []

        # Check if hydra is installed
        try:
            result = subprocess.run(["which", "hydra"], capture_output=True, text=True, timeout=2)
            if result.returncode != 0:
                errors.append("Hydra binary not found in PATH. Please install THC-Hydra.")
        except Exception:
            try:
                result = subprocess.run(["hydra", "-h"], capture_output=True, text=True, timeout=2)
                if result.returncode != 0:
                    errors.append("Hydra binary not found. Please install THC-Hydra.")
            except FileNotFoundError:
                errors.append("Hydra binary not found. Please install THC-Hydra.")

        # Validate files
        for field, name, required in [(self.userlist, "Userlist", True),
                                     (self.passlist, "Passlist", True),
                                     (self.target_input, "Target", True)]:
            path = field.text().strip()
            if not path and required:
                errors.append(f"{name} is required")
            elif path:
                if name == "Target" and self.target_mode == "single":
                    # For single target, validate it's not a file path that doesn't exist
                    if os.path.exists(path) and os.path.isfile(path):
                        errors.append("Target appears to be a file. Switch to Target List Mode.")
                    elif not path:
                        errors.append("Target is required")
                else:
                    # For file-based inputs, check file exists
                    if not os.path.isfile(path):
                        errors.append(f"{name} file not found: {path}")
                    elif not os.access(path, os.R_OK):
                        errors.append(f"{name} file is not readable: {path}")

        # Validate proxy
        if self.proxy_ip.text() or self.proxy_port.text():
            if not self.proxy_ip.text():
                errors.append("Proxy IP is required if port is set")
            if not self.proxy_port.text():
                errors.append("Proxy port is required if IP is set")

        # Validate IP format (allow hostnames too for proxy)
        if self.proxy_ip.text():
            proxy_ip_text = self.proxy_ip.text().strip()
            try:
                ipaddress.ip_address(proxy_ip_text)
            except ValueError:
                # Allow hostnames for proxy
                if not proxy_ip_text or len(proxy_ip_text) > 253:
                    errors.append("Invalid proxy IP address or hostname format")

        # Validate port
        if self.proxy_port.text():
            try:
                port = int(self.proxy_port.text())
                if not 1 <= port <= 65535:
                    errors.append("Proxy port must be between 1-65535")
            except ValueError:
                errors.append("Proxy port must be a number")

        if errors:
            QMessageBox.critical(self, "Validation Error",
                "⚠️ The following errors were found:\n\n" + "\n".join(errors))
            return False
        return True

    def runHydra(self):
        if self.attack_running:
            return

        if not self.validateInputs():
            return

        _, cmd = self.buildCommand()

        self.outputBox.clear()
        self.found_credentials.clear()
        self.attempt_count = 0
        self.appendOutput(f'<span style="color:{Theme.COLORS["primary"]}; font-weight:bold;">🚀 INITIATING ATTACK SEQUENCE:</span>')
        self.appendOutput(f'<span style="color:{Theme.COLORS["secondary"]};">$ {" ".join(cmd)}</span>')

        # Update UI state
        self.runBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.attack_running = True
        self.start_time = datetime.now()
        self.status_label.setText("● ATTACK IN PROGRESS")
        self.status_label.setStyleSheet(f"""
            color: {Theme.COLORS['error']}; 
            font-weight: 700; 
            font-size: 14px;
            background: transparent;
            padding: 8px 15px;
            border-radius: 6px;
            border: 2px solid {Theme.COLORS['error']};
        """)
        if self.progress_bar:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("Starting attack...")

        # Start animations
        self.startButtonAnimation()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updateElapsedTime)
        self.update_timer.start(1000)

        # Start hydra thread
        self.hydra_thread = HydraThread(cmd)
        self.hydra_thread.output_signal.output.connect(self.appendOutput)
        self.hydra_thread.output_signal.finished.connect(self.commandFinished)
        self.hydra_thread.output_signal.attempt_count.connect(self.updateProgress)
        self.hydra_thread.output_signal.credential_found.connect(self.addCredential)
        self.hydra_thread.output_signal.stats_update.connect(self.updateStats)
        self.hydra_thread.start()

    def startButtonAnimation(self):
        if self.pulse_animation:
            self.pulse_animation.setKeyValueAt(0,
                f"QPushButton {{ border: 1px solid {Theme.COLORS['error']}; background: #331b1b; }}")
            self.pulse_animation.setKeyValueAt(0.5,
                f"QPushButton {{ border: 1px solid {Theme.COLORS['warning']}; background: #2a1515; }}")
            self.pulse_animation.setKeyValueAt(1,
                f"QPushButton {{ border: 1px solid {Theme.COLORS['error']}; background: #331b1b; }}")
            self.pulse_animation.start()

    def stopButtonAnimation(self):
        if self.pulse_animation:
            self.pulse_animation.stop()
        if self.runBtn:
            self.runBtn.setStyleSheet("")

    def stopAttack(self):
        if hasattr(self, 'hydra_thread') and self.attack_running:
            self.hydra_thread.stop()
            self.hydra_thread.wait(5000)
            self.hydra_thread.cleanup()
            self.appendOutput("🛑 ATTACK TERMINATED BY OPERATOR")
            self.commandFinished()

    def updateElapsedTime(self):
        if self.start_time and self.attack_running:
            elapsed = datetime.now() - self.start_time
            total_seconds = int(elapsed.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.setText(f"ELAPSED: {hours:02d}:{minutes:02d}:{seconds:02d}")
            # Update progress bar with time info
            if self.progress_bar and self.attempt_count > 0:
                eta_text = ""
                if self.attempt_rate > 0:
                    # Could calculate ETA if we had total attempts
                    pass
                self.progress_bar.setFormat(f"{self.attempt_count} attempts | {hours:02d}:{minutes:02d}:{seconds:02d}")

    def updateProgress(self, count: int):
        self.attempt_count = count
        found = len(self.found_credentials)
        self.progress_label.setText(f"ATTEMPTS: {count} | FOUND: {found}")
        if self.progress_bar:
            # Update progress bar (indeterminate for now, could be based on wordlist size)
            if count > 0:
                self.progress_bar.setFormat(f"Processing... {count} attempts")
            else:
                self.progress_bar.setFormat("Initializing attack...")

    @pyqtSlot(dict)
    def updateStats(self, stats: dict):
        self.attempt_rate = stats.get('rate', 0.0)
        if self.rate_label:
            self.rate_label.setText(f"RATE: {self.attempt_rate:.1f}/sec")

    def addCredential(self, cred: str):
        self.found_credentials.append(cred)
        self.updateProgress(self.attempt_count)

    def toggleAutoScroll(self, checked: bool):
        self.auto_scroll = checked
        if checked:
            self.auto_scroll_btn.setText("📜 AUTO-SCROLL: ON")
            self.auto_scroll_btn.setStyleSheet(f"""
                border: 2px solid {Theme.COLORS['success']};
                background-color: {Theme.COLORS['bg_medium']};
            """)
        else:
            self.auto_scroll_btn.setText("📜 AUTO-SCROLL: OFF")
            self.auto_scroll_btn.setStyleSheet(f"""
                border: 2px solid {Theme.COLORS['border']};
                background-color: {Theme.COLORS['bg_medium']};
            """)
    
    def clearOutput(self):
        self.outputBox.clear()
        self.appendOutput('<span style="color:#888;">Output cleared</span>')
    
    def appendOutput(self, text: str):
        if "login:" in text.lower() and "password:" in text.lower():
            formatted = f'<span style="color:{Theme.COLORS["success"]}; font-weight:bold;">[SUCCESS] {text}</span>'
        elif any(err in text.lower() for err in ["error", "fatal", "failed"]):
            formatted = f'<span style="color:{Theme.COLORS["error"]};">{text}</span>'
        elif text.startswith("[INFO]"):
            formatted = f'<span style="color:{Theme.COLORS["primary"]};">{text}</span>'
        else:
            formatted = f'<span style="color:{Theme.COLORS["text_primary"]};">{text}</span>'

        self.outputBox.append(formatted)
        if self.auto_scroll:
            self.outputBox.moveCursor(QTextCursor.MoveOperation.End)

    def commandFinished(self):
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

        if self.attack_running:
            self.appendOutput(f'<span style="color:{Theme.COLORS["secondary"]}; font-weight:bold;">✅ ATTACK SEQUENCE COMPLETED</span>')

        # Save findings
        if self.found_credentials:
            self.saveCredentials()

        # Reset UI state
        self.runBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.attack_running = False
        self.status_label.setText("● SYSTEM READY")
        self.status_label.setStyleSheet(f"""
            color: {Theme.COLORS['secondary']}; 
            font-weight: 700; 
            font-size: 14px;
            background: transparent;
            padding: 8px 15px;
            border-radius: 6px;
            border: 2px solid {Theme.COLORS['secondary']};
        """)
        self.stopButtonAnimation()
        if self.progress_bar:
            self.progress_bar.setValue(100)
            self.progress_bar.setFormat("Attack completed")
        self.rate_label.setText("RATE: 0.0/sec")

    def saveCredentials(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hydra_results_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=== NEO HYDRA RESULTS ===\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Command: {self.previewBox.toPlainText()}\n")
                f.write("="*50 + "\n\n")
                if self.found_credentials:
                    for cred in self.found_credentials:
                        f.write(f"{cred}\n")
                else:
                    f.write("No credentials found.\n")
            self.appendOutput(f'<span style="color:{Theme.COLORS["success"]};">💾 Results saved to: {filename}</span>')
        except Exception as e:
            self.appendOutput(f'<span style="color:{Theme.COLORS["error"]};">❌ Failed to save results: {e}</span>')

    def closeEvent(self, event):
        self.saveSettings()
        if self.attack_running:
            reply = QMessageBox.question(self, "Warning", "Attack is running. Exit anyway?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.stopAttack()
            else:
                event.ignore()
                return

        try:
            if self.media_player:
                self.media_player.stop()
        except:
            pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 15)
    app.setFont(font)
    win = CyberHydra()
    win.show()
    sys.exit(app.exec())
