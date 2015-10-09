"""

NEB Simulation for a toy model made of Fe-like atoms arranged in a square
lattice. This system is described by 21 x 21 spins with interfacial DMI

A very strong magnetic field B is applied perpendicular to the sample, which
stabilises a metastable skyrmion. The ground state is the uniform state.

Magnetic parameters:
    J = 10 meV      Exchange
    D = 6 meV       DMI
    B = 25 T        Magnetic Field
    mu_s = 2 mu_B   Magnetic moment


Created by David Cortes on Fri 02 Oct 2015
University of Southampton
Contact to: d.i.cortes@soton.ac.uk

"""

# FIDIMAG Simulation imports:
from fidimag.atomistic import Sim
from fidimag.atomistic import FDMesh
from fidimag.atomistic import DMI
from fidimag.atomistic import UniformExchange
from fidimag.atomistic import Zeeman
from fidimag.atomistic import Constant

# Import physical constants from fidimag
const = Constant()

# Import the NEB method
from fidimag.common.neb_cartesian import NEB_Sundials

# Numpy utilities
import numpy as np

# For timing purposes ---------------------------------------------------------
# We will produce a file to check how long the NEB simulation takes to finish

import time


class Timer:

    def __init__(self):
        self.t1 = 0
        self.t2 = 0

    def start(self):
        self.t1 = time.clock()

    def end(self):
        self.t2 = time.clock()

    def interval(self):
        return self.t2 - self.t1
# -----------------------------------------------------------------------------


# MESH ------------------------------------------------------------------------
# This is a 21x21 spins in a square lattice with a lattice constant of 5
# angstrom and PBCs
mesh = FDMesh(nx=21, ny=21,
              dx=0.5, dy=0.5,
              unit_length=1e-9,
              pbc='2d'
              )
# -----------------------------------------------------------------------------


# NEBM Simulation Function ----------------------------------------------------

def relax_neb(k, maxst, simname, init_im, interp, save_every=10000):
    """
    Execute a simulation with the NEBM algorithm of the FIDIMAG code
    Here we use always the 21x21 Spins Mesh and don't vary the material
    parameters. This can be changed adding those parameters as variables.

    We create a new Simulation object every time this function is called
    since it can be modified in the process

    k           :: NEBM spring constant

    maxst       :: Maximum number of iterations

    simname     :: Simulation name. VTK and NPY files are saved in folders
                   starting with the 'simname' string

    init_im     :: A list with magnetisation states (usually loaded from
                   NPY files or from a function) that will be used as
                   images in the energy band, e.g. for two states:
                        [np.load('skyrmion.npy'), np.load('ferromagnet.npy')]

    interp      :: Array or list with the numbers of interpolations between
                   every pair of the 'init_im' list. The length of this array
                   is: len(__init_im) - 1

    save_every  :: Save VTK and NPY files every 'save_every' number of steps

    """

    # Initialise a simulation object and set the default gamma for the LLG
    # equation
    sim = Sim(mesh, name='neb_21x21-spins_fm-sk_atomic')
    sim.gamma = const.gamma

    # Magnetisation in units of Bohr's magneton
    sim.mu_s = 2 * const.mu_B

    # Interactions ------------------------------------------------------------

    # Exchange constant in Joules: E = Sum J_{ij} S_i S_j
    J = (10.0 / 1.) * const.meV
    exch = UniformExchange(J)
    sim.add(exch)

    # DMI constant in Joules: E = Sum D_{ij} S_i x S_j
    D = (6 / 1.) * const.meV
    dmi = DMI(D, dmi_type='interfacial')
    sim.add(dmi)

    # Zeeman field in Tesla:
    sim.add(Zeeman((0, 0, 25.)))

    # -------------------------------------------------------------------------

    # Set the initial images from the list
    init_images = init_im

    # The number of interpolations must always be
    # equal to 'the number of initial states specified', minus one.
    interpolations = interp

    # Start a NEB simulation passing the Simulation object and all the NEB
    # parameters
    neb = NEB_Sundials(sim,
                       init_images,
                       interpolations=interpolations,
                       spring=k,
                       name=simname,
                       )

    # Finally start the energy band relaxation
    neb.relax(max_steps=maxst,
              save_vtk_steps=save_every,
              save_npy_steps=save_every,
              stopping_dmdt=1e-2
              )

# -----------------------------------------------------------------------------


# #############################################################################
# SIMULATION ##################################################################
# #############################################################################

# Here we load the skyrmion and the ferromagnetic state
# Get the latest relaxed state:
import os
# Sort according to the number in the npy files,
# Files are named: m_156.npy, for example
# We will use the last element from these lists
basedir_sk = 'relaxation/relax_sk_npys/'
basedir_fm = 'relaxation/relax_fm_npys/'

sk_npys = sorted(os.listdir(basedir_sk),
                 key=lambda x: int(x[2:-4]))
fm_npys = sorted(os.listdir(basedir_fm),
                 key=lambda x: int(x[2:-4]))

print basedir_sk + sk_npys[-1]

# listdir only gives the file names so we add the base directory
init_im = [np.load(basedir_sk + sk_npys[-1]),
           np.load(basedir_fm + fm_npys[-1])]

# We specify 16 interpolations in between the sk and fm, so we have
# something like (as initial state)
#
# Energy                ...
#   ^
#   |          2    , - ~ ~ ~ - ,  15
#   |           O '               O ,
#   |     1   ,                       ,  16
#   |        O                         O
#   |       ,                           ,
#   |       O                           O
#   |      SK                           FM
#   ________________________
#   Distance
#
# So we will have 18 images in total in the Energy Band
interp = [16]

# Define different NEBM spring constant k for multiple simulations
# Here we only use 1e10
krange = ['1e10']

# Timing variables (we will save it to a file)
f = open('timings.dat', 'w')
t = Timer()

# We will do a simulation for every k
for k in krange:
    print 'Computing for k = {}'.format(k)
    # Initialise the timer
    t.start()

    # Relax the NEBM simulation passing the appropriate parameters
    relax_neb(float(k), 2000,
              'neb_21x21-spins_fm-sk_atomic_k{}'.format(k),
              init_im,
              interp,
              save_every=200,
              )
    # Finish the timer
    t.end()
    f.write('k{} {} \n'.format(k, t.interval()))
    f.flush()
f.close()
