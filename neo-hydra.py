import sys
import subprocess
import threading
import pygame
import signal
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QTextCursor, QFont, QIcon, QPalette, QColor

protocols = [
    "afp","asterisk","cisco","cisco-enable","cisco-ise","cisco-ssh","cisco-telnet","cvs","firebird","ftp","ftps",
    "http-form-get","http-form-post","http-form-auth","http-get","http-get-auth","http-head","http-head-auth",
    "http-proxy","http-proxy-urlenum","http-put","https-form-get","https-form-post","https-get","https-get-auth",
    "https-head","https-head-auth","https-proxy","https-proxy-urlenum","https-put","icq","imap","imaps","informix",
    "ldap2","ldap3","mssql","mysql","ncp","nntp","oracle","oracle-listener","pcanywhere","pcnfs","pop3","pop3s",
    "postgres","rdp","redis","rexec","rlogin","rsh","rtsp","s7-300","sftp","sip","smb","smtp","smtp-enum","smtps",
    "snmp","socks5","ssh","teamspeak","telnet","vmauthd","vnc","xmpp","xmpp-auth","xymon","mongodb"
]

class OutputSignal(QObject):
    output = pyqtSignal(str)
    finished = pyqtSignal()

class CyberHydra(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMusic()
        self.proc = None
        self.attack_running = False
        self.animation_counter = 0
        self.initAnimations()

    def initMusic(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            if os.path.exists("music.mp3"):
                pygame.mixer.music.load("music.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            else:
                print("Music file not found")
        except Exception as e:
            print(f"Audio initialization error: {e}")

    def initAnimations(self):
        self.pulse_animation = QPropertyAnimation(self.runBtn, b"styleSheet")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def initUI(self):
        self.setWindowTitle("NEO HYDRA :: MODERN EDITION")
        self.setGeometry(100, 50, 950, 800)
        self.setMinimumSize(900, 750)

        # Modern dark theme with vibrant accents
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 11px;
                border: none;
            }
            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #333333;
                padding: 10px;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #e0e0e0;
                selection-background-color: #444444;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #bb86fc;
                background-color: #252525;
            }
            QPushButton {
                border: 1px solid #333333;
                padding: 10px 15px;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2d2d2d, stop:1 #1f1f1f);
                color: #e0e0e0;
                font-weight: 500;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3a3a3a, stop:1 #2a2a2a);
                border: 1px solid #bb86fc;
                color: #ffffff;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1f1f1f, stop:1 #121212);
                border: 1px solid #03dac6;
            }
            QPushButton:disabled {
                background: #1e1e1e;
                border: 1px solid #333333;
                color: #666666;
            }
            QComboBox {
                padding: 8px 12px;
            }
            QComboBox::drop-down {
                border: none;
                background: #2d2d2d;
                width: 20px;
                border-radius: 0px 6px 6px 0px;
            }
            QComboBox::down-arrow {
                image: url();
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #bb86fc;
                margin-right: 5px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                background: #bb86fc;
                border-radius: 8px;
                margin: -5px 0;
            }
            QSlider::sub-page:horizontal {
                background: #03dac6;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 15px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #333333;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #444444;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: 500;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QGroupBox {
                border: 1px solid #333333;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: rgba(30, 30, 30, 0.5);
                font-weight: 500;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #bb86fc;
                font-weight: 600;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("NEO HYDRA :: ADVANCED PENETRATION TOOLKIT")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #bb86fc;
            padding: 5px;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Status indicator
        self.status_label = QLabel("● SYSTEM READY")
        self.status_label.setStyleSheet("color: #03dac6; font-weight: 600; font-size: 14px;")
        header_layout.addWidget(self.status_label)
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
        creds_layout.addWidget(QLabel("🔑 PASS LIST:"))
        creds_layout.addWidget(self.passlist)
        config_layout.addLayout(creds_layout)

        # Protocol section
        protocol_layout = QHBoxLayout()
        self.protocol = QComboBox()
        self.protocol.addItems(protocols)
        self.protocol.setCurrentText("ssh")
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
        self.tasksInput.setPlaceholderText("Number of parallel tasks (default: 16)")
        self.tasksInput.setText("16")
        tasks_layout.addWidget(QLabel("🧵 TASKS:"))
        tasks_layout.addWidget(self.tasksInput)
        config_layout.addLayout(tasks_layout)

        # Proxy section
        proxy_group = QGroupBox("PROXY CONFIGURATION")
        proxy_layout = QVBoxLayout()
        proxy_layout.setSpacing(12)

        # Proxy main settings
        proxy_main_layout = QHBoxLayout()
        self.proxy_ip = QLineEdit()
        self.proxy_ip.setPlaceholderText("Proxy IP (e.g., 127.0.0.1)")
        self.proxy_port = QLineEdit()
        self.proxy_port.setPlaceholderText("Port (e.g., 8080)")
        self.proxy_type = QComboBox()
        self.proxy_type.addItems(["HTTP", "SOCKS4", "SOCKS5"])
        proxy_main_layout.addWidget(QLabel("🔌 PROXY IP:"))
        proxy_main_layout.addWidget(self.proxy_ip)
        proxy_main_layout.addWidget(QLabel("PORT:"))
        proxy_main_layout.addWidget(self.proxy_port)
        proxy_main_layout.addWidget(QLabel("TYPE:"))
        proxy_main_layout.addWidget(self.proxy_type)
        proxy_layout.addLayout(proxy_main_layout)

        # Proxy authentication fields
        proxy_auth_layout = QHBoxLayout()
        self.proxy_user = QLineEdit()
        self.proxy_user.setPlaceholderText("Username (if required)")
        self.proxy_pass = QLineEdit()
        self.proxy_pass.setPlaceholderText("Password (if required)")
        self.proxy_pass.setEchoMode(QLineEdit.Password)
        proxy_auth_layout.addWidget(QLabel("👤 PROXY USER:"))
        proxy_auth_layout.addWidget(self.proxy_user)
        proxy_auth_layout.addWidget(QLabel("🔑 PROXY PASS:"))
        proxy_auth_layout.addWidget(self.proxy_pass)
        proxy_layout.addLayout(proxy_auth_layout)
        proxy_group.setLayout(proxy_layout)
        config_layout.addWidget(proxy_group)

        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # Command preview
        preview_group = QGroupBox("COMMAND PREVIEW")
        preview_layout = QVBoxLayout()
        self.previewBox = QTextEdit()
        self.previewBox.setMaximumHeight(80)
        self.previewBox.setReadOnly(True)
        self.previewBox.setStyleSheet("""
            background-color: #1e1e1e;
            border: 1px solid #333333;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: #e0e0e0;
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

        # Output section
        output_group = QGroupBox("ATTACK OUTPUT")
        output_layout = QVBoxLayout()
        self.outputBox = QTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputBox.setStyleSheet("""
            background-color: #1e1e1e;
            border: 1px solid #333333;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            color: #e0e0e0;
            padding: 8px;
        """)
        output_layout.addWidget(self.outputBox)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("🔊 VOLUME:"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.setVolume)
        volume_layout.addWidget(self.slider)
        volume_layout.addStretch()

        # Progress indicator
        self.progress_label = QLabel("PROGRESS: 0%")
        self.progress_label.setStyleSheet("color: #03dac6; font-weight: 600;")
        volume_layout.addWidget(self.progress_label)
        main_layout.addLayout(volume_layout)

        self.setLayout(main_layout)

        # Initialize signals
        self.outputSignal = OutputSignal()
        self.outputSignal.output.connect(self.appendOutput)
        self.outputSignal.finished.connect(self.commandFinished)

        # Connect all input fields to preview updater
        for widget in [self.target_input, self.userlist, self.passlist, self.protocol,
                      self.customParam, self.httpFormInput, self.proxy_ip,
                      self.proxy_port, self.proxy_user, self.proxy_pass, self.tasksInput]:
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.updatePreview)
            else:
                widget.textChanged.connect(self.updatePreview)
        self.proxy_type.currentIndexChanged.connect(self.updatePreview)
        self.updatePreview()

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

    def buildCommand(self):
        cmd = ["hydra"]

        # Add tasks parameter if specified
        if self.tasksInput.text():
            try:
                tasks = int(self.tasksInput.text())
                if tasks > 0:
                    cmd.extend(["-t", str(tasks)])
            except ValueError:
                pass  # Invalid input, ignore tasks parameter

        # Add credentials
        if self.userlist.text():
            cmd.extend(["-L", self.userlist.text()])
        if self.passlist.text():
            cmd.extend(["-P", self.passlist.text()])

        # Add proxy settings if provided
        if self.proxy_ip.text() and self.proxy_port.text():
            proxy_type = self.proxy_type.currentText().lower()
            proxy_str = f"{proxy_type}://{self.proxy_ip.text()}:{self.proxy_port.text()}"
            if self.proxy_user.text() and self.proxy_pass.text():
                proxy_str = f"{proxy_type}://{self.proxy_user.text()}:{self.proxy_pass.text()}@{self.proxy_ip.text()}:{self.proxy_port.text()}"
            cmd.extend(["-p", proxy_str])

        # Add target
        if self.target_mode == "list" and self.target_input.text():
            cmd.extend(["-M", self.target_input.text()])
        elif self.target_input.text():
            cmd.append(self.target_input.text())

        # Add protocol
        proto = self.protocol.currentText()
        cmd.append(proto)

        # Add HTTP form data if needed
        if "form" in proto and self.httpFormInput.text():
            cmd.append(self.httpFormInput.text())

        # Add custom parameters
        if self.customParam.text():
            cmd.extend(self.customParam.text().split())

        # Filter out empty strings
        cmd = [x for x in cmd if x]

        # Create pretty command string
        pretty_cmd = " ".join([f'"{x}"' if ' ' in x else x for x in cmd])
        return pretty_cmd, cmd

    def updatePreview(self):
        preview, _ = self.buildCommand()
        self.previewBox.setPlainText(f"$ {preview}")

    def setVolume(self):
        try:
            pygame.mixer.music.set_volume(self.slider.value() / 100)
        except:
            pass

    def runHydra(self):
        if self.attack_running:
            return

        # Validate proxy settings if provided
        if self.proxy_ip.text() or self.proxy_port.text():
            if not self.proxy_ip.text() or not self.proxy_port.text():
                self.outputBox.append("❌ ERROR: BOTH PROXY IP AND PORT ARE REQUIRED")
                return
            try:
                port = int(self.proxy_port.text())
                if port < 1 or port > 65535:
                    raise ValueError
            except ValueError:
                self.outputBox.append("❌ ERROR: INVALID PROXY PORT NUMBER")
                return

        _, cmd = self.buildCommand()

        # Validation
        if not self.userlist.text() or not self.passlist.text() or not self.target_input.text():
            self.outputBox.append("❌ ERROR: PLEASE FILL ALL REQUIRED FIELDS")
            return

        self.outputBox.clear()
        self.outputBox.append(f'<span style="color:#bb86fc;">🚀 INITIATING ATTACK SEQUENCE:</span>')
        self.outputBox.append(f'<span style="color:#03dac6;">$ {" ".join(cmd)}</span>')
        self.outputBox.moveCursor(QTextCursor.End)

        self.runBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.attack_running = True
        self.status_label.setText("● ATTACK IN PROGRESS")
        self.status_label.setStyleSheet("color: #cf6679; font-weight: 600;")

        # Start pulsing animation
        self.startButtonAnimation()
        threading.Thread(target=self.execCommand, args=(cmd,), daemon=True).start()

    def startButtonAnimation(self):
        self.pulse_animation.setKeyValueAt(0, "QPushButton { border: 1px solid #cf6679; background: #331b1b; }")
        self.pulse_animation.setKeyValueAt(0.5, "QPushButton { border: 1px solid #ff7979; background: #2a1515; }")
        self.pulse_animation.setKeyValueAt(1, "QPushButton { border: 1px solid #cf6679; background: #331b1b; }")
        self.pulse_animation.start()

    def stopButtonAnimation(self):
        self.pulse_animation.stop()
        self.runBtn.setStyleSheet("")

    def stopAttack(self):
        if self.proc and self.attack_running:
            try:
                self.proc.send_signal(signal.SIGINT)
            except Exception as e:
                self.appendOutput(f"❌ ERROR TERMINATING PROCESS: {e}")
            self.appendOutput("🛑 ATTACK TERMINATED BY OPERATOR")
            self.attack_running = False
            self.runBtn.setEnabled(True)
            self.stopBtn.setEnabled(False)
            self.status_label.setText("● SYSTEM READY")
            self.status_label.setStyleSheet("color: #03dac6; font-weight: 600;")
            self.stopButtonAnimation()

    def execCommand(self, cmd):
        try:
            self.proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            line_count = 0
            for line in self.proc.stdout:
                if not self.attack_running:
                    break
                self.outputSignal.output.emit(line.rstrip())
                line_count += 1
                # Update progress every 10 lines
                if line_count % 10 == 0:
                    progress = min(100, line_count // 10)
                    self.progress_label.setText(f"PROGRESS: {progress}%")

            self.proc.wait()
        except Exception as e:
            self.outputSignal.output.emit(f"❌ EXECUTION ERROR: {str(e)}")
        finally:
            self.outputSignal.finished.emit()
            self.proc = None

    def appendOutput(self, text):
        # Enhanced color coding for different output types
        if "login:" in text.lower() and "password:" in text.lower():
            formatted_text = f'<span style="color:#03dac6; font-weight:bold;">[SUCCESS] {text}</span>'
        elif text.startswith("[ERROR]"):
            formatted_text = f'<span style="color:#cf6679;">{text}</span>'
        elif text.startswith("[INFO]"):
            formatted_text = f'<span style="color:#bb86fc;">{text}</span>'
        elif text.startswith("[DATA]"):
            formatted_text = f'<span style="color:#ff7979;">{text}</span>'
        elif "host:" in text.lower():
            formatted_text = f'<span style="color:#ffff00;">{text}</span>'
        else:
            formatted_text = f'<span style="color:#e0e0e0;">{text}</span>'

        self.outputBox.append(formatted_text)
        self.outputBox.moveCursor(QTextCursor.End)

    def commandFinished(self):
        if self.attack_running:
            self.outputBox.append('<span style="color:#03dac6; font-weight:bold;">✅ ATTACK SEQUENCE COMPLETED</span>')
        self.runBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.attack_running = False
        self.status_label.setText("● SYSTEM READY")
        self.status_label.setStyleSheet("color: #03dac6; font-weight: 600;")
        self.progress_label.setText("PROGRESS: 100%")
        self.stopButtonAnimation()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont("Segoe UI", 15)
    app.setFont(font)

    win = CyberHydra()
    win.show()
    sys.exit(app.exec_())
