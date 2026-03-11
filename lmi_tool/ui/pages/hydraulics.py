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

BAR_BG = """
QFrame {
    background: #0A111B;
    border: 1px solid #223652;
    border-radius: 12px;
}
"""

BAR_FILL = """
QFrame {
    background: #6C537C;
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


class PressureRow(QtWidgets.QWidget):
    def __init__(self, name: str, unit: str = "bar", max_value: float = 420.0, parent=None):
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
        top.addWidget(self.name_lbl); top.addStretch(1); top.addWidget(self.value_lbl); top.addSpacing(10); top.addWidget(self.badge)
        self.bar_bg = QtWidgets.QFrame(); self.bar_bg.setStyleSheet(BAR_BG); self.bar_bg.setMinimumHeight(28); self.bar_bg.setMaximumHeight(28)
        self.bar_fill = QtWidgets.QFrame(self.bar_bg); self.bar_fill.setStyleSheet(BAR_FILL); self.bar_fill.setGeometry(2, 2, 0, 24)
        self.bar_text = QtWidgets.QLabel(self.bar_bg); self.bar_text.setAlignment(QtCore.Qt.AlignCenter)
        self.bar_text.setStyleSheet("color:#EAF2F7;font-size:13px;font-weight:700;background:transparent;")
        layout.addLayout(top); layout.addWidget(self.bar_bg)
    def resizeEvent(self, event):
        super().resizeEvent(event); self._apply_fill(self._last_ratio if hasattr(self, "_last_ratio") else 0.0); self.bar_text.setGeometry(self.bar_bg.rect())
    def _apply_fill(self, ratio: float):
        self._last_ratio = max(0.0, min(1.0, ratio))
        total_w = max(0, self.bar_bg.width() - 4); fill_w = int(total_w * self._last_ratio)
        self.bar_fill.setGeometry(2, 2, fill_w, max(0, self.bar_bg.height() - 4))
    def set_value(self, value, status: str):
        num = _safe_num(value, 0.0)
        self.value_lbl.setText(f"{num:.1f} {self.unit}" if self.unit == "bar" else f"{num:.4f} {self.unit}")
        self.bar_text.setText(f"{num:.0f} {self.unit}" if self.unit == "bar" else f"{num:.3f} {self.unit}")
        self.badge.set_status(status); self._apply_fill(0.0 if self.max_value <= 0 else num / self.max_value)
class InfoRow(QtWidgets.QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(10)
        self.name_lbl = QtWidgets.QLabel(name); self.name_lbl.setStyleSheet(NAME_STYLE)
        self.value_lbl = QtWidgets.QLabel("--"); self.value_lbl.setStyleSheet(VALUE_STYLE)
        self.badge = StatusBadge("NO DATA")
        layout.addWidget(self.name_lbl); layout.addStretch(1); layout.addWidget(self.value_lbl); layout.addWidget(self.badge)
    def set_value(self, text: str, status: str):
        self.value_lbl.setText(text); self.badge.set_status(status)
class DashboardCard(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent); self.setStyleSheet(CARD_STYLE)
        layout = QtWidgets.QVBoxLayout(self); layout.setContentsMargins(22, 22, 22, 22); layout.setSpacing(16)
        self.title_lbl = QtWidgets.QLabel(title); self.title_lbl.setAlignment(QtCore.Qt.AlignCenter); self.title_lbl.setStyleSheet(TITLE_STYLE); layout.addWidget(self.title_lbl)
        self.body = QtWidgets.QVBoxLayout(); self.body.setSpacing(16); layout.addLayout(self.body); layout.addStretch(1)
    def add_widget(self, widget): self.body.addWidget(widget)
class HydraulicsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        root = QtWidgets.QVBoxLayout(self); root.setContentsMargins(18, 18, 18, 18); root.setSpacing(18)
        title = QtWidgets.QLabel("Hydraulics & Weight Model"); title.setStyleSheet("color:#F4F7FB;font-size:24px;font-weight:800;"); root.addWidget(title)
        grid = QtWidgets.QGridLayout(); grid.setHorizontalSpacing(18); grid.setVerticalSpacing(18); root.addLayout(grid); root.addStretch(1)
        self.fondello_card = DashboardCard("FONDELLO"); self.stelo_card = DashboardCard("STELO"); self.model_card = DashboardCard("LOAD MODEL"); self.result_card = DashboardCard("RESULT")
        grid.addWidget(self.fondello_card, 0, 0); grid.addWidget(self.stelo_card, 0, 1); grid.addWidget(self.model_card, 1, 0); grid.addWidget(self.result_card, 1, 1)
        grid.setColumnStretch(0, 1); grid.setColumnStretch(1, 1)
        self.f_p1 = PressureRow("P1"); self.f_p2 = PressureRow("P2"); self.f_used = PressureRow("P used"); self.f_warn_fault = InfoRow("Warn / Fault")
        self.fondello_card.add_widget(self.f_p1); self.fondello_card.add_widget(self.f_p2); self.fondello_card.add_widget(self.f_used); self.fondello_card.add_widget(self.f_warn_fault)
        self.s_p1 = PressureRow("P1"); self.s_p2 = PressureRow("P2"); self.s_used = PressureRow("P used"); self.s_warn_fault = InfoRow("Warn / Fault")
        self.stelo_card.add_widget(self.s_p1); self.stelo_card.add_widget(self.s_p2); self.stelo_card.add_widget(self.s_used); self.stelo_card.add_widget(self.s_warn_fault)
        self.m_model = InfoRow("M model"); self.m_empty = InfoRow("M empty"); self.k_gain = InfoRow("K gain")
        self.model_card.add_widget(self.m_model); self.model_card.add_widget(self.m_empty); self.model_card.add_widget(self.k_gain)
        self.m_net = InfoRow("M net"); self.m_load = InfoRow("M load"); self.m_load_t = InfoRow("Load displayed")
        self.result_card.add_widget(self.m_net); self.result_card.add_widget(self.m_load); self.result_card.add_widget(self.m_load_t)
    def _get(self, d, *names, default=None):
        for name in names:
            if hasattr(d, name):
                v = getattr(d, name)
                if v is not None: return v
            if isinstance(d, dict) and name in d and d[name] is not None: return d[name]
        return default
    def _pressure_group_status(self, p1, p2, p_used, warn, fault):
        p1 = _safe_num(p1); p2 = _safe_num(p2); p_used = _safe_num(p_used); warn = int(_safe_num(warn, 0)); fault = int(_safe_num(fault, 0))
        if fault != 0: return "FAULT"
        if warn != 0: return "WARN"
        if abs(p1) < 0.01 and abs(p2) < 0.01 and abs(p_used) < 0.01: return "NO DATA"
        return "OK"
    def _single_pressure_status(self, value, group_status):
        if group_status in ("FAULT", "WARN", "NO DATA"): return group_status
        return "NO DATA" if abs(_safe_num(value)) < 0.01 else "OK"
    def _model_status(self, m_model, k_gain):
        m_model = _safe_num(m_model); k_gain = _safe_num(k_gain, 1.0)
        if abs(m_model) < 0.01: return "NO DATA"
        if abs(k_gain) < 0.000001: return "WARN"
        return "OK"
    def _result_status(self, m_model, m_load):
        m_model = _safe_num(m_model); m_load = _safe_num(m_load)
        if abs(m_model) < 0.01 and abs(m_load) > 0.01: return "NO DATA"
        if m_load < 0: return "WARN"
        return "OK" if abs(m_load) > 0.01 or abs(m_model) > 0.01 else "NO DATA"
    def update_data(self, d):
        fp1 = self._get(d, "fondello_p1_bar"); fp2 = self._get(d, "fondello_p2_bar"); fpu = self._get(d, "fondello_p_used_bar")
        fw = self._get(d, "fondello_warn", default=0); ff = self._get(d, "fondello_fault", default=0); fondello_status = self._pressure_group_status(fp1, fp2, fpu, fw, ff)
        self.f_p1.set_value(fp1, self._single_pressure_status(fp1, fondello_status)); self.f_p2.set_value(fp2, self._single_pressure_status(fp2, fondello_status))
        self.f_used.set_value(fpu, fondello_status); self.f_warn_fault.set_value(f"{int(_safe_num(fw, 0))} / {int(_safe_num(ff, 0))}", fondello_status)
        sp1 = self._get(d, "stelo_p1_bar"); sp2 = self._get(d, "stelo_p2_bar"); spu = self._get(d, "stelo_p_used_bar")
        sw = self._get(d, "stelo_warn", default=0); sf = self._get(d, "stelo_fault", default=0); stelo_status = self._pressure_group_status(sp1, sp2, spu, sw, sf)
        self.s_p1.set_value(sp1, self._single_pressure_status(sp1, stelo_status)); self.s_p2.set_value(sp2, self._single_pressure_status(sp2, stelo_status))
        self.s_used.set_value(spu, stelo_status); self.s_warn_fault.set_value(f"{int(_safe_num(sw, 0))} / {int(_safe_num(sf, 0))}", stelo_status)
        m_model = self._get(d, "m_model_kg", "g_m_model_kg"); m_empty = self._get(d, "m_empty_kg"); k_gain = self._get(d, "k_gain"); model_status = self._model_status(m_model, k_gain)
        self.m_model.set_value(f"{_safe_num(m_model):,.1f} kg".replace(",", " "), model_status)
        self.m_empty.set_value(f"{_safe_num(m_empty):,.1f} kg".replace(",", " "), "OK" if m_empty is not None else "NO DATA")
        self.k_gain.set_value(f"{_safe_num(k_gain, 1.0):.4f}", model_status)
        m_net = self._get(d, "m_net_kg"); m_load = self._get(d, "m_load_kg"); m_load_t = self._get(d, "m_load_t"); result_status = self._result_status(m_model, m_load)
        self.m_net.set_value(f"{_safe_num(m_net):,.1f} kg".replace(",", " "), result_status)
        self.m_load.set_value(f"{_safe_num(m_load):,.1f} kg".replace(",", " "), result_status)
        self.m_load_t.set_value(f"{_safe_num(m_load_t):.3f} t", result_status)
