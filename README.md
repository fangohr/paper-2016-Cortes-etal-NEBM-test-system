[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.167870.svg)](https://doi.org/10.5281/zenodo.167870)


# paper-2015-Cortes-etal

## NEBM Testing System

This repository contains a script to simulate a spin system proposed by
Bessarab et al. [1] using the Nudged Elastic Band Method, which was implemented
in our finite differences code
[Fidimag](http://computationalmodelling.github.io/fidimag/).

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

To run these simulations we need a working copy of Fidimag.  The first step is
to relax the skyrmionic and ferromagnetic states, which is done in the
`relaxation` folder. Then we use the magnetisation files to start the NEBM. We
can do this using the `Makefile` in a terminal:

```bash
    make relaxation
    make nebm
    make plot
```
 
The magnetisation profile files are saved in the `npys/` folder and for
visualisation, VTK files are saved in the `vtks/` directory. Every folder name
indicates at the end the step of the NEBM and inside there is a file for every
image of the energy band, i.e. 17 files.  The NEBM simulation also produce a
file with data from a cubic interpolation of the band which is used in the
plotting script.

The `plot` step is optional and generates a PDF file with the final energy
band, with the annotated images and interpolated band. This requires
`Matplotlib`.  

### Climbing Image NEBM

We also provide a script to test the Climbing Image NEBM (CI-NEBM). For this
case, we firstly over-relax the band as in the NEBM, in order to have a poor
resolution at the saddle point region, and then we apply the climbing image
technique to the 12th image of the band. This image will then climb up in
energy and sit at the top of the saddle point. To observe this effect we
created a script to generate an animation, by plotting every step of the
climbing image process. We can then use the images to generate a GIF or a
video. Thus, to run the CI-NEBM and generate the images we do:

```bash
    make climbing
    make plot_climbing
```

## Figures

We provide an IPython notebook with the snapshots of the energy band images.

In addition, we can use the output files to have a general view of the process
where the skyrmion is destroyed:

![](https://github.com/fangohr/paper-2015-Cortes-etal/blob/master/figs/sk-fm_NEBM.jpg "NEBM Final Step")


[1] Bessarab, P. F., Uzdin, V. M. & Jonsson, H. *Method for finding mechanism
and activation energy of magnetic transitions, applied to skyrmion and
antivortex annihilation*.  Computer Physics Communications **196**, 1–37 (2015).
URL http://linkinghub.elsevier.com/retrieve/pii/S0010465515002696
