from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QWidget, QHBoxLayout

from .config import LEFT_BAR_WIDTH, FONT_FAMILY


class LeftSideBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(LEFT_BAR_WIDTH)
        self.setStyleSheet("background-color: #1A1A3A; border-radius: 8px;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(20)

        camera_title = QLabel("摄像头列表")
        camera_title.setFont(QFont(FONT_FAMILY, 12))
        camera_title.setStyleSheet("color: #AAAAAA; padding-left: 8px;")
        self.camera_list = QListWidget()
        self.camera_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                height: 70px;
                margin: 4px 0;
            }
            QListWidget::item:selected {
                background-color: #2D2D5A;
                border-left: 4px solid #7A5CFF;
                border-radius: 4px;
            }
        """)
        camera_datas = [
            {"name": "摄像头名称1", "no": "NO.024", "avatar": "👨"},
            {"name": "摄像头名称2", "no": "NO.018", "avatar": "👩"},
            {"name": "摄像头名称3", "no": "NO.035", "avatar": "👨‍💼"},
        ]
        for data in camera_datas:
            item = QListWidgetItem()
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(12, 8, 12, 8)
            avatar_label = QLabel(data["avatar"])
            avatar_label.setFont(QFont(FONT_FAMILY, 22))
            name_label = QLabel(data["name"])
            name_label.setFont(QFont(FONT_FAMILY, 12, QFont.Medium))
            name_label.setStyleSheet("color: #FFFFFF;")
            no_label = QLabel(data["no"])
            no_label.setFont(QFont(FONT_FAMILY, 10))
            no_label.setStyleSheet("color: #AAAAAA;")
            arrow_label = QLabel(">")
            arrow_label.setStyleSheet("color: #AAAAAA;")
            item_layout.addWidget(avatar_label)
            item_layout.addWidget(name_label)
            item_layout.addStretch()
            item_layout.addWidget(no_label)
            item_layout.addWidget(arrow_label)
            self.camera_list.addItem(item)
            self.camera_list.setItemWidget(item, item_widget)
        self.camera_list.setCurrentRow(0)

        layout.addWidget(camera_title)
        layout.addWidget(self.camera_list)

        face_title = QLabel("当前人脸")
        face_title.setFont(QFont(FONT_FAMILY, 12))
        face_title.setStyleSheet("color: #AAAAAA; padding-left: 8px;")
        self.face_list = QListWidget()
        self.face_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                height: 70px;
                margin: 4px 0;
            }
            QListWidget::item:selected {
                background-color: #2D2D5A;
                border-left: 4px solid #7A5CFF;
                border-radius: 4px;
            }
        """)
        face_data = {"name": "人脸id", "no": "NO.009", "avatar": "👤", "warn": True}
        item = QListWidgetItem()
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(12, 8, 12, 8)
        avatar_label = QLabel(face_data["avatar"])
        avatar_label.setFont(QFont(FONT_FAMILY, 22))
        name_label = QLabel(face_data["name"])
        name_label.setFont(QFont(FONT_FAMILY, 12, QFont.Medium))
        name_label.setStyleSheet("color: #FFFFFF;")
        no_label = QLabel(face_data["no"])
        no_label.setFont(QFont(FONT_FAMILY, 10))
        no_label.setStyleSheet("color: #AAAAAA;")
        warn_label = QLabel("🚨")
        arrow_label = QLabel(">")
        arrow_label.setStyleSheet("color: #AAAAAA;")
        item_layout.addWidget(avatar_label)
        item_layout.addWidget(name_label)
        item_layout.addStretch()
        item_layout.addWidget(no_label)
        if face_data["warn"]:
            item_layout.addWidget(warn_label)
        item_layout.addWidget(arrow_label)
        self.face_list.addItem(item)
        self.face_list.setItemWidget(item, item_widget)
        self.face_list.setCurrentRow(0)

        layout.addWidget(face_title)
        layout.addWidget(self.face_list)
        layout.addStretch()

        bottom_status = QHBoxLayout()
        check_label = QLabel("✅")
        text_label = QLabel("可视化显示")
        text_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        bottom_status.addWidget(check_label)
        bottom_status.addWidget(text_label)
        bottom_status.addStretch()
        layout.addLayout(bottom_status)
