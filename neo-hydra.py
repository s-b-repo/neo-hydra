import sys, subprocess, threading, pygame, signal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor

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
        self.proc = None  # Track running process
        self.attack_running = False

    def initMusic(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def initUI(self):
        self.setWindowTitle("xneon hydra")
        self.setGeometry(150,100,700,600)
        self.setStyleSheet("""
            QWidget {background:#121212;color:#fff;font-family:Arial,sans-serif;}
            QLineEdit,QComboBox,QTextEdit {border:2px solid #00ffea;padding:6px;border-radius:5px;background:#181818;color:#fff;}
            QPushButton {border:2px solid #ff007f;padding:8px;border-radius:8px;background:#181818;color:#ff007f;}
            QPushButton:hover {background:#ff007f;color:#000;}
            QSlider::groove:horizontal{height:8px;background:#222;border-radius:4px;}
            QSlider::handle:horizontal{width:18px;height:18px;background:#fff;border-radius:9px;}
        """)
        form=QFormLayout()

        # Target input + toggle
        self.target_mode = "single"  # or "list"
        self.target_toggle = QPushButton("List", self)
        self.target_toggle.setCheckable(True)
        self.target_toggle.setFixedWidth(50)
        self.target_toggle.setToolTip("Toggle between single target and list")
        self.target_toggle.clicked.connect(self.toggleTargetMode)
        self.target_input = QLineEdit()
        self.target_label = QLabel("🎯 Target IP/Domain:")
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target_toggle)
        target_layout.addWidget(self.target_input)
        form.addRow(self.target_label, target_layout)

        # User/Pass/Other fields
        self.userlist, self.passlist = QLineEdit(), QLineEdit()
        self.protocol = QComboBox(); self.protocol.addItems(protocols)
        self.customParam, self.httpFormInput = QLineEdit(), QLineEdit()
        form.addRow("👤 User List Path:", self.userlist)
        form.addRow("🔑 Pass List Path:", self.passlist)
        form.addRow("📡 Protocol:", self.protocol)
        form.addRow("⚙️ Custom Params:", self.customParam)
        form.addRow("🌐 HTTP Form (user=^USER^&pass=^PASS^):", self.httpFormInput)

        # Buttons
        self.runBtn = QPushButton("🔴 Execute Attack")
        self.stopBtn = QPushButton("⏹️ Stop Attack")
        self.stopBtn.setEnabled(False)
        self.runBtn.clicked.connect(self.runHydra)
        self.stopBtn.clicked.connect(self.stopAttack)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.runBtn)
        btn_layout.addWidget(self.stopBtn)

        # Output and slider
        self.outputBox = QTextEdit(); self.outputBox.setReadOnly(True)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,100); self.slider.setValue(30); self.slider.valueChanged.connect(self.setVolume)
        slider_label = QLabel("🔊 Volume"); sl_layout = QHBoxLayout()
        sl_layout.addWidget(slider_label); sl_layout.addWidget(self.slider)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(QLabel("💻 Command Preview:"))
        self.previewBox = QLineEdit(); self.previewBox.setReadOnly(True)
        layout.addWidget(self.previewBox)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("🖥️ Output:"))
        layout.addWidget(self.outputBox)
        layout.addLayout(sl_layout)
        self.setLayout(layout)

        # RGB slider effect
        self.rgb_timer = QTimer()
        self.rgb_timer.timeout.connect(self.animateSlider); self.rgb_timer.start(50)
        self.rgb_step = 0

        # Output signal
        self.outputSignal = OutputSignal()
        self.outputSignal.output.connect(self.appendOutput)
        self.outputSignal.finished.connect(self.commandFinished)

        # Live update preview
        for w in [self.target_input, self.userlist, self.passlist, self.protocol,
                  self.customParam, self.httpFormInput]:
            if isinstance(w, QComboBox):
                w.currentIndexChanged.connect(self.updatePreview)
            else:
                w.textChanged.connect(self.updatePreview)
        self.updatePreview()

    def animateSlider(self):
        r=(self.rgb_step)%255;g=(self.rgb_step+85)%255;b=(self.rgb_step+170)%255
        self.slider.setStyleSheet(f"QSlider::handle:horizontal{{background:rgb({r},{g},{b});}}")
        self.rgb_step+=5

    def setVolume(self):
        pygame.mixer.music.set_volume(self.slider.value()/100)

    def toggleTargetMode(self):
        # Switch between single and list
        if self.target_toggle.isChecked():
            self.target_mode = "list"
            self.target_label.setText("🗂️ Target List Path:")
            self.target_toggle.setText("Single")
        else:
            self.target_mode = "single"
            self.target_label.setText("🎯 Target IP/Domain:")
            self.target_toggle.setText("List")
        self.updatePreview()

    def buildCommand(self):
        # Robust, quoting fields with spaces
        cmd = ["hydra", "-L", self.userlist.text(), "-P", self.passlist.text()]
        proto = self.protocol.currentText()
        if self.target_mode == "list":
            cmd += ["-M", self.target_input.text()]
        else:
            cmd.append(self.target_input.text())
        cmd.append(proto)
        if "form" in proto and self.httpFormInput.text():
            cmd.append(self.httpFormInput.text())
        if self.customParam.text():
            cmd += self.customParam.text().split()
        # Only show non-empty
        cmd = [x for x in cmd if x]
        # Pretty print (quote if spaces)
        pretty_cmd = " ".join([f'"{x}"' if ' ' in x else x for x in cmd])
        return pretty_cmd, cmd

    def updatePreview(self):
        preview, _ = self.buildCommand()
        self.previewBox.setText(f"$ {preview}")

    def runHydra(self):
        if self.attack_running:
            return
        _, cmd = self.buildCommand()
        # Validate fields (minimal)
        if not self.userlist.text() or not self.passlist.text() or not self.target_input.text():
            self.outputBox.append("❌ Please fill all required fields.")
            return
        self.outputBox.clear()
        self.outputBox.append(f'<span style="color:#0ff;font-weight:bold;">$ {" ".join(cmd)}</span>\n')
        self.outputBox.moveCursor(QTextCursor.End)
        self.runBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.attack_running = True
        threading.Thread(target=self.execCommand, args=(cmd,), daemon=True).start()

    def stopAttack(self):
        if self.proc and self.attack_running:
            try:
                # Send SIGINT (Ctrl+C)
                self.proc.send_signal(signal.SIGINT)
            except Exception as e:
                self.appendOutput(f"Error stopping: {e}")
            self.appendOutput("🛑 Attack stopped by user.")
            self.attack_running = False
            self.runBtn.setEnabled(True)
            self.stopBtn.setEnabled(False)

    def execCommand(self, cmd):
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in self.proc.stdout:
                if not self.attack_running: break
                self.outputSignal.output.emit(line.strip())
            self.proc.wait()
        except Exception as e:
            self.outputSignal.output.emit(f"Error: {str(e)}")
        self.outputSignal.finished.emit()
        self.proc = None

    def appendOutput(self, text):
        self.outputBox.append(text)
        self.outputBox.moveCursor(QTextCursor.End)

    def commandFinished(self):
        if self.attack_running:
            self.outputBox.append("✅ Attack Complete!")
        self.runBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.attack_running = False

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=CyberHydra()
    win.show()
    sys.exit(app.exec_())
