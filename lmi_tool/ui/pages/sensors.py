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
    background: #4A6D7C;
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

BAR_BG = """
QFrame {
    background: #0A111B;
    border: 1px solid #223652;
    border-radius: 12px;
}
"""

BAR_FILL = """
QFrame {
    background: #4A6D7C;
    border: none;
    border-radius: 10px;
}
"""


def _safe_num(v, default=0.0):
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def _safe_int(v, default=0):
    try:
        if v is None:
            return default
        if isinstance(v, str):
            s = v.strip().upper()
            if s.startswith("16#"):
                return int(s[3:], 16)
            if s.startswith("0X"):
                return int(s, 16)
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return default


def _fault_text_sfili(fault_code, offset_valid=True):
    code = _safe_int(fault_code, 0)
    mapping = {
        0x0000: "No fault",
        0x0002: "Invalid cycle time (CycleTime_s <= 0)",
        0x0101: "Position out of range",
        0x0102: "Angle out of range",
        0x0201: "Position speed too high",
        0x0202: "Angle speed too high",
        0x0211: "Position step change too large",
        0x0212: "Angle step change too large",
        0x0301: "Position stuck detected",
        0x0302: "Angle stuck detected",
        0x0401: "Home offset capture denied (not in home window)",
    }
    if not bool(offset_valid):
        return "No offset valid"
    return mapping.get(code, "Unknown fault code")


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
        self.setStyleSheet(
            f"""
            QLabel {{
                background: {bg};
                border: 1px solid {border};
                color: {fg};
                border-radius: 14px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: 700;
            }}
            """
        )


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


class PressureRow(QtWidgets.QWidget):
    def __init__(self, name: str, unit: str = "bar", max_value: float = 400.0, parent=None):
        super().__init__(parent)
        self.max_value = max_value
        self.unit = unit

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        top = QtWidgets.QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)

        self.name_lbl = QtWidgets.QLabel(name)
        self.name_lbl.setStyleSheet(NAME_STYLE)
        self.value_lbl = QtWidgets.QLabel(f"0.0 {unit}")
        self.value_lbl.setStyleSheet(VALUE_STYLE)
        self.badge = StatusBadge("NO DATA")

        top.addWidget(self.name_lbl)
        top.addStretch(1)
        top.addWidget(self.value_lbl)
        top.addSpacing(10)
        top.addWidget(self.badge)

        self.bar_bg = QtWidgets.QFrame()
        self.bar_bg.setStyleSheet(BAR_BG)
        self.bar_bg.setMinimumHeight(28)
        self.bar_bg.setMaximumHeight(28)

        self.bar_fill = QtWidgets.QFrame(self.bar_bg)
        self.bar_fill.setStyleSheet(BAR_FILL)
        self.bar_fill.setGeometry(2, 2, 0, 24)

        self.bar_text = QtWidgets.QLabel(self.bar_bg)
        self.bar_text.setAlignment(QtCore.Qt.AlignCenter)
        self.bar_text.setStyleSheet("color:#EAF2F7;font-size:13px;font-weight:700;background:transparent;")

        layout.addLayout(top)
        layout.addWidget(self.bar_bg)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_fill(self._last_ratio if hasattr(self, "_last_ratio") else 0.0)
        self.bar_text.setGeometry(self.bar_bg.rect())

    def _apply_fill(self, ratio: float):
        self._last_ratio = max(0.0, min(1.0, ratio))
        total_w = max(0, self.bar_bg.width() - 4)
        fill_w = int(total_w * self._last_ratio)
        self.bar_fill.setGeometry(2, 2, fill_w, max(0, self.bar_bg.height() - 4))

    def set_value(self, value, status: str):
        num = _safe_num(value, 0.0)
        self.value_lbl.setText(f"{num:.1f} {self.unit}")
        self.bar_text.setText(f"{num:.0f} {self.unit}")
        self.badge.set_status(status)
        ratio = 0.0 if self.max_value <= 0 else num / self.max_value
        self._apply_fill(ratio)


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


class SensorsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        title = QtWidgets.QLabel("Sensors Health")
        title.setStyleSheet("color:#F4F7FB;font-size:24px;font-weight:800;")
        root.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)
        root.addLayout(grid)
        root.addStretch(1)

        self.boom_card = DashboardCard("BOOM")
        self.ballast_card = DashboardCard("BALLAST")
        self.pressure_card = DashboardCard("PRESSURES")
        self.supply_card = DashboardCard("SUPPLY")

        grid.addWidget(self.boom_card, 0, 0)
        grid.addWidget(self.ballast_card, 0, 1)
        grid.addWidget(self.pressure_card, 1, 0)
        grid.addWidget(self.supply_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.boom_pos_meas = InfoRow("Position meas")
        self.boom_pos = InfoRow("Position filtered")
        self.boom_ang_meas = InfoRow("Angle meas")
        self.boom_ang = InfoRow("Angle filtered")
        self.boom_status = InfoRow("Status")
        self.boom_card.add_widget(self.boom_pos_meas)
        self.boom_card.add_widget(self.boom_pos)
        self.boom_card.add_widget(self.boom_ang_meas)
        self.boom_card.add_widget(self.boom_ang)
        self.boom_card.add_widget(self.boom_status)

        self.ballast_pos_meas = InfoRow("Position meas")
        self.ballast_pos = InfoRow("Position filtered")
        self.ballast_ang_meas = InfoRow("Angle meas")
        self.ballast_ang = InfoRow("Angle filtered")
        self.ballast_status = InfoRow("Status")
        self.ballast_card.add_widget(self.ballast_pos_meas)
        self.ballast_card.add_widget(self.ballast_pos)
        self.ballast_card.add_widget(self.ballast_ang_meas)
        self.ballast_card.add_widget(self.ballast_ang)
        self.ballast_card.add_widget(self.ballast_status)

        self.ph1a = PressureRow("PH1A")
        self.ph1b = PressureRow("PH1B")
        self.pl1a = PressureRow("PL1A")
        self.pl1b = PressureRow("PL1B")
        self.pressure_card.add_widget(self.ph1a)
        self.pressure_card.add_widget(self.ph1b)
        self.pressure_card.add_widget(self.pl1a)
        self.pressure_card.add_widget(self.pl1b)

        self.supply_v = InfoRow("Sensor supply")
        self.ph1a_uout = InfoRow("PH1A Uout")
        self.ph1b_uout = InfoRow("PH1B Uout")
        self.pl1a_uout = InfoRow("PL1A Uout")
        self.pl1b_uout = InfoRow("PL1B Uout")
        self.supply_card.add_widget(self.supply_v)
        self.supply_card.add_widget(self.ph1a_uout)
        self.supply_card.add_widget(self.ph1b_uout)
        self.supply_card.add_widget(self.pl1a_uout)
        self.supply_card.add_widget(self.pl1b_uout)

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

    def _fmt_deg(self, value, decimals=2):
        if value is None:
            return "--"
        return f"{_safe_num(value):,.{decimals}f} °".replace(",", " ")

    def _fmt_v(self, value, decimals=3):
        if value is None:
            return "--"
        return f"{_safe_num(value):,.{decimals}f} V".replace(",", " ")

    def _group_status(self, *values, warn=0, fault_active=0):
        if bool(fault_active):
            return "FAULT"
        if _safe_int(warn, 0) != 0:
            return "WARN"
        if all(abs(_safe_num(v, 0.0)) < 0.000001 for v in values):
            return "NO DATA"
        return "OK"

    def _status_from_numeric(self, value, zero_is_no_data=True):
        if value is None:
            return "NO DATA"
        v = _safe_num(value)
        if zero_is_no_data and abs(v) < 0.000001:
            return "NO DATA"
        return "OK"

    def _sensor_status_text(self, fault_code, offset_valid, group_status):
        if group_status == "NO DATA":
            return "No data"
        if not bool(offset_valid):
            return "No offset valid"
        code = _safe_int(fault_code, 0)
        if code == 0:
            return "OK"
        return _fault_text_sfili(code, offset_valid)

    def update_data(self, d):
        boom_pos_meas = self._get(d, "boom_pos_mm_meas", "boom_pos_meas")
        boom_pos = self._get(d, "boom_pos_mm", "boom_pos")
        boom_ang_meas = self._get(d, "boom_ang_deg_meas", "boom_ang_meas")
        boom_ang = self._get(d, "boom_ang_deg", "boom_ang")
        boom_fault_active = self._get(d, "boom_fault", default=False)
        boom_fault_code = self._get(d, "boom_fault_code", "boom_faultcode", default=0)
        boom_warn = self._get(d, "boom_warn", default=0)
        boom_offset_valid = self._get(d, "boom_offset_valid", "offset_valid", default=True)
        boom_status = self._group_status(
            boom_pos_meas, boom_pos, boom_ang_meas, boom_ang,
            warn=boom_warn, fault_active=boom_fault_active
        )

        self.boom_pos_meas.set_value(self._fmt_mm(boom_pos_meas), self._status_from_numeric(boom_pos_meas))
        self.boom_pos.set_value(self._fmt_mm(boom_pos), self._status_from_numeric(boom_pos))
        self.boom_ang_meas.set_value(self._fmt_deg(boom_ang_meas), self._status_from_numeric(boom_ang_meas))
        self.boom_ang.set_value(self._fmt_deg(boom_ang), self._status_from_numeric(boom_ang))
        self.boom_status.set_value(self._sensor_status_text(boom_fault_code, boom_offset_valid, boom_status), boom_status)

        ballast_pos_meas = self._get(d, "ballast_pos_mm_meas", "ballast_pos_meas")
        ballast_pos = self._get(d, "ballast_pos_mm", "ballast_pos")
        ballast_ang_meas = self._get(d, "ballast_ang_deg_meas", "ballast_ang_meas")
        ballast_ang = self._get(d, "ballast_ang_deg", "ballast_ang")
        ballast_fault_active = self._get(d, "ballast_fault", default=False)
        ballast_fault_code = self._get(d, "ballast_fault_code", "ballast_faultcode", default=0)
        ballast_warn = self._get(d, "ballast_warn", default=0)
        ballast_offset_valid = self._get(d, "ballast_offset_valid", default=True)
        ballast_status = self._group_status(
            ballast_pos_meas, ballast_pos, ballast_ang_meas, ballast_ang,
            warn=ballast_warn, fault_active=ballast_fault_active
        )

        self.ballast_pos_meas.set_value(self._fmt_mm(ballast_pos_meas), self._status_from_numeric(ballast_pos_meas))
        self.ballast_pos.set_value(self._fmt_mm(ballast_pos), self._status_from_numeric(ballast_pos))
        self.ballast_ang_meas.set_value(self._fmt_deg(ballast_ang_meas), self._status_from_numeric(ballast_ang_meas))
        self.ballast_ang.set_value(self._fmt_deg(ballast_ang), self._status_from_numeric(ballast_ang))
        self.ballast_status.set_value(self._sensor_status_text(ballast_fault_code, ballast_offset_valid, ballast_status), ballast_status)

        ph1a_p = self._get(d, "ph1a_p_bar")
        ph1b_p = self._get(d, "ph1b_p_bar")
        pl1a_p = self._get(d, "pl1a_p_bar")
        pl1b_p = self._get(d, "pl1b_p_bar")

        ph1a_status = self._get(d, "ph1a_status")
        ph1b_status = self._get(d, "ph1b_status")
        pl1a_status = self._get(d, "pl1a_status")
        pl1b_status = self._get(d, "pl1b_status")

        self.ph1a.set_value(ph1a_p, "OK" if _safe_int(ph1a_status, 0) else self._status_from_numeric(ph1a_p))
        self.ph1b.set_value(ph1b_p, "OK" if _safe_int(ph1b_status, 0) else self._status_from_numeric(ph1b_p))
        self.pl1a.set_value(pl1a_p, "OK" if _safe_int(pl1a_status, 0) else self._status_from_numeric(pl1a_p))
        self.pl1b.set_value(pl1b_p, "OK" if _safe_int(pl1b_status, 0) else self._status_from_numeric(pl1b_p))

        supply_v = (
            self._get(d, "supply_v")
            or self._get(d, "ph1a_us_v")
            or self._get(d, "ph1b_us_v")
            or self._get(d, "pl1a_us_v")
            or self._get(d, "pl1b_us_v")
        )
        supply_status = "OK" if _safe_num(supply_v) >= 9.0 else ("WARN" if _safe_num(supply_v) >= 1.0 else "NO DATA")

        self.supply_v.set_value(self._fmt_v(supply_v), supply_status)
        self.ph1a_uout.set_value(self._fmt_v(self._get(d, "ph1a_uout_v")), self._status_from_numeric(self._get(d, "ph1a_uout_v")))
        self.ph1b_uout.set_value(self._fmt_v(self._get(d, "ph1b_uout_v")), self._status_from_numeric(self._get(d, "ph1b_uout_v")))
        self.pl1a_uout.set_value(self._fmt_v(self._get(d, "pl1a_uout_v")), self._status_from_numeric(self._get(d, "pl1a_uout_v")))
        self.pl1b_uout.set_value(self._fmt_v(self._get(d, "pl1b_uout_v")), self._status_from_numeric(self._get(d, "pl1b_uout_v")))
