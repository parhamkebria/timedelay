# Time Delay Simulation

This repository contains a MATLAB delay simulation model and a Python port with equivalent behavior.

## Repository Structure

- `MATLAB/DelaySimulation.m`: original MATLAB simulation script
- `MATLAB/CorrDelay.m`: MATLAB correlation-related helper script
- `MATLAB/DelaySimulation.slx`: Simulink model
- `Python/DelaySimulation.py`: Python version of `DelaySimulation.m`

## What the Simulation Does

The simulation generates `Npack = 5000` packet send times over a simulation horizon (`Stime = 100` seconds), then applies one of two delay models selected at runtime:

- **Long distance (`L`)**: Normal delay with
  - mean = `1.50`
  - std = `0.50`
- **Short distance (`S`)**: Shifted exponential delay with
  - minimum offset = `0.001`
  - scale (`lambda`) = `0.002`

It then:

- Builds a pulse train representation (`nT`, `V`) for sent/received packet events
- Plots packet timing and zoomed pulse behavior
- Plots delay histograms
- Fits and overlays a probability distribution
- Exposes a MATLAB-style `SimDelay` structure in Python:
  - `SimDelay["time"]`
  - `SimDelay["signals"]["values"]`

## Python Requirements

- Python 3.9+
- Packages:
  - `numpy`
  - `matplotlib`
  - `scipy`

Install dependencies:

```bash
python -m pip install numpy matplotlib scipy
```

## Run the Python Script

From the repository root:

```bash
python DelaySimulation.py
```

When prompted:

- Enter `L` for long-distance delay model
- Enter `S` for short-distance delay model

Two figure windows will be generated to match the MATLAB workflow.

## Run the MATLAB Script

In MATLAB, open and run:

- `MATLAB/DelaySimulation.m`

Or from the MATLAB command window (with repo root as working directory):

```matlab
run('MATLAB/DelaySimulation.m')
```

## Notes

- The simulation is stochastic (randomized send times and delays), so each run produces different traces and histograms.
- The Python implementation mirrors the original script logic closely rather than optimizing for vectorized style.

## License
[LICENSE](LICENSE)
