from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QVBoxLayout

from .config import TOP_NAV_HEIGHT, FONT_FAMILY


class TopNavBar(QFrame):
    mode_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(TOP_NAV_HEIGHT)
        self.setStyleSheet("background-color: #1A1A3A; border-radius: 8px;")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        logo_label = QLabel("📌")
        logo_label.setFont(QFont(FONT_FAMILY, 16))
        title_layout = QVBoxLayout()
        title_label = QLabel("2026网课专注度分析系统")
        title_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        sub_title = QLabel("网课模式")
        sub_title.setFont(QFont(FONT_FAMILY, 11))
        sub_title.setStyleSheet("color: #AAAAAA;")
        title_layout.addWidget(title_label)
        title_layout.addWidget(sub_title)
        layout.addWidget(logo_label)
        layout.addLayout(title_layout)
        layout.addStretch()

        self.mode_group = QButtonGroup(self)
        self.mode_group.setExclusive(True)
        mode_names = ["网课模式", "考试模式", "数据查询"]
        for idx, name in enumerate(mode_names):
            btn = QPushButton(name)
            btn.setFixedSize(160, 36)
            btn.setFont(QFont(FONT_FAMILY, 12))
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    color: #FFFFFF;
                    background-color: #2D2D5A;
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:checked {
                    background-color: #41418A;
                    border: 1px solid #6666CC;
                }
                QPushButton:hover {
                    background-color: #383870;
                }
            """)
            self.mode_group.addButton(btn, idx)
            layout.addWidget(btn)
        self.mode_group.button(0).setChecked(True)
        self.mode_group.buttonClicked.connect(self.on_mode_click)
        layout.addStretch()

        record_layout = QHBoxLayout()
        record_dot = QLabel("●")
        record_dot.setStyleSheet("color: #00E080; font-size: 14px;")
        record_label = QLabel("录制中")
        record_label.setFont(QFont(FONT_FAMILY, 12))
        record_label.setStyleSheet("color: #FFFFFF;")
        record_layout.addWidget(record_dot)
        record_layout.addWidget(record_label)
        record_frame = QFrame()
        record_frame.setLayout(record_layout)
        record_frame.setStyleSheet("background-color: #2D2D5A; border-radius: 16px; padding: 4px 12px;")
        record_frame.setFixedHeight(30)
        layout.addWidget(record_frame)

    def on_mode_click(self, btn):
        self.mode_changed.emit(btn.text())

    def set_mode(self, mode):
        for i in range(self.mode_group.buttons().__len__()):
            btn = self.mode_group.button(i)
            if btn.text() == mode:
                btn.setChecked(True)
                break
