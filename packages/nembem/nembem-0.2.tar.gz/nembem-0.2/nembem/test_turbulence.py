

import subprocess
import numpy as np

# Define input parameters to Mann turbulence simulation
lines = ['3',
         '3',
         '4096',
         '32',
         '32',
         '6142.5',
         '180',
         '180',
         'land',
         '15',
         '119',
         '0.05',
         '0',
         '-5',
         'sim1.bin',
         'sim2.bin',
         'sim3.bin']

# Write input parameters to file
with open('input/turbulence/inputEx3.INP', 'w') as f:
    f.write('\n'.join(lines))

# Run turbulence simulation
subprocess.call(['input/turbulence/windsimu.exe', 'input/turbulence/inputEx3.INP'])


# def load(filename, N = (32, 32)):
#     """Load mann turbulence box

#     Parameters
#     ----------
#     filename : str
#         Filename of turbulence box
#     N : tuple, (ny,nz) or (nx,ny,nz)
#         Number of grid points

#     Returns
#     -------
#     turbulence_box : nd_array

#     Examples
#     --------
#     >>> u = load('turb_u.dat')
#     """
#     data = np.fromfile(filename, np.dtype('<f'), -1)
#     if len(N) == 2:
#         ny, nz = N
#         nx = len(data) / (ny * nz)
#         assert nx == int(nx), "Size of turbulence box (%d) does not match ny x nz (%d), nx=%.2f" % (
#             len(data), ny * nz, nx)
#         nx = int(nx)
#     else:
#         nx, ny, nz = N
#         assert len(data) == nx * ny * \
#             nz, "Size of turbulence box (%d) does not match nx x ny x nz (%d)" % (len(data), nx * ny * nz)
#     return data.reshape(nx, ny * nz)


# # Reading in parameters for the turbulent box
# turbulence_parameters = np.genfromtxt('input/turbulence/inputEx3.INP')

# # Dimensionerne skal være ints. Disse er punkterne i boxen
# n1, n2, n3 = turbulence_parameters[2:5].astype(int)

# # Disse er længdedimensionerne af boxen
# Lx, Ly, Lz = turbulence_parameters[5:8]

# # Middel wind speed fra boxen. Skal matche middel wind speed fra scriptet her
# # Hvis disse to ikke ens, gives der en fejlmeddelelse
# umean = turbulence_parameters[9]
# # if not np.isclose(umean, V_0):
# #     raise ValueError('The mean wind speed umean from the turbulent box does not match the V_0 in this script')

# deltay = Ly/(n2-1)
# deltax = Lx/(n1-1)
# deltaz = Lz/(n3-1)
# deltat = deltax/umean

# # Ligesom for middelvinden skal der være overensstemmelse mellem deltat fra turbulent
# # box og delta_t fra dette script
# # deltat_threshold = 3 # digits (Denne threshold er sat for at undgå ValueError ved f.eks. 0.16666 og 0.16666666666666666)
# # if not np.isclose(round(deltat,deltat_threshold),round(delta_t,deltat_threshold)):
# #     raise ValueError('Mismatch between deltat from turbulent box and delta_t in this script')

# # Load in the files and reshape them into 3D
# # turbulence er fordi filen ligger i en undermappe der hedder turbulence
# u = load('input/turbulence/sim1.bin',  N=(n1, n2, n3))

# ushp = np.reshape(u, (n1, n2, n3))

# # Vi ændrer på dimensionerne: fra box til aflvering
# # x bliver til z (tid)
# # z bliver til x
# # y bliver til y

# X_turb = np.arange(0,n2)*deltaz + (H - (n2-1)*deltaz/2) # Height
# Y_turb = np.arange(0,n3)*deltay - ((n3-1) * deltay)/2 # Width
# Z_turb = np.arange(0,n1)*deltax # Depth (Time)