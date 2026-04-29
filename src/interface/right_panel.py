import pyqtgraph as pg
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
)

from .config import RIGHT_PANEL_WIDTH, FONT_FAMILY


class RightPanel(QFrame):
    start_analysis = pyqtSignal()
    stop_analysis = pyqtSignal()
    score_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(RIGHT_PANEL_WIDTH)
        self.setStyleSheet("background-color: #1A1A3A; border-radius: 8px;")
        self.is_running = False
        self.init_ui()
        self.score_updated.connect(self.update_scores)
        
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.generate_simulated_data)
        self.simulation_interval = 1000

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_layout = QHBoxLayout()
        title_label = QLabel("实时评审")
        title_label.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        weight_tag = QLabel("标准权重")
        weight_tag.setStyleSheet("""
            background-color: #2D2D5A;
            color: #AAAAAA;
            font-size: 11px;
            border-radius: 10px;
            padding: 2px 8px;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(weight_tag)
        layout.addLayout(title_layout)

        self.score_items = {}
        score_config = [
            {"key": "expression", "name": "表情 (40%)", "max": 100, "default": 85},
            {"key": "behavior", "name": "行为 (40%)", "max": 100, "default": 92},
            {"key": "background", "name": "背景 (20%)", "max": 100, "default": 78},
        ]
        for config in score_config:
            item_layout = QVBoxLayout()
            label_layout = QHBoxLayout()
            name_label = QLabel(config["name"])
            name_label.setFont(QFont(FONT_FAMILY, 12))
            name_label.setStyleSheet("color: #FFFFFF;")
            score_label = QLabel(str(config["default"]))
            score_label.setFont(QFont(FONT_FAMILY, 12, QFont.Bold))
            score_label.setStyleSheet("color: #FFFFFF;")
            label_layout.addWidget(name_label)
            label_layout.addStretch()
            label_layout.addWidget(score_label)
            progress_bar = QProgressBar()
            progress_bar.setFixedHeight(8)
            progress_bar.setRange(0, config["max"])
            progress_bar.setValue(config["default"])
            progress_bar.setTextVisible(False)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #2D2D5A;
                    border-radius: 3px;
                }
                QProgressBar::chunk {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7A5CFF, stop:1 #B39DFF);
                    border-radius: 3px;
                }
            """)
            item_layout.addLayout(label_layout)
            item_layout.addWidget(progress_bar)
            layout.addLayout(item_layout)
            self.score_items[config["key"]] = {
                "label": score_label,
                "progress": progress_bar
            }

        focus_layout = QVBoxLayout()
        focus_title = QLabel("当前专注度")
        focus_title.setFont(QFont(FONT_FAMILY, 12))
        focus_title.setStyleSheet("color: #AAAAAA;")
        focus_title.setAlignment(Qt.AlignCenter)
        self.focus_score_label = QLabel("86.4")
        self.focus_score_label.setFont(QFont(FONT_FAMILY, 42, QFont.Bold))
        self.focus_score_label.setStyleSheet("color: #00E0A0;")
        self.focus_score_label.setAlignment(Qt.AlignCenter)
        focus_layout.addWidget(focus_title)
        focus_layout.addWidget(self.focus_score_label)
        layout.addLayout(focus_layout)

        curve_title = QLabel("专注度曲线")
        curve_title.setFont(QFont(FONT_FAMILY, 12))
        curve_title.setStyleSheet("color: #AAAAAA;")
        self.curve_widget = pg.PlotWidget()
        self.curve_widget.setFixedHeight(180)
        self.curve_widget.setBackground("#0A0A1A")
        self.curve_widget.showGrid(x=False, y=True, alpha=0.3)
        self.curve_widget.setYRange(0, 100)
        self.curve_widget.setMouseEnabled(x=False, y=False)
        self.curve_widget.hideAxis("bottom")
        self.curve_data = [86.4] * 50
        self.curve_line = self.curve_widget.plot(self.curve_data, pen=pg.mkPen(color="#00E0A0", width=2))
        layout.addWidget(curve_title)
        layout.addWidget(self.curve_widget)

        layout.addStretch()

        self.control_btn = QPushButton("✅ 启动/完成")
        self.control_btn.setFixedHeight(48)
        self.control_btn.setFont(QFont(FONT_FAMILY, 13, QFont.Bold))
        self.control_btn.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7A5CFF, stop:1 #997AFF);
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8A6CFF, stop:1 #A98AFF);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6A4CEE, stop:1 #8A6CEE);
            }
        """)
        self.control_btn.clicked.connect(self.on_control_click)
        layout.addWidget(self.control_btn)

    def update_scores(self, score_dict):
        if "expression" in score_dict:
            val = score_dict["expression"]
            self.score_items["expression"]["label"].setText(str(val))
            self.score_items["expression"]["progress"].setValue(val)
        if "behavior" in score_dict:
            val = score_dict["behavior"]
            self.score_items["behavior"]["label"].setText(str(val))
            self.score_items["behavior"]["progress"].setValue(val)
        if "background" in score_dict:
            val = score_dict["background"]
            self.score_items["background"]["label"].setText(str(val))
            self.score_items["background"]["progress"].setValue(val)
        if "final_focus" in score_dict:
            val = score_dict["final_focus"]
            self.focus_score_label.setText(f"{val:.1f}")
            self.curve_data.append(val)
            self.curve_data.pop(0)
            self.curve_line.setData(self.curve_data)

    def generate_simulated_data(self):
        import random
        
        base_expression = 85
        base_behavior = 92
        base_background = 78
        
        expression_variation = random.randint(-10, 10)
        behavior_variation = random.randint(-8, 8)
        background_variation = random.randint(-5, 5)
        
        expression = max(60, min(100, base_expression + expression_variation))
        behavior = max(70, min(100, base_behavior + behavior_variation))
        background = max(65, min(100, base_background + background_variation))
        
        final_focus = (expression * 0.4 + behavior * 0.4 + background * 0.2)
        
        score_dict = {
            "expression": int(expression),
            "behavior": int(behavior),
            "background": int(background),
            "final_focus": final_focus
        }
        
        self.score_updated.emit(score_dict)

    def on_control_click(self):
        if not self.is_running:
            self.is_running = True
            self.control_btn.setText("⏹️ 停止分析")
            self.start_analysis.emit()
            self.simulation_timer.start(self.simulation_interval)
        else:
            self.is_running = False
            self.control_btn.setText("✅ 启动/完成")
            self.stop_analysis.emit()
            self.simulation_timer.stop()
