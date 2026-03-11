import math
import random
import time

from PySide6 import QtCore

from lmi_tool.core.model import LMIData


class SimSource(QtCore.QObject):
    updated = QtCore.Signal(object)  # emits LMIData

    def __init__(self, parent=None, interval_ms: int = 50):
        super().__init__(parent)
        self.t0 = time.time()
        self._t = 0.0
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self._tick)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def _tick(self):
        self._t += self.timer.interval() / 1000.0
        ts = time.time() - self.t0

        boom_len = 12072 + 5000 * (0.5 + 0.5 * math.sin(self._t * 0.18))
        boom_ang = -5 + 55 * (0.5 + 0.5 * math.sin(self._t * 0.12 + 1.2))
        dist = 2500 + 6000 * (0.5 + 0.5 * math.sin(self._t * 0.16 + 0.6))
        height = 1500 + 4500 * (0.5 + 0.5 * math.sin(self._t * 0.11 + 2.3))
        ballast = 12000 + 4500 * (0.5 + 0.5 * math.sin(self._t * 0.10 + 0.4))
        ballast_ang = -3 + 18 * (0.5 + 0.5 * math.sin(self._t * 0.09 + 0.9))

        if ballast < 12100:
            cur, act = 12, "12000"
        elif ballast < 13550:
            cur, act = 13, "13000"
        elif ballast < 14050:
            cur, act = 14, "14000"
        elif ballast < 15050:
            cur, act = 15, "15000"
        else:
            cur, act = 16, "16000"

        supply_v = 10.8 + random.uniform(-0.1, 0.1)
        ph1a = 120 + 35 * math.sin(self._t * 0.6) + random.uniform(-1.5, 1.5)
        ph1b = ph1a + random.uniform(-3.0, 3.0)
        pl1a = 80 + 25 * math.sin(self._t * 0.55 + 1.0) + random.uniform(-1.5, 1.5)
        pl1b = pl1a + random.uniform(-3.0, 3.0)

        fondello_p_used = max(ph1a, ph1b)
        stelo_p_used = max(pl1a, pl1b)
        m_model = 8000 + 120000 * (0.5 + 0.5 * math.sin(self._t * 0.22)) + random.uniform(-1200, 1200)
        m_empty = 7000 + (boom_len - 12072) * 0.35 + (boom_ang - 10) * 15
        k_gain = 1.0 + 0.02 * math.sin(self._t * 0.07)
        m_net = max(0.0, m_model - m_empty)
        m_load = m_net * k_gain
        m_load_t = m_load / 1000.0

        cap_t = max(80.0, min(200.0, 200.0 - 0.004 * (boom_len - 12072) - 0.006 * (dist - 2500)))
        load_f_t = max(0.0, min(cap_t * 1.15, m_load_t + random.uniform(-1.2, 1.2)))

        util = (load_f_t / cap_t) * 100.0 if cap_t > 0 else 0.0
        warning = util >= 90.0
        overload = util >= 100.0
        near_limit = (cap_t - load_f_t) <= 5.0

        margin_t = cap_t - load_f_t
        margin_pct = 100.0 - util

        d = LMIData(
            ts=ts,
            util_pct=util,
            warning=warning,
            overload=overload,
            near_limit=near_limit,
            cap_t=cap_t,
            load_f_t=load_f_t,
            margin_t=margin_t,
            margin_pct=margin_pct,
            boom_pos_mm=boom_len,
            boom_ang_deg=boom_ang,
            ballast_pos_mm=ballast,
            dist_mm=dist,
            height_mm=height,
            cur_sel=cur,
            act_table=act,
            ph1a_p_bar=ph1a,
            ph1b_p_bar=ph1b,
            pl1a_p_bar=pl1a,
            pl1b_p_bar=pl1b,
            supply_v=supply_v,
            boom_fault=False,
            boom_fault_code=0,
            ballast_fault=False,
            ballast_fault_code=0,
            m_model_kg=m_model,
            m_empty_kg=m_empty,
            k_gain=k_gain,
            m_net_kg=m_net,
            m_load_kg=m_load,
            m_load_t=m_load_t,
            boom_pos_mm_meas=boom_len + random.uniform(-8.0, 8.0),
            boom_ang_deg_meas=boom_ang + random.uniform(-0.2, 0.2),
            ballast_pos_mm_meas=ballast + random.uniform(-10.0, 10.0),
            ballast_ang_deg=ballast_ang,
            ballast_ang_deg_meas=ballast_ang + random.uniform(-0.15, 0.15),
            ph1a_status=0,
            ph1b_status=0,
            pl1a_status=0,
            pl1b_status=0,
            ph1a_uout_v=4.2 + ph1a / 100.0,
            ph1b_uout_v=4.2 + ph1b / 100.0,
            pl1a_uout_v=4.2 + pl1a / 100.0,
            pl1b_uout_v=4.2 + pl1b / 100.0,
            fondello_fault=False,
            fondello_warn=False,
            fondello_p1_bar=ph1a,
            fondello_p2_bar=ph1b,
            fondello_p_used_bar=fondello_p_used,
            stelo_fault=False,
            stelo_warn=False,
            stelo_p1_bar=pl1a,
            stelo_p2_bar=pl1b,
            stelo_p_used_bar=stelo_p_used,
            cap_dbg_id=6,
            cap_dbg_ir=8,
            cap_dbg_td=0.34,
            cap_dbg_tr=0.61,
            cap_dbg_v00=155.0,
            cap_dbg_v10=144.0,
            cap_dbg_v01=160.0,
            cap_dbg_v11=147.0,
        )
        self.updated.emit(d)
