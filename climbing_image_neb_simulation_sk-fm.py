from __future__ import print_function

"""

Climbing image NEBM (CI-NEBM) Simulation for a toy model made of Fe-like atoms
arranged in a square lattice. This system is described by 21 x 21 spins with
interfacial DMI

To observe the effect of the climbing technique, we firstly relax the band with
a very small stopping criteria for the algorithm, generating a poor resolution
around the saddle point. Consequently, we take the relaxed band as initial
state for the climbing image algorithm, using the 12th image as the climbing
image, since it has the largest energy. We recommend running the
generate_GIF_climbing_image.py script after the simulation finishes to see the
effect of the CI-NEBM.

Magnetic parameters:
    J = 10 meV      Exchange
    D = 6 meV       DMI
    B = 25 T        Magnetic Field
    mu_s = 2 mu_B   Magnetic moment


Updated by David Cortes on Tue 08 Nov 2016
University of Southampton
Contact to: d.i.cortes@soton.ac.uk

"""


# FIDIMAG Simulation imports:
from fidimag.atomistic import Sim
from fidimag.common import CuboidMesh
from fidimag.atomistic import DMI
from fidimag.atomistic import UniformExchange
from fidimag.atomistic import Zeeman
# Import physical constants from fidimag
import fidimag.common.constant as const

# Import the NEB method
from fidimag.common.nebm_geodesic import NEBM_Geodesic

# Numpy utilities
import numpy as np

# MESH ------------------------------------------------------------------------
# This is a 21x21 spins in a square lattice with a lattice constant of 5
# angstrom and PBCs
mesh = CuboidMesh(nx=21, ny=21,
                  dx=0.5, dy=0.5,
                  unit_length=1e-9,
                  periodicity=(True, True, False)
                  )
# -----------------------------------------------------------------------------


# NEBM Simulation Function ----------------------------------------------------

def relax_neb(k, maxst, simname, init_im, interp,
              save_every=10000, stopping_dYdt=0.01,
              climbing_image=None
              ):
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
    neb = NEBM_Geodesic(sim,
                        init_images,
                        interpolations=interpolations,
                        spring_constant=k,
                        name=simname,
                        climbing_image=climbing_image
                        )

    # Finally start the energy band relaxation
    neb.relax(max_iterations=maxst,
              save_vtks_every=save_every,
              save_npys_every=save_every,
              stopping_dYdt=stopping_dYdt
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

print(basedir_sk + sk_npys[-1])

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

# Over-relax the band with a very small dYdt
relax_neb(1e4, 2000,
          'relax_neb_21x21-spins_fm-sk_atomic_k1e4',
          init_im,
          interp,
          stopping_dYdt=1e-5
          )


# Now we set the relaxed band as initial state
init_im = [np.load('npys/relax_neb_21x21-spins_fm-sk_atomic_k1e4_169/'
                   'image_{:06}.npy'.format(i)) for i in range(18)]

# The 12th image is the one with largest energy, we make it climb up
# in energy along the band
relax_neb(1e4, 2000,
          'climbing_image_neb_21x21-spins_fm-sk_atomic_k1e4',
          init_im,
          None,
          stopping_dYdt=1e-5,
          climbing_image=12
          )
