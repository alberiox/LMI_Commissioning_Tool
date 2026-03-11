from PySide6 import QtCore, QtWidgets


CARD_STYLE = """
QFrame {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #101722, stop:1 #151d2a);
    border: 1px solid #23324A;
    border-radius: 22px;
}
"""

TITLE_STYLE = """
QLabel {
    background: #536D7E;
    color: #EEF3F8;
    border-radius: 18px;
    padding: 10px 14px;
    font-size: 18px;
    font-weight: 700;
}
"""

TEXT_STYLE = "color:#D9E0E8;font-size:14px;"
HEAD_STYLE = "color:#F4F7FB;font-size:24px;font-weight:800;"


class ReportCard(QtWidgets.QFrame):
    def __init__(self, title: str, lines: list[str], parent=None):
        super().__init__(parent)
        self.setStyleSheet(CARD_STYLE)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(22, 22, 22, 22)
        lay.setSpacing(14)

        ttl = QtWidgets.QLabel(title)
        ttl.setAlignment(QtCore.Qt.AlignCenter)
        ttl.setStyleSheet(TITLE_STYLE)
        lay.addWidget(ttl)

        for line in lines:
            lbl = QtWidgets.QLabel("• " + line)
            lbl.setWordWrap(True)
            lbl.setStyleSheet(TEXT_STYLE)
            lay.addWidget(lbl)

        lay.addStretch(1)


class ReportPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        title = QtWidgets.QLabel("Report / Validation")
        title.setStyleSheet(HEAD_STYLE)
        root.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        grid.addWidget(ReportCard("VALIDATION SUMMARY", [
            "Use this area for final checks before release.",
            "Confirm sensors, geometry, hydraulics and tables are coherent.",
            "Confirm limiter warning and overload thresholds."
        ]), 0, 0)

        grid.addWidget(ReportCard("LOGGING / EXPORT", [
            "CSV logging can be connected here in a later step.",
            "Recommended fields: geometry, pressures, model mass, load, capacity, margin and utilization."
        ]), 0, 1)

        grid.addWidget(ReportCard("COMMISSIONING NOTES", [
            "Keep notes on anomalies, offsets, suspect sensors and final approved settings."
        ]), 1, 0)

        grid.addWidget(ReportCard("NEXT STEP", [
            "This page is a styled placeholder ready for future export and summary features."
        ]), 1, 1)

        for i in range(2):
            grid.setColumnStretch(i, 1)

        root.addLayout(grid)
        root.addStretch(1)

    def update_data(self, d):
        pass
