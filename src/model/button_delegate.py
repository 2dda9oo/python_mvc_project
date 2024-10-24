from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.column() == 2:
            button_rect = option.rect
            button_rect.adjust(5, 5, -5, -5)  # 버튼의 크기 조정
            button_color = QtGui.QColor(200, 200, 200)  # 버튼 색상
            painter.setBrush(button_color)
            painter.drawRect(button_rect)  # 버튼 배경 그리기
            painter.setPen(Qt.black)  # 텍스트 색상
            painter.drawText(button_rect, Qt.AlignCenter, "Translate")  # 버튼 텍스트 중앙에 그리기