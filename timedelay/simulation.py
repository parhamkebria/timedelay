from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.stats import expon, norm

DelayMode = Literal["l", "L", "s", "S"]

DEVELOPER_NAME = "Parham Kebria"


def announce_developer() -> None:
    print(f"Time Delay Simulation module developed by {DEVELOPER_NAME}")


@dataclass(slots=True)
class SimulationResult:
    model: str
    stime: float
    npack: int
    send_time: np.ndarray
    simulated_delay: np.ndarray
    pulse_time: np.ndarray
    pulse_values: np.ndarray
    min_delay: float
    mean_delay: float
    std_delay: float

    @property
    def simdelay(self) -> dict[str, dict[str, np.ndarray]]:
        return {
            "time": self.send_time.reshape(-1, 1),
            "signals": {"values": self.simulated_delay.reshape(-1, 1)},
        }


def _normalize_model(model: DelayMode) -> str:
    value = model.lower()
    if value not in {"l", "s"}:
        raise ValueError("model must be 'l' or 's'")
    return value


def _generate_send_time(npack: int, stime: float, rng: np.random.Generator) -> np.ndarray:
    population = np.arange(1, int(1.5 * npack) + 1)
    perm = rng.choice(population, size=npack, replace=False)
    return np.sort(perm) * stime / (1.5 * npack)


def _sample_delay(model: str, npack: int, rng: np.random.Generator) -> np.ndarray:
    if model == "l":
        return 1.50 + 0.50 * rng.standard_normal(npack)
    return 0.001 + rng.exponential(scale=0.002, size=npack)


def _build_pulse_train(send_time: np.ndarray, delay: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pulse_time = [0.0]
    pulse_values = [0.0]

    for send, sampled_delay in zip(send_time, delay):
        pulse_time.extend([send, send + 0.00001, send + sampled_delay, send + sampled_delay + 0.00001])
        pulse_values.extend([0.0, 1.0, 1.0, 0.0])

    return np.array(pulse_time), np.array(pulse_values)


def _delay_stats(model: str, simulated_delay: np.ndarray) -> tuple[float, float, float]:
    minimum = float(np.min(simulated_delay))
    if model == "l":
        mean_delay = float(np.mean(simulated_delay))
        std_delay = float(np.std(simulated_delay, ddof=1))
    else:
        centered = simulated_delay - minimum
        mean_delay = float(np.mean(centered))
        std_delay = float(np.std(centered, ddof=1))
    return minimum, mean_delay, std_delay


def delay(
    model: DelayMode,
    *,
    n_packets: int = 5000,
    simulation_time: float = 120.0,
    seed: int | None = None,
    output_csv: str | Path | None = "delay_data.csv",
) -> SimulationResult:
    """Run the delay simulation and return the generated data."""

    announce_developer()

    normalized_model = _normalize_model(model)
    rng = np.random.default_rng(seed)

    send_time = _generate_send_time(n_packets, simulation_time, rng)
    simulated_delay = _sample_delay(normalized_model, n_packets, rng)
    pulse_time, pulse_values = _build_pulse_train(send_time, simulated_delay)
    min_delay, mean_delay, std_delay = _delay_stats(normalized_model, simulated_delay)

    if output_csv is not None:
        delay_data = np.column_stack((send_time, simulated_delay))
        np.savetxt(
            output_csv,
            delay_data,
            delimiter=",",
            fmt="%.3f",
            header="send_time,simulated_delay",
            comments="",
        )

    return SimulationResult(
        model=normalized_model,
        stime=simulation_time,
        npack=n_packets,
        send_time=send_time,
        simulated_delay=simulated_delay,
        pulse_time=pulse_time,
        pulse_values=pulse_values,
        min_delay=min_delay,
        mean_delay=mean_delay,
        std_delay=std_delay,
    )


def plot(
    result: SimulationResult,
    *,
    zoom_start: int = 999,
    zoom_stop: int = 1100,
    show: bool = False,
    save: str | Path | None = None,
) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes, plt.Axes]]:
    """Plot the pulse train and delay distributions for a simulation result."""

    fig, (ax_signal, ax_dist, ax_dist2) = plt.subplots(3, 1, num=1, clear=True, figsize=(6, 8))

    ax_signal.plot(result.pulse_time, result.pulse_values, color="tab:blue")
    ax_signal.set_xlabel("Time (s)")
    ax_signal.set_ylabel("Signal level")
    ax_signal.set_xlim(0, result.pulse_time[-1])
    ax_signal.set_ylim(-0.5, 5)

    zoom_start = max(0, min(zoom_start, len(result.pulse_time) - 1))
    zoom_stop = max(zoom_start + 1, min(zoom_stop, len(result.pulse_time)))
    zoom_x = result.pulse_time[zoom_start:zoom_stop]
    zoom_y = result.pulse_values[zoom_start:zoom_stop]

    ax_signal.plot(zoom_x, zoom_y, color="red", linewidth=1.5)
    ax_zoom = ax_signal.inset_axes([0.3, 0.55, 0.65, 0.4])
    ax_zoom.plot(zoom_x, zoom_y, color="red")
    ax_zoom.set_xlabel("Time (s)", fontsize=8)
    ax_zoom.set_ylabel("Signal", fontsize=8)
    ax_zoom.set_xlim(zoom_x[0], zoom_x[-1])
    ax_zoom.set_ylim(0.0, 1)
    ax_signal.indicate_inset_zoom(ax_zoom, edgecolor="red")

    ax_dist.hist(result.simulated_delay, bins=100, density=True, color="tab:blue", alpha=0.55)
    ax_dist.set_xlabel("Delay (s)")
    ax_dist.set_ylabel("Density")

    measured_line = Line2D([], [], color="tab:blue", linewidth=2)
    fit_line = Line2D([], [], color="red", linewidth=2)

    if result.model == "l":
        mu, sigma = norm.fit(result.simulated_delay)
        x = np.linspace(np.min(result.simulated_delay), np.max(result.simulated_delay), 400)
        fit_pdf = norm.pdf(x, loc=mu, scale=sigma)
        ax_dist.plot(x, fit_pdf, color="red", linewidth=2)
    else:
        data = result.simulated_delay - result.min_delay
        mu = float(np.mean(data))
        sigma = float(np.std(data, ddof=1))
        x = np.linspace(0, np.max(data), 400)
        fit_pdf = expon.pdf(x, scale=mu)
        ax_dist.plot(result.min_delay + x, fit_pdf, color="red", linewidth=2)

    ax_dist.legend(
        title=f"μ={mu:.3f}, σ={sigma:.3f}",
        handles=[measured_line, fit_line],
        labels=["Measured", "Distribution fit"],
        frameon=False,
    )

    _, _, patches = ax_dist2.hist(result.simulated_delay, bins=100)
    for patch in patches:
        patch.set_facecolor((0, 0, 1))
        patch.set_edgecolor("b")

    nelement_h, edges_h = np.histogram(result.simulated_delay, bins=100)
    centres_h = 0.5 * (edges_h[:-1] + edges_h[1:])
    ax_dist2.plot(centres_h, nelement_h / 1, "r", linewidth=2)
    ax_dist2.set_xlabel("Delay (s)")
    ax_dist2.set_ylabel("Count")
    ax_dist2.legend(
        title=f"μ={mu:.3f}, σ={sigma:.3f}",
        handles=[patches[0], ax_dist2.lines[-1]],
        labels=["Frequency", "Distribution fit"],
        frameon=False,
    )

    plt.tight_layout()
    if show:
        plt.show()
    if save is not None:
        fig.savefig(save)
    return fig, (ax_signal, ax_dist, ax_dist2)