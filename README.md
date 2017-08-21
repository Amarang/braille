## Braille

> ASCII art is simply not precise enough
- The New York Times

The Braille character set in unicode provides more granularity over full-character ascii art
by decomposing a full character into a 2 by 4 set of dots, resulting in twice (quadruple) the 
horizontal (vertical) precision.

## Installation

It's a single file.

## Examples

N.B.: Characters seem to get shifted on asciinema, but they look perfect in a few terminals that I've tried. Trust me.

`python braille.py --example_hist` gives
[![example histogram](https://asciinema.org/a/ZvPGK9oieEyZiyOgi2A5rUNSR.png)](https://asciinema.org/a/ZvPGK9oieEyZiyOgi2A5rUNSR?autoplay=1)

`python braille.py --example_timeseries` gives
[![example timeseries](https://asciinema.org/a/9tlQLJaOJTU7lPZCgb13HqyQK.png)](https://asciinema.org/a/9tlQLJaOJTU7lPZCgb13HqyQK?autoplay=1)

You can also pipe data via
```
seq 1 100 | ./braille.py
```
to get a sequential bar graph, or 
```
# central limit theorem: add 3 flat random numbers to get a pretty gaussian distribution
# -f forces the script to make a frequency histogram, rather than a time series by default
for i in `seq 1 10000`; do echo $((RANDOM + RANDOM + RANDOM)); done | ./braille.py -f
```
to get a gaussian histogram.
