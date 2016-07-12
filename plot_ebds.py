import matplotlib.pyplot as plt
import matplotlib
import numpy as np

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

x_scale = 1000
meV = 1e-3 * 1.602e-19

# We load the last step. The first column is the step number, which
# we get rid of in the dms file (dms are the differences between
# images)
data1e10_energy = np.loadtxt('neb_21x21-spins_fm-sk_'
                             'atomic_k1e10_energy.ndt')[-1]
data1e10_dms = np.loadtxt('neb_21x21-spins_fm-sk'
                          '_atomic_k1e10_dms.ndt')[-1][1:]

# We will plot relatively to the skyrmion energy
sk_energy10 = np.ones(len(data1e10_energy[1:])) * data1e10_energy[1]

# Scale the x axis (distances)
data1e10_dms *= x_scale

# Compute the total distance of a point from one of the extremes
# (the extremes are energy minima). It is only necessary to
# sum the distances up an specific point
dms10 = [0]
for i in range(len(data1e10_dms)):
    dms10.append(np.sum(data1e10_dms[:i + 1]))

# -----------------------------------------------------------------------------

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)

# The label would show the total number of nebm steps
ax.plot(dms10, (data1e10_energy[1:] - sk_energy10) / meV, 'ko-',
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
ax.set_xlim([-0.5, 11])

# Annotate numbers extracting the position
# from the  plot curve and shift the y position a little
x, y = ax.lines[0].get_data()[0], ax.lines[0].get_data()[1]
for i in range(18):
    ax.text(x[i], y[i] + 1.5,
            '{}'.format(i),
            fontsize=15,
            horizontalalignment='center',
            )


if __name__ == '__main__':
    plt.savefig('energy_band.pdf',
                # dpi=500,
                bbox_inches='tight')
