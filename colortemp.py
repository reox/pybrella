#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2017 Sebastian Bachmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import numpy as np

def colortemp(T):
    """
        Returns the RGB value for a given color temperature in Kelvin

        :param T: Integer value of color temperature, between 1667 and 25000
        :rtype: tuple of R, G, B value (8bit integer)
    """

    # Definiton of approximate CIE-XYZ Black-Body Curve
    # https://en.wikipedia.org/wiki/Planckian_locus#Approximation

    # Actually we need it only up to about 6500K, but it is defined to 25000K
    def calc_x(T):
        if 1667 <= T <= 4000:
            return -0.2661239 * (10**9 / T**3) - 0.2343580 * (10**6 / T**2) + 0.8776956 * (10**3 / T) + 0.179910
        elif 4000 < T <= 25000:
            return -3.0258469 * (10**9 / T**3) + 2.1070379 * (10**6 / T**2) + 0.2226347 * (10**3 / T) + 0.240390
        else:
            return None

    def calc_y(T, x):
        if 1667 <= T <= 2222:
            return -1.1063814 * x**3 - 1.34811020 * x**2 + 2.18555832 * x - 0.20219683
        elif 2222 < T <= 4000:
            return -0.9549476 * x**3 - 1.37418593 * x**2 + 2.09137015 * x - 0.16748867
        elif 4000 < T <= 25000:
            return +3.0817580 * x**3 - 5.87338670 * x**2 + 3.75112997 * x - 0.37001483
        else:
            return None

    x_c = calc_x(T)
    if x_c is None:
        return None
    y_c = calc_y(T, x_c)
    z_c = 1 - x_c - y_c

    # Now we need to calculate RGB value from this XYZ value:
    # if X is the xyz vector and R is the rgb vector, there
    # is a linear relationship X = M R using a 3x3 Matrix M
    # http://www.brucelindbloom.com/Eqn_RGB_XYZ_Matrix.html
    # As the calculation above is for CIE, we choose this matrix as well:
    #  2.3706743 -0.9000405 -0.4706338
    # -0.5138850  1.4253036  0.0885814
    #  0.0052982 -0.0146949  1.0093968

    M = np.matrix([[2.3706743, -0.9000405, -0.4706338],
                   [-0.5138850,  1.4253036,  0.0885814],
                   [0.0052982, -0.0146949,  1.0093968]])

    X = np.matrix([[x_c], [y_c], [z_c]])

    r, g, b = (M * X * 255).round().T.astype(int).tolist()[0]

    return (r, g, b)
