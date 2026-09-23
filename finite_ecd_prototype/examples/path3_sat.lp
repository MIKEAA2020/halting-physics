\ Boolean forbidden-tuple encoding
Minimize
 obj: 0
Subject To
 c0_neq01: x0 + x1 >= 1
 c1_neq01: - x0 - x1 >= -1
 c2_neq12: x1 + x2 >= 1
 c3_neq12: - x1 - x2 >= -1
Binary
 x0
 x1
 x2
End
