import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# File path
file_path = 'HOM/HOM_measurements.xlsx'

# Read the data
df = pd.read_excel(file_path)

# Assign columns
x = df['position_mm'].values * 1e3  # convert mm to µm
y = df['col5'].values               # coincidence counts

# HOM dip model
def hom_dip(position, C_off, A, x0, sigma):
    return C_off - A * np.exp(-((position - x0)**2) / (2 * sigma**2))

# Initial guesses
n_edge = max(1, int(len(x) * 0.1))
C_off_guess = np.mean(np.concatenate([y[:n_edge], y[-n_edge:]]))
min_index = np.argmin(y)
A_guess = C_off_guess - y[min_index]
x0_guess = x[min_index]
sigma_guess = (x.max() - x.min()) / 10
p0 = [C_off_guess, A_guess, x0_guess, sigma_guess]

# Curve fitting with Levenberg-Marquardt and increased maxfev
popt, _ = curve_fit(hom_dip, x, y, p0=p0, method='lm', maxfev=5000)
C_off, A, x0, sigma = popt

# Derived metrics
C_dip = C_off - A
visibility = (C_off - C_dip) / C_off
fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma  # µm
coherence_time = (fwhm * 1e-6) / 3e8        # seconds

# Plot
plt.figure()
plt.plot(x, y, 'o', label='Data')
x_fit = np.linspace(x.min(), x.max(), 500)
plt.plot(x_fit, hom_dip(x_fit, *popt), label='Fit')
plt.xlabel('Position (µm)')
plt.ylabel('Coincidence Counts')
plt.title('HOM Dip')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Results
print(f"Offset coincidence rate (C_off): {C_off:.2f}")
print(f"Dip minimum (C_dip): {C_dip:.2f}")
print(f"Visibility: {visibility:.3f}")
print(f"FWHM: {fwhm:.2f} µm")
print(f"Coherence time: {coherence_time*1e15:.2f} fs")
