\ Boolean forbidden-tuple encoding
Minimize
 obj: 0
Subject To
 c0_neq0_1: x0 + x1 >= 1
 c1_neq0_1: - x0 - x1 >= -1
 c2_neq1_2: x1 + x2 >= 1
 c3_neq1_2: - x1 - x2 >= -1
 c4_neq2_3: x2 + x3 >= 1
 c5_neq2_3: - x2 - x3 >= -1
 c6_neq3_4: x3 + x4 >= 1
 c7_neq3_4: - x3 - x4 >= -1
 c8_neq4_0: x4 + x0 >= 1
 c9_neq4_0: - x4 - x0 >= -1
Binary
 x0
 x1
 x2
 x3
 x4
End
