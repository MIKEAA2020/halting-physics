\ Boolean forbidden-tuple encoding
Minimize
 obj: 0
Subject To
 c0_load_low__force_top_left: act_n3__load_low + act_n4__load_low + act_n5__load_low + act_n6__load_low >= 1
 c1_load_low__force_top_left: act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -1
 c2_load_low__force_top_left: act_n3__load_low - act_n4__load_low + act_n5__load_low + act_n6__load_low >= 0
 c3_load_low__force_top_left: act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c4_load_low__force_top_left: - act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c5_load_low__force_top_left: - act_n3__load_low - act_n4__load_low + act_n5__load_low - act_n6__load_low >= -2
 c6_load_low__force_top_left: - act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -3
 c7_load_low__force_bot_left: act_n3__load_low + act_n4__load_low + act_n5__load_low + act_n6__load_low >= 1
 c8_load_low__force_bot_left: act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -1
 c9_load_low__force_bot_left: act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c10_load_low__force_bot_left: - act_n3__load_low + act_n4__load_low + act_n5__load_low + act_n6__load_low >= 0
 c11_load_low__force_bot_left: - act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c12_load_low__force_bot_left: - act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -3
 c13_load_low__force_vert_tip: act_n3__load_low + act_n4__load_low + act_n5__load_low - act_n6__load_low >= 0
 c14_load_low__force_vert_tip: act_n3__load_low - act_n4__load_low + act_n5__load_low - act_n6__load_low >= -1
 c15_load_low__force_vert_tip: - act_n3__load_low + act_n4__load_low + act_n5__load_low - act_n6__load_low >= -1
 c16_load_low__force_vert_tip: - act_n3__load_low - act_n4__load_low + act_n5__load_low - act_n6__load_low >= -2
 c17_load_low__force_diag_14: act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c18_load_low__force_diag_14: - act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c19_load_low__force_diag_14: - act_n3__load_low - act_n4__load_low + act_n5__load_low - act_n6__load_low >= -2
 c20_load_low__force_diag_14: - act_n3__load_low - act_n4__load_low - act_n5__load_low + act_n6__load_low >= -2
 c21_load_low__force_diag_14: - act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -3
 c22_load_low__force_diag_23: act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c23_load_low__force_diag_23: - act_n3__load_low + act_n4__load_low + act_n5__load_low - act_n6__load_low >= -1
 c24_load_low__force_diag_23: - act_n3__load_low + act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c25_load_low__force_diag_23: - act_n3__load_low - act_n4__load_low + act_n5__load_low - act_n6__load_low >= -2
 c26_load_low__force_diag_23: - act_n3__load_low - act_n4__load_low - act_n5__load_low + act_n6__load_low >= -2
 c27_load_low__force_diag_23: - act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -3
 c28_load_low__force_diag_36: act_n3__load_low - act_n4__load_low - act_n5__load_low - act_n6__load_low >= -2
 c29_load_low__force_diag_45: act_n3__load_low - act_n4__load_low + act_n5__load_low + act_n6__load_low >= 0
 c30_load_high__force_top_left: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c31_load_high__force_top_left: act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= 0
 c32_load_high__force_top_left: act_n3__load_high + act_n4__load_high - act_n5__load_high + act_n6__load_high >= 0
 c33_load_high__force_top_left: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c34_load_high__force_top_left: act_n3__load_high - act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c35_load_high__force_top_left: act_n3__load_high - act_n4__load_high - act_n5__load_high + act_n6__load_high >= -1
 c36_load_high__force_top_left: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c37_load_high__force_top_left: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c38_load_high__force_top_left: - act_n3__load_high - act_n4__load_high - act_n5__load_high - act_n6__load_high >= -3
 c39_load_high__force_top_right: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c40_load_high__force_top_right: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c41_load_high__force_top_right: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c42_load_high__force_top_right: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c43_load_high__force_bot_left: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c44_load_high__force_bot_left: act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= 0
 c45_load_high__force_bot_left: act_n3__load_high + act_n4__load_high - act_n5__load_high + act_n6__load_high >= 0
 c46_load_high__force_bot_left: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c47_load_high__force_bot_left: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c48_load_high__force_bot_left: - act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c49_load_high__force_bot_left: - act_n3__load_high + act_n4__load_high - act_n5__load_high + act_n6__load_high >= -1
 c50_load_high__force_bot_left: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c51_load_high__force_vert_tip: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c52_load_high__force_vert_tip: act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= 0
 c53_load_high__force_vert_tip: act_n3__load_high + act_n4__load_high - act_n5__load_high - act_n6__load_high >= -1
 c54_load_high__force_vert_tip: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c55_load_high__force_vert_tip: act_n3__load_high - act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c56_load_high__force_vert_tip: act_n3__load_high - act_n4__load_high - act_n5__load_high - act_n6__load_high >= -2
 c57_load_high__force_vert_tip: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c58_load_high__force_vert_tip: - act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c59_load_high__force_vert_tip: - act_n3__load_high + act_n4__load_high - act_n5__load_high - act_n6__load_high >= -2
 c60_load_high__force_vert_tip: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c61_load_high__force_vert_tip: - act_n3__load_high - act_n4__load_high + act_n5__load_high - act_n6__load_high >= -2
 c62_load_high__force_vert_tip: - act_n3__load_high - act_n4__load_high - act_n5__load_high - act_n6__load_high >= -3
 c63_load_high__force_diag_14: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c64_load_high__force_diag_14: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c65_load_high__force_diag_14: - act_n3__load_high - act_n4__load_high - act_n5__load_high - act_n6__load_high >= -3
 c66_load_high__force_diag_23: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c67_load_high__force_diag_23: - act_n3__load_high + act_n4__load_high - act_n5__load_high - act_n6__load_high >= -2
 c68_load_high__force_diag_23: - act_n3__load_high - act_n4__load_high - act_n5__load_high - act_n6__load_high >= -3
 c69_load_high__force_diag_36: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c70_load_high__force_diag_36: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c71_load_high__force_diag_36: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c72_load_high__force_diag_36: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c73_load_high__force_diag_45: act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 1
 c74_load_high__force_diag_45: act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= 0
 c75_load_high__force_diag_45: act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c76_load_high__force_diag_45: act_n3__load_high - act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c77_load_high__force_diag_45: act_n3__load_high - act_n4__load_high - act_n5__load_high + act_n6__load_high >= -1
 c78_load_high__force_diag_45: - act_n3__load_high + act_n4__load_high + act_n5__load_high + act_n6__load_high >= 0
 c79_load_high__force_diag_45: - act_n3__load_high + act_n4__load_high + act_n5__load_high - act_n6__load_high >= -1
 c80_load_high__force_diag_45: - act_n3__load_high - act_n4__load_high + act_n5__load_high + act_n6__load_high >= -1
 c81_load_high__force_diag_45: - act_n3__load_high - act_n4__load_high + act_n5__load_high - act_n6__load_high >= -2
Binary
 act_n3__load_low
 act_n4__load_low
 act_n5__load_low
 act_n6__load_low
 act_n3__load_high
 act_n4__load_high
 act_n5__load_high
 act_n6__load_high
End
