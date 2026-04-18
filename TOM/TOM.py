import numpy as np
import pandas as pd
from itertools import product

# 1. Load data
df = pd.read_excel('TOM_measurements.xlsx', sheet_name=0)

# fix the multi‐block “Unnamed: 0” for first‐qubit outcome labels
df['s1_outcome'] = df['Unnamed: 0'].ffill()
df['s2_outcome'] = df['Unnamed: 1']
df = df.rename(columns={'C': 'counts'})

# 2. Map outcome labels → basis & binary index
basis_map = {
    'H': ('Z', 0), 'V': ('Z', 1),
    'P': ('X', 0), 'M': ('X', 1),
    'R': ('Y', 0), 'L': ('Y', 1),
}

df['b1'], df['i1'] = zip(*df['s1_outcome'].map(basis_map))
df['b2'], df['i2'] = zip(*df['s2_outcome'].map(basis_map))

# 3. Compute normalized frequencies f_{i1,i2}^{b1,b2}
#    and then T_{b1,b2} = ∑_{i1,i2} (-1)^(i1+i2) f
T = { (p,q): 0.0 for p,q in product(['X','Y','Z'],['X','Y','Z']) }
for (b1,b2), group in df.groupby(['b1','b2']):
    total = group['counts'].sum()
    freqs = group['counts'] / total
    T[(b1,b2)] = sum(((-1)**(i1+i2))*f 
                     for (_, i1, i2, f) in zip(
                         group.index, group['i1'], group['i2'], freqs
                       ))

# 4. Build ρ = (1/4) Σ_{μ,ν=0..3} T_{μν} σ_μ⊗σ_ν
#    with σ_0 = I, and T_{00}=1; T_{0j}=T_{i0}=0 for i,j>0
sigma = {
    0: np.array([[1,0],[0,1]], dtype=complex),
    1: np.array([[0,1],[1,0]], dtype=complex),  # σ_x
    2: np.array([[0,-1j],[1j,0]], dtype=complex),  # σ_y
    3: np.array([[1,0],[0,-1]], dtype=complex),  # σ_z
}
# map basis letter → Pauli index
pauli_idx = {'X':1, 'Y':2, 'Z':3}

rho = np.zeros((4,4), dtype=complex)
for mu in range(4):
    for nu in range(4):
        if mu==0 and nu==0:
            coeff = 1.0
        elif mu==0 or nu==0:
            coeff = 0.0
        else:
            b1 = {1:'X',2:'Y',3:'Z'}[mu]
            b2 = {1:'X',2:'Y',3:'Z'}[nu]
            coeff = T[(b1,b2)]
        rho += coeff * np.kron(sigma[mu], sigma[nu])
rho /= 4

# 5. Compute purity and fidelity to |φ+⟩
purity = np.real_if_close(np.trace(rho @ rho))

phi_plus = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
fidelity = np.real_if_close((phi_plus.conj().T @ rho @ phi_plus).item())

# Output
print("Reconstructed density matrix ρ:\n", rho)
print("\nPurity Tr(ρ²) =", purity)
print("Fidelity ⟨φ+|ρ|φ+⟩ =", fidelity)
