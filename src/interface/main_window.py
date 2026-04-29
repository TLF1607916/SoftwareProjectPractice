import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedLayout, QSplitter

from .config import WINDOW_WIDTH, WINDOW_HEIGHT, TOP_NAV_HEIGHT, LEFT_BAR_WIDTH, RIGHT_PANEL_WIDTH
from .top_nav_bar import TopNavBar
from .left_sidebar import LeftSideBar
from .video_widget import VideoWidget
from .right_panel import RightPanel
from .face_list_widget import FaceListWidget
from .data_record_widget import DataRecordWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2026网课专注度分析系统")
        self.setMinimumSize(1280, 720)
        self.showMaximized()
        self.setStyleSheet("background-color: #0F0F25;")
        self.current_mode = "网课模式"
        self.init_ui()
        self.connect_signals()
        self.init_simulated_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.stacked_layout = QStackedLayout(central_widget)
        self.stacked_layout.setContentsMargins(16, 16, 16, 16)
        
        self.top_nav = TopNavBar()
        self.top_nav.setMinimumHeight(TOP_NAV_HEIGHT)

        self.top_nav_query = TopNavBar()
        self.top_nav_query.setMinimumHeight(TOP_NAV_HEIGHT)

        self.left_sidebar = LeftSideBar()
        self.left_sidebar.setMinimumWidth(LEFT_BAR_WIDTH)
        self.left_sidebar.setMaximumWidth(LEFT_BAR_WIDTH * 2)

        self.video_widget = VideoWidget()
        self.video_widget.setMinimumWidth(400)

        self.right_panel = RightPanel()
        self.right_panel.setMinimumWidth(RIGHT_PANEL_WIDTH)
        self.right_panel.setMaximumWidth(RIGHT_PANEL_WIDTH * 2)

        self.face_list_widget = FaceListWidget()
        self.face_list_widget.setMinimumWidth(280)
        self.face_list_widget.setMaximumWidth(400)

        self.data_record_widget = DataRecordWidget()
        self.data_record_widget.setMinimumWidth(RIGHT_PANEL_WIDTH)

        monitoring_widget = QWidget()
        monitoring_layout = QVBoxLayout(monitoring_widget)
        monitoring_layout.setContentsMargins(0, 0, 0, 0)
        monitoring_layout.setSpacing(16)

        horizontal_splitter = QSplitter(Qt.Horizontal)
        horizontal_splitter.addWidget(self.left_sidebar)
        horizontal_splitter.addWidget(self.video_widget)
        horizontal_splitter.addWidget(self.right_panel)
        horizontal_splitter.setStretchFactor(1, 1)
        horizontal_splitter.setHandleWidth(8)
        horizontal_splitter.setChildrenCollapsible(False)
        horizontal_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2D2D5A;
                border-radius: 4px;
            }
            QSplitter::handle:hover {
                background-color: #41418A;
            }
            QSplitter::handle:pressed {
                background-color: #6666CC;
            }
        """)
        horizontal_splitter.setSizes([LEFT_BAR_WIDTH, 560, RIGHT_PANEL_WIDTH])

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(self.top_nav)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.setStretchFactor(1, 1)
        vertical_splitter.setHandleWidth(8)
        vertical_splitter.setChildrenCollapsible(False)
        vertical_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2D2D5A;
                border-radius: 4px;
            }
            QSplitter::handle:hover {
                background-color: #41418A;
            }
            QSplitter::handle:pressed {
                background-color: #6666CC;
            }
        """)
        vertical_splitter.setSizes([TOP_NAV_HEIGHT, 550])

        monitoring_layout.addWidget(vertical_splitter)

        query_widget = QWidget()
        query_layout = QVBoxLayout(query_widget)
        query_layout.setContentsMargins(0, 0, 0, 0)
        query_layout.setSpacing(16)

        query_vertical_splitter = QSplitter(Qt.Vertical)
        query_vertical_splitter.addWidget(self.top_nav_query)
        
        query_horizontal_splitter = QSplitter(Qt.Horizontal)
        query_horizontal_splitter.addWidget(self.face_list_widget)
        query_horizontal_splitter.addWidget(self.data_record_widget)
        query_horizontal_splitter.setStretchFactor(1, 2)
        query_horizontal_splitter.setHandleWidth(8)
        query_horizontal_splitter.setChildrenCollapsible(False)
        query_horizontal_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2D2D5A;
                border-radius: 4px;
            }
            QSplitter::handle:hover {
                background-color: #41418A;
            }
            QSplitter::handle:pressed {
                background-color: #6666CC;
            }
        """)
        query_horizontal_splitter.setSizes([280, 800])
        
        query_vertical_splitter.addWidget(query_horizontal_splitter)
        query_vertical_splitter.setStretchFactor(1, 1)
        query_vertical_splitter.setHandleWidth(8)
        query_vertical_splitter.setChildrenCollapsible(False)
        query_vertical_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2D2D5A;
                border-radius: 4px;
            }
            QSplitter::handle:hover {
                background-color: #41418A;
            }
            QSplitter::handle:pressed {
                background-color: #6666CC;
            }
        """)
        query_vertical_splitter.setSizes([TOP_NAV_HEIGHT, 550])
        
        query_layout.addWidget(query_vertical_splitter)

        self.stacked_layout.addWidget(monitoring_widget)
        self.stacked_layout.addWidget(query_widget)
        self.stacked_layout.setCurrentIndex(0)

    def connect_signals(self):
        self.top_nav.mode_changed.connect(self.on_mode_changed)
        self.top_nav_query.mode_changed.connect(self.on_mode_changed)
        self.right_panel.start_analysis.connect(self.on_start_analysis)
        self.right_panel.stop_analysis.connect(self.on_stop_analysis)
        self.face_list_widget.face_selected.connect(self.on_face_selected)

    def init_simulated_data(self):
        self.simulated_face_ids = [
            "STU_2024001",
            "STU_2024002",
            "STU_2024003",
            "STU_2024004",
            "STU_2024005",
            "STU_2024006",
            "STU_2024007",
            "STU_2024008",
        ]
        
        self.simulated_records = {}
        course_names = ["高等数学", "大学英语", "计算机基础", "线性代数", "概率论", "数据结构"]
        
        for face_id in self.simulated_face_ids:
            records = []
            for i in range(random.randint(5, 15)):
                date = f"2026-04-{random.randint(20, 29):02d}"
                hour = random.randint(9, 16)
                minute = random.randint(0, 59)
                time = f"{hour:02d}:{minute:02d}:00"
                
                record = {
                    "date": date,
                    "time": time,
                    "course_name": random.choice(course_names),
                    "focus_score": random.uniform(65.0, 98.0),
                    "expression_score": random.randint(70, 100),
                    "behavior_score": random.randint(68, 100),
                    "background_score": random.randint(60, 100)
                }
                records.append(record)
            
            records.sort(key=lambda x: (x["date"], x["time"]), reverse=True)
            self.simulated_records[face_id] = records

    def on_mode_changed(self, mode):
        self.current_mode = mode
        
        self.top_nav.set_mode(mode)
        self.top_nav_query.set_mode(mode)
        
        if mode == "数据查询":
            self.switch_to_query_mode()
        else:
            self.switch_to_monitoring_mode(mode)

    def switch_to_query_mode(self):
        self.face_list_widget.load_face_ids(self.simulated_face_ids)
        self.stacked_layout.setCurrentIndex(1)
        self.top_nav.set_mode("数据查询")
        self.top_nav_query.set_mode("数据查询")

    def switch_to_monitoring_mode(self, mode):
        self.stacked_layout.setCurrentIndex(0)
        self.top_nav.set_mode(mode)
        self.top_nav_query.set_mode(mode)

    def on_face_selected(self, face_id):
        if face_id in self.simulated_records:
            records = self.simulated_records[face_id]
            self.data_record_widget.load_records(face_id, records)

    def on_start_analysis(self):
        print("开始分析")
        self.video_widget.start_processing()

    def on_stop_analysis(self):
        print("停止分析")
        self.video_widget.stop_processing()
