import matplotlib.pyplot as plt

def plot_pc_case(pc_fx, epsilon, cand_fx=None, opt_fx=None,
                 title="Piecewise Constant Approximation (Failed Case)"):
    """
    pc_fx   : given function, format [(-inf, inf), (x1,y1), ..., (x_n,y_n), (x_{n+1}, inf)]
    cand_fx : candidate output, format [(x1,c1), ..., (x_K,c_K), (x_{end}, inf)]
    opt_fx  : optimal output, same format as cand_fx
    epsilon : tolerance value
    """
    # plt.style.use("dark_background")
    plt.figure(figsize=(10, 8))

    # --- Given function (blue solid) + ±epsilon band (light gray) ---
    for i in range(1, len(pc_fx) - 1):
        x_start = pc_fx[i][0]
        x_end   = pc_fx[i+1][0]
        y_val   = pc_fx[i][1]

        # epsilon band
        plt.fill_between([x_start, x_end],
                         [y_val - epsilon, y_val - epsilon],
                         [y_val + epsilon, y_val + epsilon],
                         color="gray", alpha=0.3,
                         label=fr"$\pm \epsilon$ band ($\epsilon={epsilon}$)" if i == 1 else "")

        # given function line
        plt.hlines(y_val, x_start, x_end, colors="blue", linewidth=5, label="Given Function" if i == 1 else "")



    # --- Optimal function (red dashed) ---
    if opt_fx:
        for i in range(len(opt_fx) - 1):
            x_start = opt_fx[i][0]
            x_end   = opt_fx[i+1][0]
            y_val   = opt_fx[i][1]
            plt.hlines(y_val, x_start, x_end, colors="#07f49e",
                       linewidth=3, label="OPT" if i == 0 else "")

        # --- Candidate function (green dash-dot) ---
    if cand_fx:
        for i in range(len(cand_fx) - 1):
            x_start = cand_fx[i][0]
            x_end = cand_fx[i + 1][0]
            y_val = cand_fx[i][1]
            plt.hlines(y_val, x_start, x_end, colors="magenta", linestyles="dashed",
                       linewidth=2, label="Candidate" if i == 0 else "")

    # --- Formatting ---
    plt.xlabel("x", fontsize=18)
    plt.ylabel("f(x)", fontsize=18)
    plt.tick_params(labelsize=18)
    plt.title(title, fontsize=18)
    plt.legend(loc="best", fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
