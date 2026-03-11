from PySide6 import QtCore, QtWidgets

class StatusPill(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__("DISCONNECTED", parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedHeight(28)
        self.setMinimumWidth(130)
        self._set("#3C424B", "#E6E8EB")

    def _set(self, bg: str, fg: str):
        self.setStyleSheet(f"""
            QLabel {{
                border-radius: 14px;
                padding: 4px 12px;
                background: {bg};
                color: {fg};
                font-weight: 800;
            }}
        """)

    def set_state(self, warning: bool, overload: bool, fault: bool):
        if fault:
            self.setText("FAULT")
            self._set("#E74C3C", "#121417")
        elif overload:
            self.setText("OVERLOAD")
            self._set("#E74C3C", "#121417")
        elif warning:
            self.setText("WARNING")
            self._set("#F1C40F", "#121417")
        else:
            self.setText("OK")
            self._set("#2ECC71", "#121417")