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
    color: #EAF2F7;
    border-radius: 18px;
    padding: 10px 14px;
    font-size: 18px;
    font-weight: 700;
}
"""

VALUE_STYLE = """
QLabel {
    color: #F3F6FA;
    font-size: 15px;
    font-weight: 700;
}
"""

NAME_STYLE = """
QLabel {
    color: #D9E0E8;
    font-size: 14px;
}
"""


def _safe_num(v, default=0.0):
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


class StatusBadge(QtWidgets.QLabel):
    def __init__(self, text="NO DATA", parent=None):
        super().__init__(text, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumWidth(110)
        self.setMinimumHeight(34)
        self.set_status(text)

    def set_status(self, status: str):
        status = (status or "NO DATA").upper()
        colors = {
            "OK": ("#0F4F35", "#2B8B65", "#9BE8C8"),
            "WARN": ("#5C4310", "#9A6E12", "#F2D27A"),
            "FAULT": ("#61212A", "#A73B4A", "#FFB2BE"),
            "NO DATA": ("#39414A", "#566170", "#D7DEE8"),
        }
        bg, border, fg = colors.get(status, colors["NO DATA"])
        self.setText(status)
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                border: 1px solid {border};
                color: {fg};
                border-radius: 14px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: 700;
            }}
        """)


class InfoRow(QtWidgets.QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.name_lbl = QtWidgets.QLabel(name)
        self.name_lbl.setStyleSheet(NAME_STYLE)
        self.value_lbl = QtWidgets.QLabel("--")
        self.value_lbl.setStyleSheet(VALUE_STYLE)
        self.badge = StatusBadge("NO DATA")

        layout.addWidget(self.name_lbl)
        layout.addStretch(1)
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.badge)

    def set_value(self, text: str, status: str):
        self.value_lbl.setText(text)
        self.badge.set_status(status)


class DashboardCard(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet(CARD_STYLE)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        self.title_lbl = QtWidgets.QLabel(title)
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setStyleSheet(TITLE_STYLE)
        layout.addWidget(self.title_lbl)

        self.body = QtWidgets.QVBoxLayout()
        self.body.setSpacing(16)
        layout.addLayout(self.body)
        layout.addStretch(1)

    def add_widget(self, widget):
        self.body.addWidget(widget)


class GeometryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        title = QtWidgets.QLabel("Geometry & Working Point")
        title.setStyleSheet("color:#F4F7FB;font-size:24px;font-weight:800;")
        root.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)
        root.addLayout(grid)
        root.addStretch(1)

        self.boom_card = DashboardCard("BOOM")
        self.ballast_card = DashboardCard("BALLAST")
        self.wp_card = DashboardCard("WORKING POINT")
        self.status_card = DashboardCard("GEOMETRY STATUS")

        grid.addWidget(self.boom_card, 0, 0)
        grid.addWidget(self.ballast_card, 0, 1)
        grid.addWidget(self.wp_card, 1, 0)
        grid.addWidget(self.status_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.boom_len_meas = InfoRow("Length meas")
        self.boom_len = InfoRow("Length filtered")
        self.boom_ang_meas = InfoRow("Angle meas")
        self.boom_ang = InfoRow("Angle filtered")
        self.boom_card.add_widget(self.boom_len_meas)
        self.boom_card.add_widget(self.boom_len)
        self.boom_card.add_widget(self.boom_ang_meas)
        self.boom_card.add_widget(self.boom_ang)

        self.ballast_pos_meas = InfoRow("Position meas")
        self.ballast_pos = InfoRow("Position filtered")
        self.ballast_ang_meas = InfoRow("Angle meas")
        self.ballast_ang = InfoRow("Angle filtered")
        self.ballast_card.add_widget(self.ballast_pos_meas)
        self.ballast_card.add_widget(self.ballast_pos)
        self.ballast_card.add_widget(self.ballast_ang_meas)
        self.ballast_card.add_widget(self.ballast_ang)

        self.dist = InfoRow("Distance")
        self.height = InfoRow("Height")
        self.radius = InfoRow("Radius / boom")
        self.wp_card.add_widget(self.dist)
        self.wp_card.add_widget(self.height)
        self.wp_card.add_widget(self.radius)

        self.boom_status = InfoRow("Boom inputs")
        self.ballast_status = InfoRow("Ballast inputs")
        self.wp_status = InfoRow("Working point")
        self.status_card.add_widget(self.boom_status)
        self.status_card.add_widget(self.ballast_status)
        self.status_card.add_widget(self.wp_status)

    def _get(self, d, *names, default=None):
        for name in names:
            if hasattr(d, name):
                v = getattr(d, name)
                if v is not None:
                    return v
            if isinstance(d, dict) and name in d and d[name] is not None:
                return d[name]
        return default

    def _fmt_mm(self, value, decimals=0):
        if value is None:
            return "--"
        return f"{_safe_num(value):,.{decimals}f} mm".replace(",", " ")

    def _fmt_mm_to_m(self, value, decimals=3):
        if value is None:
            return "--"
        return f"{_safe_num(value) / 1000.0:,.{decimals}f} m".replace(",", " ")

    def _fmt_deg(self, value, decimals=2):
        if value is None:
            return "--"
        return f"{_safe_num(value):,.{decimals}f} °".replace(",", " ")

    def _paired_status(self, meas, filt):
        if meas is None and filt is None:
            return "NO DATA"
        m = _safe_num(meas, 0.0) if meas is not None else None
        f = _safe_num(filt, 0.0) if filt is not None else None
        if m is None or f is None:
            return "WARN"
        if abs(m) < 0.01 and abs(f) < 0.01:
            return "NO DATA"
        return "OK"

    def _working_point_status(self, dist_mm, height_mm, radius_mm):
        vals = [dist_mm, height_mm, radius_mm]
        if all(v is None for v in vals):
            return "NO DATA"
        d = _safe_num(dist_mm, 0.0) if dist_mm is not None else 0.0
        h = _safe_num(height_mm, 0.0) if height_mm is not None else 0.0
        r = _safe_num(radius_mm, 0.0) if radius_mm is not None else 0.0
        if abs(d) < 0.01 and abs(h) < 0.01 and abs(r) < 0.01:
            return "NO DATA"
        return "OK"

    def update_data(self, d):
        boom_pos_meas = self._get(d, "boom_pos_mm_meas")
        boom_pos = self._get(d, "boom_pos_mm", "radius_mm")
        boom_ang_meas = self._get(d, "boom_ang_deg_meas")
        boom_ang = self._get(d, "boom_ang_deg")

        ballast_pos_meas = self._get(d, "ballast_pos_mm_meas")
        ballast_pos = self._get(d, "ballast_pos_mm")
        ballast_ang_meas = self._get(d, "ballast_ang_deg_meas")
        ballast_ang = self._get(d, "ballast_ang_deg")

        dist_mm = self._get(d, "dist_mm")
        height_mm = self._get(d, "height_mm")
        radius_mm = self._get(d, "radius_mm", "boom_pos_mm")

        boom_status = self._paired_status(boom_pos_meas, boom_pos)
        boom_ang_status = self._paired_status(boom_ang_meas, boom_ang)
        ballast_status = self._paired_status(ballast_pos_meas, ballast_pos)
        ballast_ang_status = self._paired_status(ballast_ang_meas, ballast_ang)
        wp_status = self._working_point_status(dist_mm, height_mm, radius_mm)

        self.boom_len_meas.set_value(self._fmt_mm_to_m(boom_pos_meas, 3), boom_status)
        self.boom_len.set_value(self._fmt_mm_to_m(boom_pos, 3), boom_status)
        self.boom_ang_meas.set_value(self._fmt_deg(boom_ang_meas, 2), boom_ang_status)
        self.boom_ang.set_value(self._fmt_deg(boom_ang, 2), boom_ang_status)

        self.ballast_pos_meas.set_value(self._fmt_mm(ballast_pos_meas, 0), ballast_status)
        self.ballast_pos.set_value(self._fmt_mm(ballast_pos, 0), ballast_status)
        self.ballast_ang_meas.set_value(self._fmt_deg(ballast_ang_meas, 2), ballast_ang_status)
        self.ballast_ang.set_value(self._fmt_deg(ballast_ang, 2), ballast_ang_status)

        self.dist.set_value(self._fmt_mm_to_m(dist_mm, 3), wp_status)
        self.height.set_value(self._fmt_mm_to_m(height_mm, 3), wp_status)
        self.radius.set_value(self._fmt_mm_to_m(radius_mm, 3), wp_status)

        self.boom_status.set_value(
            f"{self._fmt_mm_to_m(boom_pos, 3)} / {self._fmt_deg(boom_ang, 2)}",
            "OK" if boom_status == "OK" and boom_ang_status == "OK" else ("WARN" if "WARN" in (boom_status, boom_ang_status) else ("NO DATA" if "NO DATA" in (boom_status, boom_ang_status) else "FAULT")),
        )
        self.ballast_status.set_value(
            f"{self._fmt_mm(ballast_pos, 0)} / {self._fmt_deg(ballast_ang, 2)}",
            "OK" if ballast_status == "OK" and ballast_ang_status == "OK" else ("WARN" if "WARN" in (ballast_status, ballast_ang_status) else ("NO DATA" if "NO DATA" in (ballast_status, ballast_ang_status) else "FAULT")),
        )
        self.wp_status.set_value(
            f"D {self._fmt_mm_to_m(dist_mm, 3)}  H {self._fmt_mm_to_m(height_mm, 3)}",
            wp_status,
        )
