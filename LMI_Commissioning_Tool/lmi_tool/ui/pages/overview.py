from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg


CARD_STYLE = """
QFrame#dashCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #101722, stop:1 #151d2a);
    border: 1px solid #23324A;
    border-radius: 22px;
}
"""

TITLE_STYLE = """
QLabel {
    background: #55697C;
    color: #EEF3F8;
    border-radius: 16px;
    padding: 8px 12px;
    font-size: 16px;
    font-weight: 700;
}
"""

VALUE_STYLE = "color:#F4F7FB;font-size:28px;font-weight:800;"
UNIT_STYLE = "color:#AEB8C4;font-size:13px;font-weight:600;"
CAPTION_STYLE = "color:#D9E0E8;font-size:13px;"
HEAD_STYLE = "color:#F4F7FB;font-size:24px;font-weight:800;"
SUB_STYLE = "color:#C6D0DB;font-size:14px;"


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
        self.setMinimumWidth(120)
        self.setMinimumHeight(36)
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
                background:{bg};
                border:1px solid {border};
                color:{fg};
                border-radius:14px;
                padding:6px 12px;
                font-size:14px;
                font-weight:700;
            }}
        """)


class KPIWidget(QtWidgets.QFrame):
    def __init__(self, title: str, unit: str, color: str = "#55697C", parent=None):
        super().__init__(parent)
        self.setObjectName("dashCard")
        self.setStyleSheet(CARD_STYLE)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        self.title = QtWidgets.QLabel(title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(TITLE_STYLE.replace("#55697C", color))

        row = QtWidgets.QHBoxLayout()
        self.value = QtWidgets.QLabel("--")
        self.value.setStyleSheet(VALUE_STYLE)
        self.unit = QtWidgets.QLabel(unit)
        self.unit.setStyleSheet(UNIT_STYLE)
        row.addStretch(1)
        row.addWidget(self.value)
        row.addSpacing(6)
        row.addWidget(self.unit)
        row.addStretch(1)

        lay.addWidget(self.title)
        lay.addLayout(row)

    def set_value(self, text: str):
        self.value.setText(text)


class MetaCard(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("dashCard")
        self.setStyleSheet(CARD_STYLE)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)
        self.title = QtWidgets.QLabel(title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(TITLE_STYLE)
        self.body = QtWidgets.QLabel("--")
        self.body.setWordWrap(True)
        self.body.setStyleSheet(SUB_STYLE)
        lay.addWidget(self.title)
        lay.addWidget(self.body)

    def set_text(self, text: str):
        self.body.setText(text)


class OverviewPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        top = QtWidgets.QHBoxLayout()
        self.h1 = QtWidgets.QLabel("Overview")
        self.h1.setStyleSheet(HEAD_STYLE)
        self.status = StatusBadge("NO DATA")
        top.addWidget(self.h1)
        top.addStretch(1)
        top.addWidget(self.status)
        root.addLayout(top)

        meta = QtWidgets.QGridLayout()
        meta.setHorizontalSpacing(18)
        meta.setVerticalSpacing(18)
        self.meta_table = MetaCard("TABLE")
        self.meta_geom = MetaCard("GEOMETRY")
        meta.addWidget(self.meta_table, 0, 0)
        meta.addWidget(self.meta_geom, 0, 1)
        meta.setColumnStretch(0, 1)
        meta.setColumnStretch(1, 1)
        root.addLayout(meta)

        kpi = QtWidgets.QGridLayout()
        kpi.setHorizontalSpacing(18)
        kpi.setVerticalSpacing(18)
        self.kpi_load = KPIWidget("LOAD FILTERED", "t", "#4E7A8C")
        self.kpi_cap = KPIWidget("CAPACITY", "t", "#536D7E")
        self.kpi_margin = KPIWidget("MARGIN", "t", "#5E6F81")
        self.kpi_util = KPIWidget("UTILIZATION", "%", "#4E7365")
        kpi.addWidget(self.kpi_load, 0, 0)
        kpi.addWidget(self.kpi_cap, 0, 1)
        kpi.addWidget(self.kpi_margin, 0, 2)
        kpi.addWidget(self.kpi_util, 0, 3)
        for i in range(4):
            kpi.setColumnStretch(i, 1)
        root.addLayout(kpi)

        self.plot_card = QtWidgets.QFrame()
        self.plot_card.setObjectName("dashCard")
        self.plot_card.setStyleSheet(CARD_STYLE)
        pv = QtWidgets.QVBoxLayout(self.plot_card)
        pv.setContentsMargins(16, 16, 16, 16)
        pv.setSpacing(10)

        ttl = QtWidgets.QLabel("LIVE TREND")
        ttl.setAlignment(QtCore.Qt.AlignCenter)
        ttl.setStyleSheet(TITLE_STYLE)

        pg.setConfigOptions(antialias=True)
        self.plot = pg.PlotWidget()
        self.plot.setBackground("#121821")
        self.plot.showGrid(x=True, y=True, alpha=0.22)
        self.plot.addLegend(offset=(10, 10))
        self.plot.getAxis("left").setTextPen("#DCE5EE")
        self.plot.getAxis("bottom").setTextPen("#DCE5EE")

        self.cur_load = self.plot.plot(pen=pg.mkPen("#7DD3FC", width=2), name="Load_f_t")
        self.cur_cap = self.plot.plot(pen=pg.mkPen("#F8FAFC", width=2, style=QtCore.Qt.DashLine), name="Cap_t")
        self.cur_util = self.plot.plot(pen=pg.mkPen("#86EFAC", width=1), name="Util_pct x10")

        pv.addWidget(ttl)
        pv.addWidget(self.plot)
        root.addWidget(self.plot_card, 1)

        self.x = []
        self.y_load = []
        self.y_cap = []
        self.y_util = []

    def _get(self, d, name, default=None):
        if isinstance(d, dict):
            return d.get(name, default)
        return getattr(d, name, default)

    def _global_status(self, d):
        warning = bool(self._get(d, "warning", False))
        overload = bool(self._get(d, "overload", False))
        boom_fault = bool(self._get(d, "boom_fault", False))
        ballast_fault = bool(self._get(d, "ballast_fault", False))
        if overload or boom_fault or ballast_fault:
            return "FAULT"
        if warning:
            return "WARN"
        util = self._get(d, "util_pct", None)
        if util is None:
            return "NO DATA"
        return "OK"

    def update_data(self, d):
        self.status.set_status(self._global_status(d))

        act_table = self._get(d, "act_table", "---")
        cur_sel = self._get(d, "cur_sel", "---")
        self.meta_table.set_text(f"Table: {act_table}\nCurSel: {cur_sel}")

        boom_pos_mm = _safe_num(self._get(d, "boom_pos_mm", 0.0))
        dist_mm = _safe_num(self._get(d, "dist_mm", 0.0))
        boom_ang_deg = _safe_num(self._get(d, "boom_ang_deg", 0.0))
        ballast_pos_mm = _safe_num(self._get(d, "ballast_pos_mm", 0.0))
        self.meta_geom.set_text(
            f"Radius: {boom_pos_mm/1000.0:.3f} m\n"
            f"Dist: {dist_mm/1000.0:.3f} m\n"
            f"Angle: {boom_ang_deg:.1f} °\n"
            f"Ballast: {ballast_pos_mm:.0f} mm"
        )

        load_f_t = _safe_num(self._get(d, "load_f_t", 0.0))
        cap_t = _safe_num(self._get(d, "cap_t", 0.0))
        margin_t = _safe_num(self._get(d, "margin_t", 0.0))
        util_pct = _safe_num(self._get(d, "util_pct", 0.0))

        self.kpi_load.set_value(f"{load_f_t:,.1f}".replace(",", " "))
        self.kpi_cap.set_value(f"{cap_t:,.1f}".replace(",", " "))
        self.kpi_margin.set_value(f"{margin_t:,.1f}".replace(",", " "))
        self.kpi_util.set_value(f"{util_pct:,.0f}".replace(",", " "))

        ts = _safe_num(self._get(d, "ts", len(self.x)))
        self.x.append(ts)
        self.y_load.append(load_f_t)
        self.y_cap.append(cap_t)
        self.y_util.append(util_pct * 10.0)

        if len(self.x) > 600:
            self.x = self.x[-600:]
            self.y_load = self.y_load[-600:]
            self.y_cap = self.y_cap[-600:]
            self.y_util = self.y_util[-600:]

        self.cur_load.setData(self.x, self.y_load)
        self.cur_cap.setData(self.x, self.y_cap)
        self.cur_util.setData(self.x, self.y_util)
