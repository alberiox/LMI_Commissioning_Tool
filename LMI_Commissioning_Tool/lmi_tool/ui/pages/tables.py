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
    background: #6A7C8F;
    color: #EEF3F8;
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


def _fmt(v, decimals=2, unit=""):
    try:
        if v is None:
            return "--"
        txt = f"{float(v):,.{decimals}f}".replace(",", " ")
        return f"{txt} {unit}".strip()
    except Exception:
        return str(v)


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


class TablesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        title = QtWidgets.QLabel("Load Tables Debug")
        title.setStyleSheet("color:#F4F7FB;font-size:24px;font-weight:800;")
        root.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)
        root.addLayout(grid)
        root.addStretch(1)

        self.selection_card = DashboardCard("SELECTION")
        self.input_card = DashboardCard("INTERPOLATION INPUT")
        self.index_card = DashboardCard("INTERPOLATION INDEXES")
        self.cell_card = DashboardCard("INTERPOLATION CELL")

        grid.addWidget(self.selection_card, 0, 0)
        grid.addWidget(self.input_card, 0, 1)
        grid.addWidget(self.index_card, 1, 0)
        grid.addWidget(self.cell_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.act_table = InfoRow("ActTable")
        self.cur_sel = InfoRow("CurSel")
        self.hyst_mm = InfoRow("Hyst")
        self.cap_t = InfoRow("Cap limiter")

        self.selection_card.add_widget(self.act_table)
        self.selection_card.add_widget(self.cur_sel)
        self.selection_card.add_widget(self.hyst_mm)
        self.selection_card.add_widget(self.cap_t)

        self.interp_dist = InfoRow("Dist")
        self.interp_radius = InfoRow("Radius")
        self.interp_cap = InfoRow("Interp Cap")

        self.input_card.add_widget(self.interp_dist)
        self.input_card.add_widget(self.interp_radius)
        self.input_card.add_widget(self.interp_cap)

        self.idx_id = InfoRow("iD")
        self.idx_ir = InfoRow("iR")
        self.idx_td = InfoRow("tD")
        self.idx_tr = InfoRow("tR")

        self.index_card.add_widget(self.idx_id)
        self.index_card.add_widget(self.idx_ir)
        self.index_card.add_widget(self.idx_td)
        self.index_card.add_widget(self.idx_tr)

        self.v00 = InfoRow("V00")
        self.v10 = InfoRow("V10")
        self.v01 = InfoRow("V01")
        self.v11 = InfoRow("V11")

        self.cell_card.add_widget(self.v00)
        self.cell_card.add_widget(self.v10)
        self.cell_card.add_widget(self.v01)
        self.cell_card.add_widget(self.v11)

    def _get(self, d, *names, default=None):
        for name in names:
            if hasattr(d, name):
                v = getattr(d, name)
                if v is not None:
                    return v
            if isinstance(d, dict) and name in d and d[name] is not None:
                return d[name]
        return default

    def _status_numeric(self, value, eps=0.000001):
        if value is None:
            return "NO DATA"
        try:
            return "NO DATA" if abs(float(value)) <= eps else "OK"
        except Exception:
            return "OK"

    def _status_selector(self, value):
        if value is None:
            return "NO DATA"
        try:
            return "NO DATA" if int(value) == 0 else "OK"
        except Exception:
            return "OK"

    def _status_interp(self, dist, radius, cap):
        if dist is None and radius is None and cap is None:
            return "NO DATA"
        if abs(_safe_num(dist)) < 0.000001 and abs(_safe_num(radius)) < 0.000001 and abs(_safe_num(cap)) < 0.000001:
            return "NO DATA"
        return "OK"

    def update_data(self, d):
        act_table = self._get(d, "act_table")
        cur_sel = self._get(d, "cur_sel")
        hyst_mm = self._get(d, "hyst_mm")
        cap_t = self._get(d, "cap_t")

        sel_status = self._status_selector(cur_sel)
        self.act_table.set_value(str(act_table if act_table is not None else "--"), "OK" if act_table not in (None, "", "---") else "NO DATA")
        self.cur_sel.set_value(str(cur_sel if cur_sel is not None else "--"), sel_status)
        self.hyst_mm.set_value(_fmt(hyst_mm, 0, "mm"), self._status_numeric(hyst_mm))
        self.cap_t.set_value(_fmt(cap_t, 2, "t"), self._status_numeric(cap_t))

        interp_dist = self._get(d, "interp_dist_m")
        interp_radius = self._get(d, "interp_radius_m")
        interp_cap = self._get(d, "interp_cap_t")
        interp_status = self._status_interp(interp_dist, interp_radius, interp_cap)

        self.interp_dist.set_value(_fmt(interp_dist, 3, "m"), interp_status)
        self.interp_radius.set_value(_fmt(interp_radius, 3, "m"), interp_status)
        self.interp_cap.set_value(_fmt(interp_cap, 2, "t"), interp_status)

        cap_dbg_id = self._get(d, "cap_dbg_id")
        cap_dbg_ir = self._get(d, "cap_dbg_ir")
        cap_dbg_td = self._get(d, "cap_dbg_td")
        cap_dbg_tr = self._get(d, "cap_dbg_tr")

        self.idx_id.set_value(str(cap_dbg_id if cap_dbg_id is not None else "--"), self._status_selector(cap_dbg_id))
        self.idx_ir.set_value(str(cap_dbg_ir if cap_dbg_ir is not None else "--"), self._status_selector(cap_dbg_ir))
        self.idx_td.set_value(_fmt(cap_dbg_td, 4), self._status_numeric(cap_dbg_td))
        self.idx_tr.set_value(_fmt(cap_dbg_tr, 4), self._status_numeric(cap_dbg_tr))

        cap_dbg_v00 = self._get(d, "cap_dbg_v00")
        cap_dbg_v10 = self._get(d, "cap_dbg_v10")
        cap_dbg_v01 = self._get(d, "cap_dbg_v01")
        cap_dbg_v11 = self._get(d, "cap_dbg_v11")

        cell_status = "NO DATA"
        if any(v is not None and abs(_safe_num(v)) > 0.000001 for v in [cap_dbg_v00, cap_dbg_v10, cap_dbg_v01, cap_dbg_v11]):
            cell_status = "OK"

        self.v00.set_value(_fmt(cap_dbg_v00, 2, "t"), cell_status if cap_dbg_v00 is not None else "NO DATA")
        self.v10.set_value(_fmt(cap_dbg_v10, 2, "t"), cell_status if cap_dbg_v10 is not None else "NO DATA")
        self.v01.set_value(_fmt(cap_dbg_v01, 2, "t"), cell_status if cap_dbg_v01 is not None else "NO DATA")
        self.v11.set_value(_fmt(cap_dbg_v11, 2, "t"), cell_status if cap_dbg_v11 is not None else "NO DATA")
