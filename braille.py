#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import random
import math
import os
import numpy as np
import argparse

"""
values are a 4x2 (row x col) grid of dots for Braille
key (i,j) specifies a character representing i filled 
dots starting from the bottom of column 1, and j
filled dots from the bottom of column 2.
Thus, plotting a character representing a pair of consecutive
values 2 and then 3 is as simple as drawing the character
corresponding to key (2,3)
"""
braille_chars = {
        # (0,0): u"\u2800",
        (0,0): u" ",
        (0,1): u"\u2880",
        (0,2): u"\u28A0",
        (0,3): u"\u28B0",
        (0,4): u"\u28B8",

        (1,0): u"\u2840",
        (1,1): u"\u28C0",
        (1,2): u"\u28E0",
        (1,3): u"\u28F0",
        (1,4): u"\u28F8",

        (2,0): u"\u2844",
        (2,1): u"\u28C4",
        (2,2): u"\u28E4",
        (2,3): u"\u28F4",
        (2,4): u"\u28FC",

        (3,0): u"\u2846",
        (3,1): u"\u28C6",
        (3,2): u"\u28E6",
        (3,3): u"\u28F6",
        (3,4): u"\u28FE",

        (4,0): u"\u2847",
        (4,1): u"\u28C7",
        (4,2): u"\u28E7",
        (4,3): u"\u28F7",
        (4,4): u"\u28FF",
        }


def round_four(x):
    """
    transform float `x` from [0.,1.] to int [0,4]
    """
    # return int((max(x,0.)+(1./(2.*4)))*4)
    return int((max(x,0.)+(1./(2.*4)))*4)

def fourize(vals):
    """
    convenience function to map `round_four` onto list `vals`
    """
    return map(round_four, vals)

def normalize(vals, norm_to=1.):
    """
    normalize largest element of `vals` to `norm_to`
    """
    m = max(vals)
    return [1.0*norm_to*v/m for v in vals]

def get_pairs(vals):
    """
    takes 1D list `vals` and returns 1D list of pairs.
    if input does not have an even number of elements,
    a 0 is padded at the end
    """
    if len(vals) % 2 == 1:
        vals = vals + [0.]
    return zip(vals[::2],vals[1::2])

def get_ndots(val, maxval, maxnchars):
    """
    Given `maxval` (float) corresponding to a number of
    characters to display `maxnchars` (int), calculate the number
    of dots we will need to show to represent `val`
    Returns an integer number of dots.
    """
    nchars = 1.0 * val / maxval * maxnchars
    # 4 dots for every full character
    ndots = int(nchars) * 4
    # remaining dots, but round to whole number of dots
    remainder = nchars - int(nchars)
    extradots = round_four(abs(remainder))
    if remainder < 0: extradots *= -1
    ndots += extradots
    return int(ndots)

def pair_to_charcodes(ndotsL,ndotsR):
    """
    takes pair of dots for left and right columns and converts
    into list of character codes to draw, so
    0 0 -> [(0,0)]
    4 4 -> [(4,4)]
    5 4 -> [(4,4), (1,0)]
    7 9 -> [(4,4), (3,4), (0,1)]
    9 1 -> [(4,1), (4,0), (1,0)]
    For example, 9 dots on the left and 1 dot on the right
    means draw a character with 4 dots on the left, 1 on right
    then 4 dots on left, 0 on right, and then char with 1 dot
    on left and 0 on right
    """
    pairs_out = []
    while ndotsL > 0 or ndotsR > 0:
        takeL = min(ndotsL,4)
        takeR = min(ndotsR,4)
        pairs_out.append( (takeL,takeR) )
        ndotsL -= takeL
        ndotsR -= takeR
    if not pairs_out:
        pairs_out.append( (0,0) )
    return pairs_out

def pad_and_transpose(mat, fill_elem=(0,0)):
    """
    Space pad and transpose a list of lists
    """
    maxheight = max(map(len,mat))
    mat = [col+([fill_elem]*max(maxheight-len(col),0)) for col in mat]
    rows = zip(*mat)[::-1]
    return rows


def horizontal_bar_chart(vals, maxheight=5, maxwidth=-1):
    """
    return a string representing a bar chart made from a 
    list of numbers `vals` that span a maximum number of lines
    `maxheight` in height
    """
    if maxwidth > 0: vals = vals[-maxwidth*2-2:]
    pairs = get_pairs(vals)
    charcode_pairs = []
    maxval = max(vals)
    for pair in pairs:
        ndots1 = get_ndots(pair[0], maxval=maxval, maxnchars=maxheight)
        ndots2 = get_ndots(pair[1], maxval=maxval, maxnchars=maxheight)
        charcode_pairs.append(pair_to_charcodes(ndots1,ndots2))
    mat = pad_and_transpose(charcode_pairs)
    rows = []
    for row in mat:
        rows.append( "".join([braille_chars[v] for v in row]) )
    return "\n".join(rows)


def nlines_back(n):
    """
    return escape sequences to move character up `n` lines
    and to the beginning of the line
    """
    return "\033[{0}A\r".format(n+1)
    # return "\x1B[1A\x1B[2K" * n

def duplicate_elements(vals, n):
    """
    takes list `vals` and duplicates each element `n` times
    (e.g., `n=1` will return `vals`)
    """
    return sum(map(list,zip(*[vals for _ in range(n)])),[])

def make_hist(vals, nbins=-1, maxwidth=150, maxheight=10):
    """
    return a string representing a histogram made from a 
    list of numbers `vals` that span a maximum number of lines
    `maxheight` in height and `maxwidth` in width
    Optionally, `nbins` can be specified to override automatic
    binning.
    """
    extra = {}
    vals = np.array(vals)
    if nbins > 0:
        extra = {"bins": np.linspace(vals.min(), vals.max(), nbins+1)}
    content, edges = np.histogram([vals], **extra)
    ndupes = int(maxwidth/len(content))
    content = duplicate_elements(content, ndupes)
    return horizontal_bar_chart(content, maxheight=maxheight)


def example_hist():
    """
    make a constantly updating histogram with two off-center gaussians
    """
    vals = np.array([])
    painter = Painter()
    for i in range(500):
        vals = np.append(vals,np.random.normal(loc=-2.,size=15))
        vals = np.append(vals,np.random.normal(loc=2.,size=15))
        painter.draw(make_hist(vals, nbins=50))
        time.sleep(0.1)

def example_timeseries():
    """
    plot sequential data using random numbers
    when we hit `maxwidth` characters, we start truncating old values
    """
    nums = []
    painter = Painter()
    maxheight = 3
    maxwidth = 25
    for item in [4.*abs(math.sin(1.0*i/30.))+random.random() for i in range(200)]:
        nums.append(item)
        painter.draw(horizontal_bar_chart(nums, maxheight=maxheight, maxwidth=maxwidth))
        time.sleep(0.1)


class Painter(object):
    """
    Convenience class which will draw a string `content`, but clear
    the traces of the previously drawn string, so that you get a 
    constantly updating image in the terminal
    """

    def __init__(self):
        self.to_print = ""

    def draw(self, content):
        nrewind = self.to_print.count("\n")
        erase_previous = nlines_back(nrewind) if self.to_print else ""
        self.to_print = content
        print(erase_previous+self.to_print)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--example_hist", help="histogram instead of sequential data", action="store_true")
    parser.add_argument("--example_timeseries", help="histogram instead of sequential data", action="store_true")
    args = parser.parse_args()

    if sys.stdin.isatty():

        if args.example_hist:
            example_hist()
        elif args.example_timeseries:
            example_timeseries()

    else:


        nums = []
        painter = Painter()

        for item in sys.stdin:
            nums.append(float(item.strip()))
        if args.hist:
            painter.draw(make_hist(nums, maxheight=6))
        else:
            painter.draw(horizontal_bar_chart(nums, maxheight=3))

