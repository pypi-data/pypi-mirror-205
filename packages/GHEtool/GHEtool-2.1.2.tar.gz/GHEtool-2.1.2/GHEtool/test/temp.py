# -*- coding: utf-8 -*-
""" Example of calculation of g-functions using uniform and equal borehole
    wall temperatures.
    The g-functions of fields of 3x2, 6x4 and 10x10 boreholes are calculated
    for boundary condition of uniform borehole wall temperature along the
    boreholes, equal for all boreholes.
"""
import matplotlib.pyplot as plt
import numpy as np
import copy
from time import perf_counter

import pygfunction as gt


def main():
    # -------------------------------------------------------------------------
    # Simulation parameters
    # -------------------------------------------------------------------------

    # Borehole dimensions
    D = 4.0             # Borehole buried depth (m)
    H = 150.0           # Borehole length (m)
    r_b = 0.075         # Borehole radius (m)
    B = 7.5             # Borehole spacing (m)

    # Thermal properties
    alpha = 1.0e-6      # Ground thermal diffusivity (m2/s)

    # Path to validation data
    filePath = './data/CiBe14_uniform_temperature.txt'

    # g-Function calculation options
    # A uniform discretization is used to compare results with Cimmino and
    # Bernier (2014).
    options = {'nSegments': 12,
               'segment_ratios': None,
               'disp': False,
               'profiles': True}

    # Geometrically expanding time vector.
    dt = 24*3600.                  # Time step
    tmax = 8760. * 3600. *2  # Maximum time
    Nt = 25                         # Number of time steps
    ts = H**2/(9.*alpha)            # Bore field characteristic time
    time = gt.utilities.time_geometric(dt, tmax, Nt)
    lntts = np.log(time/ts)

    # -------------------------------------------------------------------------
    # Borehole fields
    # -------------------------------------------------------------------------

    # Field of 3x2 (n=6) boreholes
    N_1 = 3
    N_2 = 3
    boreField1 = gt.boreholes.rectangle_field(N_1, N_2, 10, 10, H, D, r_b)

    # Field of 6x4 (n=24) boreholes
    N_1 = 3
    N_2 = 3
    boreField2 = gt.boreholes.rectangle_field(N_1, N_2, 6, 6, H, D, r_b)

    # Field of 10x10 (n=100) boreholes
    N_1 = 3
    N_2 = 3
    boreField3 = gt.boreholes.rectangle_field(N_1, N_2, 8, 8, H, D, r_b)

    # -------------------------------------------------------------------------
    # Load data from Cimmino and Bernier (2014)
    # -------------------------------------------------------------------------
    # data = np.loadtxt(filePath, skiprows=55)

    # -------------------------------------------------------------------------
    # Evaluate g-functions for all fields
    # -------------------------------------------------------------------------
    plt.figure()

    # for i, field in enumerate([boreField2, boreField3]):
    #     nBoreholes = len(field)
    #     # Compare 'similarities' and 'equivalent' solvers
    #     t0 = perf_counter()
    #     # gfunc_similarities = gt.gfunction.gFunction(
    #     #     field, alpha, time=time, options=options, method='similarities')
    #     t1 = perf_counter()
    #     t_similarities = t1 - t0
    #
    #     print(gfunc_equivalent.gFunc)
    #     t2 = perf_counter()
    #     t_equivalent = t2 - t1
        # Draw g-function
        # ax = gfunc_similarities.visualize_g_function().axes[0]
        # ax.plot(time, gfunc_equivalent.gFunc)

        # ax.set_title(f'Field of {nBoreholes} boreholes')
    # rectangle
    gfunc_equivalent = gt.gfunction.gFunction(
        boreField2, 1.5/(2.4*10**6), time=time, options=options, method='equivalent')
    print(gfunc_equivalent.gFunc)
    plt.plot([0]+time/3600/24/ 30,[0]+ copy.copy(gfunc_equivalent.gFunc), label="6m")
    gfunc_equivalent = gt.gfunction.gFunction(
        boreField2, 2.5/(2.4*10**6), time=time, options=options, method='equivalent')
    print(gfunc_equivalent.gFunc)

    plt.plot([0] + time / 3600 / 24 / 30, [0] + copy.copy(gfunc_equivalent.gFunc), label="8m")
    gfunc_equivalent = gt.gfunction.gFunction(
        boreField2, 3.5/(2.4*10**6), time=time, options=options, method='equivalent')
    print(gfunc_equivalent.gFunc)

    plt.plot([0] + time / 3600 / 24 / 30, [0] + copy.copy(gfunc_equivalent.gFunc), label="10m")
    plt.xlabel("Time [months]")
    plt.ylabel("G-function")
    plt.title("G-function for different spacings")
    plt.legend()

    plt.tight_layout()


    plt.show()
    return


# Main function
if __name__ == '__main__':
    main()