import asyncio
import threading
import time
import traceback
from pathlib import Path

from PySide6 import QtCore
from asyncua import Client

from lmi_tool.core.model import LMIData
from lmi_tool.core.tag_map import build_flat_tag_map


class OpcUaSource(QtCore.QObject):
    updated = QtCore.Signal(object)

    def __init__(self, cfg=None, parent=None):
        super().__init__(parent)

        self.cfg = cfg or {}
        self._thread = None
        self._running = False
        self._loop = None
        self._client = None

        self.tag_map = build_flat_tag_map()
        self._latest = {key: None for key in self.tag_map.keys()}

        self._latest.update(
            {
                "util_pct": 0.0,
                "warning": False,
                "overload": False,
                "near_limit": False,
                "cap_t": 0.0,
                "load_f_t": 0.0,
                "margin_t": 0.0,
                "margin_pct": 0.0,
                "cur_sel": 12,
                "act_table": "12000",
                "k_gain": 1.0,
            }
        )

    def start(self):
        if self._thread is None:
            self._running = True
            self._thread = threading.Thread(target=self._run_thread, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False

    def _f(self, key, default=0.0):
        try:
            v = self._latest.get(key, default)
            return default if v is None else float(v)
        except Exception:
            return default

    def _fo(self, key):
        try:
            v = self._latest.get(key)
            return None if v is None else float(v)
        except Exception:
            return None

    def _io(self, key):
        v = self._latest.get(key)

        try:
            return None if v is None else int(v)
        except Exception:
            try:
                if isinstance(v, str) and v.strip().upper().startswith("16#"):
                    return int(v.strip()[3:], 16)
            except Exception:
                pass
            return None

    def _first_number(self, *keys, fallback=0.0):
        for key in keys:
            v = self._fo(key)
            if v is not None:
                return v
        return fallback

    def _emit_snapshot(self):
     d = Snapshot()

    # ---------------------------------------------------------
    # valori principali già usati dalle altre pagine
    # ---------------------------------------------------------
    for key, value in self._latest.items():
        setattr(d, key, value)

    # ---------------------------------------------------------
    # helpers locali
    # ---------------------------------------------------------
    def fo(key, default=None):
        v = self._latest.get(key, default)
        try:
            if v is None:
                return default
            return float(v)
        except Exception:
            return default

    def io(key, default=None):
        v = self._latest.get(key, default)
        try:
            if v is None:
                return default
            return int(v)
        except Exception:
            return default

    def bo(key, default=False):
        v = self._latest.get(key, default)
        try:
            return bool(v)
        except Exception:
            return default

    def tx(key, default=""):
        v = self._latest.get(key, default)
        try:
            if v is None:
                return default
            return str(v)
        except Exception:
            return default

    # ---------------------------------------------------------
    # calibration page - naming canonico + alias compatibilità
    # ---------------------------------------------------------
    extras = {
        # ---------------------------
        # stato wizard
        # ---------------------------
        "cal_enable": bo("cal_enable", False),
        "calib_enable": bo("cal_enable", False),

        "cal_mode_empty": bo("cal_mode_empty", False),
        "calib_mode_empty": bo("cal_mode_empty", False),

        "cal_step": io("cal_step", 0),
        "calib_step": io("cal_step", 0),

        "cal_status_text": tx("cal_status_text", "Calibration idle."),
        "calib_status_text": tx("cal_status_text", "Calibration idle."),

        # ---------------------------
        # posizione / target
        # ---------------------------
        "cal_curr_alpha_deg": fo("cal_curr_alpha_deg"),
        "calib_curr_alpha_deg": fo("cal_curr_alpha_deg"),

        "cal_curr_l_mm": fo("cal_curr_l_mm"),
        "calib_curr_l_mm": fo("cal_curr_l_mm"),

        "cal_target_alpha_deg": fo("cal_target_alpha_deg"),
        "calib_target_alpha_deg": fo("cal_target_alpha_deg"),

        "cal_target_l_mm": fo("cal_target_l_mm"),
        "calib_target_l_mm": fo("cal_target_l_mm"),

        "cal_err_alpha_deg": fo("cal_err_alpha_deg"),
        "calib_err_alpha_deg": fo("cal_err_alpha_deg"),

        "cal_err_l_mm": fo("cal_err_l_mm"),
        "calib_err_l_mm": fo("cal_err_l_mm"),

        # ---------------------------
        # nodo attivo
        # ---------------------------
        "cal_active_ialpha": io("cal_active_ialpha"),
        "calib_active_i_alpha": io("cal_active_ialpha"),
        "active_i_alpha": io("cal_active_ialpha"),

        "cal_active_il": io("cal_active_il"),
        "calib_active_i_l": io("cal_active_il"),
        "active_i_l": io("cal_active_il"),

        # ---------------------------
        # tolleranze
        # ---------------------------
        "cal_alpha_tol_deg": fo("cal_alpha_tol_deg"),
        "calib_alpha_tol_deg": fo("cal_alpha_tol_deg"),

        "cal_l_tol_mm": fo("cal_l_tol_mm"),
        "calib_l_tol_mm": fo("cal_l_tol_mm"),

        "cal_alpha_stable_tol_deg": fo("cal_alpha_stable_tol_deg"),
        "calib_alpha_stable_tol_deg": fo("cal_alpha_stable_tol_deg"),

        "cal_l_stable_tol_mm": fo("cal_l_stable_tol_mm"),
        "calib_l_stable_tol_mm": fo("cal_l_stable_tol_mm"),

        # ---------------------------
        # stabilità / readiness
        # ---------------------------
        "cal_stable_cycles_req": io("cal_stable_cycles_req", 10),
        "calib_stable_cycles_req": io("cal_stable_cycles_req", 10),
        "stable_cycles_req": io("cal_stable_cycles_req", 10),

        "cal_stable_count": io("cal_stable_count", 0),
        "calib_stable_count": io("cal_stable_count", 0),
        "stable_count": io("cal_stable_count", 0),

        "cal_in_tolerance": bo("cal_in_tolerance", False),
        "calib_in_tolerance": bo("cal_in_tolerance", False),
        "in_tolerance": bo("cal_in_tolerance", False),

        "cal_is_stable": bo("cal_is_stable", False),
        "calib_is_stable": bo("cal_is_stable", False),
        "is_stable": bo("cal_is_stable", False),

        "cal_ready_to_store": bo("cal_ready_to_store", False),
        "calib_ready_to_store": bo("cal_ready_to_store", False),
        "ready_to_store": bo("cal_ready_to_store", False),

        # ---------------------------
        # ultimo store
        # ---------------------------
        "cal_last_store_ok": bo("cal_last_store_ok", False),
        "calib_last_store_ok": bo("cal_last_store_ok", False),
        "last_store_ok": bo("cal_last_store_ok", False),

        "cal_last_stored_value": fo("cal_last_stored_value"),
        "calib_last_stored_value": fo("cal_last_stored_value"),
        "last_stored_value": fo("cal_last_stored_value"),

        # ---------------------------
        # errori / comandi
        # ---------------------------
        "cal_error_tolerance": bo("cal_error_tolerance", False),
        "calib_error_tolerance": bo("cal_error_tolerance", False),

        "cal_error_state": bo("cal_error_state", False),
        "calib_error_state": bo("cal_error_state", False),

        "cal_store_cmd": bo("cal_store_cmd", False),
        "calib_store_cmd": bo("cal_store_cmd", False),

        # ---------------------------
        # masse / risultati
        # ---------------------------
        "g_m_ref_kg": fo("g_m_ref_kg"),
        "m_ref_kg": fo("g_m_ref_kg"),
        "calib_m_ref_kg": fo("g_m_ref_kg"),

        "g_m_model_kg": fo("g_m_model_kg"),
        "m_model_kg": fo("g_m_model_kg"),

        "m_empty_interp_kg": fo("m_empty_interp_kg"),
        "calib_m_empty_interp_kg": fo("m_empty_interp_kg"),

        "m_net_kg": fo("m_net_kg"),
        "calib_m_net_kg": fo("m_net_kg"),
    }

    # ---------------------------------------------------------
    # export extras nel payload finale
    # ---------------------------------------------------------
    for key, value in extras.items():
        setattr(d, key, value)

    self.updated.emit(d)

    def _run_thread(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._run())
        except Exception:
            print("OPCUA THREAD ERROR:")
            traceback.print_exc()

    async def _run(self):
        opc_cfg = self.cfg.get("opcua", {}) if isinstance(self.cfg, dict) else {}

        endpoint = opc_cfg.get("endpoint", "opc.tcp://192.168.1.160:4840")
        username = opc_cfg.get("username", "alfa")
        password = opc_cfg.get("password", "alfa")

        base_dir = Path(__file__).resolve().parents[2]
        cert_path = base_dir / "certs" / "uaexpert.der"
        key_path = base_dir / "certs" / "uaexpert_key.pem"

        self._client = Client(url=endpoint)
        self._client.application_uri = "urn:XPS_Alberio:UnifiedAutomation:UaExpert"
        self._client.set_user(username)
        self._client.set_password(password)

        try:
            await self._client.set_security_string(
                f"Basic256Sha256,SignAndEncrypt,{cert_path},{key_path}"
            )

            await self._client.connect()
            print("OPC-UA connected successfully")

            nodes = {
                key: self._client.get_node(nodeid)
                for key, nodeid in self.tag_map.items()
            }

            while self._running:
                for key, node in nodes.items():
                    try:
                        self._latest[key] = await node.read_value()
                    except Exception:
                        pass

                self._emit_snapshot()
                await asyncio.sleep(0.2)

        except Exception:
            traceback.print_exc()
            self._emit_snapshot()

        finally:
            try:
                if self._client is not None:
                    await self._client.disconnect()
            except Exception:
                pass