# coding: utf-8

from __future__ import print_function, absolute_import
from math import ceil, sqrt

import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from matplotlib.path import Path
import matplotlib.patches as patches

from .utils import string_to_array, seq_to_pos

def draw_sequence(s, col):
    u = sqrt(2.0)/2.0
    seq = string_to_array(s)
    x, y = seq_to_pos(seq)
    pos = np.vstack([x, y]).T
    xmax = (pos[-1, 0]+pos[-1, 1])*u+2*u
    ymin, ymax = np.min(pos[:, 1]-pos[:, 0])*u-u, np.max(pos[:, 1]-pos[:, 0])*u+u
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    fig = plt.figure(figsize=(5*xmax/14, 5*(ymax-ymin)/14), dpi=150)
    ax = fig.add_subplot(1, 1, 1, axisbg='w')
    for k, p in enumerate(pos):
        c = col if k%2==1 else 'w'
        x0 = (p[0]+p[1])*u
        y0 = (p[1]-p[0])*u
        vertices = np.array([[x0, y0], [x0+u, y0+u], [x0+2*u, y0], [x0+u, y0-u], [x0, y0]])
        path = Path(vertices, codes)
        patch = patches.PathPatch(path, facecolor=c, edgecolor='k', linewidth=1.5)
        ax.add_patch(patch)
        ax.text(x0+u, y0, str(1+k), rotation=-45, fontsize=8, horizontalalignment='center', verticalalignment='center')
    ax.set_xlim(-0.1, xmax+0.1)
    ax.set_ylim(ymin-0.1, ymax+0.1)
    ax.axis('off')
    #plt.savefig("sequence.png",bbox_inches='tight')
    plt.show()

def coord_to_node(coord):
    x, y, z = coord
    return 1+1*x+3*y+9*z

def node_to_coord(node):
    z = (node-1)/9
    y = (node-1-z*9)/3
    x = node-1-z*9-y*3
    return [x, y, z]

def draw_path(ax, p, n):
    #grid
    r = np.arange(3)
    xx, yy, zz = np.meshgrid(r, r, r)
    ax.scatter(xx, yy, zz, marker='o', color='gray', s=20, alpha=0.6)
    xx, yy = np.meshgrid(r, r)
    for z in range(3):
        ax.plot(xx, yy, z, zdir='z', color='gray', alpha=0.15)
    for z in range(3):
        ax.plot(yy, xx, z, zdir='y', color='gray', alpha=0.15)
    for z in range(3):
        ax.plot(xx, yy, z, zdir='x', color='gray', alpha=0.15)
    d = 0.08
    for x in range(3):
        for y in range(3):
            for z in range(3):
                ax.text(x+d, y+d, z+0, str(1+1*x+3*y+9*z), color='k', alpha=0.6, ha='left', size=8)
    plt.axis('off')
    ax.view_init(elev=15, azim=-77)
    ax.dist = 6

    #path
    coord = np.array(map(node_to_coord, p))
    x = coord[:, 0]
    y = coord[:, 1]
    z = coord[:, 2]
    ax.plot(x, y, z, zdir='z', color='red', alpha=0.85, linewidth=1.35)
    ax.scatter(coord[:, 0], coord[:, 1], coord[:, 2], marker='o', color='red', alpha=1.0, s=20)
    ax.scatter(coord[0, 0], coord[0, 1], coord[0, 2], marker='o', facecolor='red', edgecolor='k', linewidth=1.5, alpha=1.0, s=75)
    ax.scatter(coord[-1, 0], coord[-1, 1], coord[-1, 2], marker='o', facecolor='red', edgecolor='k', linewidth=1.5, alpha=1.0, s=75)
    ax.text2D(0.05, 0.95, str(n), size=11, transform=ax.transAxes)

def draw_path_series(ps):
    h = 4
    v = int(ceil(float(len(ps))/h))
    fig = plt.figure(figsize=(2.5*h, 2.5*v), dpi=200)
    for k in range(len(ps)):
        ax = fig.add_subplot(v, h, 1+k, projection='3d', axisbg='w')
        draw_path(ax, ps[k], 1+k)
    plt.show()

def colored_view_df_stat(df_stat, size=(15, 25)):
    df_stat_light = df_stat.copy()
    del df_stat_light['sequence total']
    del df_stat_light['solution total']
    df_stat_light = df_stat_light.drop('total')
    df_stat_light = df_stat_light[:]
    rng_sol = np.array(df_stat_light.index, dtype=np.int)
    rng_str = np.array(df_stat_light.columns, dtype=np.int)
    arr_stat_light = np.array(df_stat_light)

    my_cmap = mpl.cm.jet_r
    my_cmap.set_under('w')

    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(111)

    #img portion
    cax = ax.matshow(arr_stat_light, interpolation='nearest', cmap=my_cmap, vmin=0.5, alpha=0.65, aspect=0.5)
    fig.colorbar(cax)

    #text portion
    x_pos, y_pos = np.meshgrid(range(len(rng_sol)), range(len(rng_str)))
    for x, y in zip(x_pos.flatten(), y_pos.flatten()):
        v = arr_stat_light[x, y]
        ax.text(y, x, v, va='center', ha='center')

    ax.grid(False)
    ax.set_xlabel('Nb Straights')
    ax.set_ylabel('Nb Solutions')

    xLabelPositions = range(len(rng_str))
    xNewLabels = rng_str
    plt.xticks(xLabelPositions, xNewLabels)

    yLabelPositions = range(len(rng_sol))
    yNewLabels = rng_sol
    plt.yticks(yLabelPositions, yNewLabels)

    plt.show()
