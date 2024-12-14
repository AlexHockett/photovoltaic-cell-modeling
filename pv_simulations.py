import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt

constants = sp.physical_constants
A = 0


def Voc(T, J0, Jsc):
    """
    Calculates open circuit voltage at a given temperature, diode saturation current, and short circuit current
    :param T: temperature (K)
    :param J0: diode saturation current density (A / m^2)
    :param Jsc: short circuit current density (A / m^2)
    :return: open circuit voltage (V)
    """
    k = constants['Boltzmann constant'][0]
    q = constants['elementary charge'][0]
    Jl = Jsc
    return ((T * k) / q) * np.log(Jl/J0 + 1)


def Jsc(I, w1, w2, Eg, m):
    """
    Calculates short curcuit current density at a given light intensity and wavelength spectrum. The spectrum is input as a range of wavelengths.
    :param I: intensity (W / m^2)
    :param w1: shortest wavelength (nm)
    :param w2: longest wavelength (nm)
    :param Eg: band gap (eV)
    :param m: spectral response slope (A / W * nm)
    :return: short circuit current density (A / m^2)
    """
    if A == 0:
        responsivity = Responsivity(w1, w2, Eg, m)
    else:
        responsivity = R
    return I * responsivity


def Responsivity(w1, w2, Eg, m):
    """
    Calculates spectral response of a photovoltaic cell at a given wavelength.
    :param w1: shortest wavelength (nm)
    :param w2: longest wavelength (nm)
    :param Eg: band gap (eV)
    :param m: spectral response slope (A / W * nm)
    :return: spectral response (A / W)
    """
    h = constants['Planck constant'][0]
    c = constants['speed of light in vacuum'][0]
    Eg /= 6.241509 * 10 ** 18  # convert to J
    Eg = (h * c) / (Eg)  # convert to m
    Eg *= 10 ** 9  # convert to nm
    if (w1 > Eg or w2 < 300):
        return 0
    elif (w2 > Eg):
        return ((Eg - w1) * (m * w1 + m * Eg)) / (2 * (w2 - w1))
    elif (w1 < 300):
        return ((w2 - 300) * (m * w2 + m * 300)) / (2 * (w2 - w1))
    else:
        return ((w1 + w2) * m) / 2
    

def J0(T, Eg):
    """
    Calculates diode saturation current density at a given temperature and band gap
    :param T: temperature (K)
    :param Eg: band gap (eV)
    :return: diode saturation current density (A / m^2)
    """
    k = constants['Boltzmann constant'][0]
    Eg = Eg / (6.241509 * 10**18)  # convert to J
    A = 2.95 * 10**5  # material independent constant (A / cm^2)
    J0 = A * np.exp((-Eg) / (k * T))  # A / cm^2
    J0 *= 10**4  # convert to A / m^2
    return J0


def FF(Voc, T):
    """
    Calculates fill factor of a photovoltaic cell at a given open circuit voltage and temperature.
    :param Voc: open circuit voltage (V)
    :param T: temperature (K)
    :return: Fill Factor
    """
    k = constants['Boltzmann constant'][0]
    q = constants['elementary charge'][0]
    v = Voc * (q / (k * T))  # normalized voltage
    return (v - (np.log(v + 0.72))) / (v + 1)


def Power(T, Eg, I, w1, w2, m):
    """
    Calculates power of a photovoltaic solar call at a given temperature, band gap, light intensity, and wavelength spectrum
    :param T: temperature (K)
    :param Eg: band gap (eV)
    :param I: intensity (W / m^2)
    :param w1: shortest wavelength (nm)
    :param w2: longest wavelength (nm)
    :param m: spectral response slope (A / W * nm)
    :return: power (W / m^2)
    """
    J0_value = J0(T, Eg)
    Jsc_value = Jsc(I, w1, w2, Eg, m)
    Voc_value = Voc(T, J0_value, Jsc_value)
    F_value = FF(Voc_value, T)
    return F_value * Voc_value * Jsc_value


def Efficiency(T, Eg, I, w1, w2, m):
    """
    Calculates efficiency percentage of a photovoltaic cell at a given temperature, band gap, light intensity, and wavelength spectrum 
    :param T: temperature (K)
    :param Eg: band gap (eV)
    :param I: intensity (W / m^2)
    :param w1: shortest wavelength (nm)
    :param w2: longest wavelength (nm)
    :return: efficiency percentage
    """
    power = Power(T, Eg, I, w1, w2, m)
    return power / I



# power vs efficiency graphs at varying wavelength:

plt.figure(1)
T = np.linspace(250, 315, 100)

P1 = Power(T, 1.12, 800, 300, 550, 0.00082)
plt.plot(T, P1, 'r')

P2 = Power(T, 1.12, 800, 550, 800, 0.00082)
plt.plot(T, P2, 'b')

P3 = Power(T, 1.12, 800, 800, 1050, 0.00082)
plt.plot(T, P3, 'g')

P4 = Power(T, 1.12, 800, 1050, 1300, 0.00082)
plt.plot(T, P4, 'y')

plt.xlabel("Temperature (K)")
plt.ylabel("Power (W / m^2)")

# power vs intensity at varying temperature:

plt.figure(2)
I = np.linspace(350, 1400, 100)

P1 = Power(300, 1.12, I, 300, 700, 0.00082)
plt.plot(I, P1, 'r')

plt.xlabel("Intensity (W / m^2)")
plt.ylabel("Power (W / m^2)")

# efficiency vs intensity at varying temperature:

plt.figure(3)
I = np.linspace(100, 1800, 100)

E1 = Efficiency(315, 1.12, I, 300, 700, 0.00082)
plt.plot(I, E1, 'r')

E2 = Efficiency(300, 1.12, I, 300, 700, 0.00082)
plt.plot(I, E2, 'y')

E3 = Efficiency(285, 1.12, I, 300, 700, 0.00082)
plt.plot(I, E3, 'b')

E4 = Efficiency(270, 1.12, I, 300, 700, 0.00082)
plt.plot(I, E4, 'g')

plt.xlabel("Intensity (W / m^2)")
plt.ylabel("Efficiency")

# power vs band gap at varying wavelengths (at higher incoming light energies, you want a higher band gap)

plt.figure(4)
Eg = np.linspace(0.5, 4.5, 200)
R = np.zeros(200)
A = 1

for i in range(len(R)):
    R[i] = Responsivity(300, 500, Eg[i], 0.00082)
P1 = Power(300, Eg, 800, 300, 500, 0.00082)
plt.plot(Eg, P1, 'm')

for i in range(len(R)):
    R[i] = Responsivity(500, 700, Eg[i], 0.00082)
P2 = Power(300, Eg, 800, 500, 700, 0.00082)
plt.plot(Eg, P2, 'g')

for i in range(len(R)):
    R[i] = Responsivity(700, 900, Eg[i], 0.00082)
P3 = Power(300, Eg, 800, 700, 900, 0.00082)
plt.plot(Eg, P3, 'r')

plt.xlabel("Band gap (eV)")
plt.ylabel("Power (W / m^2)")

# power vs wavelength

plt.figure(5)
W = np.linspace(400, 1100, 100)
R = np.zeros(100)

for i in range(len(R)):
    R[i] = Responsivity(W[i] - 200, W[i], 1.5, 0.00072)
P1 = Power(300, 1.5, 800, W - 200, W, 0.00072)
plt.plot(W, P1, 'y')

for i in range(len(R)):
    R[i] = Responsivity(W[i] - 200, W[i], 1.5, 0.0008)
P2 = Power(300, 1.5, 800, W - 200, W, 0.0008)
plt.plot(W, P2, 'g')

for i in range(len(R)):
    R[i] = Responsivity(W[i] - 200, W[i], 1.5, 0.00088)
P3 = Power(300, 1.5, 800, W - 200, W, 0.00088)
plt.plot(W, P3, 'r')

plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (W / m^2)")

plt.show()
