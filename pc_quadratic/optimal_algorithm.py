import matlab
import matlab.engine
import numpy as np

class MATLABOptimalAlgorithm:
    def __init__(self):
        # Start MATLAB engine
        self.eng = matlab.engine.start_matlab()
        # Add path to your MATLAB functions
        self.eng.addpath(r'C:/Users/kanab/OneDrive/Desktop/closest-convex-function-approximation-main\code-baron\03-1d_plq_variable_number_of_pieces', nargout=0)

    def __call__(self, f, pieces, epsilon):
        try:
            # Convert numpy arrays to MATLAB types
            f_matlab = matlab.double(f.tolist())
            pieces_matlab = matlab.double(
                [[p if abs(p) != np.inf else (float('inf') if p > 0 else float('-inf')) for p in pieces]]
            )
            # Call the first MATLAB function
            # rho, new_pieces, _ = self.eng.inf_norm_nearest_convex_function_variable_pieces_of_fixed_num(
            #     f_matlab, pieces_matlab, len(pieces) - 1, nargout=3)

            # Call the second MATLAB function
            # g, g_pieces, num_pieces = self.eng.decrease_pieces_of_convex_function(
            #     rho, new_pieces, float(epsilon),
            #     self.eng.str2func('inf_norm_get_nearest_convex_function_with_variable_pieces_of_given_num'),
            #     nargout=3)
            g, g_pieces, num_pieces = self.eng.approximate_plq_fx(f_matlab, pieces_matlab, float(epsilon),nargout=3)

            # Convert MATLAB outputs back to Python types
            g_np = np.array(g._data).reshape(g.size).T
            g_pieces_np = np.array(g_pieces._data).flatten().tolist()
            num_pieces = int(num_pieces)

            return g_np, g_pieces_np, num_pieces

        except Exception as e:
            print(f"Error in MATLAB function call: {str(e)}")
            raise

    def __del__(self):
        # Clean up MATLAB engine
        if hasattr(self, 'eng'):
            self.eng.quit()
