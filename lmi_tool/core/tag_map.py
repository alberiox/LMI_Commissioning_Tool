# lmi_tool/core/tag_map.py

# IMPORTANT:
# The keys of this map are used directly by the UI pages.
# Reordering/grouping is safe.
# Renaming an existing key requires updating the corresponding UI page(s).

TAG_MAP = {
    # ==========================================================
    # LIMITER / RESULT
    # ==========================================================
    "warning": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Warning",
    "near_limit": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.NearLimit",
    "margin_pct": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Margin_pct",
    "load_f_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Load_f_t",
    "util_pct": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Util_pct",
    "overload": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Overload",
    "margin_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Margin_t",
    "cap_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Cap_t",

    # ==========================================================
    # LOAD TABLE / SELECTION
    # ==========================================================
    "cur_sel": "ns=5;s=::LoadLimite:CurSel",
    "hyst_mm": "ns=5;s=::LoadLimite:HYST_MM",
    "act_table": "ns=5;s=::LoadLimite:ActTable",

    # ==========================================================
    # LOAD POSITION / GEOMETRY RESULT
    # ==========================================================
    "height_mm": "ns=5;s=::LoadLimite:fbLoadPosition.Height_mm",
    "distance_mm": "ns=5;s=::LoadLimite:fbLoadPosition.Distance_mm",

    # ==========================================================
    # BOOM VALIDATION / ACTIVE GEOMETRY
    # ==========================================================
    "boom_fault": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Fault",
    "boom_fault_code": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.FaultCode",
    "boom_enable": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Enable",
    "boom_pos_mm_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Pos_mm_meas",
    "boom_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Pos_mm",
    "boom_ang_deg_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Ang_deg_meas",
    "boom_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Ang_deg",

    # ==========================================================
    # BALLAST VALIDATION / ACTIVE GEOMETRY
    # ==========================================================
    "ballast_fault": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Fault",
    "ballast_fault_code": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.FaultCode",
    "ballast_enable": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Enable",
    "ballast_pos_mm_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Pos_mm_meas",
    "ballast_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Pos_mm",
    "ballast_ang_deg_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Ang_deg_meas",
    "ballast_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Ang_deg",

    # ==========================================================
    # PRESSURE SENSORS RAW / SCALED
    # ==========================================================
    "ph1a_p_bar": "ns=5;s=::LoadLimite:PH1A_FB_Pr4Pressure.P_bar",
    "ph1a_uout_v": "ns=5;s=::LoadLimite:PH1A_FB_Pr4Pressure.Uout_V",
    "ph1a_us_v": "ns=5;s=::LoadLimite:PH1A_FB_Pr4Pressure.Us_V",
    "ph1a_status": "ns=5;s=::LoadLimite:PH1A_FB_Pr4Pressure.Status",

    "ph1b_p_bar": "ns=5;s=::LoadLimite:PH1B_FB_Pr4Pressure.P_bar",
    "ph1b_uout_v": "ns=5;s=::LoadLimite:PH1B_FB_Pr4Pressure.Uout_V",
    "ph1b_us_v": "ns=5;s=::LoadLimite:PH1B_FB_Pr4Pressure.Us_V",
    "ph1b_status": "ns=5;s=::LoadLimite:PH1B_FB_Pr4Pressure.Status",

    "pl1a_p_bar": "ns=5;s=::LoadLimite:PL1A_FB_Pr4Pressure.P_bar",
    "pl1a_uout_v": "ns=5;s=::LoadLimite:PL1A_FB_Pr4Pressure.Uout_V",
    "pl1a_us_v": "ns=5;s=::LoadLimite:PL1A_FB_Pr4Pressure.Us_V",
    "pl1a_status": "ns=5;s=::LoadLimite:PL1A_FB_Pr4Pressure.Status",

    "pl1b_p_bar": "ns=5;s=::LoadLimite:PL1B_FB_Pr4Pressure.P_bar",
    "pl1b_uout_v": "ns=5;s=::LoadLimite:PL1B_FB_Pr4Pressure.Uout_V",
    "pl1b_us_v": "ns=5;s=::LoadLimite:PL1B_FB_Pr4Pressure.Us_V",
    "pl1b_status": "ns=5;s=::LoadLimite:PL1B_FB_Pr4Pressure.Status",

    # Optional raw analog channels from AsGlobalPV
    "ph1a_pressure_raw": "ns=5;s=::AsGlobalPV:IO.CPU.Ai.PH1A_Pressure",
    "ph1b_pressure_raw": "ns=5;s=::AsGlobalPV:IO.CPU.Ai.PH1B_Pressure",
    "pl1a_pressure_raw": "ns=5;s=::AsGlobalPV:IO.CPU.Ai.PL1A_Pressure",
    "pl1b_pressure_raw": "ns=5;s=::AsGlobalPV:IO.CPU.Ai.PL1B_Pressure",

    # ==========================================================
    # HYDRAULICS - VALIDATED / SELECTED PRESSURES
    # These keys are used directly by Hydraulics page
    # ==========================================================
    "fondello_p1_bar": "ns=5;s=::LoadLimite:Fondello_FB_PressurePair.P1_bar",
    "fondello_p2_bar": "ns=5;s=::LoadLimite:Fondello_FB_PressurePair.P2_bar",
    "fondello_p_used_bar": "ns=5;s=::LoadLimite:Fondello_FB_PressurePair.P_used_bar",
    "fondello_warn": "ns=5;s=::LoadLimite:Fondello_FB_PressurePair.Warn",
    "fondello_fault": "ns=5;s=::LoadLimite:Fondello_FB_PressurePair.Fault",

    "stelo_p1_bar": "ns=5;s=::LoadLimite:Stelo_FB_PressurePair.P1_bar",
    "stelo_p2_bar": "ns=5;s=::LoadLimite:Stelo_FB_PressurePair.P2_bar",
    "stelo_p_used_bar": "ns=5;s=::LoadLimite:Stelo_FB_PressurePair.P_used_bar",
    "stelo_warn": "ns=5;s=::LoadLimite:Stelo_FB_PressurePair.Warn",
    "stelo_fault": "ns=5;s=::LoadLimite:Stelo_FB_PressurePair.Fault",

    # ==========================================================
    # LOAD MODEL
    # These keys are used by Hydraulics & Weight Model page
    # ==========================================================
    "g_m_model_kg": "ns=5;s=::AsGlobalPV:g_M_model_kg",
    "m_model_kg": "ns=5;s=::AsGlobalPV:g_M_model_kg",  # alias kept for UI compatibility
    "m_empty_kg": "ns=5;s=::LoadLimite:M_empty_kg",
    "k_gain": "ns=5;s=::LoadLimite:K_gain",
    "m_net_kg": "ns=5;s=::LoadLimite:M_net_kg",
    "m_load_kg": "ns=5;s=::LoadLimite:M_Load_kg",
    "m_load_ton": "ns=5;s=::LoadLimite:M_Load_Ton",

    # ==========================================================
    # 2D CAPACITY INTERPOLATION / DEBUG
    # ==========================================================
    "interp_cap_t": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.Cap_t",
    "interp_dist_m": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.Dist_m",
    "interp_radius_m": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.Radius_m",
    "interp_id": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.iD",
    "interp_ir": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.iR",
    "interp_td": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.tD",
    "interp_tr": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.tR",
    "interp_v00": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.V00",
    "interp_v01": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.V01",
    "interp_v10": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.V10",
    "interp_v11": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.V11",

    # ==========================================================
    # CALIBRATION HMI
    # ==========================================================
    "cal_enable": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Enable",
    "cal_active_i_alpha": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iAlpha",
    "cal_active_i_l": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iL",
    "cal_alpha_stable_tol_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.AlphaStableTolDeg",
    "cal_alpha_tol_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.AlphaTolDeg",
    "cal_curr_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.CurrAlphaDeg",
    "cal_curr_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.CurrL_mm",
    "cal_err_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrAlphaDeg",
    "cal_err_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrL_mm",
    "cal_error_state": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrorState",
    "cal_error_tolerance": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrorTolerance",
    "cal_in_tolerance": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.InTolerance",
    "cal_is_stable": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.IsStable",
    "cal_l_stable_tol_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LStableTol_mm",
    "cal_l_tol_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LTol_mm",
    "cal_last_store_ok": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LastStoreOK",
    "cal_last_stored_value": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LastStoredValue",
    "cal_mode_empty": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ModeEmpty",
    "cal_ready_to_store": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ReadyToStore",
    "cal_stable_cycles_req": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StableCyclesReq",
    "cal_status_text": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StatusText",
    "cal_step": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Step",
    "cal_store_cmd": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StoreCmd",
    "cal_target_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.TargetAlphaDeg",
    "cal_target_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.TargetL_mm",
    "cal_stable_count": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StableCount",
    # extra calibration/result values used by calibration page
    "g_m_ref_kg": "ns=5;s=::AsGlobalPV:g_M_ref_kg",
    "m_ref_kg": "ns=5;s=::AsGlobalPV:g_M_ref_kg",
    "m_empty_interp_kg": "ns=5;s=::LoadLimite:M_empty_interp_kg",
    "calib_m_empty_interp_kg": "ns=5;s=::LoadLimite:M_empty_interp_kg",
    # aliases for calibration page compatibility
    "calib_active_i_alpha": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iAlpha",
    "calib_active_i_l": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iL",
    "active_i_alpha": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iAlpha",
    "active_i_l": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iL",

}
def build_flat_tag_map():
    return TAG_MAP.copy()