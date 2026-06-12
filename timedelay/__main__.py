from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from .simulation import plot_simulation, simulate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the time delay simulation.")
    parser.add_argument("model", choices=["l", "s"], help="Delay model: l for long distance, s for short distance")
    parser.add_argument("--npack", type=int, default=5000, help="Number of packets to simulate")
    parser.add_argument("--stime", type=float, default=120.0, help="Simulation time horizon in seconds")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible runs")
    parser.add_argument("--no-csv", action="store_true", help="Skip writing delay_data.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = simulate(
        args.model,
        n_packets=args.npack,
        simulation_time=args.stime,
        seed=args.seed,
        output_csv=None if args.no_csv else "delay_data.csv",
    )
    plot_simulation(result)
    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())