import json
import sys
from pathlib import Path

from PySide6 import QtWidgets

from lmi_tool.datasource.opcua_source import OpcUaSource
from lmi_tool.datasource.sim_source import SimSource
from lmi_tool.ui.main_window import MainWindow
from lmi_tool.ui.theme import APP_QSS


def load_config():
    cfg_path = Path(__file__).resolve().parents[1] / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(APP_QSS)

    cfg = load_config()
    mode = cfg.get("mode", "sim").lower()

    if mode == "opcua":
        src = OpcUaSource(cfg)
    else:
        src = SimSource(interval_ms=50)

    win = MainWindow()
    win.set_data_source(src)
    src.updated.connect(win.update_data)
    app.aboutToQuit.connect(src.stop)

    win.show()
    src.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
