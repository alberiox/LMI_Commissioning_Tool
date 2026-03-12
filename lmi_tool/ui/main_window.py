from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from lmi_tool.ui.pages.overview import OverviewPage
from lmi_tool.ui.pages.sensors import SensorsPage
from lmi_tool.ui.pages.hydraulics import HydraulicsPage
from lmi_tool.ui.pages.geometry import GeometryPage
from lmi_tool.ui.pages.tables import TablesPage
from lmi_tool.ui.pages.calibration import CalibrationPage
from lmi_tool.ui.pages.report import ReportPage


ICON_DIR = Path(r"D:\LMI_Commissioning_Tool\lmi_tool\icons")


def tint_icon(icon_path: Path, color: str = "#DCE8F3", size: int = 26) -> QtGui.QIcon:
    pix = QtGui.QPixmap(str(icon_path))
    if pix.isNull():
        return QtGui.QIcon()

    pix = pix.scaled(
        size,
        size,
        QtCore.Qt.KeepAspectRatio,
        QtCore.Qt.SmoothTransformation,
    )

    tinted = QtGui.QPixmap(pix.size())
    tinted.fill(QtCore.Qt.transparent)

    painter = QtGui.QPainter(tinted)
    painter.drawPixmap(0, 0, pix)
    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    painter.fillRect(tinted.rect(), QtGui.QColor(color))
    painter.end()

    return QtGui.QIcon(tinted)


def load_icon(filename: str, fallback: QtGui.QIcon | None = None) -> QtGui.QIcon:
    path = ICON_DIR / filename
    if path.exists():
        icon = tint_icon(path, color="#DCE8F3", size=26)
        if not icon.isNull():
            return icon
    return fallback or QtGui.QIcon()


class NavButton(QtWidgets.QToolButton):
    def __init__(self, text: str, icon: QtGui.QIcon, parent=None):
        super().__init__(parent)

        self.setCheckable(True)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setIcon(icon)
        self.setText(text)
        self.setIconSize(QtCore.QSize(26, 26))
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumHeight(52)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setStyleSheet(
            """
            QToolButton {
                color: #EEF4FA;
                background: transparent;
                border: 1px solid transparent;
                border-radius: 14px;
                padding: 10px 16px;
                text-align: left;
                font-size: 14px;
                font-weight: 600;
            }

            QToolButton:hover {
                background: rgba(90, 114, 134, 0.18);
                border: 1px solid rgba(90, 114, 134, 0.35);
            }

            QToolButton:checked {
                background: rgba(90, 114, 134, 0.35);
                border: 1px solid rgba(120, 150, 176, 0.55);
            }
            """
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._source = None

        self.setWindowTitle("LMI Commissioning Tool")
        self.resize(1440, 860)

        self.stack = QtWidgets.QStackedWidget()

        self.page_overview = OverviewPage()
        self.page_sensors = SensorsPage()
        self.page_hydraulics = HydraulicsPage()
        self.page_geometry = GeometryPage()
        self.page_tables = TablesPage()
        self.page_calibration = CalibrationPage()
        self.page_report = ReportPage()

        self.pages = [
            ("  Overview", "home.svg", self.page_overview),
            ("  Sensors", "sensors.svg", self.page_sensors),
            ("  Hydraulics", "hydraulics.svg", self.page_hydraulics),
            ("  Geometry", "geometry.svg", self.page_geometry),
            ("  Load Tables", "tables.svg", self.page_tables),
            ("  Calibration", "calibration.svg", self.page_calibration),
            ("  Report", "report.svg", self.page_report),
        ]

        for _, _, page in self.pages:
            self.stack.addWidget(page)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        root = QtWidgets.QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setStyleSheet(
            """
            QFrame#Sidebar {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0E1723,
                    stop:1 #09121D
                );
                border-right: 1px solid #23324A;
            }
            """
        )

        side_layout = QtWidgets.QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(16, 18, 16, 18)
        side_layout.setSpacing(8)

        title = QtWidgets.QLabel("LMI Tool")
        title.setStyleSheet(
            """
            QLabel {
                color: #F3F7FB;
                font-size: 22px;
                font-weight: 800;
            }
            """
        )

        subtitle = QtWidgets.QLabel("Commissioning ")
        subtitle.setStyleSheet(
            """
            QLabel {
                color: #AEBCCA;
                font-size: 12px;
                font-weight: 500;
            }
            """
        )

        side_layout.addWidget(title)
        side_layout.addWidget(subtitle)
        side_layout.addSpacing(14)

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.nav_buttons: list[NavButton] = []

        fallback_style = self.style()
        fallback_icons = [
            fallback_style.standardIcon(QtWidgets.QStyle.SP_ComputerIcon),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_DialogYesButton),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_ArrowUp),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_FileDialogDetailedView),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_DriveHDIcon),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_FileDialogNewFolder),
            fallback_style.standardIcon(QtWidgets.QStyle.SP_FileDialogInfoView),
        ]

        for idx, ((text, icon_file, _page), fallback_icon) in enumerate(zip(self.pages, fallback_icons)):
            icon = load_icon(icon_file, fallback_icon)
            btn = NavButton(text, icon)
            self.button_group.addButton(btn, idx)
            self.nav_buttons.append(btn)
            side_layout.addWidget(btn)

        side_layout.addStretch(1)

        footer = QtWidgets.QLabel("B&R OPC-UA")
        footer.setStyleSheet(
            """
            QLabel {
                color: #7F8C99;
                font-size: 11px;
                padding: 6px 4px 0 4px;
            }
            """
        )
        side_layout.addWidget(footer)

        root.addWidget(self.sidebar)
        root.addWidget(self.stack, 1)

        self.button_group.idClicked.connect(self.set_page)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

        self._wire_calibration_page()

    def set_page(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def _wire_calibration_page(self):
        page = self.page_calibration

        # abilita i comandi operatore sulla pagina calibration
        if hasattr(page, "set_read_only"):
            page.set_read_only(False)

        # collegamenti UI -> MainWindow
        if hasattr(page, "enableRequested"):
            page.enableRequested.connect(self._on_cal_enable_requested)

        if hasattr(page, "modeEmptyRequested"):
            page.modeEmptyRequested.connect(self._on_cal_mode_empty_requested)

        if hasattr(page, "storeRequested"):
            page.storeRequested.connect(self._on_cal_store_requested)

        if hasattr(page, "resetRequested"):
            page.resetRequested.connect(self._on_cal_reset_requested)

    def _on_cal_enable_requested(self, value: bool):
        if self._source is not None and hasattr(self._source, "write_tag"):
            self._source.write_tag("cal_enable", value)

    def _on_cal_mode_empty_requested(self, value: bool):
        if self._source is not None and hasattr(self._source, "write_tag"):
            self._source.write_tag("cal_mode_empty", value)

    def _on_cal_store_requested(self):
        if self._source is not None and hasattr(self._source, "write_tag"):
            self._source.write_tag("cal_store_cmd", True)

            try:
                QtCore.QTimer.singleShot(
                    150,
                    lambda: self._source.write_tag("cal_store_cmd", False)
                )
            except Exception:
                pass

    def _on_cal_reset_requested(self):
        if self._source is not None and hasattr(self._source, "write_tag"):
            self._source.write_tag("cal_store_cmd", False)
            self._source.write_tag("cal_enable", False)

    def set_data_source(self, source):
        self._source = source

    def update_data(self, d):
        for _, _, page in self.pages:
            if hasattr(page, "update_data"):
                page.update_data(d)

    def closeEvent(self, event):
        if self._source is not None and hasattr(self._source, "stop"):
            try:
                self._source.stop()
            except Exception:
                pass
        super().closeEvent(event)