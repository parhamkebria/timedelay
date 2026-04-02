import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon
from matplotlib.lines import Line2D

def main():

    Stime = 120  # Sec
    Npack = 5000  # Packet

    population = np.arange(1, int(1.5 * Npack) + 1)
    perm = np.random.choice(population, size=Npack, replace=False)
    pack_send_time = np.sort(perm) * Stime / (1.5 * Npack)

    user_input = "0"
    while user_input not in ("l", "L", "s", "S"):
        user_input = input("L: Long Distance | S: Short Distance: \t")

    if user_input in ("l", "L"):
        mn = 1.50
        sd = 0.50
        simdelay = mn + sd * np.random.randn(Npack)
    else:
        Min = 0.001
        lam = 0.002
        simdelay = Min + np.random.exponential(scale=lam, size=Npack)

    k = 0
    nT = [0.0]
    V = [0.0]

    for i in range(Npack):
        k += 1
        V.append(0.0)
        nT.append(pack_send_time[i])

        k += 1
        V.append(1.0)
        nT.append(pack_send_time[i] + 0.00001)

        k += 1
        V.append(1.0)
        nT.append(pack_send_time[i] + simdelay[i])

        k += 1
        V.append(0.0)
        nT.append(pack_send_time[i] + simdelay[i] + 0.00001)

    nT = np.array(nT)
    V = np.array(V)

    fig1, (ax_signal, ax_dist, ax_dist2) = plt.subplots(3, 1, num=1, clear=True, figsize=(6, 8))
    ax_signal.plot(nT, V, color="tab:blue")
    # ax_signal.set_title("5000 packets with random send time and random time delay")
    ax_signal.set_xlabel("Time (s)")
    ax_signal.set_ylabel("Signal level")
    ax_signal.set_xlim(0, nT[-1])
    ax_signal.set_ylim(-.5, 5)

    zoom_x = nT[999:1100]
    zoom_y = V[999:1100]
    ax_signal.plot(zoom_x, zoom_y, color="red", linewidth=1.5)

    # Show the selected red segment as an inset zoom inside the main signal plot.
    ax_zoom = ax_signal.inset_axes([0.3, 0.55, 0.65, 0.4])
    ax_zoom.plot(zoom_x, zoom_y, color="red")
    ax_zoom.set_xlabel("Time (s)", fontsize=8)
    ax_zoom.set_ylabel("Signal", fontsize=8)
    ax_zoom.set_xlim(nT[999], nT[1099])
    ax_zoom.set_ylim(0.0, 1)
    # ax_zoom.set_title("Zoomed segment", fontsize=9)
    ax_signal.indicate_inset_zoom(ax_zoom, edgecolor="red")

    ax_dist.hist(simdelay, bins=100, density=True, color="tab:blue", alpha=0.55)
    # ax_dist.set_title("Frequency distribution and distribution fit")
    ax_dist.set_xlabel("Delay (s)")
    ax_dist.set_ylabel("Density")

    if user_input in ("l", "L"):
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay)
        stdDealy = np.std(simdelay, ddof=1)
    else:
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay - MinDelay)
        stdDealy = np.std(simdelay - MinDelay, ddof=1)

    measured_line = Line2D([], [], color="tab:blue", linewidth=2)
    fit_line = Line2D([], [], color="red", linewidth=2)
    stats_line = Line2D([], [], linestyle="None")

    if user_input in ("l", "L"):
        mu, sigma = norm.fit(simdelay)
        x = np.linspace(np.min(simdelay), np.max(simdelay), 400)
        fit_pdf = norm.pdf(x, loc=mu, scale=sigma)
        ax_dist.plot(x, fit_pdf, color="red", linewidth=2)
        ax_dist.legend(
            title = f"\u03BC={mu:.3f}, \u03C3={sigma:.3f}",
            handles=[measured_line, fit_line],
            labels=["Measured", "Distribution fit"],
            frameon=False
        )
    else:
        data = simdelay - MinDelay
        mu = np.mean(data)
        sigma = np.std(data, ddof=1)
        x = np.linspace(0, np.max(data), 400)
        fit_pdf = expon.pdf(x, scale=mu)
        ax_dist.plot(MinDelay + x, fit_pdf, color="red", linewidth=2)
        ax_dist.legend(
            title = f"\u03BC={mu:.3f}, \u03C3={sigma:.3f}",
            handles=[measured_line, fit_line],
            labels=["Measured", "Distribution fit"],
            frameon=False
        )

    nelement2, edges2, patches = ax_dist2.hist(simdelay, bins=100)
    for p in patches:
        p.set_facecolor((0, 0, 1))
        p.set_edgecolor("b")

    nelement_h, edges_h = np.histogram(simdelay, bins=100)
    centres_h = 0.5 * (edges_h[:-1] + edges_h[1:])
    fit_line = ax_dist2.plot(centres_h, nelement_h / 1, "r", linewidth=2)
    _ = np.sum(nelement_h)

    if user_input in ("l", "L"):
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay)
        stdDealy = np.std(simdelay, ddof=1)
    else:
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay - MinDelay)
        stdDealy = np.std(simdelay - MinDelay, ddof=1)

    ax_dist2.set_xlabel("Delay (s)")
    ax_dist2.set_ylabel("Count")
    ax_dist2.legend(
        title = f"\u03BC={mu:.3f}, \u03C3={sigma:.3f}",
        handles=[patches[0], fit_line[0]],
        labels=["Frequency", "Distribution fit"],
        frameon=False
    )

    SimDelay = {
        "time": pack_send_time.reshape(-1, 1),
        "signals": {"values": simdelay.reshape(-1, 1)},
    }

    delay_data = np.column_stack((pack_send_time, simdelay))
    np.savetxt(
        "delay_data.csv",
        delay_data,
        delimiter=",",
        fmt="%.3f",
        header="send_time,simulated_delay",
        comments="",
    )

    # Keep variables available in interactive sessions
    _ = (MinDelay, MeanDelay, stdDealy, SimDelay)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()