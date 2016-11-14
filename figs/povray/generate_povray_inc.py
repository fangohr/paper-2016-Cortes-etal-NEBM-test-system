"""

Script to generate INC files for Povray

We load 3 states: skyrmion, ferromagnetic, and sk destruction
from the NEBM npys output folder (assumed 239 steps)

the .inc files include a row of data for every spin, with
the sentence:
    spins(x, y, z, mx, my, mz, r, g, b)

i.e. positions, spin orientations, and rgb colours with the
mz magnitude (colours are normalised, [0,1])


Created by David Cortes on Fri 09 Oct 2015
University of Southampton
Contact to: d.i.cortes@soton.ac.uk

"""

# FIDIMAG Simulation imports:
from fidimag.atomistic import Sim
from fidimag.common import CuboidMesh
from os import listdir
import re

# Import physical constants from fidimag
import fidimag.common.constant as const


# Numpy utilities
import numpy as np
from matplotlib import cm

mesh = CuboidMesh(nx=21, ny=21,
                  dx=0.5, dy=0.5,
                  unit_length=1e-9,
                  periodicity=(True, True, False)
                  )

# Initialise a simulation object and load the skyrmion
# or ferromagnetic states
sim = Sim(mesh, name='neb_21x21-spins_fm-sk_atomic')

# Get the directories inside the npys folder from the NEBM simulation
# and sort them by the last number (after the k magnitude)
npys_folder = '../../npys/'
files_list = listdir(npys_folder)
files_list = sorted(files_list,
                    key=lambda f: int(re.search(r'(?<=k1e4_)[0-9]+', f).group(0))
                    )

# Use the largest step from the files directory
sk = npys_folder + files_list[-1] + '/image_000000.npy'
fm = npys_folder + files_list[-1] + '/image_000017.npy'
ds = npys_folder + files_list[-1] + '/image_000011.npy'

states = {'skyrmion': sk, 'ferromagnetic': fm, 'destruction': ds}

for key in states.keys():
    sim.set_m(np.load(states[key]))

    # Append coordinates and spin orientations
    data = np.append(np.array(sim.mesh.coordinates),
                     sim.spin.reshape(-1, 3), axis=1)

    # Get the colormap using the last row, i.e. mz
    # We must normalise it: [-1, 1]  --> [0, 1]
    # So we sum by 1 to shift the scale and divide by 1 - (-1) = 2
    mz_rgb = cm.RdYlBu((data[:, -1] + 1) * 0.5)
    # Remove last column with alpha values
    mz_rgb = mz_rgb[:, :-1]

    data = np.append(data, mz_rgb, axis=1)

    # Open the output file
    _file = open('{}.inc'.format(key), 'w')

    # Now we write the spins(...) sentence for every spin
    for row in data:
        line = 'spins('
        # We transform the axes according to POVRAY's coordinate
        # system: x --> -z, y --> x, x --> y
        line += '{},{},{},'.format(-row[2], row[1], row[0])
        # The same for the spins orientations
        # but somehow, Povray's left handed system gives the wrong directions
        # if we do not correct the sign of the Y, Z components (?)
        line += '{},{},{},'.format(-row[5], -row[4], -row[3])

        # Now the colours
        for num in row[6:]:
            line += '{},'.format(num)

        # Remove last comma and close brackets
        line = line[:-1]
        line += ')\n'

        _file.write(line)

    _file.close()
