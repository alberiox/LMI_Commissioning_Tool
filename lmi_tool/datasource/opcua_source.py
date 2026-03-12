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
        cur = int(self._latest.get("cur_sel") or 12)
         # ✅ DEBUG PRINT - CORRETTO
        print("\n" + "="*70)
        print(f"📊 OPC-UA VALUES @ {time.time():.3f}")  # ✅ Usa time.time() invece
        print("="*70)
    
        print("\n🔵 LIMITER:")
        print(f"  util_pct={self._latest.get('util_pct')} | warning={self._latest.get('warning')} | overload={self._latest.get('overload')}")
        print(f"  cap_t={self._latest.get('cap_t')} | load_f_t={self._latest.get('load_f_t')} | margin_t={self._latest.get('margin_t')}")
    
        print("\n🟢 BOOM:")
        print(f"  pos_meas={self._latest.get('boom_pos_mm_meas')} | pos={self._latest.get('boom_pos_mm')}")
        print(f"  ang_meas={self._latest.get('boom_ang_deg_meas')} | ang={self._latest.get('boom_ang_deg')}")
        print(f"  fault={self._latest.get('boom_fault')} | fault_code={self._latest.get('boom_fault_code')}")
    
        print("\n🟡 BALLAST:")
        print(f"  pos_meas={self._latest.get('ballast_pos_mm_meas')} | pos={self._latest.get('ballast_pos_mm')}")
        print(f"  ang_meas={self._latest.get('ballast_ang_deg_meas')} | ang={self._latest.get('ballast_ang_deg')}")
        print(f"  fault={self._latest.get('ballast_fault')} | fault_code={self._latest.get('ballast_fault_code')}")
    
        print("\n🔴 PRESSURES:")
        print(f"  ph1a={self._latest.get('ph1a_p_bar')} | ph1b={self._latest.get('ph1b_p_bar')} | pl1a={self._latest.get('pl1a_p_bar')} | pl1b={self._latest.get('pl1b_p_bar')}")
        print(f"  status: ph1a={self._latest.get('ph1a_status')} | ph1b={self._latest.get('ph1b_status')} | pl1a={self._latest.get('pl1a_status')} | pl1b={self._latest.get('pl1b_status')}")
        
        print("\n🟣 CYLINDER PRESSURES (PressurePair):")
        print(f"  FONDELLO -> " f"P1={self._latest.get('fondello_p1_bar')} | " f"P2={self._latest.get('fondello_p2_bar')} | "f"P_used={self._latest.get('fondello_p_used_bar')}")
        print(f"  STELO -> " f"P1={self._latest.get('stelo_p1_bar')} | " f"P2={self._latest.get('stelo_p2_bar')} | " f"P_used={self._latest.get('stelo_p_used_bar')}")
        
        print("\n⚡ SUPPLY:")
        print(f"  ph1a_us={self._latest.get('ph1a_us_v')} | ph1b_us={self._latest.get('ph1b_us_v')} | pl1a_us={self._latest.get('pl1a_us_v')} | pl1b_us={self._latest.get('pl1b_us_v')}")
        print(f"  uout: ph1a={self._latest.get('ph1a_uout_v')} | ph1b={self._latest.get('ph1b_uout_v')} | pl1a={self._latest.get('pl1a_uout_v')} | pl1b={self._latest.get('pl1b_uout_v')}")
    
        print("\n📦 LOAD MODEL:")
        print(f"  m_model={self._latest.get('m_model_kg')} | m_empty={self._latest.get('m_empty_kg')} | m_net={self._latest.get('m_net_kg')} | m_load={self._latest.get('m_load_kg')}")
        print(f"  k_gain={self._latest.get('k_gain')}")
    
        print("\n temporanei:")
        print("CAL REF:", self._latest.get("g_m_ref_kg"))
        print("CAL EMPTY INTERP:", self._latest.get("m_empty_interp_kg"))

        print("="*70 + "\n")


        act_table = self._latest.get("act_table")
        if act_table in (None, ""):
            act_table = {
                12: "12000",
                13: "13000",
                14: "14000",
                15: "15000",
                16: "16000",
            }.get(cur, "---")

        supply_v = self._first_number(
            "ph1a_us_v",
            "ph1b_us_v",
            "pl1a_us_v",
            "pl1b_us_v",
            fallback=0.0,
        )

        d = LMIData(
            ts=time.time(),

            util_pct=self._f("util_pct"),
            warning=bool(self._latest.get("warning")),
            overload=bool(self._latest.get("overload")),
            near_limit=bool(self._latest.get("near_limit")),
            cap_t=self._first_number("limiter_cap_t", "cap_t", fallback=0.0),
            load_f_t=self._f("load_f_t"),
            margin_t=self._f("margin_t"),
            margin_pct=self._f("margin_pct"),

            boom_pos_mm=self._f("boom_pos_mm"),
            boom_ang_deg=self._f("boom_ang_deg"),
            ballast_pos_mm=self._f("ballast_pos_mm"),
            ballast_ang_deg=self._fo("ballast_ang_deg"),
            dist_mm=self._f("distance_mm"),
            height_mm=self._f("height_mm"),

            cur_sel=cur,
            act_table=str(act_table),
            hyst_mm=self._fo("hyst_mm"),

            ph1a_p_bar=self._f("ph1a_p_bar"),
            ph1b_p_bar=self._f("ph1b_p_bar"),
            pl1a_p_bar=self._f("pl1a_p_bar"),
            pl1b_p_bar=self._f("pl1b_p_bar"),
            supply_v=supply_v,

            boom_fault=bool(self._latest.get("boom_fault")),
            boom_fault_code=self._io("boom_fault_code") or 0,
            ballast_fault=bool(self._latest.get("ballast_fault")),
            ballast_fault_code=self._io("ballast_fault_code") or 0,

            m_model_kg=self._first_number("g_m_model_kg", "m_model_kg", fallback=0.0),
            m_empty_kg=self._f("m_empty_kg"),
            k_gain=self._f("k_gain", 1.0),
            m_net_kg=self._f("m_net_kg"),
            m_load_kg=self._f("m_load_kg"),
            m_load_t=self._first_number("m_load_ton", "m_load_t", fallback=0.0),

            fondello_fault=bool(self._latest.get("fondello_fault")),
            fondello_warn=bool(self._latest.get("fondello_warn")),
            fondello_p1_bar=self._fo("fondello_p1_bar"),
            fondello_p2_bar=self._fo("fondello_p2_bar"),
            fondello_p_used_bar=self._fo("fondello_p_used_bar"),

            stelo_fault=bool(self._latest.get("stelo_fault")),
            stelo_warn=bool(self._latest.get("stelo_warn")),
            stelo_p1_bar=self._fo("stelo_p1_bar"),
            stelo_p2_bar=self._fo("stelo_p2_bar"),
            stelo_p_used_bar=self._fo("stelo_p_used_bar"),

            boom_pos_mm_meas=self._fo("boom_pos_mm_meas"),
            boom_ang_deg_meas=self._fo("boom_ang_deg_meas"),
            ballast_pos_mm_meas=self._fo("ballast_pos_mm_meas"),
            ballast_ang_deg_meas=self._fo("ballast_ang_deg_meas"),

            ph1a_status=self._io("ph1a_status"),
            ph1b_status=self._io("ph1b_status"),
            pl1a_status=self._io("pl1a_status"),
            pl1b_status=self._io("pl1b_status"),

            ph1a_uout_v=self._fo("ph1a_uout_v"),
            ph1b_uout_v=self._fo("ph1b_uout_v"),
            pl1a_uout_v=self._fo("pl1a_uout_v"),
            pl1b_uout_v=self._fo("pl1b_uout_v"),

            interp_dist_m=self._fo("interp_dist_m"),
            interp_radius_m=self._fo("interp_radius_m"),
            interp_cap_t=self._fo("interp_cap_t"),

            cap_dbg_id=self._io("interp_id"),
            cap_dbg_ir=self._io("interp_ir"),
            cap_dbg_td=self._fo("interp_td"),
            cap_dbg_tr=self._fo("interp_tr"),
            cap_dbg_v00=self._fo("interp_v00"),
            cap_dbg_v10=self._fo("interp_v10"),
            cap_dbg_v01=self._fo("interp_v01"),
            cap_dbg_v11=self._fo("interp_v11"),
        )
        # copia tutti i valori raw letti da OPC-UA nello snapshot finale
        for key, value in self._latest.items():
            setattr(d, key, value)
        # --- campi aggiuntivi per calibration.py ---
        extras = {
            "cal_enable": bool(self._latest.get("cal_enable")),
            "calib_enable": bool(self._latest.get("cal_enable")),

            "cal_mode_empty": bool(self._latest.get("cal_mode_empty")),
            "calib_mode_empty": bool(self._latest.get("cal_mode_empty")),

            "cal_step": self._io("cal_step"),
            "calib_step": self._io("cal_step"),

            "cal_status_text": self._latest.get("cal_status_text"),
            "calib_status_text": self._latest.get("cal_status_text"),

            "cal_curr_alpha_deg": self._fo("cal_curr_alpha_deg"),
            "calib_curr_alpha_deg": self._fo("cal_curr_alpha_deg"),

            "cal_curr_l_mm": self._fo("cal_curr_l_mm"),
            "calib_curr_l_mm": self._fo("cal_curr_l_mm"),

            "cal_target_alpha_deg": self._fo("cal_target_alpha_deg"),
            "calib_target_alpha_deg": self._fo("cal_target_alpha_deg"),

            "cal_target_l_mm": self._fo("cal_target_l_mm"),
            "calib_target_l_mm": self._fo("cal_target_l_mm"),

            "cal_err_alpha_deg": self._fo("cal_err_alpha_deg"),
            "calib_err_alpha_deg": self._fo("cal_err_alpha_deg"),

            "cal_err_l_mm": self._fo("cal_err_l_mm"),
            "calib_err_l_mm": self._fo("cal_err_l_mm"),

            "cal_alpha_tol_deg": self._fo("cal_alpha_tol_deg"),
            "calib_alpha_tol_deg": self._fo("cal_alpha_tol_deg"),

            "cal_l_tol_mm": self._fo("cal_l_tol_mm"),
            "calib_l_tol_mm": self._fo("cal_l_tol_mm"),

            "cal_alpha_stable_tol_deg": self._fo("cal_alpha_stable_tol_deg"),
            "calib_alpha_stable_tol_deg": self._fo("cal_alpha_stable_tol_deg"),

            "cal_l_stable_tol_mm": self._fo("cal_l_stable_tol_mm"),
            "calib_l_stable_tol_mm": self._fo("cal_l_stable_tol_mm"),

            "cal_stable_cycles_req": self._io("cal_stable_cycles_req"),
            "calib_stable_cycles_req": self._io("cal_stable_cycles_req"),

            "cal_stable_count": self._io("cal_stable_count"),
            "calib_stable_count": self._io("cal_stable_count"),

            "cal_in_tolerance": bool(self._latest.get("cal_in_tolerance")),
            "calib_in_tolerance": bool(self._latest.get("cal_in_tolerance")),

            "cal_is_stable": bool(self._latest.get("cal_is_stable")),
            "calib_is_stable": bool(self._latest.get("cal_is_stable")),

            "cal_ready_to_store": bool(self._latest.get("cal_ready_to_store")),
            "calib_ready_to_store": bool(self._latest.get("cal_ready_to_store")),

            "cal_last_store_ok": bool(self._latest.get("cal_last_store_ok")),
            "calib_last_store_ok": bool(self._latest.get("cal_last_store_ok")),

            "cal_last_stored_value": self._fo("cal_last_stored_value"),
            "calib_last_stored_value": self._fo("cal_last_stored_value"),

            "cal_active_i_alpha": self._io("cal_active_ialpha"),
            "calib_active_i_alpha": self._io("cal_active_ialpha"),

            "cal_active_i_l": self._io("cal_active_il"),
            "calib_active_i_l": self._io("cal_active_il"),

            "cal_error_tolerance": bool(self._latest.get("cal_error_tolerance")),
            "calib_error_tolerance": bool(self._latest.get("cal_error_tolerance")),

            "cal_error_state": bool(self._latest.get("cal_error_state")),
            "calib_error_state": bool(self._latest.get("cal_error_state")),

            "cal_store_cmd": bool(self._latest.get("cal_store_cmd")),
            "calib_store_cmd": bool(self._latest.get("cal_store_cmd")),

            "g_m_ref_kg": self._fo("g_m_ref_kg"),
            "m_ref_kg": self._fo("g_m_ref_kg"),
            "calib_m_ref_kg": self._fo("g_m_ref_kg"),

            "g_m_model_kg": self._fo("g_m_model_kg"),
            "m_model_kg": self._fo("g_m_model_kg"),

            "m_empty_interp_kg": self._fo("m_empty_interp_kg") or self._fo("m_empty_kg"),
            "calib_m_empty_interp_kg": self._fo("m_empty_interp_kg") or self._fo("m_empty_kg"),

            "m_net_kg": self._fo("m_net_kg"),
            "calib_m_net_kg": self._fo("m_net_kg"),
        }

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