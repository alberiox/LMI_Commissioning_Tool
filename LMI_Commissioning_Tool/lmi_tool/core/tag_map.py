TAG_GROUPS = {

    "overview": {
        "m_load_ton": "ns=5;s=::LoadLimite:M_Load_Ton",
        "m_model_kg": "ns=5;s=::LoadLimite:g_M_model_kg",
        "cap_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Cap_t",
        "util_pct": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Util_pct",
        "margin_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Margin_t",
        "warning": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Warning",
        "overload": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Overload",
    },

    "sensors": {

        # BOOM
        "boom_pos_mm_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Pos_mm_meas",
        "boom_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Pos_mm",
        "boom_ang_deg_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Ang_deg_meas",
        "boom_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Ang_deg",
        "boom_fault": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Fault",
        "boom_fault_code": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.FaultCode",

        # BALLAST
        "ballast_pos_mm_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Pos_mm_meas",
        "ballast_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Pos_mm",
        "ballast_ang_deg_meas": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Ang_deg_meas",
        "ballast_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Ang_deg",
        "ballast_fault": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Fault",
        "ballast_fault_code": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.FaultCode",

           
         # PRESSURE
        "ph1a_p_bar": "ns=5;s=::LoadLimite:PH1A_FB_Pr4Pressure.P_bar",
        "ph1b_p_bar": "ns=5;s=::LoadLimite:PH1B_FB_Pr4Pressure.P_bar",
        "pl1a_p_bar": "ns=5;s=::LoadLimite:PL1A_FB_Pr4Pressure.P_bar",
        "pl1b_p_bar": "ns=5;s=::LoadLimite:PL1B_FB_Pr4Pressure.P_bar",

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
    
    
    
    
    
    },

    "geometry": {

        "distance_mm": "ns=5;s=::LoadLimite:fbLoadPosition.Distance_mm",
        "height_mm": "ns=5;s=::LoadLimite:fbLoadPosition.Height_mm",

        "boom_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Pos_mm",
        "boom_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Boom.Ang_deg",

        "ballast_pos_mm": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Pos_mm",
        "ballast_ang_deg": "ns=5;s=::LoadLimite:FB_CET12_CanOpen_Validate_Ballas.Ang_deg",
    },

    "tables": {

        "cap_t": "ns=5;s=::LoadLimite:FB_Interp2D_LoadCap_0.Cap_t",
        "margin_t": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Margin_t",
        "util_pct": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Util_pct",
        "warning": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Warning",
        "overload": "ns=5;s=::LoadLimite:FB_LoadLimCheck_0.Overload",
    },

    "calibration": {

        "calib_enable": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Enable",
        "calib_mode_empty": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ModeEmpty",
        "calib_step": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Step",
        "calib_status_text": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StatusText",

        "calib_curr_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.CurrAlphaDeg",
        "calib_curr_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.CurrL_mm",

        "calib_target_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.TargetAlphaDeg",
        "calib_target_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.TargetL_mm",

        "calib_err_alpha_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrAlphaDeg",
        "calib_err_l_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrL_mm",

        "calib_alpha_tol_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.AlphaTolDeg",
        "calib_l_tol_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LTol_mm",

        "calib_alpha_stable_tol_deg": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.AlphaStableTolDeg",
        "calib_l_stable_tol_mm": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LStableTol_mm",

        "calib_stable_cycles_req": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StableCyclesReq",
        "calib_stable_count": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StableCount",

        "calib_in_tolerance": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.InTolerance",
        "calib_is_stable": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.IsStable",

        "calib_ready_to_store": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ReadyToStore",
        "calib_last_store_ok": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LastStoreOK",

        "calib_last_stored_value": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.LastStoredValue",

        "calib_active_i_alpha": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iAlpha",
        "calib_active_i_l": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.Active_iL",

        "calib_error_tolerance": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrorTolerance",
        "calib_error_state": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.ErrorState",

        "calib_store_cmd": "ns=5;s=::AsGlobalPV:g_LM_CalibHMI.StoreCmd",
    },
}


def build_flat_tag_map(groups=None):

    if groups is None:
        groups = TAG_GROUPS.keys()

    flat = {}

    for group in groups:
        flat.update(TAG_GROUPS[group])

    return flat