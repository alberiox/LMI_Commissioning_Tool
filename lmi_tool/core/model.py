from dataclasses import dataclass
from typing import Optional


@dataclass
class LMIData:
    ts: float

    # Limiter
    util_pct: float = 0.0
    warning: bool = False
    overload: bool = False
    near_limit: bool = False
    cap_t: float = 0.0
    load_f_t: float = 0.0
    margin_t: float = 0.0
    margin_pct: float = 0.0

    # Geometry / selection
    boom_pos_mm: float = 0.0
    boom_ang_deg: float = 0.0
    ballast_pos_mm: float = 0.0
    ballast_ang_deg: Optional[float] = None
    dist_mm: float = 0.0
    height_mm: float = 0.0
    cur_sel: int = 0
    act_table: str = "---"
    hyst_mm: Optional[float] = None

    # Pressures (scaled)
    ph1a_p_bar: float = 0.0
    ph1b_p_bar: float = 0.0
    pl1a_p_bar: float = 0.0
    pl1b_p_bar: float = 0.0
    supply_v: float = 0.0

    # Validate status
    boom_fault: bool = False
    boom_fault_code: int = 0
    ballast_fault: bool = False
    ballast_fault_code: int = 0

    # Model chain
    m_model_kg: float = 0.0
    m_empty_kg: float = 0.0
    k_gain: float = 1.0
    m_net_kg: float = 0.0
    m_load_kg: float = 0.0
    m_load_t: float = 0.0

    # Pressure-pair model inputs
    fondello_fault: bool = False
    fondello_warn: bool = False
    fondello_p1_bar: Optional[float] = None
    fondello_p2_bar: Optional[float] = None
    fondello_p_used_bar: Optional[float] = None
    stelo_fault: bool = False
    stelo_warn: bool = False
    stelo_p1_bar: Optional[float] = None
    stelo_p2_bar: Optional[float] = None
    stelo_p_used_bar: Optional[float] = None

    # Extra sensor details for Sensors page
    boom_pos_mm_meas: Optional[float] = None
    boom_ang_deg_meas: Optional[float] = None
    ballast_pos_mm_meas: Optional[float] = None
    ballast_ang_deg_meas: Optional[float] = None

    ph1a_status: Optional[int] = None
    ph1b_status: Optional[int] = None
    pl1a_status: Optional[int] = None
    pl1b_status: Optional[int] = None

    ph1a_uout_v: Optional[float] = None
    ph1b_uout_v: Optional[float] = None
    pl1a_uout_v: Optional[float] = None
    pl1b_uout_v: Optional[float] = None

    ph1a_us_v: Optional[float] = None
    ph1b_us_v: Optional[float] = None
    pl1a_us_v: Optional[float] = None
    pl1b_us_v: Optional[float] = None

    # Load table debug
    interp_dist_m: Optional[float] = None
    interp_radius_m: Optional[float] = None
    interp_cap_t: Optional[float] = None
    cap_dbg_id: Optional[int] = None
    cap_dbg_ir: Optional[int] = None
    cap_dbg_td: Optional[float] = None
    cap_dbg_tr: Optional[float] = None
    cap_dbg_v00: Optional[float] = None
    cap_dbg_v10: Optional[float] = None
    cap_dbg_v01: Optional[float] = None
    cap_dbg_v11: Optional[float] = None
