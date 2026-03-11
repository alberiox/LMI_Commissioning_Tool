from PySide6 import QtCore, QtWidgets

class KPICard(QtWidgets.QFrame):
    def __init__(self, title: str, unit: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.title = QtWidgets.QLabel(title)
        self.title.setObjectName("H2")
        self.value = QtWidgets.QLabel("--")
        self.value.setStyleSheet("font-size: 28px; font-weight: 800;")
        self.unit = QtWidgets.QLabel(unit)
        self.unit.setObjectName("H2")

        top = QtWidgets.QHBoxLayout()
        top.addWidget(self.title)
        top.addStretch(1)
        top.addWidget(self.unit)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.addLayout(top)
        lay.addWidget(self.value, alignment=QtCore.Qt.AlignLeft)
        lay.addStretch(1)

    def set_value(self, txt: str):
        self.value.setText(txt)