# Time Delay Simulation

This repository contains a MATLAB delay simulation model and a Python package with equivalent behavior.

## Repository Structure

- `MATLAB/DelaySimulation.m`: original MATLAB simulation script
- `MATLAB/CorrDelay.m`: MATLAB correlation-related helper script
- `MATLAB/DelaySimulation.slx`: Simulink model
- `timedelay/`: importable Python package that implements the simulation and plotting
- `Python/DelaySimulation.py`: original standalone script, left intact

## What the Simulation Does

The simulation generates `Npack = 5000` packet send times over a simulation horizon (`Stime = 120` seconds), then applies one of two delay models selected at runtime:

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
python -m timedelay l
```

- Pass `l` for long-distance delay model
- Pass `s` for short-distance delay model

You can also adjust the simulation size:

```bash
python -m timedelay l --npack 1000 --stime 60 --seed 42
```

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
- The plotting logic now lives in `timedelay.plot_simulation(...)`, and the data generation is exposed through `timedelay.simulate(...)`.

## Python API

```python
from timedelay import plot_simulation, simulate

result = simulate("l", seed=123)
fig, axes = plot_simulation(result)
```

## License
[LICENSE](LICENSE)
