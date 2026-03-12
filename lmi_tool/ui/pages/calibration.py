from PySide6 import QtCore, QtWidgets, QtGui

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
    background: #5A7286;
    color: #EEF3F8;
    border-radius: 18px;
    padding: 10px 14px;
    font-size: 18px;
    font-weight: 700;
}
"""
VALUE_STYLE = "QLabel { color: #F3F6FA; font-size: 15px; font-weight: 700; }"
NAME_STYLE = "QLabel { color: #D9E0E8; font-size: 14px; }"
STATUS_TEXT_STYLE = """
QLabel {
    color: #EAF2F7;
    background: #0D1520;
    border: 1px solid #23324A;
    border-radius: 14px;
    padding: 10px 12px;
    font-size: 14px;
    font-weight: 600;
}
"""
TEXTBOX_STYLE = """
QPlainTextEdit {
    background: #0D1520;
    color: #EAF2F7;
    border: 1px solid #23324A;
    border-radius: 14px;
    padding: 8px;
    font-size: 13px;
}
"""
BUTTON_STYLE = """
QPushButton {
    background: #2C4B60;
    color: #F2F6FA;
    border: 1px solid #4E7087;
    border-radius: 14px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 700;
}
QPushButton:hover { background: #375E78; }
QPushButton:pressed { background: #274457; }
QPushButton:disabled {
    background: #1A2430;
    color: #7D8895;
    border: 1px solid #2D3948;
}
"""
TOGGLE_STYLE = """
QRadioButton, QCheckBox {
    color: #EAF2F7;
    font-size: 14px;
    font-weight: 600;
    spacing: 8px;
}
"""
PROGRESS_STYLE = """
QProgressBar {
    background: #0A111B;
    color: #EAF2F7;
    border: 1px solid #223652;
    border-radius: 10px;
    text-align: center;
    height: 22px;
}
QProgressBar::chunk { background: #5A7286; border-radius: 8px; }
"""
TABLE_STYLE = """
QTableWidget {
    background: #0D1520;
    alternate-background-color: #101A27;
    color: #EAF2F7;
    border: 1px solid #23324A;
    border-radius: 14px;
    gridline-color: #23324A;
}
QTableWidget::item { padding: 4px; }
QHeaderView::section {
    background: #162131;
    color: #DDE7F2;
    border: none;
    padding: 6px;
    font-size: 12px;
    font-weight: 700;
}
"""

STEP_IDLE = 0
STEP_WAIT_POS = 1
STEP_WAIT_STABLE = 2
STEP_READY = 3
STEP_AFTER_STORE = 4


def _safe_num(v, default=0.0):
    try:
        return default if v is None else float(v)
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


def _safe_bool(v, default=False):
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("1", "true", "yes", "on"):
            return True
        if s in ("0", "false", "no", "off"):
            return False
    try:
        return bool(int(v))
    except Exception:
        return bool(v)


def _fmt(v, decimals=2, unit=""):
    if v is None:
        return "--"
    try:
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
            "READY": ("#0F4F35", "#2B8B65", "#9BE8C8"),
            "ACTIVE": ("#123E59", "#2E6E97", "#A8DAFF"),
            "WARN": ("#5C4310", "#9A6E12", "#F2D27A"),
            "FAULT": ("#61212A", "#A73B4A", "#FFB2BE"),
            "NO DATA": ("#39414A", "#566170", "#D7DEE8"),
            "IDLE": ("#39414A", "#566170", "#D7DEE8"),
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

    def set_value(self, text: str, status: str = "OK"):
        self.value_lbl.setText(text)
        self.badge.set_status(status)


class DashboardCard(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet(CARD_STYLE)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self.title_lbl = QtWidgets.QLabel(title)
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setStyleSheet(TITLE_STYLE)
        layout.addWidget(self.title_lbl)
        self.body = QtWidgets.QVBoxLayout()
        self.body.setSpacing(12)
        layout.addLayout(self.body)
        layout.addStretch(1)

    def add_widget(self, widget):
        self.body.addWidget(widget)

    def add_layout(self, layout):
        self.body.addLayout(layout)


class StepItem(QtWidgets.QWidget):
    def __init__(self, index: int, title: str, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self.dot = QtWidgets.QLabel(str(index))
        self.dot.setFixedSize(28, 28)
        self.dot.setAlignment(QtCore.Qt.AlignCenter)
        self.title = QtWidgets.QLabel(title)
        self.title.setStyleSheet(NAME_STYLE)
        self.state = StatusBadge("IDLE")
        self.state.setMinimumWidth(90)
        lay.addWidget(self.dot)
        lay.addWidget(self.title, 1)
        lay.addWidget(self.state)
        self.set_state("IDLE")

    def set_state(self, state: str):
        state = state.upper()
        dot_styles = {
            "DONE": ("#0F4F35", "#2B8B65", "#D7FBEA"),
            "ACTIVE": ("#123E59", "#2E6E97", "#D3EEFF"),
            "WAIT": ("#5C4310", "#9A6E12", "#FFF0C2"),
            "IDLE": ("#39414A", "#566170", "#D7DEE8"),
        }
        bg, border, fg = dot_styles.get(state, dot_styles["IDLE"])
        self.dot.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                border: 1px solid {border};
                color: {fg};
                border-radius: 14px;
                font-size: 13px;
                font-weight: 800;
            }}
        """)
        badge_state = "ACTIVE" if state == "ACTIVE" else ("READY" if state == "DONE" else ("WARN" if state == "WAIT" else "IDLE"))
        self.state.set_status(badge_state)


class BigStatusPanel(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(8)
        self.caption = QtWidgets.QLabel("Store readiness")
        self.caption.setStyleSheet(NAME_STYLE)
        self.text = QtWidgets.QLabel("NOT READY")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setMinimumHeight(54)
        self.detail = QtWidgets.QLabel("Move into tolerance and wait for stability.")
        self.detail.setAlignment(QtCore.Qt.AlignCenter)
        self.detail.setWordWrap(True)
        self.detail.setStyleSheet("color:#D9E0E8;font-size:13px;")
        lay.addWidget(self.caption)
        lay.addWidget(self.text)
        lay.addWidget(self.detail)
        self.set_state("NO DATA")

    def set_state(self, state: str, detail: str = ""):
        state = (state or "NO DATA").upper()
        colors = {
            "READY": ("#0F4F35", "#2B8B65", "#D7FBEA"),
            "ACTIVE": ("#123E59", "#2E6E97", "#D3EEFF"),
            "WARN": ("#5C4310", "#9A6E12", "#FFF0C2"),
            "FAULT": ("#61212A", "#A73B4A", "#FFD1D8"),
            "NO DATA": ("#39414A", "#566170", "#D7DEE8"),
        }
        bg, border, fg = colors.get(state, colors["NO DATA"])
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: 1px solid {border};
                border-radius: 18px;
            }}
        """)
        self.text.setText(state)
        self.text.setStyleSheet(f"color:{fg};font-size:26px;font-weight:800;")
        if detail:
            self.detail.setText(detail)


class CheckRow(QtWidgets.QWidget):
    def __init__(self, label: str, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self.icon = QtWidgets.QLabel("•")
        self.icon.setFixedWidth(20)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.text = QtWidgets.QLabel(label)
        self.text.setStyleSheet("color:#EAF2F7;font-size:15px;font-weight:600;")
        lay.addWidget(self.icon)
        lay.addWidget(self.text, 1)
        self.set_checked(False, label)

    def set_checked(self, checked: bool, text: str):
        if checked:
            self.icon.setText("✓")
            self.icon.setStyleSheet("color:#9BE8C8;font-size:18px;font-weight:800;")
        else:
            self.icon.setText("✗")
            self.icon.setStyleSheet("color:#F2D27A;font-size:18px;font-weight:800;")
        self.text.setText(text)


class GaugeRow(QtWidgets.QWidget):
    def __init__(self, name: str, unit: str = "", parent=None):
        super().__init__(parent)
        self.unit = unit
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        top = QtWidgets.QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        self.name_lbl = QtWidgets.QLabel(name)
        self.name_lbl.setStyleSheet(NAME_STYLE)
        self.value_lbl = QtWidgets.QLabel("--")
        self.value_lbl.setStyleSheet(VALUE_STYLE)
        self.badge = StatusBadge("NO DATA")
        top.addWidget(self.name_lbl)
        top.addStretch(1)
        top.addWidget(self.value_lbl)
        top.addWidget(self.badge)
        self.bar = QtWidgets.QProgressBar()
        self.bar.setStyleSheet(PROGRESS_STYLE)
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        lay.addLayout(top)
        lay.addWidget(self.bar)

    def set_error(self, value, tol, decimals=2):
        v = abs(_safe_num(value))
        t = abs(_safe_num(tol))
        if t <= 0.0:
            self.value_lbl.setText("--")
            self.badge.set_status("NO DATA")
            self.bar.setValue(0)
            self.bar.setFormat("No tolerance")
            return
        ratio = min(2.0, v / t)
        pct = int((ratio / 2.0) * 100.0)
        state = "OK" if v <= t else ("WARN" if v <= t * 1.5 else "FAULT")
        self.value_lbl.setText(f"{_fmt(value, decimals, self.unit)} / tol {_fmt(tol, decimals, self.unit)}")
        self.badge.set_status(state)
        self.bar.setValue(pct)
        self.bar.setFormat(f"|err| {_fmt(v, decimals, self.unit)}")


class NodeMatrix(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(5, 5, parent)
        self.setStyleSheet(TABLE_STYLE)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setMinimumHeight(170)
        self.update_matrix(None, None, None)

    def update_matrix(self, active_i_alpha, active_i_l, done_nodes=None):
        done = set()
        if isinstance(done_nodes, (list, tuple, set)):
            for item in done_nodes:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    done.add((int(item[0]), int(item[1])))

        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                item = self.item(r, c)
                if item is None:
                    item = QtWidgets.QTableWidgetItem("")
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.setItem(r, c, item)
                txt = f"A{r}\nL{c}"
                bg = QtGui.QColor(16, 26, 39)
                fg = QtGui.QColor(142, 164, 184)
                if (r, c) in done:
                    txt = f"A{r}\nL{c}\n✓"
                    bg = QtGui.QColor(15, 79, 53)
                    fg = QtGui.QColor(215, 251, 234)
                if active_i_alpha is not None and active_i_l is not None and r == int(active_i_alpha) and c == int(active_i_l):
                    txt = f"A{r}\nL{c}\nACT"
                    bg = QtGui.QColor(18, 62, 89)
                    fg = QtGui.QColor(211, 238, 255)
                item.setText(txt)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setBackground(bg)
                item.setForeground(fg)
                item.setTextAlignment(QtCore.Qt.AlignCenter)


class CalibrationPage(QtWidgets.QWidget):
    enableRequested = QtCore.Signal(bool)
    modeEmptyRequested = QtCore.Signal(bool)
    storeRequested = QtCore.Signal()
    resetRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._read_only = True
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)
        title = QtWidgets.QLabel("Calibration Wizard")
        title.setStyleSheet("color:#F4F7FB;font-size:24px;font-weight:800;")
        root.addWidget(title)
        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)
        root.addLayout(grid)
        root.addStretch(1)

        self.summary_card = DashboardCard("SESSION")
        self.position_card = DashboardCard("TARGET / POSITION")
        self.stability_card = DashboardCard("STABILITY / STORE")
        self.result_card = DashboardCard("STORE RESULT")
        self.procedure_card = DashboardCard("GUIDED PROCEDURE")
        self.actions_card = DashboardCard("OPERATOR ACTIONS")
        grid.addWidget(self.summary_card, 0, 0)
        grid.addWidget(self.position_card, 0, 1)
        grid.addWidget(self.stability_card, 0, 2)
        grid.addWidget(self.result_card, 1, 0)
        grid.addWidget(self.procedure_card, 1, 1)
        grid.addWidget(self.actions_card, 1, 2)
        for i in range(3):
            grid.setColumnStretch(i, 1)

        self.session_mode = InfoRow("Mode")
        self.session_step = InfoRow("Wizard step")
        self.session_enable = InfoRow("Enable")
        self.session_status = InfoRow("Status")
        for w in (self.session_mode, self.session_step, self.session_enable, self.session_status):
            self.summary_card.add_widget(w)

        self.curr_alpha = InfoRow("Current angle")
        self.curr_l = InfoRow("Current boom")
        self.target_alpha = InfoRow("Target angle")
        self.target_l = InfoRow("Target boom")
        self.err_alpha = GaugeRow("Angle error", "°")
        self.err_l = GaugeRow("Boom error", "mm")
        self.active_node = InfoRow("Active node")
        self.node_map = NodeMatrix()
        for w in (self.curr_alpha, self.curr_l, self.target_alpha, self.target_l, self.err_alpha, self.err_l, self.active_node, self.node_map):
            self.position_card.add_widget(w)

        self.readiness = BigStatusPanel()
        self.check_in_tol = CheckRow("In tolerance")
        self.check_stable = CheckRow("Stable")
        self.check_ready = CheckRow("Ready to store")
        self.last_store_ok = InfoRow("Last store")
        self.progress_label = QtWidgets.QLabel("Stability progress")
        self.progress_label.setStyleSheet(NAME_STYLE)
        self.progress = QtWidgets.QProgressBar()
        self.progress.setStyleSheet(PROGRESS_STYLE)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        for w in (self.readiness, self.check_in_tol, self.check_stable, self.check_ready, self.progress_label, self.progress, self.last_store_ok):
            self.stability_card.add_widget(w)

        self.last_value = InfoRow("Last stored value")
        self.m_ref = InfoRow("Reference mass")
        self.m_model = InfoRow("Model mass")
        self.m_empty_interp = InfoRow("Interp empty")
        self.m_net = InfoRow("Net mass")
        for w in (self.last_value, self.m_ref, self.m_model, self.m_empty_interp, self.m_net):
            self.result_card.add_widget(w)

        self.step_idle = StepItem(1, "Enable calibration")
        self.step_pos = StepItem(2, "Move near target node")
        self.step_stable = StepItem(3, "Hold boom steady")
        self.step_ready = StepItem(4, "Store calibration value")
        for w in (self.step_idle, self.step_pos, self.step_stable, self.step_ready):
            self.procedure_card.add_widget(w)
        self.status_text = QtWidgets.QLabel("Calibration idle.")
        self.status_text.setWordWrap(True)
        self.status_text.setStyleSheet(STATUS_TEXT_STYLE)
        self.procedure_card.add_widget(self.status_text)
        self.notes = QtWidgets.QPlainTextEdit()
        self.notes.setReadOnly(True)
        self.notes.setStyleSheet(TEXTBOX_STYLE)
        self.notes.setMaximumHeight(120)
        self.notes.setPlainText(
            "Recommended workflow:\n"
            "1) Select mode Empty or K_gain.\n"
            "2) Move the machine close to the target node.\n"
            "3) Wait until position is in tolerance and stable.\n"
            "4) Press STORE only when ready.\n"
            "5) For K_gain use the certified reference load."
        )
        self.procedure_card.add_widget(self.notes)

        self.chk_enable = QtWidgets.QCheckBox("Enable wizard")
        self.chk_enable.setStyleSheet(TOGGLE_STYLE)
        self.rb_empty = QtWidgets.QRadioButton("Empty calibration")
        self.rb_kgain = QtWidgets.QRadioButton("K_gain calibration")
        self.rb_empty.setStyleSheet(TOGGLE_STYLE)
        self.rb_kgain.setStyleSheet(TOGGLE_STYLE)
        self.rb_empty.setChecked(True)
        self.btn_store = QtWidgets.QPushButton("STORE")
        self.btn_reset = QtWidgets.QPushButton("RESET SESSION")
        self.btn_store.setStyleSheet(BUTTON_STYLE)
        self.btn_reset.setStyleSheet(BUTTON_STYLE)
        self.action_info = QtWidgets.QLabel("Read-only mode: commands disabled.")
        self.action_info.setWordWrap(True)
        self.action_info.setStyleSheet(STATUS_TEXT_STYLE)
        mode_box = QtWidgets.QVBoxLayout()
        mode_box.setSpacing(10)
        mode_box.addWidget(self.chk_enable)
        mode_box.addWidget(self.rb_empty)
        mode_box.addWidget(self.rb_kgain)
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addWidget(self.btn_store)
        btn_row.addWidget(self.btn_reset)
        self.actions_card.add_layout(mode_box)
        self.actions_card.add_layout(btn_row)
        self.actions_card.add_widget(self.action_info)

        self.chk_enable.toggled.connect(self.enableRequested.emit)
        self.rb_empty.toggled.connect(self._on_mode_changed)
        self.btn_store.clicked.connect(self.storeRequested.emit)
        self.btn_reset.clicked.connect(self.resetRequested.emit)
        self.set_read_only(True)

    def _on_mode_changed(self, checked: bool):
        self.modeEmptyRequested.emit(bool(checked))

    def set_read_only(self, read_only: bool = True):
        self._read_only = bool(read_only)
        for w in (self.chk_enable, self.rb_empty, self.rb_kgain, self.btn_store, self.btn_reset):
            w.setEnabled(not self._read_only)
        self.action_info.setText("Read-only mode: commands disabled." if self._read_only else "Command mode enabled: operator actions available.")

    def _get(self, d, *names, default=None):
        for name in names:
            if hasattr(d, name):
                v = getattr(d, name)
                if v is not None:
                    return v
            if isinstance(d, dict) and name in d and d[name] is not None:
                return d[name]
        return default

    def _bool_status(self, value, true_text="YES", false_text="NO", true_state="OK", false_state="NO DATA"):
        return (true_text, true_state) if _safe_bool(value, False) else (false_text, false_state)

    def _step_name(self, step):
        s = _safe_int(step, 0)
        names = {STEP_IDLE: "IDLE", STEP_WAIT_POS: "WAIT_POS", STEP_WAIT_STABLE: "WAIT_STABLE", STEP_READY: "READY", STEP_AFTER_STORE: "AFTER_STORE"}
        return names.get(s, f"STEP {s}")

    def _step_status(self, step):
        s = _safe_int(step, 0)
        if s == STEP_IDLE:
            return "IDLE"
        if s == STEP_READY:
            return "READY"
        if s in (STEP_WAIT_POS, STEP_WAIT_STABLE, STEP_AFTER_STORE):
            return "ACTIVE"
        return "WARN"

    def _set_step_widgets(self, step):
        s = _safe_int(step, 0)
        self.step_idle.set_state("ACTIVE" if s == STEP_IDLE else ("DONE" if s > STEP_IDLE else "IDLE"))
        self.step_pos.set_state("ACTIVE" if s == STEP_WAIT_POS else ("DONE" if s > STEP_WAIT_POS else "IDLE"))
        self.step_stable.set_state("ACTIVE" if s == STEP_WAIT_STABLE else ("DONE" if s > STEP_WAIT_STABLE else "IDLE"))
        self.step_ready.set_state("ACTIVE" if s in (STEP_READY, STEP_AFTER_STORE) else "IDLE")

    def _update_readiness(self, in_tol, is_stable, ready_store):
        if _safe_bool(ready_store, False):
            self.readiness.set_state("READY", "Press STORE to save the current node.")
        elif _safe_bool(in_tol, False) and not _safe_bool(is_stable, False):
            self.readiness.set_state("ACTIVE", "Node reached. Hold the boom steady.")
        elif not _safe_bool(in_tol, False):
            self.readiness.set_state("WARN", "Move the machine inside angle and boom tolerance.")
        else:
            self.readiness.set_state("NO DATA", "Waiting for valid calibration conditions.")

    def update_data(self, d):
            enable = self._get(d, "cal_enable", "calib_enable", "enable", "g_lm_calibhmi_enable", default=False)
            mode_empty = self._get(d, "cal_mode_empty", "calib_mode_empty", "mode_empty", "g_lm_calibhmi_modeempty", default=True)
            step = self._get(d, "cal_step", "calib_step", "step", "g_lm_calibhmi_step", default=STEP_IDLE)
            status_text = self._get(d, "cal_status_text", "calib_status_text", "status_text", "g_lm_calibhmi_statustext", default="Calibration idle.")
            curr_alpha = self._get(d, "cal_curr_alpha_deg", "calib_curr_alpha_deg", "curr_alpha_deg", "g_lm_calibhmi_curralphadeg")
            curr_l = self._get(d, "cal_curr_l_mm", "calib_curr_l_mm", "curr_l_mm", "g_lm_calibhmi_currl_mm")
            target_alpha = self._get(d, "cal_target_alpha_deg", "calib_target_alpha_deg", "target_alpha_deg", "g_lm_calibhmi_targetalphadeg")
            target_l = self._get(d, "cal_target_l_mm", "calib_target_l_mm", "target_l_mm", "g_lm_calibhmi_targetl_mm")
            err_alpha = self._get(d, "cal_err_alpha_deg", "calib_err_alpha_deg", "err_alpha_deg", "g_lm_calibhmi_erralphadeg")
            err_l = self._get(d, "cal_err_l_mm", "calib_err_l_mm", "err_l_mm", "g_lm_calibhmi_errl_mm")
            active_i_alpha = self._get(d, "cal_active_i_alpha", "calib_active_i_alpha", "active_i_alpha", "g_lm_calibhmi_active_i_alpha")
            active_i_l = self._get(d, "cal_active_i_l", "calib_active_i_l", "active_i_l", "g_lm_calibhmi_active_i_l")
            alpha_tol = self._get(d, "cal_alpha_tol_deg", "calib_alpha_tol_deg", "alpha_tol_deg", "g_lm_calibhmi_alphatoldeg")
            l_tol = self._get(d, "cal_l_tol_mm", "calib_l_tol_mm", "l_tol_mm", "g_lm_calibhmi_ltol_mm")
            stable_req = self._get(d, "cal_stable_cycles_req", "calib_stable_cycles_req", "stable_cycles_req", "g_lm_calibhmi_stablecyclesreq", default=10)
            stable_count = self._get(d, "cal_stable_count", "calib_stable_count", "stable_count", default=0)
            in_tol = self._get(d, "cal_in_tolerance", "calib_in_tolerance", "in_tolerance", "g_lm_calibhmi_intolerance", default=False)
            is_stable = self._get(d, "cal_is_stable", "calib_is_stable", "is_stable", "g_lm_calibhmi_isstable", default=False)
            ready_store = self._get(d, "cal_ready_to_store", "calib_ready_to_store", "ready_to_store", "g_lm_calibhmi_readytostore", default=False)
            last_store_ok = self._get(d, "cal_last_store_ok", "calib_last_store_ok", "last_store_ok", "g_lm_calibhmi_laststoreok", default=False)
            last_stored_value = self._get(d, "cal_last_stored_value", "calib_last_stored_value", "last_stored_value", "g_lm_calibhmi_laststoredvalue")
            m_ref = self._get(d, "g_m_ref_kg", "m_ref_kg", "calib_m_ref_kg")
            m_model = self._get(d, "g_m_model_kg", "m_model_kg")
            m_empty_interp = self._get(d, "m_empty_interp_kg", "calib_m_empty_interp_kg")
            m_net = self._get(d, "m_net_kg", "calib_m_net_kg")
            done_nodes = self._get(d, "cal_done_nodes", "calib_done_nodes", "done_nodes")

            mode_text = "EMPTY" if _safe_bool(mode_empty, True) else "K_GAIN"
            self.session_mode.set_value(mode_text, "ACTIVE" if _safe_bool(enable, False) else "IDLE")
            self.session_step.set_value(self._step_name(step), self._step_status(step))
            txt, st = self._bool_status(enable, "ENABLED", "DISABLED", "ACTIVE", "IDLE")
            self.session_enable.set_value(txt, st)
            self.session_status.set_value(status_text, self._step_status(step))

            self.curr_alpha.set_value(_fmt(curr_alpha, 2, "°"), "OK" if curr_alpha is not None else "NO DATA")
            self.curr_l.set_value(_fmt(curr_l, 0, "mm"), "OK" if curr_l is not None else "NO DATA")
            self.target_alpha.set_value(_fmt(target_alpha, 2, "°"), "OK" if target_alpha is not None else "NO DATA")
            self.target_l.set_value(_fmt(target_l, 0, "mm"), "OK" if target_l is not None else "NO DATA")
            self.err_alpha.set_error(err_alpha, alpha_tol, decimals=3)
            self.err_l.set_error(err_l, l_tol, decimals=0)
            self.active_node.set_value(f"Alpha idx {_safe_int(active_i_alpha, -1)} | L idx {_safe_int(active_i_l, -1)}", "OK" if active_i_alpha is not None and active_i_l is not None else "NO DATA")
            self.node_map.update_matrix(active_i_alpha, active_i_l, done_nodes)

            self.check_in_tol.set_checked(_safe_bool(in_tol, False), "In tolerance")
            self.check_stable.set_checked(_safe_bool(is_stable, False), "Stable")
            self.check_ready.set_checked(_safe_bool(ready_store, False), "Ready to store")
            txt, st = self._bool_status(last_store_ok, "OK", "NO DATA", "OK", "NO DATA")
            self.last_store_ok.set_value(txt, st)
            req = max(1, _safe_int(stable_req, 10))
            cnt = max(0, min(req, _safe_int(stable_count, 0)))
            self.progress.setValue(int((cnt / req) * 100.0))
            self.progress.setFormat(f"{cnt} / {req} cycles")
            self._update_readiness(in_tol, is_stable, ready_store)

            #result_state = "OK" if _safe_bool(last_store_ok, False) else ("READY" if _safe_bool(ready_store, False) else "NO DATA")
            if last_stored_value is not None:
                result_state = "OK" if _safe_bool(last_store_ok, False) else "IDLE"
            else:
                result_state = "READY" if _safe_bool(ready_store, False) else "NO DATA"


            self.last_value.set_value(_fmt(last_stored_value, 3), result_state if last_stored_value is not None else "NO DATA")
            self.m_ref.set_value(_fmt(m_ref, 1, "kg"), "OK" if m_ref is not None else "NO DATA")
            self.m_model.set_value(_fmt(m_model, 1, "kg"), "OK" if m_model is not None else "NO DATA")
            self.m_empty_interp.set_value(_fmt(m_empty_interp, 1, "kg"), "OK" if m_empty_interp is not None else "NO DATA")
            self.m_net.set_value(_fmt(m_net, 1, "kg"), "OK" if m_net is not None else "NO DATA")

            self._set_step_widgets(step)
            self.status_text.setText(status_text or "Calibration idle.")
            blocker1 = QtCore.QSignalBlocker(self.chk_enable)
            blocker2 = QtCore.QSignalBlocker(self.rb_empty)
            blocker3 = QtCore.QSignalBlocker(self.rb_kgain)
            self.chk_enable.setChecked(_safe_bool(enable, False))
            self.rb_empty.setChecked(_safe_bool(mode_empty, True))
            self.rb_kgain.setChecked(not _safe_bool(mode_empty, True))
