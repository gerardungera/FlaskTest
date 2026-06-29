import numpy as np

def calculate_julia(width, height, max_iterations, c_real, c_imag):
    # Cálculo directo con NumPy en tiempo real
    x = np.linspace(-1.8, 1.8, width)
    y = np.linspace(-1.8, 1.8, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = complex(c_real, c_imag)
    
    output = np.zeros(Z.shape, dtype=int)
    mask = np.full(Z.shape, True, dtype=bool)
    
    for i in range(max_iterations):
        Z[mask] = Z[mask] * Z[mask] + C
        diverged = np.abs(Z) > 2
        escaping_now = diverged & mask
        output[escaping_now] = i
        mask[diverged] = False
        
    return output