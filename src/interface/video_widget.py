from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout

from .config import FONT_FAMILY


class VideoWidget(QFrame):
    warn_updated = pyqtSignal(str)
    frame_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1A1A3A; border-radius: 8px;")
        self.is_running = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 16)
        layout.setSpacing(16)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: #0A0A1A; border-radius: 6px;")
        self.video_label.setText("等待预处理模块接入...")
        self.video_label.setFont(QFont(FONT_FAMILY, 13))
        self.video_label.setStyleSheet("color: #666666; background-color: #0A0A1A; border-radius: 6px;")
        layout.addWidget(self.video_label)

        self.warn_bar = QFrame()
        self.warn_bar.setFixedHeight(56)
        self.warn_bar.setStyleSheet("background-color: #4A1A2A; border-radius: 8px;")
        warn_layout = QHBoxLayout(self.warn_bar)
        warn_layout.setContentsMargins(20, 10, 20, 10)
        warn_icon = QLabel("📋")
        warn_icon.setFont(QFont(FONT_FAMILY, 13))
        self.warn_text = QLabel("当前xxx值低于阈值，请注意xxx")
        self.warn_text.setFont(QFont(FONT_FAMILY, 12))
        self.warn_text.setStyleSheet("color: #FFFFFF;")
        warn_layout.addWidget(warn_icon)
        warn_layout.addWidget(self.warn_text)
        warn_layout.addStretch()
        self.warn_bar.hide()
        layout.addWidget(self.warn_bar)

        self.warn_updated.connect(self.update_warn)

    def update_warn(self, text):
        if text:
            self.warn_text.setText(text)
            self.warn_bar.show()
        else:
            self.warn_bar.hide()

    def start_processing(self):
        self.is_running = True
        self.video_label.setText("预处理模块运行中...")
        self.video_label.setStyleSheet("color: #00E0A0; background-color: #0A0A1A; border-radius: 6px;")

    def stop_processing(self):
        self.is_running = False
        self.video_label.setText("等待预处理模块接入...")
        self.video_label.setStyleSheet("color: #666666; background-color: #0A0A1A; border-radius: 6px;")

    def update_frame(self, processed_data=None):
        pass

    def set_preprocessing_callback(self, callback):
        pass
