from timedelay import plot_simulation, simulate

result = simulate("l", seed=123)
fig, axes = plot_simulation(result, show=True, save="long_distance_plot.pdf")