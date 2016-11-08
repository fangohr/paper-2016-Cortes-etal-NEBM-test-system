from __future__ import print_function

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# Matplotlib tweaks -----------------------------------------------------------
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rcParams.update({'xtick.labelsize': 22})
matplotlib.rcParams.update({'ytick.labelsize': 22})


def remove_ticks(ax):
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')


def remove_splines(ax, spl):
    for s in spl:
        ax.spines[s].set_visible(False)


def modify_splines(ax, lwd=0.75, col='0.8'):
    for s in ['bottom', 'left', 'top', 'right']:
        ax.spines[s].set_linewidth(lwd)
        ax.spines[s].set_color(col)

# -----------------------------------------------------------------------------

x_scale = 1
meV = 1e-3 * 1.602e-19

# We load the last step. The first column is the step number, which
# we get rid of in the dms file (dms are the differences between
# images)
data_energy = np.loadtxt('climbing_image_neb_21x21-spins_fm-sk_atomic_k1e4_energy.ndt')[:, 1:]
data_dYs = np.loadtxt('climbing_image_neb_21x21-spins_fm-sk_atomic_k1e4_dYs.ndt')[:, 1:]

# We will plot relatively to the skyrmion energy
sk_energy = np.ones(len(data_energy[0])) * data_energy[0][0]

# Scale the x axis (distances)
data_dYs *= x_scale


# Compute the total distance of a point from one of the extremes
# (the extremes are energy minima). It is only necessary to
# sum the distances up an specific point
def compute_dYs(step):
    dYs = [0]
    for i in range(len(data_dYs[step])):
        dYs.append(np.sum(data_dYs[step][:i + 1]))

    return dYs

# -----------------------------------------------------------------------------

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)

# The label would show the total number of nebm steps
ax.plot(compute_dYs(0), (data_energy[0] - sk_energy) / meV, 'ko-',
        lw=2, ms=8,
        # label=r'$k=10^{10}$ /' + ' {} Steps'.format(int(data1e10_energy[0]))
        )

# Decorations
remove_ticks(ax)
modify_splines(ax, lwd=0.75, col='0.9')
remove_splines(ax, ['top', 'right'])

ax.patch.set_facecolor('0.93')
ax.grid(True, 'major', color='0.98', linestyle='-', linewidth=2.0)
ax.set_axisbelow(True)


ax.set_xlabel('Distance')
ax.set_ylabel(r'Energy  [ ' + 'meV' + r' ]')

# plt.legend(loc='upper left')

ax.set_ylim([-15, 44])
ax.set_xlim([-1, 18])

# -----------------------------------------------------------------------------

folder = 'climbing_image_gif/'
if not os.path.exists(folder):
    os.makedirs(folder)

for i in range(66):

    ax.texts = []
    ax.lines[0].set_data(compute_dYs(i), (data_energy[i] - sk_energy) / meV)

    # Annotate numbers extracting the position
    # from the  plot curve and shift the y position a little
    x, y = ax.lines[0].get_data()[0], ax.lines[0].get_data()[1]
    for j in range(18):
        ax.text(x[j], y[j] + 1.5,
                '{}'.format(j),
                fontsize=15,
                horizontalalignment='center',
                )

    plt.text(0.05, 0.9,
             'Step {:02}'.format(i),
             horizontalalignment='left',
             transform=ax.transAxes, fontsize=20
             )

    plt.savefig(folder + 'snapshot_{:06}.png'.format(i),
                # dpi=500,
                bbox_inches='tight')
