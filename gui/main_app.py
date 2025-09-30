from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
    QWidget, QLabel, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from api.openai_api import get_image_description  

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenAI 이미지 설명 프로그램")
        self.setGeometry(100, 100, 700, 500)

        # 이미지 출력 라벨
        self.image_label = QLabel("이미지를 불러오세요")
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # 이미지 불러오기 버튼
        self.load_button = QPushButton("이미지 열기")
        self.load_button.clicked.connect(self.load_image)

        # 텍스트 입력
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("GPT에게 보낼 추가 프롬프트 입력")

        # GPT 설명 출력
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # 설명 생성 버튼
        
        self.generate_button = QPushButton("gpt 설명 생성")
        self.generate_button.clicked.connect(self.generate_description)
        


        # 레이아웃 설정 예시
        # 상단 수평 레이아웃: 이미지 라벨 + 이미지 불러오기 버튼
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.image_label)        # 왼쪽: 이미지를 보여주는 QLabel
        top_layout.addWidget(self.load_button)        # 오른쪽: 이미지 불러오기 버튼
        
        # 전체 수직 레이아웃 구성
        layout = QVBoxLayout()
        
        # 첫 번째 줄: 이미지 라벨과 버튼이 나란히 들어간 수평 레이아웃
        layout.addLayout(top_layout)
        # 두 번째 줄: 사용자 입력창 (GPT에게 보낼 프롬프트)
        layout.addWidget(self.text_input)
        # 세 번째 줄: GPT 설명 생성 버튼
        layout.addWidget(self.generate_button)
        # 네 번째 줄: GPT의 결과 텍스트 출력창
        layout.addWidget(self.result_output)
        
        # 레이아웃을 QWidget에 붙이고, 해당 위젯을 윈도우의 중앙 위젯으로 설정
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = None                        # 선택한 이미지 경로 저장
    
    # 이미지 불러오기 + 이미지 고정
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, '이미지 선택', '', 'Images (*.png *.jpg *.jpeg)')
        if path:
            pixmap = QPixmap(path).scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_path = path
    

    def generate_description(self):
        if not self.image_path:
            self.result_output.setPlainText("이미지를 먼저 선택하세요.")
            return
        prompt = self.text_input.toPlainText().strip()
        try:
            result = get_image_description(self.image_path, prompt)
            self.result_output.setPlainText(result or "(빈 응답)")
        except Exception as e:
            self.result_output.setPlainText(f"오류: {e}")

"""
    def generate_description(self):
        prompt = self.text_input.toPlainText()
        result = get_image_description(self.image_path, prompt) 
        # 코드 구현
        self.result_output.setPlainText(result)
"""
