#7dec 12:38pm 70 testcases - performing it only once for the experiment

test_cases1 = [
    # ----------------------------------------------------------------------
    # Group 1: Baseline and Simple Approximations (10 cases)
    # Testing basic functionality, flat lines, and perfect fits.
    # ----------------------------------------------------------------------
    {'name': 'G1_Perfect_Fit_1_Segment_Flat', 'pw_linear_fx': [(0.0, 5.0), (10.0, 5.0)], 'epsilon': 0.1, 'expected_k': 1},
    {'name': 'G1_Perfect_Fit_1_Segment_Slope', 'pw_linear_fx': [(0.0, 0.0), (5.0, 5.0), (10.0, 10.0)], 'epsilon': 0.5, 'expected_k': 1},
    {'name': 'G1_Requires_2_Segments_Simple_Bend', 'pw_linear_fx': [(0.0, 0.0), (5.0, 1.0), (10.0, 0.0)], 'epsilon': 0.4, 'expected_k': 2},
    {'name': 'G1_Single_Point_No_Segments', 'pw_linear_fx': [(0.0, 0.0)], 'epsilon': 0.01, 'expected_k': 0}, # Should handle 0 or 1 point gracefully
    {'name': 'G1_Two_Points_1_Segment_Min_Data', 'pw_linear_fx': [(1.0, 1.0), (2.0, 2.0)], 'epsilon': 0.01, 'expected_k': 1},
    {'name': 'G1_Flat_Tolerance_Too_Small', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0)], 'epsilon': 0.01, 'expected_k': 2},
    {'name': 'G1_Linear_Interpolation_Max_Eps', 'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 1.0, 'expected_k': 1},
    {'name': 'G1_Linear_Interpolation_Mid_Eps', 'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 0.49, 'expected_k': 2},
    {'name': 'G1_Long_Flat_Line', 'pw_linear_fx': [(i, 5.0) for i in range(11)], 'epsilon': 0.001, 'expected_k': 1},
    {'name': 'G1_Constant_Slope', 'pw_linear_fx': [(i, 2.0 * i) for i in range(6)], 'epsilon': 0.001, 'expected_k': 1},

    # ----------------------------------------------------------------------
    # Group 2: L-Infinity Edge Cases (10 cases)
    # Focusing on points exactly at the epsilon boundary.
    # ----------------------------------------------------------------------
    {'name': 'G2_Exact_Eps_Boundary_Fit_In', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], 'epsilon': 0.5, 'expected_k': 1}, # Fits exactly
    {'name': 'G2_Exact_Eps_Boundary_Fit_Out', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.50001), (2.0, 0.0)], 'epsilon': 0.5, 'expected_k': 2}, # Fails just outside
    {'name': 'G2_Multiple_Points_Boundary', 'pw_linear_fx': [(i, 0.5 * (1 - abs(i-2))) for i in range(5)], 'epsilon': 0.5, 'expected_k': 2}, # Two segments, points touch eps band
    {'name': 'G2_Tight_Sawtooth_Requires_Many', 'pw_linear_fx': [(i, 0.5 * (i % 2)) for i in range(11)], 'epsilon': 0.2, 'expected_k': 5}, # Alternating points
    {'name': 'G2_Negative_Deviation', 'pw_linear_fx': [(0.0, 0.0), (1.0, -0.5), (2.0, 0.0)], 'epsilon': 0.5, 'expected_k': 1}, # Testing negative deviations
    {'name': 'G2_Boundary_Midpoint_Test', 'pw_linear_fx': [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], 'epsilon': 0.5, 'expected_k': 2}, # Midpoint exceeds
    {'name': 'G2_Tight_Segment_Separation', 'pw_linear_fx': [(0,0), (1,0.5), (2,0), (3,0), (4,0.5), (5,0)], 'epsilon': 0.49, 'expected_k': 3}, # Two distinct humps
    {'name': 'G2_Boundary_Float_Epsilon', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0001)], 'epsilon': 0.0001, 'expected_k': 1},
    {'name': 'G2_Boundary_Float_Exceed', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.000100001)], 'epsilon': 0.0001, 'expected_k': 2},
    {'name': 'G2_Large_Data_Small_Eps', 'pw_linear_fx': [(i, (i % 3) / 100.0) for i in range(31)], 'epsilon': 0.005, 'expected_k': 15}, # Many segments needed

    # ----------------------------------------------------------------------
    # Group 3: Optimality/Greedy Algorithm Traps (10 cases)
    # Cases designed to make a simple greedy algorithm fail to find the minimum 'k'.
    # ----------------------------------------------------------------------
    # (The optimal solution requires a shorter first segment to enable a much longer second segment.)
    {'name': 'G3_Greedy_Trap_Short_First', 'pw_linear_fx': [(0,0), (2,0.5), (4,0), (6,0.6), (10,0)], 'epsilon': 0.5, 'expected_k': 2},
    {'name': 'G3_Greedy_Trap_Shorter_Optimal', 'pw_linear_fx': [(0,0), (1, 0.5), (2, 0.4), (3, 0.5), (4, 0.0)], 'epsilon': 0.45, 'expected_k': 3},
    {'name': 'G3_Greedy_Trap_Longer_Second', 'pw_linear_fx': [(0,0), (3, 0.5), (4, 0.1), (5, 0.5), (8, 0.0)], 'epsilon': 0.4, 'expected_k': 3},
    {'name': 'G3_Greedy_Trap_Three_Segments', 'pw_linear_fx': [(0,0), (2,0.4), (4,0), (6,0.5), (8,0), (10,0.4), (12,0)], 'epsilon': 0.39, 'expected_k': 5},
    {'name': 'G3_Optimal_Boundary_Shift_1', 'pw_linear_fx': [(0,0), (1, 0.45), (2, 0.0), (3, 0.0), (4, 0.45), (5, 0.0)], 'epsilon': 0.4, 'expected_k': 4},
    {'name': 'G3_Optimal_Boundary_Shift_2', 'pw_linear_fx': [(0,0), (1, 0.4), (2, 0.0), (3, 0.0), (4, 0.4), (5, 0.0)], 'epsilon': 0.4, 'expected_k': 2}, # Same points, slightly different eps
    {'name': 'G3_Overlapping_Segments_1', 'pw_linear_fx': [(0,0), (2, 0.5), (4, -0.5), (6, 0.5), (8, 0.0)], 'epsilon': 0.5, 'expected_k': 2},
    {'name': 'G3_Overlapping_Segments_2', 'pw_linear_fx': [(0,0), (2, 0.5), (4, -0.5), (6, 0.5), (8, 0.0)], 'epsilon': 0.49, 'expected_k': 4}, # Minimal eps change forces more segments
    {'name': 'G3_Small_Initial_Segment_Saves', 'pw_linear_fx': [(0,0), (1,0.1), (2,0.0), (4,0.5), (6,0.0), (8,0.5), (10,0.0)], 'epsilon': 0.4, 'expected_k': 4},
    {'name': 'G3_Small_Initial_Segment_Optimal', 'pw_linear_fx': [(0,0), (1,0.0), (2,0.0), (4,0.5), (6,0.0), (8,0.5), (10,0.0)], 'epsilon': 0.4, 'expected_k': 3},

    # ----------------------------------------------------------------------
    # Group 4: Concave/Convex Shapes (10 cases)
    # Testing curves that change direction, like parabolas or sine waves.
    # ----------------------------------------------------------------------
    {'name': 'G4_Parabola_Concave_Wide_Eps', 'pw_linear_fx': [(i, -i * (i-10)) for i in range(11)], 'epsilon': 5.0, 'expected_k': 1},
    {'name': 'G4_Parabola_Concave_Tight_Eps', 'pw_linear_fx': [(i, -i * (i-10)) for i in range(11)], 'epsilon': 1.0, 'expected_k': 5},
    {'name': 'G4_Parabola_Convex_Wide_Eps', 'pw_linear_fx': [(i, i * (i-10)) for i in range(11)], 'epsilon': 5.0, 'expected_k': 1},
    {'name': 'G4_Parabola_Convex_Tight_Eps', 'pw_linear_fx': [(i, i * (i-10)) for i in range(11)], 'epsilon': 1.0, 'expected_k': 5},
    {'name': 'G4_Sine_Wave_One_Period_Wide_Eps', 'pw_linear_fx': [(i, 5.0 * (i % 2)) for i in range(11)], 'epsilon': 2.5, 'expected_k': 3},
    {'name': 'G4_Sine_Wave_One_Period_Tight_Eps', 'pw_linear_fx': [(i, 5.0 * (i % 2)) for i in range(11)], 'epsilon': 1.0, 'expected_k': 5},
    {'name': 'G4_Exponential_Curve', 'pw_linear_fx': [(i, 2**i) for i in range(6)], 'epsilon': 5.0, 'expected_k': 2},
    {'name': 'G4_Step_Function_Jump', 'pw_linear_fx': [(0,0), (0.99,0), (1,10), (2,10)], 'epsilon': 1.0, 'expected_k': 2},
    {'name': 'G4_High_Frequency_Noise', 'pw_linear_fx': [(i, (-1)**i * 0.4) for i in range(11)], 'epsilon': 0.39, 'expected_k': 10},
    {'name': 'G4_Slow_Start_Fast_Finish', 'pw_linear_fx': [(i, i**2) for i in range(6)], 'epsilon': 5.0, 'expected_k': 2},

    # ----------------------------------------------------------------------
    # Group 5: Data Point Distribution (10 cases)
    # Unevenly spaced x-values, data density changes.
    # ----------------------------------------------------------------------
    {'name': 'G5_Uneven_X_High_Density_Start', 'pw_linear_fx': [(i/10.0, 0.0) for i in range(11)] + [(i, 0.0) for i in range(2, 11)], 'epsilon': 0.001, 'expected_k': 1},
    {'name': 'G5_Uneven_X_Low_Density_Start', 'pw_linear_fx': [(i*2, 0.0) for i in range(6)] + [(10+i/10.0, 0.0) for i in range(11)], 'epsilon': 0.001, 'expected_k': 1},
    {'name': 'G5_Uneven_X_Dense_Center_Bend', 'pw_linear_fx': [(0,0), (0.1, 0.5), (0.2, 0.0), (10, 0.0)], 'epsilon': 0.4, 'expected_k': 2},
    {'name': 'G5_Uneven_X_Sparse_Center_Bend', 'pw_linear_fx': [(0,0), (5, 0.5), (10, 0.0)], 'epsilon': 0.4, 'expected_k': 2},
    {'name': 'G5_X_Change_Effect_1', 'pw_linear_fx': [(0,0), (1,0.5), (2,0), (10,0)], 'epsilon': 0.4, 'expected_k': 2},
    {'name': 'G5_X_Change_Effect_2', 'pw_linear_fx': [(0,0), (5,0.5), (6,0), (10,0)], 'epsilon': 0.4, 'expected_k': 2},
    {'name': 'G5_X_Change_Effect_3_Tighter_Eps', 'pw_linear_fx': [(0,0), (1,0.5), (2,0), (10,0)], 'epsilon': 0.49, 'expected_k': 2},
    {'name': 'G5_X_Change_Effect_4_Boundary', 'pw_linear_fx': [(0,0), (1, 0.5001), (2,0), (10,0)], 'epsilon': 0.5, 'expected_k': 3},
    {'name': 'G5_Exponential_X_Slope_Change', 'pw_linear_fx': [(2**i, 0.0) for i in range(6)] + [(30, 1.0)], 'epsilon': 0.5, 'expected_k': 2},
    {'name': 'G5_Zero_X_Spacing_Check', 'pw_linear_fx': [(0,0), (0,0), (1,1)], 'epsilon': 0.1, 'expected_k': 1}, # Should handle duplicate x-values gracefully

    # ----------------------------------------------------------------------
    # Group 6: Extreme Values and Floating Point Precision (10 cases)
    # Large/small coordinates and epsilon, testing numerical stability.
    # ----------------------------------------------------------------------
    {'name': 'G6_Large_Y_Values_Small_Eps', 'pw_linear_fx': [(i, 10000.0) for i in range(5)], 'epsilon': 0.0001, 'expected_k': 1},
    {'name': 'G6_Small_Y_Values_Small_Eps', 'pw_linear_fx': [(i, 1e-6) for i in range(5)], 'epsilon': 1e-7, 'expected_k': 1},
    {'name': 'G6_Large_X_Values', 'pw_linear_fx': [(i * 10000.0, 0.0) for i in range(5)], 'epsilon': 0.01, 'expected_k': 1},
    {'name': 'G6_Zero_Epsilon_Exact_Fit', 'pw_linear_fx': [(0,0), (1,1), (2,2)], 'epsilon': 0.0, 'expected_k': 1},
    {'name': 'G6_Zero_Epsilon_Requires_All_Segments', 'pw_linear_fx': [(0,0), (1,1), (2,0)], 'epsilon': 0.0, 'expected_k': 2},
    {'name': 'G6_Very_Small_Eps_High_K', 'pw_linear_fx': [(i, (i%2) * 0.1) for i in range(21)], 'epsilon': 1e-10, 'expected_k': 20},
    {'name': 'G6_Very_Large_Eps_Low_K', 'pw_linear_fx': [(i, 10.0 * (i%2)) for i in range(21)], 'epsilon': 5.0, 'expected_k': 5},
    {'name': 'G6_Floating_Point_Error_Check_1', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.3333333333333333), (2.0, 0.0)], 'epsilon': 0.3333333333333333, 'expected_k': 1}, # Should fit
    {'name': 'G6_Floating_Point_Error_Check_2', 'pw_linear_fx': [(0.0, 0.0), (1.0, 0.3333333333333334), (2.0, 0.0)], 'epsilon': 0.3333333333333333, 'expected_k': 2}, # Should not fit
    {'name': 'G6_Negative_Coordinates_Check', 'pw_linear_fx': [(-2, 2), (-1, -1), (0, 0), (1, -1), (2, 2)], 'epsilon': 1.0, 'expected_k': 3},

    # ----------------------------------------------------------------------
    # Group 7: Complex & Mixed Edge Cases (10 cases)
    # Combining multiple challenges (e.g., uneven x, greedy trap, boundary $\varepsilon$).
    # ----------------------------------------------------------------------
    {'name': 'G7_Complex_Greedy_Trap_Uneven', 'pw_linear_fx': [(0,0), (1,0.5), (1.1,0.0), (2,0.5), (10,0)], 'epsilon': 0.45, 'expected_k': 4},
    {'name': 'G7_Alternating_Slopes_Boundary', 'pw_linear_fx': [(i, (-1)**i * 0.5) for i in range(11)], 'epsilon': 0.5, 'expected_k': 1},
    {'name': 'G7_Alternating_Slopes_Exceed', 'pw_linear_fx': [(i, (-1)**i * 0.5) for i in range(11)], 'epsilon': 0.499, 'expected_k': 10},
    {'name': 'G7_Two_Sharp_Turns_Same_Eps', 'pw_linear_fx': [(0,0), (1,1), (2,0), (3,0), (4,1), (5,0)], 'epsilon': 0.1, 'expected_k': 4},
    {'name': 'G7_Flat_Region_Separating_Curves', 'pw_linear_fx': [(0,0), (1,0.5), (2,0), (10,0), (11,0.5), (12,0)], 'epsilon': 0.49, 'expected_k': 4},
    {'name': 'G7_Minimal_Difference_Max_Points', 'pw_linear_fx': [(i, 0.01 * (i % 2)) for i in range(21)], 'epsilon': 0.001, 'expected_k': 10},
    {'name': 'G7_Long_Run_Followed_by_Trap', 'pw_linear_fx': [(i, 0.0) for i in range(10)] + [(11, 0.5), (12, 0.0)], 'epsilon': 0.49, 'expected_k': 2},
    {'name': 'G7_Tight_Fit_With_Long_Extension', 'pw_linear_fx': [(0,0), (1, 0.4), (2, 0.0), (20, 0.0)], 'epsilon': 0.4, 'expected_k': 1},
    {'name': 'G7_Large_Dataset_Optimal_K_Known', 'pw_linear_fx': [(i, 0.0) for i in range(50)] + [(51, 1.0), (52, 0.0)], 'epsilon': 0.1, 'expected_k': 3},
    {'name': 'G7_Alternating_Tight_Wide_Fit', 'pw_linear_fx': [(i, (i%4)/4.0) for i in range(21)], 'epsilon': 0.2, 'expected_k': 10},
]
