# paper-2015-Cortes-etal

## NEBM Testing System

This repository contains a script to simulate a spin system proposed by
Bessarab et al. [1] using the Nudged Elastic Band Method, which
was implemented in our finite differences
code [Fidimag](https://github.com/fangohr/fidimag) and published
in Cortés-Ortuño et al. [2]

The system is a test model of 21 by 21 magnetic spins, with an interfacial
Dzyaloshinskii-Moriya interaction (DMI), where the skyrmion is a metastable
state under a strong external magnetic field.  We describe this system using an
atomistic formalism with the following magnetic parameters:

```
    J = 10 meV      Exchange
    D = 6 meV       DMI
    B = 25 T        Magnetic Field
    mu_s = 2 mu_B   Magnetic moment

```

## Scripts

To run these simulations we need a working copy of Fidimag.
The first step is to relax the skyrmionic and ferromagnetic states,
which is done in the `relaxation` folder. Then we use the
magnetisation files to start the NEBM. We can do this using
the `Makefile` in a terminal:

```bash
    make relaxation
    make nebm
    make plot
```

The last step is optional and generates a PDF file with the final energy band,
with the annotated images, this requires `Matplotlib`.  The magnetisation
profile files are saved in the `npys/` folder and for visualisation, VTK files
are saved in the `vtks/` directory. Every folder name indicates at the end the
step of the NEBM and inside there is a file for every image of the energy band,
i.e. 17 files.

## Figures

We provide an IPython notebook with the snapshots of the energy band images.

In addition, we can use the output files to have a general view of the process
where the skyrmion is destroyed:

![](https://github.com/fangohr/paper-2015-Cortes-etal/blob/master/figs/sk-fm_NEBM.jpg "NEBM Final Step")


[1] Bessarab, P. F., Uzdin, V. M. & Jonsson, H. *Method for finding mechanism
and activation energy of magnetic transitions, applied to skyrmion and
antivortex annihilation*.  Computer Physics Communications **196**, 1–37 (2015).
URL http://linkinghub.elsevier.com/retrieve/pii/S0010465515002696

[2] Cortés-Ortuño, D. et al, ... Nature(?)
