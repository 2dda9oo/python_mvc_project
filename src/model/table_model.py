from PyQt5.QtCore import QAbstractTableModel, Qt

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 3  # 체크 텍스트, 번역 텍스트, 번역 버튼

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()]['check_text']
            elif index.column() == 1:
                return self._data[index.row()]['check_translation_text']
            elif index.column() == 2:
                return "Translate"  # Return "Translate" for the button column
        return None

    def flags(self, index):
        if index.column() == 2:  # Translation 버튼 열
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable