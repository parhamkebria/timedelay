import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon

def main():

    Stime = 100  # Sec
    Npack = 5000  # Packet

    population = np.arange(1, int(1.5 * Npack) + 1)
    perm = np.random.choice(population, size=Npack, replace=False)
    pack_send_time = np.sort(perm) * Stime / (1.5 * Npack)

    user_input = "0"
    while user_input not in ("l", "L", "s", "S"):
        user_input = input("L: Long Distance | S: Short Distance: \t")

    if user_input in ("l", "L"):
        mn = 1.52
        sd = 0.38
        simdelay = mn + sd * np.random.randn(Npack)
    else:
        Min = 0.002
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

    plt.figure(1)
    plt.subplot(2, 2, 1)
    plt.plot(nT, V)
    plt.title("5000 packets with random send time and random delay time")
    plt.axis([0, nT[-1], -2, 5])
    plt.plot(nT[999:1100], V[999:1100], "r")

    plt.subplot(2, 2, 2)
    plt.plot(nT[999:1100], V[999:1100], "r")
    plt.title("zoom on the read segment/delay is the width of each pulse")
    plt.axis([nT[999], nT[1099], -2, 5])

    plt.subplot(2, 2, 3)
    plt.hist(simdelay, bins=100)
    plt.title("Frequency distribution")
    nelement, edges = np.histogram(simdelay, bins=100)
    centres = 0.5 * (edges[:-1] + edges[1:])
    _ = np.sum(nelement)

    if user_input in ("l", "L"):
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay)
        stdDealy = np.std(simdelay, ddof=1)
    else:
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay - MinDelay)
        stdDealy = np.std(simdelay - MinDelay, ddof=1)

    plt.subplot(2, 2, 4)
    plt.plot(centres, nelement / 1)

    if user_input in ("l", "L"):
        mu, sigma = norm.fit(simdelay)
        x = np.linspace(0.005, 0.015, 100)
        dx = 0.010 / 100
        Pdf = norm.pdf(x, loc=mu, scale=sigma) * dx
        Pdf = Pdf / np.sum(Pdf)
        _ = np.sum(Pdf)
        plt.plot(x, Pdf, linewidth=2)
        plt.legend(
            [
                f"Measuredmean ={mu} std={sigma}",
                f"Distribution Fit mean ={mu} std={sigma}",
            ]
        )
    else:
        data = simdelay - MinDelay
        mu = np.mean(data)
        sigma = np.std(data, ddof=1)
        x = np.linspace(0, 0.020, 100)
        dx = 0.020 / 100
        Pdf = expon.pdf(x, scale=mu) * dx / 1.039
        Pdf = Pdf / np.sum(Pdf)
        _ = np.sum(Pdf)
        plt.plot(MinDelay + x, Pdf, linewidth=2)
        plt.legend([f"Measuredmean ={mu}", f"Distribution Fit mean ={mu}"])

    plt.title("Distribution fit")

    plt.figure(2)
    plt.subplot(1, 3, 3)
    nelement2, edges2, patches = plt.hist(simdelay, bins=100)
    for p in patches:
        p.set_facecolor((0, 0, 1))
        p.set_edgecolor("b")

    nelement_h, edges_h = np.histogram(simdelay, bins=100)
    centres_h = 0.5 * (edges_h[:-1] + edges_h[1:])
    _ = np.sum(nelement_h)

    if user_input in ("l", "L"):
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay)
        stdDealy = np.std(simdelay, ddof=1)
    else:
        MinDelay = np.min(simdelay)
        MeanDelay = np.mean(simdelay - MinDelay)
        stdDealy = np.std(simdelay - MinDelay, ddof=1)

    plt.plot(centres_h, nelement_h / 1, "r", linewidth=2)
    plt.legend(
        [
            "Frequency distribution",
            f"Distribution mean ={mu} std={sigma}",
        ]
    )

    plt.subplot(1, 3, (1, 2))

    # MATLAB struct-style outputs
    SimDelay = {
        "time": pack_send_time.reshape(-1, 1),
        "signals": {"values": simdelay.reshape(-1, 1)},
    }

    delay_data = np.column_stack((pack_send_time, simdelay))
    np.savetxt(
        "delay_data.csv",
        delay_data,
        delimiter=",",
        header="send_time,simulated_delay",
        comments="",
    )

    # Keep variables available in interactive sessions
    _ = (MinDelay, MeanDelay, stdDealy, SimDelay)

    # plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()