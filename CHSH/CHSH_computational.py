import numpy as np
import matplotlib.pyplot as plt

def projection_matrix(theta1, theta2):
    """
    Construct the 4x4 projection matrix for polarizers at angles theta1 and theta2.
    """
    # init a vector of cos/sin of theta1 
    v1 = np.array([np.cos(theta1), np.sin(theta1)])
    # calulate the outer product of v1
    v1_outer = np.outer(v1, v1.conj())

    # do the same for theta2
    v2 = np.array([np.cos(theta2), np.sin(theta2)])
    v2_outer = np.outer(v2, v2.conj())

    return np.kron(v1_outer, v2_outer)

def coincidence_probability(state_or_rho, theta1, theta2):
    """
    Calculate the coincidence probability for a given state (vector or density matrix)
    and polarizer angles theta1 and theta2.
    """
    P = projection_matrix(theta1, theta2)
    
    if state_or_rho.ndim == 1:
        # for state vector, the probability is <psi|P|psi>
        probability = np.vdot(state_or_rho, P.dot(state_or_rho)).real

    elif state_or_rho.ndim == 2:  
        # for density matrix the probability is Tr[rho P]
        probability = np.trace(state_or_rho.dot(P)).real

    else:
        raise ValueError("Input must be either a state vector or a density matrix.")
    
    return probability

def expectation_value(state_or_rho, theta1, theta2):
    """
    Calculate the expectation value E(theta1, theta2) for a given state or density matrix.
    """
    P_plusplus = coincidence_probability(state_or_rho, theta1, theta2) 
    P_plusminus = coincidence_probability(state_or_rho, theta1, theta2 + np.pi/2)
    P_minusplus = coincidence_probability(state_or_rho, theta1 + np.pi/2, theta2)
    P_minusminus = coincidence_probability(state_or_rho, theta1 + np.pi/2, theta2 + np.pi/2)
    
    # E(theta1, theta2) from coincidence counts
    E = (P_plusplus + P_minusminus - P_plusminus - P_minusplus) / (P_plusplus + P_minusminus + P_plusminus + P_minusplus)
    return E

def calculate_chsh_s(state_or_rho):
    """
    Calculate the S value for the CHSH inequality using a given state or density matrix.
    """
    # the angles that we used in the lab
    angles = [
        (0,   +np.pi/8),   # E(A0,B0)
        (0,   -np.pi/8),   # E(A0,B1)
        (np.pi/4, +np.pi/8),  # E(A1,B0)
        (np.pi/4, -np.pi/8)   # E(A1,B1)
    ]

    # Calculate the expectation values for each angle pair
    E_values = [expectation_value(state_or_rho, theta1, theta2) for (theta1, theta2) in angles]

    S = E_values[0] + E_values[1] + E_values[2] - E_values[3]
    
    return S


def plot_alpha_sweep():
    measured_qued = 2.43
    qued_err = 0.12
    measured_ibm = 2.60
    ibm_err = 0.003
    S_min = np.sqrt(2)

    alphas = np.linspace(0, 1, 201)
    S_vals = []

    for alpha in alphas:
        rho_real = 0.5 * np.array([
            [1,      0, 0, alpha],
            [0,      0, 0,     0],
            [0,      0, 0,     0],
            [alpha,  0, 0,     1]
        ])
        S_vals.append(calculate_chsh_s(rho_real))

    plt.figure()
    plt.plot(alphas, S_vals, lw=2, zorder=4, label=r'$S(\alpha)$')
    plt.xlabel(r'$\alpha$ (coherence parameter)')
    plt.ylabel(r'$S(\alpha)$')
    plt.xlim(0, 1)
    plt.ylim(1, 3)
    plt.title('CHSH $S$ vs. Purity Parameter $\\alpha$')
    plt.axhline(2, color='k', ls='--', label=r'Classical bound $S=2$', zorder=3)
    plt.axhline(2*np.sqrt(2),
                color='k',
                ls=':',
                label=r'Quantum max $2\sqrt{2}$',
                zorder=3)

    # shaded error bands
    plt.fill_between(alphas,
                     measured_qued - qued_err,
                     measured_qued + qued_err,
                     color='r',
                     alpha=0.2,
                     label=f'quED ±{qued_err}',
                     zorder=1)
    plt.axhline(measured_qued,
                color='r',
                ls='-.',
                label=f'quED measurement $S={measured_qued}$',
                zorder=5)

    plt.fill_between(alphas,
                     measured_ibm - ibm_err,
                     measured_ibm + ibm_err,
                     color='tab:purple',
                     alpha=0.15,
                     label=f'IBM ±{ibm_err}',
                     zorder=1)
    plt.axhline(measured_ibm,
                color='tab:purple',
                ls='-.',
                label=f'IBM measurement $S={measured_ibm}$',
                zorder=5)
    plt.axhline(S_min,
                color='g',
                ls='-.',
                label=r'S min value $\sqrt{2}$',
                zorder=5)

    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_beta_sweep():
    """
    Plot CHSH S-value as a function of the amplitude imbalance parameter beta
    for the pure state sqrt(beta)|HH> + sqrt(1-beta)|VV>.
    """
    measured_qued = 2.43
    qued_err = 0.12
    measured_ibm = 2.60
    ibm_err = 0.003
    S_min = np.sqrt(2)


    betas = np.linspace(0, 1, 201)
    S_vals = []

    for beta in betas:
        # State vector: sqrt(beta)|HH> + sqrt(1-beta)|VV>
        psi_beta = np.array([
            np.sqrt(beta),  # |HH>
            0.0,            # |HV>
            0.0,            # |VH>
            np.sqrt(1 - beta)  # |VV>
        ])
        S_vals.append(calculate_chsh_s(psi_beta))

    plt.figure()
    plt.plot(betas, S_vals, lw=2, zorder=4, label=r'$S(\beta)$')
    plt.xlabel(r'$\beta$ (amplitude imbalance parameter)')
    plt.ylabel(r'$S(\beta)$')
    plt.title('CHSH $S$ vs. Amplitude Imbalance Parameter $\\beta$')
    plt.axhline(2, color='k', ls='--', label=r'Classical bound $S=2$', zorder=3)
    plt.axhline(2*np.sqrt(2),
                color='k',
                ls=':',
                label=r'Quantum max $2\sqrt{2}$',
                zorder=3)

    # shaded error bands
    plt.fill_between(betas,
                     measured_qued - qued_err,
                     measured_qued + qued_err,
                     color='r',
                     alpha=0.2,
                     label=f'quED ±{qued_err}',
                     zorder=1)
    plt.axhline(measured_qued,
                color='r',
                ls='-.',
                label=f'quED measurement $S={measured_qued}$',
                zorder=5)

    plt.fill_between(betas,
                     measured_ibm - ibm_err,
                     measured_ibm + ibm_err,
                     color='tab:purple',
                     alpha=0.15,
                     label=f'IBM ±{ibm_err}',
                     zorder=1)
    plt.axhline(measured_ibm,
                color='tab:purple',
                ls='-.',
                label=f'IBM measurement $S={measured_ibm}$',
                zorder=5)
    
    plt.axhline(S_min,
                color='g',
                ls='-.',
                label=r'S min value $\sqrt{2}$',
                zorder=5)


    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(1, 3)

    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_polarizer_error(state_or_rho=None,
                         max_error_deg=2.0, step_deg=0.1, n_samples=2000,
                         seed=None):
    """
    Plot mean CHSH S vs polarizer error magnitude (degrees), showing only:
      - the mean S curve
      - the horizontal line for 2*sqrt(2)

    Each Monte Carlo trial applies independent systematic offsets for Alice and Bob
    sampled uniformly from [-delta, +delta] where delta = error magnitude (radians).
    """
    measured_qued = 2.43
    qued_err = 0.12
    measured_ibm = 2.60
    ibm_err = 0.003

    if seed is not None:
        np.random.seed(seed)

    if state_or_rho is None:
        phi_plus = 1/np.sqrt(2) * np.array([1, 0, 0, 1])
        state_or_rho = np.outer(phi_plus, phi_plus.conj())

    base_angles = [
        (0.0,   +np.pi/8),   # E(A0,B0)
        (0.0,   -np.pi/8),   # E(A0,B1)
        (np.pi/4, +np.pi/8),  # E(A1,B0)
        (np.pi/4, -np.pi/8)   # E(A1,B1)
    ]

    error_degs = np.arange(0.0, max_error_deg + 1e-12, step_deg)
    means = []

    for ed in error_degs:
        delta = np.deg2rad(ed)
        S_samples = np.zeros(n_samples)

        offsets_A = np.random.uniform(-delta, delta, size=n_samples)
        offsets_B = np.random.uniform(-delta, delta, size=n_samples)

        for i in range(n_samples):
            offA = offsets_A[i]
            offB = offsets_B[i]

            E_vals = []
            for (thetaA, thetaB) in base_angles:
                E_vals.append(expectation_value(state_or_rho, thetaA + offA, thetaB + offB))

            S_samples[i] = E_vals[0] + E_vals[1] + E_vals[2] - E_vals[3]

        means.append(S_samples.mean())

    means = np.array(means)

    plt.figure(figsize=(7,4.5))
    plt.plot(error_degs, means, marker='o', lw=1.5, label=r'$\langle S\rangle$')
    plt.xlabel('Polarizer error magnitude (degrees)')
    plt.ylabel('CHSH $S$')
    plt.title('Mean CHSH $S$ vs Polarizer Misalignment')
    plt.axhline(2*np.sqrt(2),
                color='k',
                ls=':',
                label=r'Quantum max $2\sqrt{2}$')
    # quED shaded error band and central line
    plt.fill_between(error_degs,
                     measured_qued - qued_err,
                     measured_qued + qued_err,
                     color='r',
                     alpha=0.2,
                     label=f'quED ±{qued_err}',
                     zorder=1)
    plt.axhline(measured_qued,
                color='r',
                ls='-.',
                label=f'quED measurement $S={measured_qued}$',
                zorder=5)

    # IBM shaded error band and central line
    plt.fill_between(error_degs,
                     measured_ibm - ibm_err,
                     measured_ibm + ibm_err,
                     color='tab:purple',
                     alpha=0.15,
                     label=f'IBM ±{ibm_err}',
                     zorder=1)
    plt.axhline(measured_ibm,
                color='tab:purple',
                ls='-.',
                label=f'IBM measurement $S={measured_ibm}$',
                zorder=5)
    plt.legend()
    ax = plt.gca()
    ax.legend(loc='lower left')   # or plt.legend(loc='lower left')

    plt.xlim(0, max_error_deg)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # Define the maximally entangled Bell state |phi+> = (|HH> + |VV>)/sqrt(2)
    phi_plus = 1/np.sqrt(2) * np.array([1, 0, 0, 1])

    # Define the density matrix for |phi+>
    rho_phi_plus = np.outer(phi_plus, phi_plus.conj())

    # Calculate the S value for the pure state vector
    S_pure = calculate_chsh_s(phi_plus)
    print(f"S value (pure state): {S_pure:.10f}")

    # Calculate the S value for the density matrix
    S_mixed = calculate_chsh_s(rho_phi_plus)
    print(f"S value (density matrix): {S_mixed:.10f}")

    plot_alpha_sweep()
    
    plot_beta_sweep()

    # use the Bell state density matrix already defined in your __main__
    plot_polarizer_error(state_or_rho=rho_phi_plus, max_error_deg=21.0, step_deg=0.1, n_samples=2000, seed=111)

